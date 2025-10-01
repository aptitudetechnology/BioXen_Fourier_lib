import numpy as np
from astropy.timeseries import LombScargle

# Create perfect 24-hour sine wave
duration_hours = 72
sampling_interval_minutes = 5
samples_per_hour = 60 // sampling_interval_minutes

# Generate timestamps in seconds
timestamps_seconds = np.arange(0, duration_hours * 3600, sampling_interval_minutes * 60)
print(f"Timestamps range: {timestamps_seconds[0]} to {timestamps_seconds[-1]} seconds")
print(f"Duration: {timestamps_seconds[-1] / 3600} hours")
print(f"Number of samples: {len(timestamps_seconds)}")

# Generate perfect 24-hour period sine wave
period_seconds = 24 * 3600  # 24 hours in seconds
angular_freq = 2 * np.pi / period_seconds
signal = np.sin(angular_freq * timestamps_seconds)

print(f"\nExpected period: {period_seconds} seconds = 24.00 hours")
print(f"Expected frequency: {1/period_seconds} Hz = {1/period_seconds:.10f} Hz")

# Run Lomb-Scargle
ls = LombScargle(timestamps_seconds, signal, fit_mean=True)
frequency, power = ls.autopower(
    minimum_frequency=1.0/(100*3600),
    maximum_frequency=1.0/(10),
    samples_per_peak=10
)

# Find dominant frequency
peak_idx = np.argmax(power)
dominant_freq = frequency[peak_idx]
dominant_period_seconds = 1.0 / dominant_freq
dominant_period_hours = dominant_period_seconds / 3600.0

print(f"\nDetected frequency: {dominant_freq:.10f} Hz")
print(f"Detected period: {dominant_period_seconds:.2f} seconds = {dominant_period_hours:.4f} hours")
print(f"Peak power: {power[peak_idx]:.6f}")
print(f"Error: {abs(dominant_period_hours - 24.0):.4f} hours")
