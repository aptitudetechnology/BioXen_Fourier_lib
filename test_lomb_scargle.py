import numpy as np
from astropy.timeseries import LombScargle

# Create perfect 24-hour sine wave
duration_hours = 72
sampling_interval_minutes = 5
num_samples = int(duration_hours * 60 / sampling_interval_minutes) + 1
timestamps_seconds = np.linspace(0, duration_hours * 3600, num_samples)

# Generate perfect 24-hour period sine wave
period_seconds = 24 * 3600
angular_freq = 2 * np.pi / period_seconds
signal = np.sin(angular_freq * timestamps_seconds)

# Calculate expected frequency
expected_freq = 1.0 / period_seconds
print(f"Expected frequency: {expected_freq:.12f} Hz")
print(f"Expected period: {period_seconds} seconds = 24.00 hours")

# Run Lomb-Scargle
sampling_interval_seconds = sampling_interval_minutes * 60
nyquist_freq = 1.0 / (2 * sampling_interval_seconds)
ls = LombScargle(timestamps_seconds, signal, fit_mean=True)
frequency, power = ls.autopower(
    minimum_frequency=1.0/(100*3600),
    maximum_frequency=nyquist_freq,
    samples_per_peak=10
)

# Find the frequency bin closest to expected
closest_idx = np.argmin(np.abs(frequency - expected_freq))
print(f"\nClosest frequency bin: {frequency[closest_idx]:.12f} Hz")
print(f"Closest period: {1/frequency[closest_idx]:.2f} seconds = {1/frequency[closest_idx]/3600:.4f} hours")
print(f"Power at closest bin: {power[closest_idx]:.6f}")

# Find dominant frequency (max power)
peak_idx = np.argmax(power)
print(f"\nPeak frequency: {frequency[peak_idx]:.12f} Hz")
print(f"Peak period: {1/frequency[peak_idx]:.2f} seconds = {1/frequency[peak_idx]/3600:.4f} hours")
print(f"Peak power: {power[peak_idx]:.6f}")

# Check frequency resolution
freq_spacing = frequency[1] - frequency[0]
print(f"\nFrequency resolution: {freq_spacing:.12f} Hz")
print(f"Period resolution at 24h: {abs(1/(expected_freq+freq_spacing) - 1/expected_freq)/3600:.4f} hours")

# Try higher resolution
print("\n" + "="*70)
print("TRYING WITH HIGHER FREQUENCY RESOLUTION")
print("="*70)
frequency_hr, power_hr = ls.autopower(
    minimum_frequency=1.0/(100*3600),
    maximum_frequency=nyquist_freq,
    samples_per_peak=50  # Much higher resolution
)

peak_idx_hr = np.argmax(power_hr)
dominant_freq_hr = frequency_hr[peak_idx_hr]
dominant_period_hr = 1.0 / dominant_freq_hr

print(f"Detected frequency: {dominant_freq_hr:.12f} Hz")
print(f"Detected period: {dominant_period_hr:.2f} seconds = {dominant_period_hr/3600:.4f} hours")
print(f"Error: {abs(dominant_period_hr/3600 - 24.0):.4f} hours")

if abs(dominant_period_hr/3600 - 24.0) < 0.1:
    print("✅ SUCCESS!")
else:
    print("❌ STILL FAILED")
