"""
TimeSimulator Validation Test

Validates that TimeSimulator produces accurate 24-hour rhythms
using Fourier lens analysis.

This tests an EXISTING BioXen component (hypervisor/TimeSimulator.py)
to verify it generates accurate circadian cycles that can be detected
by our Fourier analysis.

Expected: Detect 24.0 hours ± 0.1 hours with >95% significance
"""

import numpy as np
import sys
from pathlib import Path
import time

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from bioxen_fourier_vm_lib.hypervisor.TimeSimulator import TimeSimulator
from bioxen_fourier_vm_lib.analysis.system_analyzer import SystemAnalyzer


def validate_time_simulator():
    """
    Validate TimeSimulator produces accurate 24h cycles.
    
    Collects light intensity data over 72 hours (3 full days) and analyzes
    with Fourier lens to verify period accuracy.
    
    Returns:
        Dictionary with validation results
    """
    print("=" * 70)
    print("TimeSimulator Validation Test")
    print("=" * 70)
    print("\nThis test validates that BioXen's TimeSimulator generates")
    print("accurate 24-hour circadian cycles using Fourier analysis.")
    
    # Initialize TimeSimulator (uses real Earth astronomical constants)
    print("\n🌍 Initializing TimeSimulator...")
    sim = TimeSimulator(
        latitude=37.7749,      # San Francisco
        longitude=-122.4194,
        time_acceleration=1.0  # Real-time (can speed up for testing)
    )
    print(f"   Location: San Francisco (37.77°N, 122.42°W)")
    print(f"   Solar day constant: {TimeSimulator.SOLAR_DAY_LENGTH:.2f} seconds")
    print(f"   Time acceleration: 1.0x (real-time)")
    
    # Collect light intensity over 2 years for maximum accuracy
    duration_hours = 2 * 365 * 24  # 17520 hours = 730 days = 2 years
    sampling_interval_minutes = 5
    samples_per_hour = 60 // sampling_interval_minutes  # 12 samples/hour
    
    print(f"\n📊 Collecting {duration_hours} hours of light intensity data...")
    print(f"   That's {duration_hours / 24:.0f} days = {duration_hours / 24 / 365:.2f} years")
    print(f"   Sampling every {sampling_interval_minutes} minutes")
    print(f"   Expected samples: {duration_hours * samples_per_hour}")
    
    samples = []
    timestamps_seconds = []
    
    print("\n   Progress: ", end='', flush=True)
    progress_interval = max(1, duration_hours // 20)  # Show ~20 progress markers
    for hour in range(duration_hours):
        if hour % progress_interval == 0:
            days = hour / 24
            print(f"{days:.0f}d ", end='', flush=True)
        
        for minute in range(0, 60, sampling_interval_minutes):
            state = sim.get_current_state()
            samples.append(state.light_intensity)
            # Use actual simulation time from the state
            timestamps_seconds.append(state.simulation_time_elapsed)
            
            # Advance simulation time by sampling interval
            sim.advance_time(sampling_interval_minutes * 60)  # Convert minutes to seconds
    
    print("Done!")
    
    samples = np.array(samples)
    timestamps_seconds = np.array(timestamps_seconds)
    timestamps_hours = timestamps_seconds / 3600.0  # For display purposes
    
    print(f"\n   ✓ Collected {len(samples)} samples over {duration_hours} hours")
    print(f"   Debug: First 5 timestamps (sec): {timestamps_seconds[:5]}")
    print(f"   Debug: Last 5 timestamps (sec): {timestamps_seconds[-5:]}")
    print(f"   Debug: Timestamp range: {timestamps_seconds[0]} to {timestamps_seconds[-1]} seconds")
    print(f"   Debug: Timestamp spacing (first 5 intervals): {np.diff(timestamps_seconds[:6])}")
    print(f"   Light intensity range: {samples.min():.3f} - {samples.max():.3f}")
    print(f"   Mean intensity: {samples.mean():.3f}")
    print(f"   Std deviation: {samples.std():.3f}")
    
    # Analyze with Fourier lens
    print("\n🔍 Analyzing with Fourier Lens (Lomb-Scargle)...")
    print("   This may take a few seconds...")
    
    # Calculate sampling rate
    sampling_rate = samples_per_hour / 3600.0  # samples per second
    analyzer = SystemAnalyzer(sampling_rate=sampling_rate)
    
    # Validate signal quality first
    validation = analyzer.validate_signal(samples)
    if not validation['all_passed']:
        print("\n❌ Signal validation failed:")
        for check, passed in validation.items():
            if not passed and check != 'all_passed':
                print(f"   ✗ {check}")
        return {'passed': False, 'error': 'Signal validation failed'}
    
    print("   ✓ Signal validation passed")
    
    # Apply Fourier analysis
    result = analyzer.fourier_lens(samples, timestamps_seconds)
    
    # Display results
    print("\n" + "="*70)
    print("RESULTS")
    print("="*70)
    
    expected_period = 24.0
    detected_period = result.dominant_period
    frequency_hz = result.dominant_frequency
    significance = result.significance
    
    print(f"\nExpected period:          {expected_period:.2f} hours")
    print(f"Detected period:          {detected_period:.2f} hours")
    print(f"Dominant frequency:       {frequency_hz:.8f} Hz")
    print(f"                          ({1/frequency_hz:.2f} seconds)")
    print(f"Statistical significance: {significance:.4f} ({significance*100:.2f}%)")
    
    # Calculate accuracy
    period_error = abs(detected_period - expected_period)
    accuracy = (1.0 - period_error / expected_period) * 100
    print(f"\nPeriod error:             {period_error:.4f} hours")
    print(f"Accuracy:                 {accuracy:.2f}%")
    
    # Pass/Fail criteria
    print("\n" + "="*70)
    print("VALIDATION CRITERIA")
    print("="*70)
    
    tolerance_passed = 23.9 <= detected_period <= 24.1
    significance_passed = significance > 0.95
    
    print(f"\n1. Period within tolerance (24.0 ± 0.1 hours):")
    if tolerance_passed:
        print(f"   ✅ PASSED - {detected_period:.2f}h is within acceptable range")
    else:
        print(f"   ❌ FAILED - {detected_period:.2f}h is outside acceptable range")
    
    print(f"\n2. High statistical significance (>95%):")
    if significance_passed:
        print(f"   ✅ PASSED - {significance*100:.2f}% confidence")
    else:
        print(f"   ❌ FAILED - {significance*100:.2f}% confidence (too low)")
    
    # Overall result
    overall_passed = tolerance_passed and significance_passed
    
    print("\n" + "="*70)
    if overall_passed:
        print("✅ VALIDATION PASSED")
        print("\nTimeSimulator successfully generates accurate 24-hour circadian cycles!")
        print("The Fourier lens correctly detected the expected periodicity.")
    else:
        print("❌ VALIDATION FAILED")
        print("\nTimeSimulator output does not meet accuracy requirements.")
        if not tolerance_passed:
            print(f"   Issue: Period {detected_period:.2f}h outside tolerance")
        if not significance_passed:
            print(f"   Issue: Significance {significance*100:.1f}% too low")
    print("="*70)
    
    return {
        'passed': overall_passed,
        'detected_period': detected_period,
        'expected_period': expected_period,
        'accuracy': accuracy,
        'significance': significance,
        'period_error': period_error,
        'tolerance_passed': tolerance_passed,
        'significance_passed': significance_passed
    }


if __name__ == "__main__":
    result = validate_time_simulator()
    
    # Exit with appropriate code
    exit_code = 0 if result['passed'] else 1
    
    print(f"\nExit code: {exit_code}")
    exit(exit_code)
