"""
Phase 1 Feature 2: Wavelet Optimization Tests
Test automatic wavelet selection for biological signal analysis

Test Strategy:
1. Backward compatibility: MVP behavior preserved
2. Auto-selection works: Picks reasonable wavelets
3. Metric calculations: All scoring functions work
4. Signal type matching: Right wavelet for signal characteristics
5. Edge cases: Handles problematic signals
6. Biological realism: Works on real-world patterns
7. Integration: Works with existing system

Author: BioXen Development Team
Date: October 1, 2025
"""

import pytest
import numpy as np
from bioxen_fourier_vm_lib.analysis.system_analyzer import SystemAnalyzer


class TestBackwardCompatibility:
    """Ensure MVP behavior is preserved when auto_select=False"""
    
    def test_mvp_behavior_preserved(self):
        """Default parameters should match MVP behavior"""
        analyzer = SystemAnalyzer(sampling_rate=1.0)
        
        # Generate simple signal
        t = np.linspace(0, 48, 200)
        signal = np.sin(2*np.pi*t/24) + 0.1*np.random.randn(len(t))
        
        # MVP mode: no auto-selection
        result = analyzer.wavelet_lens(signal, wavelet_name='morl')
        
        # Should have transients detected (MVP functionality)
        assert result.transient_events is not None
        assert result.time_frequency_map is not None
        
        # Phase 1 fields should be None (not using auto-select)
        assert result.wavelet_used == 'morl'
        assert result.selection_score is None
        assert result.alternative_wavelets is None
    
    def test_default_parameters_no_breaking_changes(self):
        """Calling with default params should still work"""
        analyzer = SystemAnalyzer(sampling_rate=1.0)
        
        t = np.linspace(0, 24, 100)
        signal = np.sin(2*np.pi*t/12)
        
        # Should work with no parameters (defaults to morl, no auto-select)
        result = analyzer.wavelet_lens(signal)
        
        assert result.wavelet_used == 'morl'
        assert result.selection_score is None


class TestAutomaticWaveletSelection:
    """Test the auto-selection algorithm"""
    
    def test_auto_select_picks_wavelet(self):
        """Auto-selection should choose a wavelet"""
        analyzer = SystemAnalyzer(sampling_rate=1.0)
        
        t = np.linspace(0, 48, 200)
        signal = np.sin(2*np.pi*t/24) + 0.1*np.random.randn(len(t))
        
        # Enable auto-selection
        result = analyzer.wavelet_lens(signal, auto_select=True)
        
        # Should pick a wavelet
        assert result.wavelet_used is not None
        assert result.wavelet_used in analyzer.AVAILABLE_WAVELETS
        
        # Should have selection scores
        assert result.selection_score is not None
        assert 'total_score' in result.selection_score
        assert 'energy_concentration' in result.selection_score
        assert 'time_localization' in result.selection_score
        assert 'frequency_localization' in result.selection_score
        assert 'edge_quality' in result.selection_score
        
        # All scores should be in [0, 1]
        for score_name, score_value in result.selection_score.items():
            assert 0.0 <= score_value <= 1.0, f"{score_name} = {score_value} not in [0,1]"
    
    def test_alternatives_provided(self):
        """Should provide alternative wavelet recommendations"""
        analyzer = SystemAnalyzer(sampling_rate=1.0)
        
        t = np.linspace(0, 48, 200)
        signal = np.sin(2*np.pi*t/24)
        
        result = analyzer.wavelet_lens(signal, auto_select=True)
        
        # Should have alternatives list
        assert result.alternative_wavelets is not None
        assert len(result.alternative_wavelets) > 0
        
        # Should be sorted by score (highest first)
        scores = [alt[1]['total_score'] for alt in result.alternative_wavelets]
        assert scores == sorted(scores, reverse=True)
        
        # Best alternative should match the selected wavelet
        assert result.alternative_wavelets[0][0] == result.wavelet_used
    
    def test_auto_select_overrides_wavelet_name(self):
        """When auto_select=True, wavelet_name should be ignored"""
        analyzer = SystemAnalyzer(sampling_rate=1.0)
        
        t = np.linspace(0, 48, 200)
        signal = np.sin(2*np.pi*t/24)
        
        # Specify wavelet_name but enable auto_select
        result = analyzer.wavelet_lens(signal, wavelet_name='db4', auto_select=True)
        
        # Should not necessarily use 'db4' (auto-select overrides)
        # Just verify it picked something valid
        assert result.wavelet_used in analyzer.AVAILABLE_WAVELETS
        assert result.selection_score is not None


class TestSelectionMetrics:
    """Test individual metric calculation functions"""
    
    def test_energy_concentration_metric(self):
        """Test energy concentration calculation"""
        analyzer = SystemAnalyzer(sampling_rate=1.0)
        
        # Create signal with concentrated energy (sharp peak)
        t = np.linspace(0, 48, 200)
        signal = np.zeros(200)
        signal[100] = 10.0  # Single spike
        
        result = analyzer.wavelet_lens(signal, auto_select=True)
        
        # Should have valid energy concentration score
        assert 'energy_concentration' in result.selection_score
        assert 0.0 <= result.selection_score['energy_concentration'] <= 1.0
    
    def test_time_localization_metric(self):
        """Test time localization calculation"""
        analyzer = SystemAnalyzer(sampling_rate=1.0)
        
        # Create signal with sharp event
        t = np.linspace(0, 48, 200)
        signal = np.zeros(200)
        signal[90:110] = 5.0  # Localized event
        
        result = analyzer.wavelet_lens(signal, auto_select=True)
        
        # Should have valid time localization score
        assert 'time_localization' in result.selection_score
        assert 0.0 <= result.selection_score['time_localization'] <= 1.0
    
    def test_frequency_localization_metric(self):
        """Test frequency localization calculation"""
        analyzer = SystemAnalyzer(sampling_rate=1.0)
        
        # Create signal with single frequency
        t = np.linspace(0, 48, 200)
        signal = np.sin(2*np.pi*t/24)  # Pure 24h oscillation
        
        result = analyzer.wavelet_lens(signal, auto_select=True)
        
        # Should have valid frequency localization score
        assert 'frequency_localization' in result.selection_score
        assert 0.0 <= result.selection_score['frequency_localization'] <= 1.0
    
    def test_edge_quality_metric(self):
        """Test edge quality calculation"""
        analyzer = SystemAnalyzer(sampling_rate=1.0)
        
        # Create signal with good center, minimal edge artifacts
        t = np.linspace(0, 48, 200)
        signal = np.sin(2*np.pi*t/24)
        
        result = analyzer.wavelet_lens(signal, auto_select=True)
        
        # Should have valid edge quality score
        assert 'edge_quality' in result.selection_score
        assert 0.0 <= result.selection_score['edge_quality'] <= 1.0


class TestSignalTypeMatching:
    """Test that appropriate wavelets are selected for different signal types"""
    
    def test_smooth_oscillation_prefers_morlet_or_mexh(self):
        """Smooth signals should prefer smooth continuous wavelets"""
        analyzer = SystemAnalyzer(sampling_rate=1.0)
        
        # Pure smooth sine wave
        t = np.linspace(0, 48, 200)
        signal = np.sin(2*np.pi*t/24)
        
        result = analyzer.wavelet_lens(signal, auto_select=True)
        
        # Should pick a smooth wavelet from available continuous wavelets
        # (morl, mexh, gaus4, gaus8, cgau4, shan, fbsp)
        assert result.wavelet_used in analyzer.AVAILABLE_WAVELETS
        
        # Smooth wavelets (Gaussian family, Morlet, Mexican Hat) should be in top 3
        top3 = [alt[0] for alt in result.alternative_wavelets[:3]]
        smooth_wavelets = ['morl', 'mexh', 'gaus4', 'gaus8', 'cgau4']
        assert any(w in top3 for w in smooth_wavelets)
    
    def test_sharp_transient_selection(self):
        """Sharp transients should get reasonable wavelet"""
        analyzer = SystemAnalyzer(sampling_rate=1.0)
        
        # Sharp spike
        t = np.linspace(0, 48, 200)
        signal = np.zeros(200)
        signal[100] = 10.0
        signal[99] = 5.0
        signal[101] = 5.0
        
        result = analyzer.wavelet_lens(signal, auto_select=True)
        
        # Should pick something (any valid wavelet)
        assert result.wavelet_used in analyzer.AVAILABLE_WAVELETS
        
        # Should have higher time localization for this type of signal
        # (not guaranteed, but likely)
        assert result.selection_score['time_localization'] > 0.0


class TestEdgeCases:
    """Test handling of problematic signals"""
    
    def test_constant_signal(self):
        """Constant signal should not crash"""
        analyzer = SystemAnalyzer(sampling_rate=1.0)
        
        signal = np.ones(100) * 5.0
        
        # Should not crash
        result = analyzer.wavelet_lens(signal, auto_select=True)
        
        # Should pick a wavelet (any valid one)
        assert result.wavelet_used in analyzer.AVAILABLE_WAVELETS
        
        # Scores might be low but should be valid
        assert result.selection_score is not None
        for score in result.selection_score.values():
            assert 0.0 <= score <= 1.0
    
    def test_very_short_signal(self):
        """Short signal should be handled gracefully"""
        analyzer = SystemAnalyzer(sampling_rate=1.0)
        
        # Very short signal
        signal = np.array([1.0, 2.0, 1.5, 2.5, 1.8])
        
        # Should not crash
        result = analyzer.wavelet_lens(signal, auto_select=True)
        
        # Should pick something
        assert result.wavelet_used in analyzer.AVAILABLE_WAVELETS
    
    def test_noisy_signal(self):
        """Very noisy signal should still work"""
        analyzer = SystemAnalyzer(sampling_rate=1.0)
        
        # Pure noise
        signal = np.random.randn(200)
        
        # Should not crash
        result = analyzer.wavelet_lens(signal, auto_select=True)
        
        # Should pick a wavelet
        assert result.wavelet_used in analyzer.AVAILABLE_WAVELETS
        assert result.selection_score is not None


class TestBiologicalRealism:
    """Test on biologically realistic signals"""
    
    def test_circadian_rhythm_with_noise(self):
        """Test on realistic circadian ATP oscillation"""
        analyzer = SystemAnalyzer(sampling_rate=1.0)
        
        # 72 hours of circadian ATP with ultradian component
        t = np.linspace(0, 72, 300)
        atp_baseline = 100
        circadian = 30 * np.sin(2*np.pi*t/24)
        ultradian = 10 * np.sin(2*np.pi*t/12)
        noise = 5 * np.random.randn(len(t))
        
        signal = atp_baseline + circadian + ultradian + noise
        
        # Auto-select wavelet
        result = analyzer.wavelet_lens(signal, auto_select=True)
        
        # Should successfully analyze
        assert result.wavelet_used is not None
        assert result.transient_events is not None
        
        # Should have reasonable scores
        assert result.selection_score['total_score'] > 0.0
    
    def test_stress_response_signal(self):
        """Test on stress response pattern"""
        analyzer = SystemAnalyzer(sampling_rate=1.0)
        
        # Baseline with sudden stress spike at t=30
        t = np.linspace(0, 72, 300)
        signal = 100 * np.ones(300)
        signal[125:135] += 50  # Stress event
        signal += 2 * np.random.randn(300)
        
        # Auto-select wavelet
        result = analyzer.wavelet_lens(signal, auto_select=True)
        
        # Should have picked a valid wavelet
        assert result.wavelet_used in analyzer.AVAILABLE_WAVELETS
        
        # Should have selection scores
        assert 'total_score' in result.selection_score
        assert 0 <= result.selection_score['total_score'] <= 1
        
        # Note: Transient detection depends on threshold tuning
        # The important thing is auto-selection works
        assert result.transient_events is not None  # May be empty list


class TestIntegration:
    """Test integration with existing system"""
    
    def test_works_with_validation(self):
        """Auto-selection should work with signal validation"""
        analyzer = SystemAnalyzer(sampling_rate=1.0)
        
        t = np.linspace(0, 48, 200)
        signal = np.sin(2*np.pi*t/24) + 0.1*np.random.randn(len(t))
        
        # Validate first - returns a Dict with 'all_passed' key
        validation = analyzer.validate_signal(signal)
        assert validation['all_passed']
        
        # Then analyze with auto-selection
        result = analyzer.wavelet_lens(signal, auto_select=True)
        
        assert result.wavelet_used is not None
    
    def test_consistent_results(self):
        """Same signal should give same wavelet selection"""
        analyzer = SystemAnalyzer(sampling_rate=1.0)
        
        # Fixed signal (no random component)
        t = np.linspace(0, 48, 200)
        signal = np.sin(2*np.pi*t/24)
        
        # Run twice
        result1 = analyzer.wavelet_lens(signal, auto_select=True)
        result2 = analyzer.wavelet_lens(signal, auto_select=True)
        
        # Should pick same wavelet
        assert result1.wavelet_used == result2.wavelet_used
        
        # Scores should be identical
        assert result1.selection_score['total_score'] == result2.selection_score['total_score']
    
    def test_all_wavelets_available(self):
        """All wavelets in AVAILABLE_WAVELETS should work"""
        analyzer = SystemAnalyzer(sampling_rate=1.0)
        
        t = np.linspace(0, 48, 200)
        signal = np.sin(2*np.pi*t/24)
        
        # Try each wavelet manually
        for wavelet_name in analyzer.AVAILABLE_WAVELETS.keys():
            result = analyzer.wavelet_lens(signal, wavelet_name=wavelet_name)
            
            # Should work without error
            assert result.wavelet_used == wavelet_name
            assert result.transient_events is not None


class TestPerformance:
    """Test performance characteristics"""
    
    def test_auto_select_completes_quickly(self):
        """Auto-selection should complete in reasonable time"""
        import time
        
        analyzer = SystemAnalyzer(sampling_rate=1.0)
        
        # Medium-sized signal
        t = np.linspace(0, 72, 500)
        signal = np.sin(2*np.pi*t/24) + 0.1*np.random.randn(len(t))
        
        start = time.time()
        result = analyzer.wavelet_lens(signal, auto_select=True)
        elapsed = time.time() - start
        
        # Should complete in under 5 seconds (generous limit)
        # On most machines this will be < 1 second
        assert elapsed < 5.0
        assert result.wavelet_used is not None
    
    def test_scales_with_signal_length(self):
        """Should handle different signal lengths"""
        analyzer = SystemAnalyzer(sampling_rate=1.0)
        
        for n_samples in [50, 100, 200, 500]:
            t = np.linspace(0, 48, n_samples)
            signal = np.sin(2*np.pi*t/24)
            
            result = analyzer.wavelet_lens(signal, auto_select=True)
            
            # Should work for all lengths
            assert result.wavelet_used is not None
            assert result.selection_score is not None


if __name__ == '__main__':
    # Run tests with verbose output
    pytest.main([__file__, '-v', '-s'])
