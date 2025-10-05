"""
Test module: Parameter Tuning

Tests for rate constant tuning, timestep adjustments, damping optimization, and automated sweeps.

Status: 🔮 Wishful - Defines ideal parameter tuning APIs
"""

import pytest


@pytest.mark.wishful
class TestRateConstantTuning:
    """Test rate constant tuning APIs."""
    
    def test_tune_single_rate_constant(self, test_client, ecoli_vm_config):
        """POST /api/v1/vms/{vm_id}/tuning/rate-constants"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/tuning/rate-constants",
            json={
                "reaction_id": "glycolysis_step1",
                "target_rate": 0.5,
                "optimization_method": "gradient_descent",
                "max_iterations": 100
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "tuned_rate" in result
        assert "iterations" in result
        assert "convergence_achieved" in result
    
    def test_tune_multiple_rate_constants(self, test_client, ecoli_vm_config):
        """Tune multiple rate constants simultaneously"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/tuning/rate-constants",
            json={
                "reactions": [
                    {"id": "glycolysis_step1", "target_rate": 0.5},
                    {"id": "glycolysis_step2", "target_rate": 0.3},
                    {"id": "tca_cycle_step1", "target_rate": 0.2}
                ],
                "optimization_method": "simulated_annealing",
                "max_iterations": 500
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert len(result["tuned_rates"]) == 3
        assert "convergence_achieved" in result
    
    def test_tune_to_target_period(self, test_client, yeast_circadian_vm_config):
        """Tune rate constants to achieve target circadian period"""
        create_response = test_client.post("/api/v1/vms", json=yeast_circadian_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/tuning/circadian-period",
            json={
                "target_period_hours": 24.0,
                "tolerance_hours": 0.5,
                "tunable_parameters": ["frq_transcription", "frq_degradation"],
                "max_iterations": 200
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "achieved_period_hours" in result
        assert "tuned_parameters" in result
        assert 23.5 <= result["achieved_period_hours"] <= 24.5
    
    def test_tune_to_target_amplitude(self, test_client, cyanobacteria_vm_config):
        """Tune to achieve target oscillation amplitude"""
        create_response = test_client.post("/api/v1/vms", json=cyanobacteria_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/tuning/oscillation-amplitude",
            json={
                "protein": "KaiC",
                "target_amplitude": 0.6,
                "tolerance": 0.05,
                "tunable_parameters": ["kaiA_kaiC_binding", "kaiC_phosphorylation"],
                "max_iterations": 150
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "achieved_amplitude" in result
        assert "tuned_parameters" in result
        assert 0.55 <= result["achieved_amplitude"] <= 0.65


@pytest.mark.wishful
class TestTimestepAdjustment:
    """Test adaptive timestep adjustment."""
    
    def test_set_fixed_timestep(self, test_client, ecoli_vm_config):
        """POST /api/v1/vms/{vm_id}/config/timestep"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/config/timestep",
            json={"timestep_seconds": 0.1}
        )
        assert response.status_code == 200
        assert response.json()["timestep_seconds"] == 0.1
    
    def test_enable_adaptive_timestep(self, test_client, ecoli_vm_config):
        """Enable adaptive timestep control"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/config/adaptive-timestep",
            json={
                "enabled": True,
                "min_timestep_seconds": 0.01,
                "max_timestep_seconds": 10.0,
                "error_tolerance": 1e-6
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert result["adaptive_timestep_enabled"] is True
        assert result["min_timestep_seconds"] == 0.01
        assert result["max_timestep_seconds"] == 10.0
    
    def test_optimize_timestep_for_stability(self, test_client, ecoli_vm_config):
        """POST /api/v1/vms/{vm_id}/tuning/optimize-timestep"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/tuning/optimize-timestep",
            json={
                "target_metric": "stability",
                "simulation_duration_hours": 6
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "optimal_timestep_seconds" in result
        assert "stability_score" in result
    
    def test_optimize_timestep_for_accuracy(self, test_client, yeast_circadian_vm_config):
        """Optimize timestep for circadian accuracy"""
        create_response = test_client.post("/api/v1/vms", json=yeast_circadian_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/tuning/optimize-timestep",
            json={
                "target_metric": "circadian_accuracy",
                "simulation_duration_hours": 48
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "optimal_timestep_seconds" in result
        assert "period_accuracy" in result
    
    def test_get_timestep_statistics(self, test_client, ecoli_vm_config):
        """GET /api/v1/vms/{vm_id}/simulations/{sim_id}/timestep-stats"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        # Run simulation with adaptive timestep
        test_client.post(f"/api/v1/vms/{vm_id}/config/adaptive-timestep", json={
            "enabled": True,
            "min_timestep_seconds": 0.01,
            "max_timestep_seconds": 1.0
        })
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "adaptive_sim",
            "duration_hours": 12
        })
        
        response = test_client.get(
            f"/api/v1/vms/{vm_id}/simulations/adaptive_sim/timestep-stats"
        )
        assert response.status_code == 200
        stats = response.json()
        
        assert "mean_timestep_seconds" in stats
        assert "min_timestep_seconds" in stats
        assert "max_timestep_seconds" in stats
        assert "timestep_adjustments" in stats


@pytest.mark.wishful
class TestDampingOptimization:
    """Test damping parameter optimization."""
    
    def test_tune_damping_coefficient(self, test_client, yeast_circadian_vm_config):
        """POST /api/v1/vms/{vm_id}/tuning/damping"""
        create_response = test_client.post("/api/v1/vms", json=yeast_circadian_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/tuning/damping",
            json={
                "target_decay_percent_per_day": 5,
                "simulation_duration_hours": 96,
                "tunable_parameters": ["feedback_strength", "degradation_rate"]
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "tuned_damping_coefficient" in result
        assert "achieved_decay_percent" in result
    
    def test_minimize_amplitude_decay(self, test_client, cyanobacteria_vm_config):
        """Minimize amplitude decay in free-running conditions"""
        create_response = test_client.post("/api/v1/vms", json=cyanobacteria_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/tuning/minimize-decay",
            json={
                "protein": "KaiC",
                "simulation_duration_hours": 120,
                "max_decay_percent": 3,
                "tunable_parameters": ["kai_feedback_loops"]
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "final_decay_percent" in result
        assert "tuned_parameters" in result
        assert result["final_decay_percent"] <= 3
    
    def test_tune_transient_response(self, test_client, yeast_circadian_vm_config):
        """Tune transient response after perturbation"""
        create_response = test_client.post("/api/v1/vms", json=yeast_circadian_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/tuning/transient-response",
            json={
                "perturbation": {"type": "light_pulse", "duration_hours": 1},
                "target_settling_time_hours": 12,
                "tolerance_hours": 2
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "achieved_settling_time_hours" in result
        assert "tuned_parameters" in result


@pytest.mark.wishful
class TestInitialConditionTuning:
    """Test initial condition optimization."""
    
    def test_tune_initial_metabolite_levels(self, test_client, ecoli_vm_config):
        """POST /api/v1/vms/{vm_id}/tuning/initial-conditions"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/tuning/initial-conditions",
            json={
                "metabolites": {
                    "ATP": {"target": 5.0, "tunable": True},
                    "NADH": {"target": 2.0, "tunable": True}
                },
                "target_steady_state": True,
                "simulation_duration_hours": 6
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "tuned_initial_conditions" in result
        assert "steady_state_achieved" in result
    
    def test_find_circadian_phase(self, test_client, yeast_circadian_vm_config):
        """Find initial conditions for specific circadian phase"""
        create_response = test_client.post("/api/v1/vms", json=yeast_circadian_vm_config)
        vm_id = create_response.json()["vm_id"]
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/tuning/circadian-phase",
            json={
                "target_phase_ct": 0,  # CT0 (dawn)
                "simulation_duration_hours": 48
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "initial_conditions" in result
        assert "achieved_phase_ct" in result
        assert 0 <= result["achieved_phase_ct"] <= 1
    
    def test_tune_to_experimental_data(self, test_client, ecoli_vm_config):
        """Tune initial conditions to match experimental data"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        
        experimental_data = {
            "timestamp_hours": [0, 2, 4, 6],
            "atp_levels": [100, 105, 108, 110]
        }
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/tuning/match-experimental",
            json={
                "experimental_data": experimental_data,
                "tunable_initial_conditions": ["ATP", "NADH", "biomass"],
                "simulation_duration_hours": 6,
                "optimization_method": "least_squares"
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "tuned_initial_conditions" in result
        assert "fit_quality" in result
        assert "rmse" in result


@pytest.mark.wishful
class TestParameterSweeps:
    """Test automated parameter sweeps."""
    
    def test_sweep_single_parameter(self, test_client, ecoli_vm_config):
        """POST /api/v1/vms/{vm_id}/sweeps"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/sweeps",
            json={
                "sweep_id": "atp_sweep",
                "parameter": "initial_atp",
                "range": {"min": 1.0, "max": 10.0, "step": 1.0},
                "simulation_duration_hours": 12,
                "metrics": ["growth_rate", "oscillation_period"]
            }
        )
        assert response.status_code == 201
        result = response.json()
        
        assert result["sweep_id"] == "atp_sweep"
        assert result["parameter_count"] == 10  # (10-1)/1 + 1
        assert "status" in result
    
    def test_sweep_two_parameters(self, test_client, yeast_circadian_vm_config):
        """2D parameter sweep (rate constants)"""
        create_response = test_client.post("/api/v1/vms", json=yeast_circadian_vm_config)
        vm_id = create_response.json()["vm_id"]
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/sweeps",
            json={
                "sweep_id": "2d_sweep",
                "parameters": [
                    {"name": "frq_transcription", "range": {"min": 0.1, "max": 1.0, "step": 0.1}},
                    {"name": "frq_degradation", "range": {"min": 0.05, "max": 0.5, "step": 0.05}}
                ],
                "simulation_duration_hours": 48,
                "metrics": ["circadian_period", "amplitude"]
            }
        )
        assert response.status_code == 201
        result = response.json()
        
        assert result["parameter_count"] == 100  # 10 x 10 grid
    
    def test_get_sweep_results(self, test_client, ecoli_vm_config):
        """GET /api/v1/vms/{vm_id}/sweeps/{sweep_id}/results"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        
        # Start sweep
        test_client.post(f"/api/v1/vms/{vm_id}/sweeps", json={
            "sweep_id": "test_sweep",
            "parameter": "initial_atp",
            "range": {"min": 1.0, "max": 5.0, "step": 1.0},
            "simulation_duration_hours": 6,
            "metrics": ["growth_rate"]
        })
        
        # Get results
        response = test_client.get(f"/api/v1/vms/{vm_id}/sweeps/test_sweep/results")
        assert response.status_code == 200
        results = response.json()
        
        assert "parameter_values" in results
        assert "metric_values" in results
        assert len(results["parameter_values"]) == 5
    
    def test_get_sweep_heatmap(self, test_client, yeast_circadian_vm_config):
        """GET /api/v1/vms/{vm_id}/sweeps/{sweep_id}/heatmap"""
        create_response = test_client.post("/api/v1/vms", json=yeast_circadian_vm_config)
        vm_id = create_response.json()["vm_id"]
        
        # 2D sweep
        test_client.post(f"/api/v1/vms/{vm_id}/sweeps", json={
            "sweep_id": "heatmap_sweep",
            "parameters": [
                {"name": "param1", "range": {"min": 0, "max": 1, "step": 0.25}},
                {"name": "param2", "range": {"min": 0, "max": 1, "step": 0.25}}
            ],
            "simulation_duration_hours": 24,
            "metrics": ["circadian_period"]
        })
        
        response = test_client.get(
            f"/api/v1/vms/{vm_id}/sweeps/heatmap_sweep/heatmap",
            params={"metric": "circadian_period"}
        )
        assert response.status_code == 200
        heatmap = response.json()
        
        assert "x_values" in heatmap
        assert "y_values" in heatmap
        assert "z_values" in heatmap  # 2D array
    
    def test_optimize_from_sweep(self, test_client, ecoli_vm_config):
        """POST /api/v1/vms/{vm_id}/sweeps/{sweep_id}/optimize"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        
        # Run sweep
        test_client.post(f"/api/v1/vms/{vm_id}/sweeps", json={
            "sweep_id": "opt_sweep",
            "parameter": "initial_atp",
            "range": {"min": 1.0, "max": 10.0, "step": 1.0},
            "simulation_duration_hours": 12,
            "metrics": ["growth_rate"]
        })
        
        # Find optimal
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/sweeps/opt_sweep/optimize",
            json={
                "metric": "growth_rate",
                "optimization_goal": "maximize"
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "optimal_parameter_value" in result
        assert "optimal_metric_value" in result
    
    def test_cancel_sweep(self, test_client, ecoli_vm_config):
        """POST /api/v1/vms/{vm_id}/sweeps/{sweep_id}/cancel"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        
        # Start long sweep
        test_client.post(f"/api/v1/vms/{vm_id}/sweeps", json={
            "sweep_id": "long_sweep",
            "parameter": "initial_atp",
            "range": {"min": 1.0, "max": 100.0, "step": 1.0},
            "simulation_duration_hours": 24,
            "metrics": ["growth_rate"]
        })
        
        # Cancel
        response = test_client.post(f"/api/v1/vms/{vm_id}/sweeps/long_sweep/cancel")
        assert response.status_code == 200
        assert response.json()["status"] == "cancelled"


@pytest.mark.wishful
class TestMultiObjectiveOptimization:
    """Test multi-objective optimization."""
    
    def test_optimize_period_and_amplitude(self, test_client, yeast_circadian_vm_config):
        """POST /api/v1/vms/{vm_id}/tuning/multi-objective"""
        create_response = test_client.post("/api/v1/vms", json=yeast_circadian_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/tuning/multi-objective",
            json={
                "objectives": [
                    {"metric": "circadian_period", "target": 24.0, "weight": 0.6},
                    {"metric": "oscillation_amplitude", "target": 0.7, "weight": 0.4}
                ],
                "tunable_parameters": ["frq_transcription", "frq_degradation", "feedback_strength"],
                "optimization_method": "pareto_front",
                "max_iterations": 300
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "pareto_solutions" in result
        assert "best_compromise" in result
        assert len(result["pareto_solutions"]) > 0
