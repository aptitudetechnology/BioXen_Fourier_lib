"""
Phase 1.5 Feature: Multi-Resolution Analysis (MRA) Tests
Test wavelet-based signal decomposition and denoising capabilities

Test Strategy:
1. Backward compatibility: Existing wavelet functionality preserved
2. MRA decomposition: Signal properly decomposed into components
3. Denoising: High-frequency noise effectively removed
4. Reconstruction: Components sum back to original (within error)
5. Energy conservation: Total energy preserved across components
6. Biological realism: Works on realistic biological signals
7. Integration: Works with auto-selection and existing features

Author: BioXen Development Team
Date: October 1, 2025
"""

import pytest
import numpy as np
from bioxen_fourier_vm_lib.analysis.system_analyzer import SystemAnalyzer


class TestBackwardCompatibility:
    """Ensure existing wavelet functionality is preserved"""
    
    def test_existing_wavelet_functionality_unchanged(self):
        """Existing wavelet_lens calls should work exactly as before"""
        analyzer = SystemAnalyzer(sampling_rate=1.0)
        
        # Generate test signal
        t = np.linspace(0, 48, 200)
        signal = np.sin(2*np.pi*t/24) + 0.1*np.random.randn(len(t))
        
        # Call without MRA (default behavior)
        result = analyzer.wavelet_lens(signal, wavelet_name='morl')
        
        # Should have all original fields
        assert result.scales is not None
        assert result.coefficients is not None
        assert result.transient_events is not None
        assert result.time_frequency_map is not None
        assert result.wavelet_used == 'morl'
        
        # MRA fields should be None (not enabled)
        assert result.mra_components is None
        assert result.denoised_signal is None
        assert result.reconstruction_error is None
    
    def test_auto_select_still_works_without_mra(self):
        """Auto-selection should work unchanged when MRA not enabled"""
        analyzer = SystemAnalyzer(sampling_rate=1.0)
        
        t = np.linspace(0, 48, 200)
        signal = np.sin(2*np.pi*t/24)
        
        result = analyzer.wavelet_lens(signal, auto_select=True)
        
        # Should have auto-selection fields
        assert result.wavelet_used is not None
        assert result.selection_score is not None
        assert result.alternative_wavelets is not None
        
        # But not MRA fields
        assert result.mra_components is None
        assert result.denoised_signal is None
        assert result.reconstruction_error is None


class TestMRADecomposition:
    """Test multi-resolution analysis decomposition"""
    
    def test_mra_creates_components(self):
        """MRA should create approximation and detail components"""
        analyzer = SystemAnalyzer(sampling_rate=1.0)
        
        t = np.linspace(0, 48, 200)
        signal = np.sin(2*np.pi*t/24) + 0.1*np.random.randn(len(t))
        
        # Enable MRA with 3 levels
        result = analyzer.wavelet_lens(signal, enable_mra=True, mra_levels=3)
        
        # Should have MRA components
        assert result.mra_components is not None
        assert 'approximation' in result.mra_components
        assert 'detail_1' in result.mra_components  # Highest frequency
        assert 'detail_2' in result.mra_components  # Medium frequency
        assert 'detail_3' in result.mra_components  # Lowest frequency
        
        # Components should be same length as original
        for component in result.mra_components.values():
            assert len(component) == len(signal)
    
    def test_mra_with_different_levels(self):
        """Test MRA with different decomposition levels"""
        analyzer = SystemAnalyzer(sampling_rate=1.0)
        
        t = np.linspace(0, 48, 200)
        signal = np.sin(2*np.pi*t/24)
        
        # Test different levels
        for levels in [2, 3, 5, 7]:
            result = analyzer.wavelet_lens(signal, enable_mra=True, mra_levels=levels)
            
            # Should have approximation + N detail levels
            assert 'approximation' in result.mra_components
            
            expected_details = [f'detail_{i}' for i in range(1, levels+1)]
            for detail_name in expected_details:
                assert detail_name in result.mra_components
            
            # Should have exactly levels+1 components
            assert len(result.mra_components) == levels + 1
    
    def test_reconstruction_accuracy(self):
        """Components should sum back to original signal (within numerical error)"""
        analyzer = SystemAnalyzer(sampling_rate=1.0)
        
        # Simple test signal (easier to verify)
        signal = np.array([1, 2, 3, 4, 3, 2, 1, 0, -1, 0, 1, 2] * 10)
        
        result = analyzer.wavelet_lens(signal, enable_mra=True, mra_levels=3)
        
        # Reconstruct signal from components
        reconstructed = result.mra_components['approximation'].copy()
        for i in range(1, 4):  # Add all details
            reconstructed += result.mra_components[f'detail_{i}']
        
        # Should be very close to original (within 1e-10 typically)
        reconstruction_error = np.sqrt(np.mean((signal - reconstructed)**2))
        assert reconstruction_error < 1e-6, f"Reconstruction error too high: {reconstruction_error}"
        
        # Also check the returned reconstruction error
        assert result.reconstruction_error < 1e-6
    
    def test_wavelet_compatibility(self):
        """Different wavelets should work with MRA"""
        analyzer = SystemAnalyzer(sampling_rate=1.0)
        
        t = np.linspace(0, 48, 100)
        signal = np.sin(2*np.pi*t/24)
        
        # Test orthogonal wavelets (should work directly)
        orthogonal_wavelets = ['db4', 'db8', 'sym4', 'coif2']
        for wavelet in orthogonal_wavelets:
            result = analyzer.wavelet_lens(
                signal, 
                wavelet_name=wavelet, 
                enable_mra=True, 
                mra_levels=3
            )
            
            assert result.mra_components is not None
            assert result.wavelet_used == wavelet
        
        # Test non-orthogonal wavelets (should be converted)
        non_orthogonal = ['morl', 'mexh', 'gaus4']
        for wavelet in non_orthogonal:
            result = analyzer.wavelet_lens(
                signal, 
                wavelet_name=wavelet, 
                enable_mra=True, 
                mra_levels=3
            )
            
            # Should work (wavelet gets converted internally)
            assert result.mra_components is not None
            assert result.wavelet_used == wavelet  # Original name preserved


class TestDenoising:
    """Test signal denoising capabilities"""
    
    def test_denoising_reduces_noise(self):
        """Denoised signal should have less high-frequency noise"""
        analyzer = SystemAnalyzer(sampling_rate=1.0)
        
        # Create signal with known noise level
        t = np.linspace(0, 48, 200)
        clean_signal = np.sin(2*np.pi*t/24)
        noise = 0.2 * np.random.randn(len(t))
        noisy_signal = clean_signal + noise
        
        result = analyzer.wavelet_lens(noisy_signal, enable_mra=True, mra_levels=5)
        
        # Denoised signal should exist
        assert result.denoised_signal is not None
        assert len(result.denoised_signal) == len(noisy_signal)
        
        # Denoised should be smoother (less high-frequency content)
        original_variation = np.std(np.diff(noisy_signal))
        denoised_variation = np.std(np.diff(result.denoised_signal))
        
        assert denoised_variation < original_variation, \
            f"Denoising failed: {denoised_variation} >= {original_variation}"
    
    def test_denoising_preserves_signal(self):
        """Denoising should preserve main signal characteristics"""
        analyzer = SystemAnalyzer(sampling_rate=1.0)
        
        # Signal with clear pattern + noise
        t = np.linspace(0, 48, 200)
        signal = 5*np.sin(2*np.pi*t/24) + 0.5*np.random.randn(len(t))
        
        result = analyzer.wavelet_lens(signal, enable_mra=True, mra_levels=4)
        
        # Denoised should have similar mean and overall trend
        assert abs(np.mean(result.denoised_signal) - np.mean(signal)) < 0.5
        
        # Should preserve main oscillation (correlation should be high)
        correlation = np.corrcoef(signal, result.denoised_signal)[0, 1]
        assert correlation > 0.8, f"Denoising destroyed signal: correlation = {correlation}"
    
    def test_denoising_different_noise_levels(self):
        """Denoising should work with different noise levels"""
        analyzer = SystemAnalyzer(sampling_rate=1.0)
        
        t = np.linspace(0, 48, 200)
        clean_signal = np.sin(2*np.pi*t/24)
        
        noise_levels = [0.05, 0.1, 0.2, 0.5]
        for noise_level in noise_levels:
            noisy_signal = clean_signal + noise_level * np.random.randn(len(t))
            
            result = analyzer.wavelet_lens(noisy_signal, enable_mra=True, mra_levels=4)
            
            # Should always produce denoised signal
            assert result.denoised_signal is not None
            
            # Denoising should improve SNR
            original_snr = np.var(clean_signal) / np.var(noisy_signal - clean_signal)
            denoised_residual = result.denoised_signal - clean_signal
            denoised_snr = np.var(clean_signal) / np.var(denoised_residual)
            
            # Allow some cases where heavily noised signals can't be improved much
            if noise_level <= 0.2:
                assert denoised_snr >= original_snr, \
                    f"SNR not improved at noise level {noise_level}"


class TestEnergyConservation:
    """Test energy conservation across MRA components"""
    
    def test_energy_conservation(self):
        """Total energy should be conserved across components"""
        analyzer = SystemAnalyzer(sampling_rate=1.0)
        
        # Signal with known energy
        t = np.linspace(0, 24, 100)
        signal = 2*np.sin(2*np.pi*t/12) + np.sin(2*np.pi*t/6) + 0.1*np.random.randn(len(t))
        
        original_energy = np.sum(signal**2)
        
        result = analyzer.wavelet_lens(signal, enable_mra=True, mra_levels=4)
        
        # Sum energy across all components
        total_component_energy = 0
        for component in result.mra_components.values():
            total_component_energy += np.sum(component**2)
        
        # Energy should be conserved (within numerical precision)
        energy_ratio = total_component_energy / original_energy
        assert 0.99 < energy_ratio < 1.01, \
            f"Energy not conserved: ratio = {energy_ratio}"
    
    def test_mra_summary_statistics(self):
        """MRA summary should provide meaningful statistics"""
        analyzer = SystemAnalyzer(sampling_rate=1.0)
        
        # Multi-frequency signal
        t = np.linspace(0, 48, 200)
        signal = (5*np.sin(2*np.pi*t/24) +      # Strong 24h
                 2*np.sin(2*np.pi*t/12) +      # Medium 12h
                 0.5*np.random.randn(len(t)))   # Weak noise
        
        result = analyzer.wavelet_lens(signal, enable_mra=True, mra_levels=5)
        
        # Get summary statistics
        summary = analyzer.get_mra_summary(result.mra_components)
        
        # Should have statistics for all components
        expected_components = ['approximation'] + [f'detail_{i}' for i in range(1, 6)]
        for comp in expected_components:
            assert comp in summary
            
            stats = summary[comp]
            assert 'energy' in stats
            assert 'rms' in stats
            assert 'peak_to_peak' in stats
            assert 'frequency_estimate' in stats
            
            # Energy percentages should be reasonable
            assert 0 <= stats['energy'] <= 100
            assert stats['rms'] >= 0
            assert stats['peak_to_peak'] >= 0
            assert stats['frequency_estimate'] >= 0
        
        # Total energy should sum to ~100%
        total_energy = sum(stats['energy'] for stats in summary.values())
        assert 99 < total_energy < 101, f"Total energy percentage: {total_energy}"


class TestBiologicalRealism:
    """Test MRA on biologically realistic signals"""
    
    def test_circadian_atp_decomposition(self):
        """Test MRA on realistic circadian ATP signal"""
        analyzer = SystemAnalyzer(sampling_rate=1.0)
        
        # 72 hours of ATP with circadian + ultradian + noise
        t = np.linspace(0, 72, 300)
        atp_baseline = 100
        circadian = 30 * np.sin(2*np.pi*t/24)      # Strong 24h
        ultradian = 10 * np.sin(2*np.pi*t/12)      # Medium 12h
        noise = 3 * np.random.randn(len(t))        # Measurement noise
        
        atp_signal = atp_baseline + circadian + ultradian + noise
        
        result = analyzer.wavelet_lens(atp_signal, enable_mra=True, mra_levels=6)
        
        # Should decompose successfully
        assert result.mra_components is not None
        assert result.denoised_signal is not None
        
        # Denoised signal should preserve circadian pattern
        # (correlation with clean circadian should be high)
        clean_circadian = atp_baseline + circadian + ultradian
        correlation = np.corrcoef(clean_circadian, result.denoised_signal)[0, 1]
        assert correlation > 0.85, f"Circadian pattern not preserved: r = {correlation}"
        
        # Approximation should capture the baseline trend
        assert abs(np.mean(result.mra_components['approximation']) - atp_baseline) < 10
        
        # Get energy distribution
        summary = analyzer.get_mra_summary(result.mra_components)
        
        # Approximation should have substantial energy (captures baseline + low freq)
        assert summary['approximation']['energy'] > 50, \
            "Approximation should capture most energy"
    
    def test_stress_response_detection(self):
        """Test MRA on signal with stress response"""
        analyzer = SystemAnalyzer(sampling_rate=1.0)
        
        # Baseline with sudden stress spike
        t = np.linspace(0, 48, 200)
        baseline = 100 * np.ones(len(t))
        
        # Add stress response at t=24h (middle)
        stress_center = len(t) // 2
        stress_width = 10
        for i in range(max(0, stress_center-stress_width), 
                      min(len(t), stress_center+stress_width)):
            baseline[i] += 50 * np.exp(-0.5 * ((i - stress_center) / 3)**2)
        
        # Add measurement noise
        signal = baseline + 2*np.random.randn(len(t))
        
        result = analyzer.wavelet_lens(signal, enable_mra=True, mra_levels=5)
        
        # Detail components should capture the stress event
        # Check if any detail has high peak-to-peak variation
        summary = analyzer.get_mra_summary(result.mra_components)
        
        max_detail_variation = 0
        for name, stats in summary.items():
            if name.startswith('detail_'):
                max_detail_variation = max(max_detail_variation, stats['peak_to_peak'])
        
        # Some detail should capture significant variation from stress
        assert max_detail_variation > 10, \
            "Stress response not captured in detail components"


class TestIntegration:
    """Test MRA integration with other features"""
    
    def test_mra_with_auto_selection(self):
        """MRA should work with automatic wavelet selection"""
        analyzer = SystemAnalyzer(sampling_rate=1.0)
        
        t = np.linspace(0, 48, 200)
        signal = np.sin(2*np.pi*t/24) + 0.1*np.random.randn(len(t))
        
        # Enable both auto-selection and MRA
        result = analyzer.wavelet_lens(
            signal, 
            auto_select=True, 
            enable_mra=True, 
            mra_levels=4
        )
        
        # Should have both sets of features
        assert result.wavelet_used is not None
        assert result.selection_score is not None
        assert result.alternative_wavelets is not None
        
        assert result.mra_components is not None
        assert result.denoised_signal is not None
        assert result.reconstruction_error is not None
    
    def test_mra_with_transient_detection(self):
        """MRA should not interfere with transient detection"""
        analyzer = SystemAnalyzer(sampling_rate=1.0)
        
        # Signal with clear transient
        t = np.linspace(0, 48, 200)
        signal = np.ones(200)
        signal[90:110] = 5  # Transient event
        signal += 0.1*np.random.randn(200)
        
        result = analyzer.wavelet_lens(signal, enable_mra=True, mra_levels=3)
        
        # Should still detect transients
        assert result.transient_events is not None
        # Should detect the spike we added
        assert len(result.transient_events) > 0
        
        # Should also have MRA
        assert result.mra_components is not None
    
    def test_mra_works_with_validation(self):
        """MRA should work with signal validation"""
        analyzer = SystemAnalyzer(sampling_rate=1.0)
        
        t = np.linspace(0, 48, 200)
        signal = np.sin(2*np.pi*t/24) + 0.1*np.random.randn(len(t))
        
        # Validate first
        is_valid, issues = analyzer.validate_signal(signal)
        assert is_valid
        
        # Then analyze with MRA
        result = analyzer.wavelet_lens(signal, enable_mra=True, mra_levels=4)
        
        assert result.mra_components is not None


class TestEdgeCases:
    """Test MRA with edge cases"""
    
    def test_short_signal(self):
        """MRA should handle short signals gracefully"""
        analyzer = SystemAnalyzer(sampling_rate=1.0)
        
        # Very short signal
        signal = np.array([1, 2, 3, 4, 5, 4, 3, 2, 1])
        
        # Should not crash, but may have limited decomposition
        result = analyzer.wavelet_lens(signal, enable_mra=True, mra_levels=2)
        
        # Should have some components (even if limited)
        assert result.mra_components is not None
        assert 'approximation' in result.mra_components
    
    def test_constant_signal(self):
        """MRA should handle constant signals"""
        analyzer = SystemAnalyzer(sampling_rate=1.0)
        
        signal = np.ones(100) * 5.0
        
        result = analyzer.wavelet_lens(signal, enable_mra=True, mra_levels=3)
        
        # Should work
        assert result.mra_components is not None
        
        # Approximation should be close to constant
        assert abs(np.mean(result.mra_components['approximation']) - 5.0) < 0.1
        
        # Details should be near zero
        for i in range(1, 4):
            detail_energy = np.sum(result.mra_components[f'detail_{i}']**2)
            assert detail_energy < 0.1  # Very low energy in details
    
    def test_high_frequency_signal(self):
        """MRA should handle high-frequency signals"""
        analyzer = SystemAnalyzer(sampling_rate=1.0)
        
        # High-frequency oscillation
        t = np.linspace(0, 10, 200)
        signal = np.sin(2*np.pi*t*5)  # 5 Hz
        
        result = analyzer.wavelet_lens(signal, enable_mra=True, mra_levels=5)
        
        # Should capture high frequencies in detail components
        summary = analyzer.get_mra_summary(result.mra_components)
        
        # High-frequency details should have significant energy
        high_freq_energy = sum(summary[f'detail_{i}']['energy'] 
                              for i in range(1, 3))  # Highest freq details
        assert high_freq_energy > 20, "High frequencies not captured"


class TestPerformance:
    """Test MRA performance characteristics"""
    
    def test_mra_completes_quickly(self):
        """MRA should complete in reasonable time"""
        import time
        
        analyzer = SystemAnalyzer(sampling_rate=1.0)
        
        # Medium-sized signal
        t = np.linspace(0, 72, 500)
        signal = np.sin(2*np.pi*t/24) + 0.1*np.random.randn(len(t))
        
        start = time.time()
        result = analyzer.wavelet_lens(signal, enable_mra=True, mra_levels=6)
        elapsed = time.time() - start
        
        # Should complete quickly (generous limit)
        assert elapsed < 2.0, f"MRA too slow: {elapsed:.2f}s"
        assert result.mra_components is not None
    
    def test_different_signal_lengths(self):
        """MRA should handle different signal lengths"""
        analyzer = SystemAnalyzer(sampling_rate=1.0)
        
        for n_samples in [50, 100, 200, 500, 1000]:
            t = np.linspace(0, 48, n_samples)
            signal = np.sin(2*np.pi*t/24) + 0.1*np.random.randn(n_samples)
            
            result = analyzer.wavelet_lens(signal, enable_mra=True, mra_levels=4)
            
            # Should work for all lengths
            assert result.mra_components is not None
            
            # Components should match signal length
            for component in result.mra_components.values():
                assert len(component) == n_samples


if __name__ == '__main__':
    # Run tests with verbose output
    pytest.main([__file__, '-v', '-s'])