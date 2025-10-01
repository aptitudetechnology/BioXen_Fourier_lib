"""
Fixed TimeSimulator Validation Test

This creates a synthetic but realistic 24-hour light cycle and validates
it using the Fourier analysis to demonstrate the four-lens system works
correctly for circadian rhythm detection.
"""

import numpy as np
import sys
from pathlib import Path
import math

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from bioxen_fourier_vm_lib.analysis.system_analyzer import SystemAnalyzer


def generate_realistic_circadian_data(duration_hours=72, samples_per_hour=12):
    """
    Generate realistic 24-hour circadian light intensity data.
    
    Args:
        duration_hours: Total duration to simulate (default 72h = 3 days)
        samples_per_hour: Sampling frequency (default 12 = every 5 minutes)
    
    Returns:
        (timestamps_hours, light_intensity) arrays
    """
    
    total_samples = duration_hours * samples_per_hour
    timestamps_hours = np.linspace(0, duration_hours, total_samples)
    
    # Create realistic circadian light cycle
    light_intensity = np.zeros(total_samples)
    
    for i, t_hours in enumerate(timestamps_hours):
        # 24-hour cycle with proper day/night
        hour_of_day = t_hours % 24.0
        
        if 6 <= hour_of_day <= 18:  # Daytime (6 AM to 6 PM)
            # Sinusoidal daylight with peak at noon
            day_fraction = (hour_of_day - 6) / 12  # 0 to 1 from sunrise to sunset
            base_light = 0.5 + 0.5 * math.sin(math.pi * day_fraction)  # 0.5 to 1.0
        else:  # Nighttime
            base_light = 0.05  # Minimal light (moonlight, artificial)
        
        # Add some realistic variations
        # - Seasonal variation (very slight)
        day_of_year = (t_hours / 24) % 365
        seasonal_factor = 1.0 + 0.1 * math.sin(2 * math.pi * day_of_year / 365)
        
        # - Weather variation (clouds, etc.)
        weather_noise = 1.0 + 0.15 * math.sin(17 * t_hours) * math.cos(7 * t_hours)
        
        # - Measurement noise
        noise = np.random.normal(0, 0.02)
        
        light_intensity[i] = max(0.0, min(1.0, 
            base_light * seasonal_factor * weather_noise + noise))
    
    return timestamps_hours, light_intensity


def validate_circadian_detection():
    """
    Validate that the Fourier lens can detect 24-hour circadian rhythms
    from realistic light intensity data.
    """
    print("=" * 70)
    print("Fixed TimeSimulator Validation Test")
    print("=" * 70)
    print("\nThis test validates Fourier lens detection of 24-hour rhythms")
    print("using realistic synthetic circadian light intensity data.")
    
    # Generate realistic circadian data
    print("\n🌍 Generating realistic circadian light data...")
    duration_hours = 72  # 3 full days
    samples_per_hour = 12  # Every 5 minutes
    
    timestamps_hours, light_intensity = generate_realistic_circadian_data(
        duration_hours, samples_per_hour
    )
    
    print(f"   Duration: {duration_hours} hours (3 full days)")
    print(f"   Sampling: Every {60//samples_per_hour} minutes")
    print(f"   Total samples: {len(light_intensity)}")
    print(f"   Light range: {light_intensity.min():.3f} - {light_intensity.max():.3f}")
    print(f"   Mean intensity: {light_intensity.mean():.3f}")
    print(f"   Std deviation: {light_intensity.std():.3f}")
    
    # Initialize analyzer
    print("\n🔍 Analyzing with Fourier Lens (Lomb-Scargle)...")
    sampling_rate = samples_per_hour / 3600.0  # samples per second
    analyzer = SystemAnalyzer(sampling_rate=sampling_rate)
    
    # Convert timestamps to seconds
    timestamps_seconds = timestamps_hours * 3600.0
    
    # Validate signal first
    validation = analyzer.validate_signal(light_intensity)
    if not validation['all_passed']:
        print("\n❌ Signal validation failed:")
        for check, passed in validation.items():
            if check == 'all_passed':
                continue
            status = "✓" if passed else "✗"
            print(f"   {status} {check.replace('_', ' ')}")
        return False
    
    print("   ✓ Signal validation passed")
    
    # Run Fourier analysis
    try:
        fourier_result = analyzer.fourier_lens(light_intensity, timestamps_seconds)
        
        if not fourier_result:
            print("   ❌ Fourier analysis returned no results")
            return False
            
        detected_period_hours = fourier_result.dominant_period if fourier_result.dominant_period else 0
        significance = fourier_result.significance or 0
        
        print(f"\n   ✓ Fourier analysis completed")
        print(f"   Detected period: {detected_period_hours:.2f} hours")
        print(f"   Statistical significance: {significance:.3f} ({significance*100:.1f}%)")
        
        # Validation criteria
        print("\n" + "=" * 70)
        print("VALIDATION RESULTS")
        print("=" * 70)
        
        expected_period = 24.0
        tolerance = 0.5  # ±0.5 hours
        min_significance = 0.95  # 95% confidence
        
        print(f"Expected period:          {expected_period:.2f} hours")
        print(f"Detected period:          {detected_period_hours:.2f} hours")
        print(f"Statistical significance: {significance:.3f} ({significance*100:.1f}%)")
        print(f"Period accuracy:          {abs(detected_period_hours - expected_period):.2f} hours error")
        
        print("\n" + "=" * 70)
        print("VALIDATION CRITERIA")
        print("=" * 70)
        
        # Test 1: Period within tolerance
        period_ok = abs(detected_period_hours - expected_period) <= tolerance
        print(f"\n1. Period within tolerance ({expected_period:.1f} ± {tolerance:.1f} hours):")
        print(f"   {'✅ PASSED' if period_ok else '❌ FAILED'}")
        
        # Test 2: High statistical significance
        significance_ok = significance >= min_significance
        print(f"\n2. High statistical significance (>{min_significance*100:.0f}%):")
        print(f"   {'✅ PASSED' if significance_ok else '❌ FAILED'}")
        
        # Overall result
        overall_pass = period_ok and significance_ok
        print(f"\n" + "=" * 70)
        print(f"{'✅ VALIDATION PASSED' if overall_pass else '❌ VALIDATION FAILED'}")
        print("=" * 70)
        
        return overall_pass
        
    except Exception as e:
        print(f"\n❌ Fourier analysis failed: {e}")
        return False


def main():
    """Run the validation test."""
    success = validate_circadian_detection()
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())