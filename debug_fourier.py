"""
Debug Fourier Period Calculation Issue

Investigates why Fourier lens is detecting 0.00h periods instead of 24h.
"""

import numpy as np
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from bioxen_fourier_vm_lib.analysis.system_analyzer import SystemAnalyzer

def generate_24h_signal(duration_hours=48, samples_per_hour=10):
    """Generate clean 24-hour circadian signal"""
    total_samples = int(duration_hours * samples_per_hour)
    
    # Time in hours
    t_hours = np.linspace(0, duration_hours, total_samples)
    
    # 24-hour rhythm
    signal = 100 + 30 * np.sin(2*np.pi*t_hours/24)
    
    return t_hours, signal

def test_fourier_with_different_units():
    """Test Fourier with timestamps in different units"""
    print("="*70)
    print("Fourier Period Calculation Debug")
    print("="*70)
    
    # Generate test signal
    t_hours, signal = generate_24h_signal(duration_hours=48, samples_per_hour=10)
    
    print(f"\n📊 Generated Signal:")
    print(f"   Duration: {t_hours[-1]:.1f} hours")
    print(f"   Samples: {len(signal)}")
    print(f"   Expected period: 24.0 hours")
    
    # Test 1: Timestamps in HOURS
    print("\n" + "-"*70)
    print("TEST 1: Timestamps in HOURS")
    print("-"*70)
    
    sampling_rate_hourly = 10.0 / 3600.0  # 10 samples per hour = samples per second
    analyzer1 = SystemAnalyzer(sampling_rate=sampling_rate_hourly)
    
    print(f"Sampling rate: {sampling_rate_hourly:.8f} Hz")
    print(f"Nyquist freq: {analyzer1.nyquist_freq:.8f} Hz")
    print(f"Passing timestamps in HOURS: min={t_hours[0]:.2f}, max={t_hours[-1]:.2f}")
    
    result1 = analyzer1.fourier_lens(signal, t_hours)
    
    print(f"\nResults:")
    print(f"   Dominant frequency: {result1.dominant_frequency:.8f} Hz")
    print(f"   Dominant period: {result1.dominant_period:.6f} hours")
    print(f"   Expected: 24.0 hours")
    print(f"   Error: {abs(result1.dominant_period - 24.0):.2f} hours")
    
    # Test 2: Timestamps in SECONDS
    print("\n" + "-"*70)
    print("TEST 2: Timestamps in SECONDS")
    print("-"*70)
    
    t_seconds = t_hours * 3600.0  # Convert to seconds
    
    analyzer2 = SystemAnalyzer(sampling_rate=sampling_rate_hourly)
    
    print(f"Sampling rate: {sampling_rate_hourly:.8f} Hz")
    print(f"Passing timestamps in SECONDS: min={t_seconds[0]:.2f}, max={t_seconds[-1]:.2f}")
    
    result2 = analyzer2.fourier_lens(signal, t_seconds)
    
    print(f"\nResults:")
    print(f"   Dominant frequency: {result2.dominant_frequency:.8f} Hz")
    print(f"   Dominant period: {result2.dominant_period:.6f} hours")
    print(f"   Expected: 24.0 hours")
    print(f"   Error: {abs(result2.dominant_period - 24.0):.2f} hours")
    
    # Test 3: NO timestamps (uniform sampling)
    print("\n" + "-"*70)
    print("TEST 3: NO TIMESTAMPS (uniform sampling assumed)")
    print("-"*70)
    
    analyzer3 = SystemAnalyzer(sampling_rate=sampling_rate_hourly)
    
    print(f"Sampling rate: {sampling_rate_hourly:.8f} Hz")
    print(f"Analyzer will create timestamps internally")
    
    result3 = analyzer3.fourier_lens(signal, None)
    
    print(f"\nResults:")
    print(f"   Dominant frequency: {result3.dominant_frequency:.8f} Hz")
    print(f"   Dominant period: {result3.dominant_period:.6f} hours")
    print(f"   Expected: 24.0 hours")
    print(f"   Error: {abs(result3.dominant_period - 24.0):.2f} hours")
    
    # Diagnostic: Manual calculation
    print("\n" + "-"*70)
    print("MANUAL DIAGNOSTIC")
    print("-"*70)
    
    expected_period_seconds = 24 * 3600  # 24 hours in seconds
    expected_frequency_hz = 1.0 / expected_period_seconds
    
    print(f"\nExpected values:")
    print(f"   Period: 24 hours = {expected_period_seconds} seconds")
    print(f"   Frequency: {expected_frequency_hz:.10f} Hz")
    print(f"   Period from freq: {1/expected_frequency_hz:.2f} seconds = {1/expected_frequency_hz/3600:.2f} hours")
    
    print(f"\nActual detected values (Test 2 - seconds):")
    print(f"   Frequency: {result2.dominant_frequency:.10f} Hz")
    if result2.dominant_frequency > 0:
        period_seconds = 1.0 / result2.dominant_frequency
        period_hours = period_seconds / 3600.0
        print(f"   Period: {period_seconds:.2f} seconds = {period_hours:.2f} hours")
        print(f"   Reported period: {result2.dominant_period:.6f} hours")
    
    # Summary
    print("\n" + "="*70)
    print("DIAGNOSIS SUMMARY")
    print("="*70)
    
    results = [
        ("Hours", result1.dominant_period),
        ("Seconds", result2.dominant_period),
        ("None (auto)", result3.dominant_period)
    ]
    
    for name, period in results:
        status = "✅ CORRECT" if 20 < period < 28 else "❌ WRONG"
        error = abs(period - 24.0)
        print(f"{name:15} → {period:8.2f} hours (error: {error:6.2f}h) {status}")
    
    # Identify the issue
    print("\n🔍 ROOT CAUSE ANALYSIS:")
    
    if result2.dominant_period < 1.0:
        print("❌ Period is too small (< 1 hour)")
        print("   Likely cause: Frequency calculated correctly but conversion wrong")
        print("   OR: Timestamps not being interpreted correctly by Lomb-Scargle")
    elif result2.dominant_period > 1000:
        print("❌ Period is too large (> 1000 hours)")  
        print("   Likely cause: Frequency too small, wrong unit interpretation")
    elif 20 < result2.dominant_period < 28:
        print("✅ Calculation is CORRECT when timestamps are in SECONDS")
    
    return results


def test_with_synthetic_timesimulator_data():
    """Test with data similar to TimeSimulator output"""
    print("\n\n" + "="*70)
    print("TEST WITH TIMESIMULATOR-LIKE DATA")
    print("="*70)
    
    # Simulate TimeSimulator light intensity over 72 hours
    duration_hours = 72
    sampling_interval_minutes = 5
    samples_per_hour = 60 // sampling_interval_minutes  # 12 samples/hour
    
    total_samples = duration_hours * samples_per_hour
    
    # Create timestamps (in hours for display)
    timestamps_hours = []
    light_values = []
    
    for hour in range(duration_hours):
        for minute in range(0, 60, sampling_interval_minutes):
            time_hours = hour + minute/60.0
            timestamps_hours.append(time_hours)
            
            # Simulate light intensity (sine wave, 24h period)
            time_fraction = (time_hours % 24) / 24.0
            light = max(0.0, np.sin(2 * np.pi * time_fraction))
            light_values.append(light)
    
    timestamps_hours = np.array(timestamps_hours)
    light_values = np.array(light_values)
    timestamps_seconds = timestamps_hours * 3600.0  # Convert to seconds
    
    print(f"\nGenerated TimeSimulator-like data:")
    print(f"   Duration: {duration_hours} hours")
    print(f"   Samples: {len(light_values)}")
    print(f"   Sampling interval: {sampling_interval_minutes} minutes")
    print(f"   Light range: {light_values.min():.3f} - {light_values.max():.3f}")
    
    # Analyze
    sampling_rate = samples_per_hour / 3600.0  # Convert to Hz
    analyzer = SystemAnalyzer(sampling_rate=sampling_rate)
    
    print(f"\nAnalyzer config:")
    print(f"   Sampling rate: {sampling_rate:.8f} Hz")
    print(f"   Nyquist freq: {analyzer.nyquist_freq:.8f} Hz")
    
    result = analyzer.fourier_lens(light_values, timestamps_seconds)
    
    print(f"\nFourier Analysis Results:")
    print(f"   Dominant frequency: {result.dominant_frequency:.10f} Hz")
    print(f"   Dominant period: {result.dominant_period:.6f} hours")
    print(f"   Significance: {result.significance:.4f}")
    print(f"   Expected: 24.0 hours")
    
    if 23.9 < result.dominant_period < 24.1:
        print(f"\n✅ SUCCESS! Detected period within tolerance")
    else:
        print(f"\n❌ FAILED! Period detection is off by {abs(result.dominant_period - 24.0):.2f} hours")
    
    return result


if __name__ == "__main__":
    # Run tests
    basic_results = test_fourier_with_different_units()
    timesim_result = test_with_synthetic_timesimulator_data()
    
    print("\n" + "="*70)
    print("FINAL ASSESSMENT")
    print("="*70)
    print("\nThe issue is likely related to:")
    print("1. Timestamp unit interpretation (hours vs seconds)")
    print("2. Sampling rate specification")
    print("3. Lomb-Scargle frequency range calculation")
