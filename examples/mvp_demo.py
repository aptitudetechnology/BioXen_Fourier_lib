"""
MVP Demo: Four-Lens Analysis System

Demonstrates all four lenses analyzing synthetic biological VM data.

This demo shows:
1. Synthetic signal generation (circadian + transient + noise)
2. Signal validation
3. All four lens analyses
4. Result interpretation

No dependencies on running hypervisor - pure standalone demo.
"""

import numpy as np
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from bioxen_fourier_vm_lib.analysis.system_analyzer import SystemAnalyzer


def generate_synthetic_signal(duration_hours=48, sampling_rate=1.0):
    """
    Generate synthetic biological signal with:
    - 24-hour circadian rhythm (base metabolic cycle)
    - Transient stress response at t=24h (spike in ATP)
    - Measurement noise (realistic sensor noise)
    
    Args:
        duration_hours: Total duration of signal (hours)
        sampling_rate: Samples per hour
    
    Returns:
        (timestamps, signal) tuple
    """
    t = np.arange(0, duration_hours, 1.0/sampling_rate)
    
    # Base circadian rhythm (ATP levels oscillating around 100%)
    # Peak at midday, trough at midnight
    circadian = 100 + 30 * np.sin(2*np.pi*t/24 + np.pi/2)
    
    # Add transient stress response (spike at t=24h)
    # Simulates: resource reallocation, VM context switch, metabolic shift
    stress_response = 50 * np.exp(-((t - 24)**2) / 10)
    
    # Measurement noise (sensor variability, molecular fluctuations)
    noise = 5 * np.random.randn(len(t))
    
    signal = circadian + stress_response + noise
    
    return t, signal


def main():
    print("=" * 70)
    print("BioXen Four-Lens Analysis System - MVP Demo")
    print("=" * 70)
    print("\nThis demo analyzes synthetic biological signal to demonstrate")
    print("all four mathematical lenses working together.")
    
    # Generate synthetic data
    print("\n📊 Generating synthetic biological signal...")
    print("   Components:")
    print("   - 24-hour circadian rhythm (base metabolic cycle)")
    print("   - Transient stress response at t=24h (ATP spike)")
    print("   - Gaussian measurement noise (realistic sensor)")
    
    timestamps, signal = generate_synthetic_signal(duration_hours=48, sampling_rate=1.0)
    
    print(f"\n   Duration: 48 hours")
    print(f"   Samples: {len(signal)}")
    print(f"   Sampling rate: 1.0 samples/hour")
    print(f"   Signal range: {signal.min():.1f} - {signal.max():.1f}")
    
    # Initialize analyzer
    print("\n🔬 Initializing SystemAnalyzer...")
    analyzer = SystemAnalyzer(sampling_rate=1.0/3600.0)  # 1 sample/hour = 1/3600 Hz
    print("   ✓ Analyzer ready")
    
    # Validate signal
    print("\n✅ Validating signal quality...")
    validation = analyzer.validate_signal(signal)
    for check, passed in validation.items():
        if check == 'all_passed':
            continue
        status = "✓" if passed else "✗"
        check_name = check.replace('_', ' ').title()
        print(f"   {status} {check_name}")
    
    if not validation['all_passed']:
        print("\n❌ Signal validation failed!")
        return 1
    
    print("\n   ✓ All validation checks passed")
    
    # LENS 1: Fourier (Lomb-Scargle)
    print("\n" + "="*70)
    print("🔍 LENS 1: Fourier Analysis (Lomb-Scargle)")
    print("="*70)
    print("Purpose: Detect periodic rhythms in frequency domain")
    print("Question: 'What rhythms exist in this biological system?'")
    print("\nAnalyzing...")
    
    # Convert timestamps to seconds for analyzer
    timestamps_seconds = timestamps * 3600.0
    fourier = analyzer.fourier_lens(signal, timestamps_seconds)
    
    print(f"\nResults:")
    print(f"   Dominant frequency: {fourier.dominant_frequency:.6f} Hz")
    print(f"   Dominant period: {fourier.dominant_period:.2f} hours")
    print(f"   Statistical significance: {fourier.significance:.4f} ({fourier.significance*100:.1f}%)")
    
    if 20 < fourier.dominant_period < 28:
        print(f"\n   ✅ Successfully detected ~24h circadian rhythm!")
    else:
        print(f"\n   ⚠️  Expected ~24h period, got {fourier.dominant_period:.1f}h")
    
    # LENS 2: Wavelet
    print("\n" + "="*70)
    print("🔍 LENS 2: Wavelet Analysis")
    print("="*70)
    print("Purpose: Localize transient events in time-frequency domain")
    print("Question: 'When and where do sudden changes occur?'")
    print("\nAnalyzing...")
    
    wavelet = analyzer.wavelet_lens(signal)
    
    print(f"\nResults:")
    print(f"   Scales analyzed: {len(wavelet.scales)}")
    print(f"   Time-frequency map: {wavelet.time_frequency_map.shape}")
    print(f"   Transient events detected: {len(wavelet.transient_events)}")
    
    if wavelet.transient_events:
        print("\n   Detected events:")
        for i, event in enumerate(wavelet.transient_events[:3]):  # Show first 3
            time_hours = timestamps[event['time_index']]
            duration_hours = event['duration_samples'] / 1.0  # samples per hour
            print(f"   Event {i+1}:")
            print(f"      Time: {time_hours:.1f} hours")
            print(f"      Intensity: {event['intensity']:.2f}")
            print(f"      Duration: {duration_hours:.1f} hours")
        
        # Check if we detected the stress response around t=24h
        for event in wavelet.transient_events:
            time_hours = timestamps[event['time_index']]
            if 20 < time_hours < 28:
                print(f"\n   ✅ Successfully detected stress response near t=24h!")
                break
    else:
        print("   No significant transient events detected")
    
    # LENS 3: Laplace (Stability)
    print("\n" + "="*70)
    print("🔍 LENS 3: Laplace Analysis (System Stability)")
    print("="*70)
    print("Purpose: Assess system stability via pole locations")
    print("Question: 'Is this biological system stable or unstable?'")
    print("\nAnalyzing...")
    
    laplace = analyzer.laplace_lens(signal)
    
    print(f"\nResults:")
    print(f"   System stability: {laplace.stability.upper()}")
    print(f"   Natural frequency: {laplace.natural_frequency:.6f} Hz")
    print(f"   Damping ratio: {laplace.damping_ratio:.4f}")
    print(f"   Poles: {laplace.poles}")
    
    print("\n   Interpretation:")
    if laplace.stability == 'stable':
        print("   ✅ System is STABLE - returns to equilibrium after perturbations")
        print("      (Healthy homeostasis maintained)")
    elif laplace.stability == 'oscillatory':
        print("   ⚠️  System is OSCILLATORY - sustained rhythmic behavior")
        print("      (Natural biological rhythms present)")
    else:
        print("   ❌ System is UNSTABLE - diverges from equilibrium")
        print("      (Homeostasis compromised, potential failure)")
    
    # LENS 4: Z-Transform (Filtering)
    print("\n" + "="*70)
    print("🔍 LENS 4: Z-Transform (Digital Filtering)")
    print("="*70)
    print("Purpose: Remove noise while preserving biological signal")
    print("Question: 'What is the true signal beneath the noise?'")
    print("\nAnalyzing...")
    
    ztransform = analyzer.z_transform_lens(signal)
    
    print(f"\nResults:")
    print(f"   Cutoff frequency: {ztransform.cutoff_frequency:.6f} Hz")
    print(f"   Noise reduction: {ztransform.noise_reduction_percent:.1f}%")
    print(f"   Original signal std: {np.std(signal):.2f}")
    print(f"   Filtered signal std: {np.std(ztransform.filtered_signal):.2f}")
    
    # Calculate SNR improvement
    snr_improvement = 20 * np.log10(
        np.std(signal) / np.std(ztransform.filtered_signal)
    )
    print(f"   SNR improvement: {snr_improvement:.1f} dB")
    
    if ztransform.noise_reduction_percent > 30:
        print(f"\n   ✅ Successfully reduced noise by {ztransform.noise_reduction_percent:.1f}%")
    
    # Summary
    print("\n" + "="*70)
    print("✅ MVP Demo Complete!")
    print("="*70)
    
    print("\n📊 Summary of Four-Lens Analysis:")
    print(f"   1. Fourier: Detected {fourier.dominant_period:.1f}h period (circadian rhythm)")
    print(f"   2. Wavelet: Found {len(wavelet.transient_events)} transient events")
    print(f"   3. Laplace: System is {laplace.stability} (ζ={laplace.damping_ratio:.2f})")
    print(f"   4. Z-Transform: Reduced noise by {ztransform.noise_reduction_percent:.1f}%")
    
    print("\n🚀 Next steps:")
    print("   1. Run: python examples/validate_time_simulator.py")
    print("      (Validates BioXen TimeSimulator produces accurate 24h cycles)")
    print("   ")
    print("   2. Run: python examples/demo_profiler_integration.py")
    print("      (Analyzes real PerformanceProfiler data from running hypervisor)")
    print("   ")
    print("   3. Run: pytest tests/")
    print("      (Execute full test suite)")
    
    return 0


if __name__ == "__main__":
    exit(main())
