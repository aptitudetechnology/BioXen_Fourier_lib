"""
Test module: Four-Lens Analysis

Tests for Fourier, Wavelet, Laplace, and Z-Transform analysis APIs.

Status: 🔮 Wishful - Defines ideal multi-domain analysis APIs
"""

import pytest
import numpy as np


@pytest.mark.wishful
class TestFourierAnalysis:
    """Test Fourier transform analysis APIs."""
    
    def test_compute_fft(self, test_client, ecoli_vm_config):
        """POST /api/v1/vms/{vm_id}/analysis/fourier"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        # Run simulation
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "fft_test",
            "duration_hours": 24,
            "enable_history": True
        })
        
        # Compute FFT
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/analysis/fourier",
            json={
                "simulation_id": "fft_test",
                "variable": "NADH"
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "frequencies" in result
        assert "magnitudes" in result
        assert "phases" in result
        assert len(result["frequencies"]) == len(result["magnitudes"])
    
    def test_detect_circadian_period_fft(self, test_client, yeast_circadian_vm_config):
        """Detect circadian period using FFT"""
        create_response = test_client.post("/api/v1/vms", json=yeast_circadian_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "circadian_fft",
            "duration_hours": 72,
            "enable_history": True
        })
        
        # Fourier analysis
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/analysis/fourier",
            json={
                "simulation_id": "circadian_fft",
                "variable": "FRQ_protein"
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        # Find dominant frequency
        dominant_idx = np.argmax(result["magnitudes"][1:]) + 1  # Skip DC
        dominant_freq = result["frequencies"][dominant_idx]
        period_hours = 1 / (dominant_freq / 3600)  # Convert to hours
        
        assert 22 <= period_hours <= 26  # Circadian range
    
    def test_power_spectral_density(self, test_client, ecoli_vm_config):
        """POST /api/v1/vms/{vm_id}/analysis/psd"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "psd_test",
            "duration_hours": 24,
            "enable_history": True
        })
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/analysis/psd",
            json={
                "simulation_id": "psd_test",
                "variable": "ATP"
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "frequencies" in result
        assert "power" in result
    
    def test_detect_harmonics(self, test_client, cyanobacteria_vm_config):
        """Detect harmonic frequencies"""
        create_response = test_client.post("/api/v1/vms", json=cyanobacteria_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "harmonics_test",
            "duration_hours": 96,
            "enable_history": True
        })
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/analysis/harmonics",
            json={
                "simulation_id": "harmonics_test",
                "variable": "KaiC_phosphorylation",
                "num_harmonics": 5
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "fundamental_frequency" in result
        assert "harmonics" in result
        assert len(result["harmonics"]) <= 5
    
    def test_compare_frequency_spectra(self, test_client, yeast_circadian_vm_config):
        """Compare frequency spectra across conditions"""
        create_response = test_client.post("/api/v1/vms", json=yeast_circadian_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        # Run two simulations
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "condition_a",
            "duration_hours": 72,
            "temperature_celsius": 25
        })
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "condition_b",
            "duration_hours": 72,
            "temperature_celsius": 35
        })
        
        # Compare spectra
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/analysis/compare-spectra",
            json={
                "simulation_ids": ["condition_a", "condition_b"],
                "variable": "FRQ_protein"
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert len(result["spectra"]) == 2
        assert "spectral_similarity" in result


@pytest.mark.wishful
class TestWaveletAnalysis:
    """Test wavelet transform analysis APIs."""
    
    def test_compute_cwt(self, test_client, yeast_circadian_vm_config):
        """POST /api/v1/vms/{vm_id}/analysis/wavelet"""
        create_response = test_client.post("/api/v1/vms", json=yeast_circadian_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "wavelet_test",
            "duration_hours": 72,
            "enable_history": True
        })
        
        # Continuous Wavelet Transform
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/analysis/wavelet",
            json={
                "simulation_id": "wavelet_test",
                "variable": "FRQ_protein",
                "wavelet_type": "morlet",
                "scales": list(range(1, 100))
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "scales" in result
        assert "coefficients" in result  # 2D array
        assert "frequencies" in result
    
    def test_detect_transients(self, test_client, yeast_circadian_vm_config):
        """Detect transient events using wavelets"""
        create_response = test_client.post("/api/v1/vms", json=yeast_circadian_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        # Simulation with light pulse (transient)
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "transient_test",
            "duration_hours": 48,
            "perturbations": [
                {"type": "light_pulse", "time_hour": 12, "duration_hours": 1}
            ]
        })
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/analysis/wavelet-transients",
            json={
                "simulation_id": "transient_test",
                "variable": "FRQ_protein"
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "transients_detected" in result
        if result["transients_detected"]:
            assert "transient_times" in result
            assert "transient_magnitudes" in result
    
    def test_analyze_phase_coherence(self, test_client, cyanobacteria_vm_config):
        """Analyze phase coherence between signals"""
        create_response = test_client.post("/api/v1/vms", json=cyanobacteria_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "coherence_test",
            "duration_hours": 96
        })
        
        # Wavelet coherence between KaiA and KaiC
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/analysis/wavelet-coherence",
            json={
                "simulation_id": "coherence_test",
                "variable1": "KaiA",
                "variable2": "KaiC"
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "coherence" in result  # 2D array (time x frequency)
        assert "phase_difference" in result
    
    def test_time_frequency_ridge(self, test_client, yeast_circadian_vm_config):
        """Extract time-frequency ridge (instantaneous frequency)"""
        create_response = test_client.post("/api/v1/vms", json=yeast_circadian_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "ridge_test",
            "duration_hours": 72
        })
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/analysis/wavelet-ridge",
            json={
                "simulation_id": "ridge_test",
                "variable": "FRQ_protein"
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "times" in result
        assert "instantaneous_frequency" in result
        assert len(result["times"]) == len(result["instantaneous_frequency"])


@pytest.mark.wishful
class TestLaplaceAnalysis:
    """Test Laplace transform analysis APIs."""
    
    def test_compute_laplace(self, test_client, ecoli_vm_config):
        """POST /api/v1/vms/{vm_id}/analysis/laplace"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "laplace_test",
            "duration_hours": 24,
            "enable_history": True
        })
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/analysis/laplace",
            json={
                "simulation_id": "laplace_test",
                "variable": "ATP"
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "s_values" in result  # Complex frequency values
        assert "laplace_transform" in result
    
    def test_find_poles_zeros(self, test_client, ecoli_vm_config):
        """POST /api/v1/vms/{vm_id}/analysis/laplace-poles"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "poles_test",
            "duration_hours": 24
        })
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/analysis/laplace-poles",
            json={
                "simulation_id": "poles_test",
                "variable": "NADH"
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "poles" in result
        assert "zeros" in result
        
        # Check pole structure
        for pole in result["poles"]:
            assert "real" in pole
            assert "imaginary" in pole
    
    def test_stability_analysis(self, test_client, ecoli_vm_config):
        """Analyze system stability via Laplace poles"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "stability_test",
            "duration_hours": 24
        })
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/analysis/laplace-stability",
            json={
                "simulation_id": "stability_test",
                "variable": "ATP"
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "stable" in result
        assert "dominant_pole" in result
        assert "settling_time_estimate" in result
    
    def test_frequency_response(self, test_client, yeast_circadian_vm_config):
        """Compute frequency response (Bode plot data)"""
        create_response = test_client.post("/api/v1/vms", json=yeast_circadian_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "freq_response_test",
            "duration_hours": 48
        })
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/analysis/frequency-response",
            json={
                "simulation_id": "freq_response_test",
                "variable": "FRQ_protein",
                "frequency_range": {"min": 0.01, "max": 1.0, "num_points": 50}
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "frequencies" in result
        assert "magnitude_db" in result
        assert "phase_degrees" in result
    
    def test_step_response_prediction(self, test_client, ecoli_vm_config):
        """Predict step response from Laplace domain"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "step_test",
            "duration_hours": 12
        })
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/analysis/laplace-step-response",
            json={
                "simulation_id": "step_test",
                "variable": "ATP",
                "step_magnitude": 10.0
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "predicted_response" in result
        assert "rise_time" in result
        assert "settling_time" in result
        assert "overshoot_percent" in result


@pytest.mark.wishful
class TestZTransformAnalysis:
    """Test Z-transform analysis APIs."""
    
    def test_compute_ztransform(self, test_client, ecoli_vm_config):
        """POST /api/v1/vms/{vm_id}/analysis/ztransform"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "ztransform_test",
            "duration_hours": 24,
            "enable_history": True
        })
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/analysis/ztransform",
            json={
                "simulation_id": "ztransform_test",
                "variable": "NADH"
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "z_values" in result
        assert "ztransform" in result
    
    def test_design_digital_filter(self, test_client, ecoli_vm_config):
        """POST /api/v1/vms/{vm_id}/analysis/design-filter"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/analysis/design-filter",
            json={
                "filter_type": "lowpass",
                "cutoff_frequency": 0.1,
                "order": 4,
                "sampling_rate": 1.0
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "filter_coefficients" in result
        assert "b" in result["filter_coefficients"]  # Numerator
        assert "a" in result["filter_coefficients"]  # Denominator
    
    def test_apply_digital_filter(self, test_client, ecoli_vm_config):
        """POST /api/v1/vms/{vm_id}/analysis/apply-filter"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "filter_test",
            "duration_hours": 24
        })
        
        # Design filter
        filter_response = test_client.post(
            f"/api/v1/vms/{vm_id}/analysis/design-filter",
            json={"filter_type": "lowpass", "cutoff_frequency": 0.1, "order": 4}
        )
        filter_coeff = filter_response.json()["filter_coefficients"]
        
        # Apply filter
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/analysis/apply-filter",
            json={
                "simulation_id": "filter_test",
                "variable": "ATP",
                "filter_coefficients": filter_coeff
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "filtered_signal" in result
        assert "timestamps" in result
    
    def test_detect_oscillation_stability_ztransform(self, test_client, yeast_circadian_vm_config):
        """Detect oscillation stability using Z-transform"""
        create_response = test_client.post("/api/v1/vms", json=yeast_circadian_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "z_stability_test",
            "duration_hours": 72
        })
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/analysis/ztransform-stability",
            json={
                "simulation_id": "z_stability_test",
                "variable": "FRQ_protein"
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "stable" in result
        assert "poles" in result
        
        # Z-domain poles should be inside unit circle for stability
        for pole in result["poles"]:
            magnitude = (pole["real"]**2 + pole["imaginary"]**2)**0.5
            if result["stable"]:
                assert magnitude < 1.0
    
    def test_compute_discrete_frequency_response(self, test_client, ecoli_vm_config):
        """Compute discrete-time frequency response"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "discrete_freq_test",
            "duration_hours": 24
        })
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/analysis/discrete-frequency-response",
            json={
                "simulation_id": "discrete_freq_test",
                "variable": "ATP",
                "num_frequencies": 100
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "frequencies" in result
        assert "magnitude" in result
        assert "phase" in result


@pytest.mark.wishful
class TestMultiLensComparison:
    """Test multi-domain comparison and analysis."""
    
    def test_four_lens_analysis(self, test_client, yeast_circadian_vm_config):
        """POST /api/v1/vms/{vm_id}/analysis/four-lens"""
        create_response = test_client.post("/api/v1/vms", json=yeast_circadian_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "four_lens_test",
            "duration_hours": 72,
            "enable_history": True
        })
        
        # Run all four analyses
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/analysis/four-lens",
            json={
                "simulation_id": "four_lens_test",
                "variable": "FRQ_protein"
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "fourier" in result
        assert "wavelet" in result
        assert "laplace" in result
        assert "ztransform" in result
        
        # Each lens should have key metrics
        assert "dominant_frequency" in result["fourier"]
        assert "transients_detected" in result["wavelet"]
        assert "stable" in result["laplace"]
        assert "digital_filter_suggested" in result["ztransform"]
    
    def test_compare_time_vs_frequency_domain(self, test_client, cyanobacteria_vm_config):
        """Compare time-domain vs frequency-domain insights"""
        create_response = test_client.post("/api/v1/vms", json=cyanobacteria_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "domain_compare",
            "duration_hours": 96
        })
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/analysis/compare-domains",
            json={
                "simulation_id": "domain_compare",
                "variable": "KaiC_phosphorylation"
            }
        )
        assert response.status_code == 200
        result = response.json()
        
        assert "time_domain" in result
        assert "frequency_domain" in result
        assert "comparison_summary" in result
    
    def test_generate_comprehensive_report(self, test_client, yeast_circadian_vm_config):
        """POST /api/v1/vms/{vm_id}/analysis/comprehensive-report"""
        create_response = test_client.post("/api/v1/vms", json=yeast_circadian_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "report_test",
            "duration_hours": 72
        })
        
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/analysis/comprehensive-report",
            json={
                "simulation_id": "report_test",
                "variable": "FRQ_protein",
                "include_all_lenses": True
            }
        )
        assert response.status_code == 200
        report = response.json()
        
        assert "summary" in report
        assert "fourier_analysis" in report
        assert "wavelet_analysis" in report
        assert "laplace_analysis" in report
        assert "ztransform_analysis" in report
        assert "recommendations" in report
    
    def test_export_analysis_plots(self, test_client, yeast_circadian_vm_config):
        """GET /api/v1/vms/{vm_id}/analysis/{analysis_id}/plots"""
        create_response = test_client.post("/api/v1/vms", json=yeast_circadian_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        # Run analysis
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "plot_test",
            "duration_hours": 72
        })
        
        analysis_response = test_client.post(
            f"/api/v1/vms/{vm_id}/analysis/four-lens",
            json={"simulation_id": "plot_test", "variable": "FRQ_protein"}
        )
        analysis_id = analysis_response.json()["analysis_id"]
        
        # Get plots
        response = test_client.get(
            f"/api/v1/vms/{vm_id}/analysis/{analysis_id}/plots",
            params={"format": "png"}
        )
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/zip"
    
    def test_batch_multi_lens_analysis(self, test_client, ecoli_vm_config):
        """POST /api/v1/vms/{vm_id}/analysis/batch-four-lens"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        
        # Run simulation
        test_client.post(f"/api/v1/vms/{vm_id}/simulations", json={
            "simulation_id": "batch_test",
            "duration_hours": 24
        })
        
        # Analyze multiple variables
        response = test_client.post(
            f"/api/v1/vms/{vm_id}/analysis/batch-four-lens",
            json={
                "simulation_id": "batch_test",
                "variables": ["ATP", "NADH", "biomass"]
            }
        )
        assert response.status_code == 200
        results = response.json()
        
        assert len(results) == 3
        for var_result in results:
            assert "variable" in var_result
            assert "fourier" in var_result
            assert "wavelet" in var_result
            assert "laplace" in var_result
            assert "ztransform" in var_result
