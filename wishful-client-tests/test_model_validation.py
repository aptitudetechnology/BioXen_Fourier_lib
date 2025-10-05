"""
Test module: Model Validation

Tests for oscillation validation, numerical stability, deviation detection, and quality scores.

Status: 🔮 Wishful - Defines ideal model validation APIs
"""

import pytest
import numpy as np


@pytest.mark.wishful
class TestOscillationValidation:
    """Test oscillation period and amplitude validation."""
    
    def test_validate_circadian_period(self, test_client, yeast_circadian_vm_config):
        """POST /api/v1/vms/{vm_id}/validations/circadian-period"""
        create_response = test_client.post("/api/v1/vms", json=yeast_circadian_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        # Run simulation
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "yeast_48h",
            "duration_hours": 48,
            "enable_history": True
        })
        
        # Validate period
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/validations/circadian-period",
            json={
                "simulation_id": "yeast_48h",
                "gene": "FRQ",
                "expected_period_hours": 24,
                "tolerance_hours": 2
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "measured_period_hours" in result
        assert "validation_passed" in result
        assert 22 <= result["measured_period_hours"] <= 26
    
    def test_validate_oscillation_amplitude(self, test_client, cyanobacteria_vm_config):
        """POST /api/v1/vms/{vm_id}/validations/oscillation-amplitude"""
        create_response = test_client.post("/api/v1/vms", json=cyanobacteria_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "cyano_72h",
            "duration_hours": 72,
            "enable_history": True
        })
        
        # Validate amplitude
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/validations/oscillation-amplitude",
            json={
                "simulation_id": "cyano_72h",
                "protein": "KaiC",
                "min_amplitude": 0.3,
                "max_amplitude": 0.8
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "measured_amplitude" in result
        assert "validation_passed" in result
        assert result["validation_passed"] is True
    
    def test_detect_metabolic_oscillations(self, test_client, ecoli_vm_config):
        """POST /api/v1/vms/{vm_id}/validations/detect-oscillations"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "ecoli_24h",
            "duration_hours": 24,
            "enable_history": True
        })
        
        # Detect oscillations
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/validations/detect-oscillations",
            json={
                "simulation_id": "ecoli_24h",
                "metabolite": "NADH"
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "oscillation_detected" in result
        if result["oscillation_detected"]:
            assert "period_seconds" in result
            assert "amplitude" in result
    
    def test_validate_phase_relationship(self, test_client, yeast_circadian_vm_config):
        """Validate phase relationship between genes"""
        create_response = test_client.post("/api/v1/vms", json=yeast_circadian_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "phase_test",
            "duration_hours": 72,
            "enable_history": True
        })
        
        # Check phase relationship
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/validations/phase-relationship",
            json={
                "simulation_id": "phase_test",
                "gene1": "FRQ",
                "gene2": "WC-1",
                "expected_phase_shift_hours": 6,
                "tolerance_hours": 1
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "measured_phase_shift_hours" in result
        assert "validation_passed" in result
    
    def test_validate_entrainment_range(self, test_client, yeast_circadian_vm_config):
        """Validate entrainment range (T-cycle tolerance)"""
        create_response = test_client.post("/api/v1/vms", json=yeast_circadian_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        # Test entrainment at T=20h
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "entrainment_t20",
            "duration_hours": 72,
            "light_dark_cycle_hours": 20,  # 10L:10D
            "enable_circadian_analysis": True
        })
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/validations/entrainment",
            json={
                "simulation_id": "entrainment_t20",
                "t_cycle_hours": 20,
                "check_1_to_1_entrainment": True
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "entrained" in result
        assert "entrainment_ratio" in result  # Should be 1:1


@pytest.mark.wishful
class TestNumericalStability:
    """Test numerical stability using Laplace analysis."""
    
    def test_laplace_stability_check(self, test_client, ecoli_vm_config):
        """POST /api/v1/vms/{vm_id}/validations/stability-laplace"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "stability_test",
            "duration_hours": 24,
            "enable_history": True
        })
        
        # Check stability via Laplace
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/validations/stability-laplace",
            json={
                "simulation_id": "stability_test",
                "variable": "ATP"
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "stable" in result
        assert "poles" in result
        # All poles should have negative real parts for stability
        if result["stable"]:
            for pole in result["poles"]:
                assert pole["real"] < 0
    
    def test_check_timestep_stability(self, test_client, ecoli_vm_config):
        """POST /api/v1/vms/{vm_id}/validations/timestep-stability"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        # Test with 1s timestep
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "timestep_1s",
            "duration_hours": 12,
            "timestep_seconds": 1.0
        })
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/validations/timestep-stability",
            json={"simulation_id": "timestep_1s"}
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "stable" in result
        assert "cfl_condition" in result
        assert result["stable"] is True
    
    def test_detect_numerical_instability(self, test_client, ecoli_vm_config):
        """Detect NaN/Inf in simulation results"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "instability_check",
            "duration_hours": 24
        })
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/validations/check-instability",
            json={"simulation_id": "instability_check"}
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "nan_detected" in result
        assert "inf_detected" in result
        assert result["nan_detected"] is False
        assert result["inf_detected"] is False
    
    def test_validate_conservation_laws(self, test_client, ecoli_vm_config):
        """Validate mass/energy conservation"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "conservation_test",
            "duration_hours": 24,
            "enable_history": True
        })
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/validations/conservation-laws",
            json={
                "simulation_id": "conservation_test",
                "check_mass": True,
                "check_energy": True,
                "tolerance": 0.01  # 1% tolerance
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "mass_conserved" in result
        assert "energy_conserved" in result
        assert result["mass_conserved"] is True


@pytest.mark.wishful
class TestDeviationDetection:
    """Test biological deviation detection."""
    
    def test_detect_period_deviation(self, test_client, yeast_circadian_vm_config):
        """POST /api/v1/vms/{vm_id}/validations/detect-deviations"""
        create_response = test_client.post("/api/v1/vms", json=yeast_circadian_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "deviation_test",
            "duration_hours": 72
        })
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/validations/detect-deviations",
            json={
                "simulation_id": "deviation_test",
                "check_circadian_period": True,
                "expected_period_hours": 24,
                "deviation_threshold_hours": 3
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "deviations_detected" in result
        if result["deviations_detected"]:
            assert "deviations" in result
    
    def test_detect_amplitude_decay(self, test_client, cyanobacteria_vm_config):
        """Detect amplitude decay (damping)"""
        create_response = test_client.post("/api/v1/vms", json=cyanobacteria_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "decay_test",
            "duration_hours": 96,
            "environmental_conditions": {"light": "constant_dark"}
        })
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/validations/amplitude-decay",
            json={
                "simulation_id": "decay_test",
                "protein": "KaiC",
                "max_decay_percent": 10
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "decay_detected" in result
        assert "decay_percent" in result
    
    def test_detect_phase_drift(self, test_client, yeast_circadian_vm_config):
        """Detect phase drift in constant conditions"""
        create_response = test_client.post("/api/v1/vms", json=yeast_circadian_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "phase_drift_test",
            "duration_hours": 120,
            "environmental_conditions": {"light": "constant_dark"}
        })
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/validations/phase-drift",
            json={
                "simulation_id": "phase_drift_test",
                "gene": "FRQ",
                "max_drift_hours_per_day": 0.5
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "drift_detected" in result
        assert "drift_hours_per_day" in result
    
    def test_compare_to_reference_data(self, test_client, ecoli_vm_config):
        """Compare simulation to experimental reference data"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "reference_compare",
            "duration_hours": 24
        })
        
        # Upload reference data
        reference_data = {
            "timestamps": [0, 6, 12, 18, 24],
            "atp_levels": [100, 110, 105, 108, 102]
        }
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/validations/compare-reference",
            json={
                "simulation_id": "reference_compare",
                "reference_data": reference_data,
                "variable": "ATP",
                "tolerance_percent": 15
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "within_tolerance" in result
        assert "rmse" in result
        assert "max_deviation_percent" in result


@pytest.mark.wishful
class TestQualityScores:
    """Test simulation quality scoring."""
    
    def test_compute_quality_score(self, test_client, ecoli_vm_config):
        """POST /api/v1/vms/{vm_id}/validations/quality-score"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "quality_test",
            "duration_hours": 24,
            "enable_history": True
        })
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/validations/quality-score",
            json={"simulation_id": "quality_test"}
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "overall_score" in result
        assert "components" in result
        assert 0 <= result["overall_score"] <= 100
        
        # Check score components
        components = result["components"]
        assert "numerical_stability" in components
        assert "biological_realism" in components
        assert "oscillation_quality" in components
    
    def test_quality_score_circadian(self, test_client, yeast_circadian_vm_config):
        """Quality score for circadian simulation"""
        create_response = test_client.post("/api/v1/vms", json=yeast_circadian_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "circadian_quality",
            "duration_hours": 72
        })
        
        response = test_client.post(
            f="/api/v1/vms/{vm_id}/validations/quality-score",
            json={
                "simulation_id": "circadian_quality",
                "circadian_specific": True
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        # Circadian-specific components
        components = result["components"]
        assert "period_accuracy" in components
        assert "amplitude_stability" in components
        assert "entrainment_quality" in components
    
    def test_generate_validation_report(self, test_client, ecoli_vm_config):
        """POST /api/v1/vms/{vm_id}/validations/report"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "report_test",
            "duration_hours": 24
        })
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/validations/report",
            json={"simulation_id": "report_test"}
        )
        assert response.status_code == 200
        report = response.json()
        
        assert "quality_score" in report
        assert "stability_checks" in report
        assert "deviation_checks" in report
        assert "oscillation_analysis" in report
        assert "recommendations" in report
    
    def test_batch_validation(self, test_client, ecoli_vm_config):
        """POST /api/v1/vms/{vm_id}/validations/batch"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        # Run multiple simulations
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "batch_1",
            "duration_hours": 24
        })
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "batch_2",
            "duration_hours": 24
        })
        
        # Validate all
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/validations/batch",
            json={
                "simulation_ids": ["batch_1", "batch_2"],
                "validations": ["quality-score", "stability-laplace"]
            }
        )
        assert response.status_code == 200
        results = response.json()
        
        assert len(results) == 2
        for result in results:
            assert "simulation_id" in result
            assert "validations" in result


@pytest.mark.wishful
class TestBiologicalRealism:
    """Test biological realism checks."""
    
    def test_validate_realistic_growth_rate(self, test_client, ecoli_vm_config):
        """Validate E. coli growth rate is realistic"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "growth_rate_test",
            "duration_hours": 12,
            "track_biomass": True
        })
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/validations/growth-rate",
            json={
                "simulation_id": "growth_rate_test",
                "expected_doubling_time_minutes": 20,
                "tolerance_minutes": 5
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "measured_doubling_time_minutes" in result
        assert "realistic" in result
        assert 15 <= result["measured_doubling_time_minutes"] <= 25
    
    def test_validate_metabolite_ranges(self, test_client, ecoli_vm_config):
        """Validate metabolite concentrations are in realistic ranges"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "metabolite_range_test",
            "duration_hours": 24
        })
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/validations/metabolite-ranges",
            json={
                "simulation_id": "metabolite_range_test",
                "metabolites": {
                    "ATP": {"min": 1.0, "max": 10.0},
                    "NADH": {"min": 0.1, "max": 5.0}
                }
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "all_in_range" in result
        assert "out_of_range" in result
    
    def test_validate_protein_expression_timing(self, test_client, ecoli_vm_config):
        """Validate protein expression timing is realistic"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "expression_timing_test",
            "duration_hours": 6
        })
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/validations/expression-timing",
            json={
                "simulation_id": "expression_timing_test",
                "gene": "lacZ",
                "expected_lag_minutes": 10,
                "tolerance_minutes": 5
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "measured_lag_minutes" in result
        assert "realistic" in result
