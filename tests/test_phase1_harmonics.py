"""
Phase 1 Tests: Multi-Harmonic Detection

Tests for advanced Fourier analysis features including:
- Multi-harmonic detection
- Phase estimation
- Amplitude estimation
- Backward compatibility with MVP
"""

import pytest
import numpy as np
from bioxen_fourier_vm_lib.analysis.system_analyzer import SystemAnalyzer


@pytest.fixture
def analyzer():
    """Standard analyzer for testing"""
    return SystemAnalyzer(sampling_rate=1.0)  # 1 sample/hour


class TestBackwardCompatibility:
    """Test that MVP behavior is preserved"""
    
    def test_single_harmonic_default_behavior(self, analyzer):
        """Test that default behavior matches MVP (no harmonics)"""
        # 24h circadian signal
        t = np.linspace(0, 72, 300)
        signal = 100 + 30*np.sin(2*np.pi*t/24)
        
        # Default behavior (detect_harmonics=False)
        result = analyzer.fourier_lens(signal, t)
        
        assert result.harmonics is None, "Default should not detect harmonics"
        assert result.harmonic_power is None
        assert 20 < result.dominant_period < 28, "Should detect ~24h period"
        assert result.significance > 0.95
    
    def test_explicit_no_harmonics(self, analyzer):
        """Test explicit detect_harmonics=False"""
        t = np.linspace(0, 72, 300)
        signal = 100 + 30*np.sin(2*np.pi*t/24) + 10*np.sin(2*np.pi*t/12)
        
        result = analyzer.fourier_lens(signal, t, detect_harmonics=False)
        
        assert result.harmonics is None
        assert result.harmonic_power is None


class TestMultiHarmonicDetection:
    """Test multi-harmonic detection functionality"""
    
    def test_detect_two_harmonics(self, analyzer):
        """Test detection of 24h + 12h harmonics"""
        # Signal with two components
        t = np.linspace(0, 72, 300)
        signal = (100 + 
                  30*np.sin(2*np.pi*t/24) +  # 24h fundamental
                  10*np.sin(2*np.pi*t/12))   # 12h harmonic
        
        result = analyzer.fourier_lens(signal, t, detect_harmonics=True)
        
        assert result.harmonics is not None
        assert len(result.harmonics) >= 2, "Should detect at least 2 harmonics"
        
        # Check periods detected
        periods = [h['period'] for h in result.harmonics]
        assert any(20 < p < 28 for p in periods), "Should detect 24h"
        assert any(10 < p < 14 for p in periods), "Should detect 12h"
    
    def test_detect_three_harmonics(self, analyzer):
        """Test detection of 24h + 12h + 8h harmonics"""
        t = np.linspace(0, 72, 300)
        signal = (100 + 
                  30*np.sin(2*np.pi*t/24) +  # 24h
                  15*np.sin(2*np.pi*t/12) +  # 12h
                  8*np.sin(2*np.pi*t/8))     # 8h
        
        result = analyzer.fourier_lens(signal, t, detect_harmonics=True)
        
        assert len(result.harmonics) >= 3
        
        periods = [h['period'] for h in result.harmonics]
        assert any(20 < p < 28 for p in periods), "Should detect 24h"
        assert any(10 < p < 14 for p in periods), "Should detect 12h"
        assert any(7 < p < 9 for p in periods), "Should detect 8h"
    
    def test_harmonic_power_calculation(self, analyzer):
        """Test that harmonic power is summed correctly"""
        t = np.linspace(0, 72, 300)
        signal = 100 + 30*np.sin(2*np.pi*t/24) + 10*np.sin(2*np.pi*t/12)
        
        result = analyzer.fourier_lens(signal, t, detect_harmonics=True)
        
        assert result.harmonic_power is not None
        assert result.harmonic_power > 0
        assert len(result.harmonics) >= 2
        
        # Harmonic power should be sum of individual powers
        individual_sum = sum(h['power'] for h in result.harmonics)
        assert abs(result.harmonic_power - individual_sum) < 1e-10
    
    def test_max_harmonics_limit(self, analyzer):
        """Test that max_harmonics parameter works"""
        t = np.linspace(0, 72, 300)
        # Complex signal with many components
        signal = (100 + 
                  30*np.sin(2*np.pi*t/24) +
                  15*np.sin(2*np.pi*t/12) +
                  8*np.sin(2*np.pi*t/8) +
                  5*np.sin(2*np.pi*t/6))
        
        result = analyzer.fourier_lens(signal, t, detect_harmonics=True, max_harmonics=2)
        
        assert len(result.harmonics) <= 2, "Should respect max_harmonics limit"
    
    def test_noisy_signal_harmonics(self, analyzer):
        """Test robustness with noisy signal"""
        np.random.seed(42)  # Reproducible
        t = np.linspace(0, 72, 300)
        clean = 100 + 30*np.sin(2*np.pi*t/24) + 10*np.sin(2*np.pi*t/12)
        noise = 5*np.random.randn(len(t))
        signal = clean + noise
        
        result = analyzer.fourier_lens(signal, t, detect_harmonics=True)
        
        # Should still detect at least one harmonic
        assert len(result.harmonics) >= 1
        
        # Dominant should be around 24h
        assert 20 < result.harmonics[0]['period'] < 28


class TestPhaseEstimation:
    """Test phase estimation accuracy"""
    
    def test_zero_phase(self, analyzer):
        """Test detection of zero phase signal"""
        t = np.linspace(0, 48, 200)
        phase_true = 0.0
        signal = 100 + 30*np.sin(2*np.pi*t/24 + phase_true)
        
        result = analyzer.fourier_lens(signal, t, detect_harmonics=True)
        
        assert len(result.harmonics) >= 1
        phase_detected = result.harmonics[0]['phase']
        
        # Should be within 0.2 radians (~11 degrees)
        # (allows for some numerical error)
        phase_error = abs(phase_detected - phase_true)
        phase_error = min(phase_error, 2*np.pi - phase_error)  # Account for wraparound
        assert phase_error < 0.2
    
    def test_quarter_phase(self, analyzer):
        """Test detection of π/2 phase"""
        t = np.linspace(0, 48, 200)
        phase_true = np.pi / 2
        signal = 100 + 30*np.sin(2*np.pi*t/24 + phase_true)
        
        result = analyzer.fourier_lens(signal, t, detect_harmonics=True)
        
        assert len(result.harmonics) >= 1
        phase_detected = result.harmonics[0]['phase']
        
        phase_error = abs(phase_detected - phase_true)
        phase_error = min(phase_error, 2*np.pi - phase_error)
        assert phase_error < 0.2
    
    def test_phase_wraparound(self, analyzer):
        """Test phase near 2π boundary"""
        t = np.linspace(0, 48, 200)
        phase_true = 7*np.pi/4  # Near 2π
        signal = 100 + 30*np.sin(2*np.pi*t/24 + phase_true)
        
        result = analyzer.fourier_lens(signal, t, detect_harmonics=True)
        
        assert len(result.harmonics) >= 1
        phase_detected = result.harmonics[0]['phase']
        
        # Phase should be in [0, 2π)
        assert 0 <= phase_detected < 2*np.pi
        
        # Check wrapped distance
        phase_error = abs(phase_detected - phase_true)
        phase_error = min(phase_error, 2*np.pi - phase_error)
        assert phase_error < 0.3


class TestAmplitudeEstimation:
    """Test amplitude estimation accuracy"""
    
    def test_small_amplitude(self, analyzer):
        """Test detection of small amplitude (10 units)"""
        t = np.linspace(0, 48, 200)
        amplitude_true = 10.0
        signal = 100 + amplitude_true*np.sin(2*np.pi*t/24)
        
        result = analyzer.fourier_lens(signal, t, detect_harmonics=True)
        
        assert len(result.harmonics) >= 1
        amplitude_detected = result.harmonics[0]['amplitude']
        
        # Should be within 10%
        relative_error = abs(amplitude_detected - amplitude_true) / amplitude_true
        assert relative_error < 0.1
    
    def test_large_amplitude(self, analyzer):
        """Test detection of large amplitude (50 units)"""
        t = np.linspace(0, 48, 200)
        amplitude_true = 50.0
        signal = 100 + amplitude_true*np.sin(2*np.pi*t/24)
        
        result = analyzer.fourier_lens(signal, t, detect_harmonics=True)
        
        assert len(result.harmonics) >= 1
        amplitude_detected = result.harmonics[0]['amplitude']
        
        relative_error = abs(amplitude_detected - amplitude_true) / amplitude_true
        assert relative_error < 0.1
    
    def test_multiple_amplitudes(self, analyzer):
        """Test correct amplitude estimation for multiple harmonics"""
        t = np.linspace(0, 72, 300)
        amp1, amp2 = 30.0, 15.0
        signal = (100 + 
                  amp1*np.sin(2*np.pi*t/24) +
                  amp2*np.sin(2*np.pi*t/12))
        
        result = analyzer.fourier_lens(signal, t, detect_harmonics=True)
        
        assert len(result.harmonics) >= 2
        
        # Check that detected amplitudes are close to true values
        amplitudes = sorted([h['amplitude'] for h in result.harmonics[:2]], reverse=True)
        assert abs(amplitudes[0] - amp1) / amp1 < 0.15  # 15% tolerance
        assert abs(amplitudes[1] - amp2) / amp2 < 0.15


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_constant_signal(self, analyzer):
        """Test handling of constant signal (no oscillation)"""
        t = np.linspace(0, 48, 200)
        signal = np.ones(200) * 100
        
        result = analyzer.fourier_lens(signal, t, detect_harmonics=True)
        
        # Should detect nothing or very weak components
        if result.harmonics:
            assert len(result.harmonics) == 0 or result.harmonics[0]['power'] < 0.1
    
    def test_single_frequency_only(self, analyzer):
        """Test that single pure sine only detects one harmonic"""
        t = np.linspace(0, 72, 300)
        signal = 100 + 30*np.sin(2*np.pi*t/24)
        
        result = analyzer.fourier_lens(signal, t, detect_harmonics=True, max_harmonics=5)
        
        # Should detect 1-2 harmonics (main + possibly weak noise)
        assert 1 <= len(result.harmonics) <= 2
    
    def test_irregular_timestamps(self, analyzer):
        """Test with irregular timestamp spacing"""
        # Create irregular timestamps (missing some points)
        t_regular = np.linspace(0, 72, 300)
        # Remove random points
        np.random.seed(42)
        keep_indices = np.random.choice(300, size=250, replace=False)
        keep_indices = np.sort(keep_indices)
        t_irregular = t_regular[keep_indices]
        
        signal = 100 + 30*np.sin(2*np.pi*t_irregular/24)
        
        result = analyzer.fourier_lens(signal, t_irregular, detect_harmonics=True)
        
        # Should still detect 24h period
        assert len(result.harmonics) >= 1
        assert 20 < result.harmonics[0]['period'] < 28


class TestBiologicalRealism:
    """Test with biologically realistic signals"""
    
    def test_circadian_plus_ultradian(self, analyzer):
        """Test realistic circadian + ultradian rhythm"""
        # Typical ATP levels: 24h circadian + 12h metabolic
        t = np.linspace(0, 96, 400)  # 4 days
        
        circadian = 30*np.sin(2*np.pi*t/24 + np.pi/6)  # Peak at 6am
        ultradian = 15*np.sin(2*np.pi*t/12)  # Metabolic
        baseline = 100
        noise = 3*np.random.randn(len(t))
        
        atp_signal = baseline + circadian + ultradian + noise
        
        result = analyzer.fourier_lens(atp_signal, t, detect_harmonics=True)
        
        assert len(result.harmonics) >= 2
        
        # Should find both rhythms
        periods = [h['period'] for h in result.harmonics]
        has_circadian = any(20 < p < 28 for p in periods)
        has_ultradian = any(10 < p < 14 for p in periods)
        
        assert has_circadian, "Should detect circadian (24h)"
        assert has_ultradian, "Should detect ultradian (12h)"
    
    def test_damped_oscillation(self, analyzer):
        """Test with damped oscillation (transient rhythm)"""
        t = np.linspace(0, 72, 300)
        
        # Damped sine wave (e.g., after perturbation)
        damping = np.exp(-t/48)  # Decay over 48 hours
        signal = 100 + 30*damping*np.sin(2*np.pi*t/24)
        
        result = analyzer.fourier_lens(signal, t, detect_harmonics=True)
        
        # Should still detect dominant period even if damped
        if len(result.harmonics) > 0:
            assert 20 < result.harmonics[0]['period'] < 28


class TestIntegration:
    """Integration tests with other components"""
    
    def test_harmonics_with_mvp_validation(self, analyzer):
        """Test that harmonic detection works with signal validation"""
        t = np.linspace(0, 72, 300)
        signal = 100 + 30*np.sin(2*np.pi*t/24) + 10*np.sin(2*np.pi*t/12)
        
        # First validate
        validation = analyzer.validate_signal(signal)
        assert validation['all_passed']
        
        # Then analyze with harmonics
        result = analyzer.fourier_lens(signal, t, detect_harmonics=True)
        
        assert len(result.harmonics) >= 2
    
    def test_performance_large_signal(self, analyzer):
        """Test performance with large signal (1000 points)"""
        import time
        
        t = np.linspace(0, 168, 1000)  # 1 week, 1000 samples
        signal = (100 + 
                  30*np.sin(2*np.pi*t/24) +
                  15*np.sin(2*np.pi*t/12) +
                  8*np.sin(2*np.pi*t/8))
        
        start = time.time()
        result = analyzer.fourier_lens(signal, t, detect_harmonics=True, max_harmonics=5)
        elapsed = time.time() - start
        
        # Should complete in reasonable time (< 2 seconds for 1000 points)
        assert elapsed < 2.0
        assert len(result.harmonics) >= 3


if __name__ == "__main__":
    pytest.main([__file__, '-v'])
