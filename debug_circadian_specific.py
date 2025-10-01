"""
Debug the exact circadian validation issue
"""

import numpy as np
import sys
from pathlib import Path
import math

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from bioxen_fourier_vm_lib.analysis.system_analyzer import SystemAnalyzer


def debug_circadian_validation():
    """Debug the exact same data generation as validate_circadian_fixed.py"""
    
    print("Debugging Circadian Validation Issue")
    print("=" * 50)
    
    # Use EXACT same parameters as validate_circadian_fixed.py
    duration_hours = 72
    samples_per_hour = 12
    
    total_samples = duration_hours * samples_per_hour
    timestamps_hours = np.linspace(0, duration_hours, total_samples)
    
    print(f"Duration: {duration_hours} hours")
    print(f"Samples per hour: {samples_per_hour}")
    print(f"Total samples: {total_samples}")
    print(f"Timestamps (hours): {timestamps_hours[0]:.3f} to {timestamps_hours[-1]:.3f}")
    
    # Create realistic circadian light cycle (EXACT same as validation script)
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
        np.random.seed(42)  # Fixed seed for reproducible results
        noise = np.random.normal(0, 0.02)
        
        light_intensity[i] = max(0.0, min(1.0, 
            base_light * seasonal_factor * weather_noise + noise))
    
    print(f"Light range: {light_intensity.min():.3f} to {light_intensity.max():.3f}")
    print(f"Light mean: {light_intensity.mean():.3f}")
    print(f"Light std: {light_intensity.std():.3f}")
    
    # Initialize analyzer (EXACT same as validation script)
    sampling_rate = samples_per_hour / 3600.0  # samples per second
    analyzer = SystemAnalyzer(sampling_rate=sampling_rate)
    
    print(f"Sampling rate: {sampling_rate:.8f} Hz")
    print(f"Nyquist frequency: {analyzer.nyquist_freq:.8f} Hz")
    
    # Convert timestamps to seconds (EXACT same as validation script)
    timestamps_seconds = timestamps_hours * 3600.0
    
    print(f"Timestamps (seconds): {timestamps_seconds[0]:.1f} to {timestamps_seconds[-1]:.1f}")
    
    # Validate signal
    validation = analyzer.validate_signal(light_intensity)
    print(f"Signal validation: {validation}")
    
    if not validation['all_passed']:
        print("❌ Signal validation failed!")
        return
    
    # Run Fourier analysis
    print("\nRunning Fourier analysis...")
    fourier_result = analyzer.fourier_lens(light_intensity, timestamps_seconds)
    
    print(f"Dominant frequency: {fourier_result.dominant_frequency:.10f} Hz")
    print(f"Dominant period: {fourier_result.dominant_period:.6f} hours")
    print(f"Significance: {fourier_result.significance:.6f}")
    
    # Expected values
    expected_period_hours = 24.0
    expected_freq_hz = 1.0 / (expected_period_hours * 3600.0)
    
    print(f"\nExpected frequency: {expected_freq_hz:.10f} Hz")
    print(f"Expected period: {expected_period_hours:.2f} hours")
    
    # Check if the frequency range includes the expected frequency
    freq_min = fourier_result.frequencies.min()
    freq_max = fourier_result.frequencies.max()
    
    print(f"\nFrequency range analyzed:")
    print(f"  Min: {freq_min:.10f} Hz (period: {1.0/(freq_min*3600):.2f} hours)")
    print(f"  Max: {freq_max:.10f} Hz (period: {1.0/(freq_max*3600):.2f} hours)")
    print(f"  Expected freq in range: {freq_min <= expected_freq_hz <= freq_max}")
    
    # Show top 5 peaks
    power_spectrum = fourier_result.power_spectrum
    frequencies = fourier_result.frequencies
    
    # Find top 5 peaks
    peak_indices = np.argsort(power_spectrum)[-5:][::-1]
    
    print(f"\nTop 5 frequency peaks:")
    for i, idx in enumerate(peak_indices):
        freq = frequencies[idx]
        power = power_spectrum[idx]
        period_hours = 1.0 / (freq * 3600.0) if freq > 0 else float('inf')
        print(f"  {i+1}. Freq: {freq:.8f} Hz, Period: {period_hours:.2f}h, Power: {power:.6f}")


if __name__ == "__main__":
    debug_circadian_validation()