"""
Test module: Performance Monitoring

Tests for profiler data streaming, validation alerts, historical results, and benchmarking.

Status: 🔮 Wishful - Defines ideal performance monitoring APIs
"""

import pytest
from datetime import datetime, timedelta


@pytest.mark.wishful
class TestProfilerStreaming:
    """Test real-time profiler data streaming."""
    
    def test_start_profiler_stream(self, test_client, ecoli_vm_config):
        """POST /api/v1/vms/{vm_id}/profiler/stream"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        # Start simulation with profiling
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "profiled_sim",
            "duration_hours": 24,
            "enable_profiling": True
        })
        
        # Start profiler stream
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/profiler/stream",
            json={
                "simulation_id": "profiled_sim",
                "metrics": ["cpu_usage", "memory_usage", "iterations_per_second"],
                "update_interval_seconds": 1
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "stream_id" in result
        assert "status" in result
        assert result["status"] == "streaming"
    
    def test_get_profiler_snapshot(self, test_client, ecoli_vm_config):
        """GET /api/v1/vms/{vm_id}/profiler/snapshot"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "snapshot_sim",
            "duration_hours": 12,
            "enable_profiling": True
        })
        
        # Get current snapshot
        response = test_client.get(
            f"/api/v1/vms/{vm_id}/profiler/snapshot",
            params={"simulation_id": "snapshot_sim"}
        )
        assert response.status_code == 200
        snapshot = response.json()
        
        assert "timestamp" in snapshot
        assert "cpu_usage_percent" in snapshot
        assert "memory_usage_mb" in snapshot
        assert "iterations_per_second" in snapshot
        assert "simulation_time_hours" in snapshot
    
    def test_get_profiler_history(self, test_client, ecoli_vm_config):
        """GET /api/v1/vms/{vm_id}/profiler/history"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "history_sim",
            "duration_hours": 24,
            "enable_profiling": True
        })
        
        response = test_client.get(
            f"/api/v1/vms/{vm_id}/profiler/history",
            params={"simulation_id": "history_sim"}
        )
        assert response.status_code == 200
        history = response.json()
        
        assert "timestamps" in history
        assert "cpu_usage" in history
        assert "memory_usage" in history
        assert "iterations_per_second" in history
        assert len(history["timestamps"]) > 0
    
    def test_stop_profiler_stream(self, test_client, ecoli_vm_config):
        """POST /api/v1/vms/{vm_id}/profiler/stream/stop"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "stream_stop_test",
            "duration_hours": 24,
            "enable_profiling": True
        })
        
        # Start stream
        stream_response = test_client.post(
            f"/api/v1/vms/{vm_id}/profiler/stream",
            json={"simulation_id": "stream_stop_test"}
        )
        stream_id = stream_response.json()["stream_id"]
        
        # Stop stream
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/profiler/stream/{stream_id}/stop"
        )
        assert response.status_code == 200
        assert response.json()["status"] == "stopped"


@pytest.mark.wishful
class TestValidationAlerts:
    """Test validation alert system."""
    
    def test_create_validation_alert(self, test_client, yeast_circadian_vm_config):
        """POST /api/v1/vms/{vm_id}/alerts/validations"""
        create_response = test_client.post("/api/v1/vms", json=yeast_circadian_vm_config)
        vm_id = create_response.json()["vm_id"]
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/alerts/validations",
            json={
                "alert_id": "period_alert",
                "alert_type": "circadian_period_deviation",
                "conditions": {
                    "expected_period_hours": 24,
                    "max_deviation_hours": 3
                },
                "notification_method": "webhook",
                "webhook_url": "https://example.com/alerts"
            }
        )
        assert response.status_code == 201
        result = response.json()
        
        assert result["alert_id"] == "period_alert"
        assert result["status"] == "active"
    
    def test_trigger_alert_on_validation_failure(self, test_client, yeast_circadian_vm_config):
        """Test alert triggers when validation fails"""
        create_response = test_client.post("/api/v1/vms", json=yeast_circadian_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        # Create alert
        test_client.post(f"/api/v1/vms/{vm_id}/alerts/validations", json={
            "alert_id": "amplitude_alert",
            "alert_type": "amplitude_decay",
            "conditions": {"max_decay_percent": 5}
        })
        
        # Run simulation that triggers alert
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "trigger_alert_sim",
            "duration_hours": 72
        })
        
        # Check alerts
        response = test_client.get(f"/api/v1/vms/{vm_id}/alerts/triggered")
        assert response.status_code == 200
        alerts = response.json()
        
        # May or may not trigger depending on simulation
        assert isinstance(alerts, list)
    
    def test_get_alert_history(self, test_client, ecoli_vm_config):
        """GET /api/v1/vms/{vm_id}/alerts/history"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        
        response = test_client.get(f"/api/v1/vms/{vm_id}/alerts/history")
        assert response.status_code == 200
        history = response.json()
        
        assert isinstance(history, list)
        for alert in history:
            assert "alert_id" in alert
            assert "triggered_at" in alert
            assert "message" in alert
    
    def test_disable_alert(self, test_client, yeast_circadian_vm_config):
        """POST /api/v1/vms/{vm_id}/alerts/{alert_id}/disable"""
        create_response = test_client.post("/api/v1/vms", json=yeast_circadian_vm_config)
        vm_id = create_response.json()["vm_id"]
        
        # Create alert
        test_client.post(f"/api/v1/vms/{vm_id}/alerts/validations", json={
            "alert_id": "test_alert",
            "alert_type": "circadian_period_deviation",
            "conditions": {"expected_period_hours": 24}
        })
        
        # Disable
        response = test_client.post(f"/api/v1/vms/{vm_id}/alerts/test_alert/disable")
        assert response.status_code == 200
        assert response.json()["status"] == "disabled"
    
    def test_delete_alert(self, test_client, ecoli_vm_config):
        """DELETE /api/v1/vms/{vm_id}/alerts/{alert_id}"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        
        # Create alert
        test_client.post(f"/api/v1/vms/{vm_id}/alerts/validations", json={
            "alert_id": "delete_test",
            "alert_type": "numerical_instability"
        })
        
        # Delete
        response = test_client.delete(f"/api/v1/vms/{vm_id}/alerts/delete_test")
        assert response.status_code == 204


@pytest.mark.wishful
class TestHistoricalResults:
    """Test historical simulation result storage and retrieval."""
    
    def test_list_historical_simulations(self, test_client, ecoli_vm_config):
        """GET /api/v1/vms/{vm_id}/history/simulations"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        # Run multiple simulations
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "hist_sim_1",
            "duration_hours": 12
        })
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "hist_sim_2",
            "duration_hours": 24
        })
        
        # List history
        response = test_client.get(f"/api/v1/vms/{vm_id}/history/simulations")
        assert response.status_code == 200
        simulations = response.json()
        
        assert len(simulations) >= 2
        for sim in simulations:
            assert "simulation_id" in sim
            assert "started_at" in sim
            assert "duration_hours" in sim
            assert "status" in sim
    
    def test_get_historical_simulation_details(self, test_client, ecoli_vm_config):
        """GET /api/v1/vms/{vm_id}/history/simulations/{sim_id}"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "detail_test",
            "duration_hours": 12
        })
        
        response = test_client.get(f"/api/v1/vms/{vm_id}/history/simulations/detail_test")
        assert response.status_code == 200
        details = response.json()
        
        assert details["simulation_id"] == "detail_test"
        assert "configuration" in details
        assert "results" in details
        assert "metrics" in details
    
    def test_compare_historical_simulations(self, test_client, yeast_circadian_vm_config):
        """POST /api/v1/vms/{vm_id}/history/compare"""
        create_response = test_client.post("/api/v1/vms", json=yeast_circadian_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        # Run two simulations
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "compare_a",
            "duration_hours": 48,
            "temperature_celsius": 25
        })
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "compare_b",
            "duration_hours": 48,
            "temperature_celsius": 35
        })
        
        # Compare
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/history/compare",
            json={
                "simulation_ids": ["compare_a", "compare_b"],
                "metrics": ["circadian_period", "amplitude"]
            }
        )
        assert response.status_code == 200
        comparison = response.json()
        
        assert len(comparison["simulations"]) == 2
        assert "differences" in comparison
    
    def test_delete_historical_simulation(self, test_client, ecoli_vm_config):
        """DELETE /api/v1/vms/{vm_id}/history/simulations/{sim_id}"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "to_delete",
            "duration_hours": 6
        })
        
        response = test_client.delete(f"/api/v1/vms/{vm_id}/history/simulations/to_delete")
        assert response.status_code == 204
    
    def test_export_historical_data(self, test_client, ecoli_vm_config):
        """GET /api/v1/vms/{vm_id}/history/export"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        
        response = test_client.get(
            f"/api/v1/vms/{vm_id}/history/export",
            params={"format": "json"}
        )
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"


@pytest.mark.wishful
class TestBenchmarking:
    """Test benchmarking and performance analysis."""
    
    def test_run_benchmark_suite(self, test_client, ecoli_vm_config):
        """POST /api/v1/vms/{vm_id}/benchmarks"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/benchmarks",
            json={
                "benchmark_id": "standard_suite",
                "tests": [
                    {"name": "short_simulation", "duration_hours": 1},
                    {"name": "medium_simulation", "duration_hours": 12},
                    {"name": "long_simulation", "duration_hours": 24}
                ],
                "runs_per_test": 3
            }
        )
        assert response.status_code == 201
        result = response.json()
        
        assert result["benchmark_id"] == "standard_suite"
        assert "status" in result
    
    def test_get_benchmark_results(self, test_client, ecoli_vm_config):
        """GET /api/v1/vms/{vm_id}/benchmarks/{benchmark_id}"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        # Run benchmark
        test_client.post(f"/api/v1/vms/{vm_id}/benchmarks", json={
            "benchmark_id": "perf_test",
            "tests": [{"name": "test_1", "duration_hours": 1}]
        })
        
        response = test_client.get(f"/api/v1/vms/{vm_id}/benchmarks/perf_test")
        assert response.status_code == 200
        results = response.json()
        
        assert "benchmark_id" in results
        assert "tests" in results
        for test in results["tests"]:
            assert "name" in test
            assert "mean_runtime_seconds" in test
            assert "std_dev_runtime_seconds" in test
            assert "mean_iterations_per_second" in test
    
    def test_compare_vm_performance(self, test_client, ecoli_vm_config, syn3a_vm_config):
        """POST /api/v1/benchmarks/compare-vms"""
        # Create two VMs
        ecoli_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        syn3a_response = test_client.post("/api/v1/vms", json=syn3a_vm_config)
        
        vm_id_1 = ecoli_response.json()["vm_id"]
        vm_id_2 = syn3a_response.json()["vm_id"]
        
        # Compare performance
        response = test_client.post(
            "/api/v1/benchmarks/compare-vms",
            json={
                "vm_ids": [vm_id_1, vm_id_2],
                "test": {"duration_hours": 6},
                "runs": 3
            }
        )
        assert response.status_code == 200
        comparison = response.json()
        
        assert len(comparison["vms"]) == 2
        assert "performance_ranking" in comparison
    
    def test_analyze_computational_overhead(self, test_client, ecoli_vm_config):
        """POST /api/v1/vms/{vm_id}/benchmarks/overhead"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/benchmarks/overhead",
            json={
                "features": [
                    "profiling",
                    "history_tracking",
                    "validation",
                    "analysis"
                ],
                "baseline_duration_hours": 6
            }
        )
        assert response.status_code == 200
        overhead = response.json()
        
        assert "baseline_runtime_seconds" in overhead
        for feature in overhead["features"]:
            assert "name" in feature
            assert "overhead_percent" in feature
    
    def test_scaling_benchmark(self, test_client, ecoli_vm_config):
        """POST /api/v1/vms/{vm_id}/benchmarks/scaling"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/benchmarks/scaling",
            json={
                "parameter": "timestep_seconds",
                "values": [0.1, 0.5, 1.0, 5.0, 10.0],
                "test_duration_hours": 6
            }
        )
        assert response.status_code == 200
        scaling = response.json()
        
        assert "parameter" in scaling
        assert "measurements" in scaling
        assert len(scaling["measurements"]) == 5
        
        for measurement in scaling["measurements"]:
            assert "parameter_value" in measurement
            assert "runtime_seconds" in measurement
            assert "accuracy_score" in measurement


@pytest.mark.wishful
class TestResourceMonitoring:
    """Test resource usage monitoring."""
    
    def test_get_cpu_usage(self, test_client, ecoli_vm_config):
        """GET /api/v1/vms/{vm_id}/resources/cpu"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "cpu_test",
            "duration_hours": 12
        })
        
        response = test_client.get(f"/api/v1/vms/{vm_id}/resources/cpu")
        assert response.status_code == 200
        cpu = response.json()
        
        assert "current_usage_percent" in cpu
        assert "mean_usage_percent" in cpu
        assert "peak_usage_percent" in cpu
    
    def test_get_memory_usage(self, test_client, ecoli_vm_config):
        """GET /api/v1/vms/{vm_id}/resources/memory"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "memory_test",
            "duration_hours": 12
        })
        
        response = test_client.get(f"/api/v1/vms/{vm_id}/resources/memory")
        assert response.status_code == 200
        memory = response.json()
        
        assert "current_usage_mb" in memory
        assert "peak_usage_mb" in memory
        assert "allocated_mb" in memory
    
    def test_get_disk_usage(self, test_client, ecoli_vm_config):
        """GET /api/v1/vms/{vm_id}/resources/disk"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        
        response = test_client.get(f"/api/v1/vms/{vm_id}/resources/disk")
        assert response.status_code == 200
        disk = response.json()
        
        assert "history_size_mb" in disk
        assert "checkpoint_size_mb" in disk
        assert "total_size_mb" in disk
    
    def test_set_resource_limits(self, test_client, ecoli_vm_config):
        """POST /api/v1/vms/{vm_id}/resources/limits"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/resources/limits",
            json={
                "max_cpu_percent": 80,
                "max_memory_mb": 4096,
                "max_disk_mb": 10240
            }
        )
        assert response.status_code == 200
        limits = response.json()
        
        assert limits["max_cpu_percent"] == 80
        assert limits["max_memory_mb"] == 4096
    
    def test_resource_alert_on_limit_exceeded(self, test_client, ecoli_vm_config):
        """Test alert when resource limit exceeded"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        
        # Set low limit
        test_client.post(f"/api/v1/vms/{vm_id}/resources/limits", json={
            "max_memory_mb": 100  # Intentionally low
        })
        
        # Create resource alert
        test_client.post(f"/api/v1/vms/{vm_id}/alerts/resources", json={
            "alert_id": "memory_limit_alert",
            "resource_type": "memory",
            "threshold_percent": 90
        })
        
        # Start simulation (may exceed limit)
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "resource_alert_test",
            "duration_hours": 6
        })
        
        # Check if alert triggered
        response = test_client.get(f"/api/v1/vms/{vm_id}/alerts/triggered")
        assert response.status_code == 200


@pytest.mark.wishful
class TestMetricsExport:
    """Test metrics export and integration."""
    
    def test_export_prometheus_metrics(self, test_client, ecoli_vm_config):
        """GET /api/v1/vms/{vm_id}/metrics/prometheus"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "prometheus_test",
            "duration_hours": 12
        })
        
        response = test_client.get(f"/api/v1/vms/{vm_id}/metrics/prometheus")
        assert response.status_code == 200
        metrics = response.text
        
        # Check Prometheus format
        assert "# HELP" in metrics
        assert "# TYPE" in metrics
    
    def test_export_grafana_dashboard(self, test_client, ecoli_vm_config):
        """GET /api/v1/vms/{vm_id}/metrics/grafana-dashboard"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        
        response = test_client.get(f"/api/v1/vms/{vm_id}/metrics/grafana-dashboard")
        assert response.status_code == 200
        dashboard = response.json()
        
        assert "dashboard" in dashboard
        assert "panels" in dashboard["dashboard"]
    
    def test_export_custom_metrics(self, test_client, yeast_circadian_vm_config):
        """POST /api/v1/vms/{vm_id}/metrics/custom"""
        create_response = test_client.post("/api/v1/vms", json=yeast_circadian_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "custom_metrics_test",
            "duration_hours": 48
        })
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/metrics/custom",
            json={
                "metrics": [
                    {"name": "circadian_period", "unit": "hours"},
                    {"name": "amplitude", "unit": "normalized"},
                    {"name": "phase_ct", "unit": "circadian_time"}
                ],
                "format": "json"
            }
        )
        assert response.status_code == 200
        custom_metrics = response.json()
        
        assert len(custom_metrics) == 3
