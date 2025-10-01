"""MVP Unit Tests for SystemAnalyzer

Tests all four lenses with synthetic data and validates integration
with PerformanceProfiler and BioXenHypervisor.

Run with: pytest tests/test_system_analyzer_mvp.py -v
"""

import pytest
import numpy as np
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from bioxen_fourier_vm_lib.analysis.system_analyzer import SystemAnalyzer


@pytest.fixture
def analyzer():
    """Create analyzer with default sampling rate"""
    return SystemAnalyzer(sampling_rate=1.0)


@pytest.fixture
def synthetic_signal():
    """Generate 24-hour circadian rhythm signal"""
    # Use 3 days of data with good sampling
    t = np.linspace(0, 72, 864)  # 72 hours (3 days), 12 samples/hour  
    signal = 100 + 30*np.sin(2*np.pi*t/24)  # 24-hour rhythm
    return t, signal


@pytest.fixture
def noisy_signal():
    """Generate clean signal + noise for filtering tests"""
    t = np.linspace(0, 10, 100)
    clean = np.sin(2*np.pi*t)
    noisy = clean + 0.5*np.random.randn(len(t))
    return t, clean, noisy


# ========== LENS 1: FOURIER TESTS ==========

def test_fourier_lens_detects_circadian(analyzer, synthetic_signal):
    """Test that Fourier lens detects 24-hour rhythm"""
    timestamps, signal = synthetic_signal
    
    # Convert to seconds for analyzer
    timestamps_seconds = timestamps * 3600.0
    
    result = analyzer.fourier_lens(signal, timestamps_seconds)
    
    # Check result structure
    assert hasattr(result, 'frequencies')
    assert hasattr(result, 'power_spectrum')
    assert hasattr(result, 'dominant_frequency')
    assert hasattr(result, 'dominant_period')
    assert hasattr(result, 'significance')
    
    # Check period detection (should be ~24 hours)
    assert 20 < result.dominant_period < 28, \
        f"Expected ~24h period, got {result.dominant_period:.2f}h"
    
    # Check significance (should be high for clean signal)
    assert result.significance > 0.90, \
        f"Expected high significance, got {result.significance:.4f}"


def test_fourier_lens_with_uniform_sampling(analyzer):
    """Test Fourier lens with uniform sampling (no timestamps)"""
    # Simple sine wave
    t = np.linspace(0, 10, 100)
    signal = np.sin(2*np.pi*t)
    
    result = analyzer.fourier_lens(signal)  # No timestamps provided
    
    assert result.dominant_frequency > 0
    assert result.dominant_period > 0


# ========== LENS 2: WAVELET TESTS ==========

def test_wavelet_lens_runs(analyzer, synthetic_signal):
    """Test that wavelet lens executes without error"""
    _, signal = synthetic_signal
    
    result = analyzer.wavelet_lens(signal)
    
    # Check result structure
    assert hasattr(result, 'scales')
    assert hasattr(result, 'coefficients')
    assert hasattr(result, 'transient_events')
    assert hasattr(result, 'time_frequency_map')
    
    # Check dimensions
    assert result.coefficients.shape[1] == len(signal), \
        "Coefficients should match signal length"
    assert isinstance(result.transient_events, list)
    assert len(result.scales) > 0


def test_wavelet_lens_detects_transient(analyzer):
    """Test wavelet detection of transient spike"""
    # Signal with transient spike
    t = np.linspace(0, 100, 500)
    signal = np.sin(2*np.pi*t/10)  # Base signal
    signal += 5 * np.exp(-((t - 50)**2) / 5)  # Spike at t=50
    
    result = analyzer.wavelet_lens(signal)
    
    # Should detect at least one transient event
    assert len(result.transient_events) > 0, "Should detect transient spike"
    
    # Check event structure
    for event in result.transient_events:
        assert 'time_index' in event
        assert 'intensity' in event
        assert 'duration_samples' in event


# ========== LENS 3: LAPLACE TESTS ==========

def test_laplace_lens_stability(analyzer, synthetic_signal):
    """Test that Laplace lens classifies stable system"""
    _, signal = synthetic_signal
    
    result = analyzer.laplace_lens(signal)
    
    # Check result structure
    assert hasattr(result, 'poles')
    assert hasattr(result, 'stability')
    assert hasattr(result, 'natural_frequency')
    assert hasattr(result, 'damping_ratio')
    
    # Check stability classification
    assert result.stability in ['stable', 'oscillatory', 'unstable']
    assert result.natural_frequency > 0
    assert result.damping_ratio >= 0


def test_laplace_lens_pole_locations(analyzer):
    """Test that Laplace correctly identifies pole locations"""
    # Damped oscillation (should be stable)
    t = np.linspace(0, 10, 200)
    signal = np.exp(-0.5*t) * np.sin(2*np.pi*t)
    
    result = analyzer.laplace_lens(signal)
    
    # For damped oscillation, should be stable
    assert result.stability in ['stable', 'oscillatory']
    
    # Should have complex conjugate poles
    assert len(result.poles) == 2


# ========== LENS 4: Z-TRANSFORM TESTS ==========

def test_z_transform_lens_reduces_noise(analyzer, noisy_signal):
    """Test that Z-transform reduces noise"""
    _, clean, noisy = noisy_signal
    
    result = analyzer.z_transform_lens(noisy, cutoff_freq=0.2)
    
    # Check result structure
    assert hasattr(result, 'filtered_signal')
    assert hasattr(result, 'noise_reduction_percent')
    assert hasattr(result, 'cutoff_frequency')
    
    # Check filtered signal length matches input
    assert len(result.filtered_signal) == len(noisy)
    
    # Filtered should be closer to clean than noisy
    error_noisy = np.mean((noisy - clean)**2)
    error_filtered = np.mean((result.filtered_signal - clean)**2)
    
    assert error_filtered < error_noisy, "Filtering should reduce error"
    
    # Noise reduction should be positive
    assert result.noise_reduction_percent >= 0


def test_z_transform_lens_auto_cutoff(analyzer, noisy_signal):
    """Test Z-transform with automatic cutoff frequency selection"""
    _, _, noisy = noisy_signal
    
    result = analyzer.z_transform_lens(noisy)  # No cutoff specified
    
    # Should auto-select cutoff
    assert result.cutoff_frequency > 0
    assert result.cutoff_frequency < analyzer.nyquist_freq


# ========== VALIDATION TESTS ==========

def test_validation_passes_good_signal(analyzer, synthetic_signal):
    """Test that validation passes for good signal"""
    _, signal = synthetic_signal
    
    result = analyzer.validate_signal(signal)
    
    assert 'sufficient_length' in result
    assert 'not_constant' in result
    assert 'no_nans' in result
    assert 'no_infs' in result
    assert 'sufficient_variance' in result
    assert 'all_passed' in result
    
    assert result['all_passed'], "Good signal should pass all checks"


def test_validation_catches_constant_signal(analyzer):
    """Test that validation catches constant signal"""
    constant = np.ones(100)
    
    result = analyzer.validate_signal(constant)
    
    assert not result['not_constant'], "Should detect constant signal"
    assert not result['all_passed'], "Constant signal should fail validation"


def test_validation_catches_nans(analyzer):
    """Test that validation catches NaN values"""
    with_nans = np.array([1, 2, np.nan, 4, 5, 6, 7, 8, 9, 10])
    
    result = analyzer.validate_signal(with_nans)
    
    assert not result['no_nans'], "Should detect NaN values"
    assert not result['all_passed'], "Signal with NaNs should fail validation"


def test_validation_catches_insufficient_length(analyzer):
    """Test that validation catches too-short signals"""
    short_signal = np.random.randn(20)  # Less than 50 samples
    
    result = analyzer.validate_signal(short_signal)
    
    assert not result['sufficient_length'], "Should detect insufficient length"
    assert not result['all_passed'], "Short signal should fail validation"


# ========== INTEGRATION TESTS ==========

def test_profiler_integration():
    """Test that PerformanceProfiler integration works"""
    from bioxen_fourier_vm_lib.monitoring.profiler import PerformanceProfiler
    from bioxen_fourier_vm_lib.hypervisor.core import BioXenHypervisor
    from bioxen_fourier_vm_lib.chassis import ChassisType
    
    # Initialize hypervisor and profiler
    hypervisor = BioXenHypervisor(chassis_type=ChassisType.ECOLI)
    profiler = PerformanceProfiler(hypervisor, monitoring_interval=1.0)
    
    # Check analyzer was created (if imports successful)
    if hasattr(profiler, 'analyzer'):
        assert profiler.analyzer is not None
        assert profiler.analyzer.sampling_rate == 1.0
        
        # Check methods exist
        assert hasattr(profiler, 'extract_time_series')
        assert hasattr(profiler, 'analyze_metric_fourier')
        assert hasattr(profiler, 'analyze_metric_wavelet')
        assert hasattr(profiler, 'analyze_metric_laplace')
        assert hasattr(profiler, 'analyze_metric_ztransform')
        assert hasattr(profiler, 'analyze_metric_all')


def test_hypervisor_integration():
    """Test that BioXenHypervisor analysis integration works"""
    from bioxen_fourier_vm_lib.hypervisor.core import BioXenHypervisor
    from bioxen_fourier_vm_lib.monitoring.profiler import PerformanceProfiler
    from bioxen_fourier_vm_lib.chassis import ChassisType
    
    # Initialize
    hypervisor = BioXenHypervisor(chassis_type=ChassisType.ECOLI)
    profiler = PerformanceProfiler(hypervisor, monitoring_interval=1.0)
    
    # Check integration attributes
    assert hasattr(hypervisor, 'profiler')
    assert hasattr(hypervisor, '_analysis_enabled')
    
    # Check methods exist
    assert hasattr(hypervisor, 'enable_performance_analysis')
    assert hasattr(hypervisor, 'analyze_system_dynamics')
    assert hasattr(hypervisor, 'validate_time_simulator')
    
    # Test enabling analysis
    hypervisor.enable_performance_analysis(profiler)
    assert hypervisor._analysis_enabled
    assert hypervisor.profiler is profiler


# ========== EDGE CASE TESTS ==========

def test_empty_signal_handling(analyzer):
    """Test behavior with empty signal"""
    empty = np.array([])
    
    result = analyzer.validate_signal(empty)
    
    assert not result['all_passed']
    assert not result['sufficient_length']


def test_single_value_signal(analyzer):
    """Test behavior with single-value signal"""
    single = np.array([42.0])
    
    result = analyzer.validate_signal(single)
    
    assert not result['all_passed']


def test_very_long_signal(analyzer):
    """Test that analyzer handles very long signals"""
    # 10,000 samples
    long_signal = np.sin(2*np.pi*np.linspace(0, 100, 10000))
    
    result = analyzer.fourier_lens(long_signal)
    
    assert result.dominant_frequency > 0
    assert len(result.frequencies) > 0


# ========== PERFORMANCE TESTS ==========

def test_analysis_completes_quickly(analyzer, synthetic_signal):
    """Test that analysis completes in reasonable time"""
    import time
    
    _, signal = synthetic_signal
    
    start = time.time()
    
    # Run all lenses
    analyzer.fourier_lens(signal)
    analyzer.wavelet_lens(signal)
    analyzer.laplace_lens(signal)
    analyzer.z_transform_lens(signal)
    
    elapsed = time.time() - start
    
    # Should complete in under 5 seconds on reasonable hardware
    assert elapsed < 5.0, f"Analysis took {elapsed:.2f}s (too slow)"


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, '-v', '--tb=short'])
