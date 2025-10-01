# Check if the expected 24.00-hour frequency is in the grid
expected_freq_24h = 1.0 / (24.0 * 3600.0)  # 0.000011574074 Hz

# Calculate frequency grid parameters used by SystemAnalyzer
min_freq = 1.0 / (100 * 3600)  # 0.00000 2778 Hz
max_freq = 0.001666663448  # From debug output
num_points = 21540

# Reconstruct the frequency grid (linear spacing)
import numpy as np
frequency = np.linspace(min_freq, max_freq, num_points)

# Find closest frequency bin
closest_idx = np.argmin(np.abs(frequency - expected_freq_24h))
closest_freq = frequency[closest_idx]
closest_period_hours = (1.0 / closest_freq) / 3600.0

print(f"Expected 24.00h frequency: {expected_freq_24h:.12f} Hz")
print(f"Closest frequency bin: {closest_freq:.12f} Hz (index {closest_idx})")
print(f"Closest period: {closest_period_hours:.4f} hours")
print(f"Difference: {abs(closest_freq - expected_freq_24h):.15f} Hz")
print(f"Period error: {abs(closest_period_hours - 24.0):.4f} hours")

# Check the peak from debug output
peak_idx = 115
peak_freq = frequency[peak_idx]
peak_period_hours = (1.0 / peak_freq) / 3600.0
print(f"\nPeak at index 115:")
print(f"Peak frequency: {peak_freq:.12f} Hz")
print(f"Peak period: {peak_period_hours:.4f} hours")

# Check frequency spacing
freq_spacing = frequency[1] - frequency[0]
print(f"\nFrequency spacing: {freq_spacing:.15f} Hz")
print(f"Period resolution at 24h: {abs(1/(expected_freq_24h+freq_spacing) - 1/expected_freq_24h)/3600:.4f} hours")
