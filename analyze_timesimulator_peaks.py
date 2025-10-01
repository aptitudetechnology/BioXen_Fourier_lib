import numpy as np
from scipy.signal import find_peaks
from bioxen_fourier_vm_lib.hypervisor.TimeSimulator import TimeSimulator

# Initialize TimeSimulator
sim = TimeSimulator(latitude=37.7749, longitude=-122.4194)

# Collect 72 hours of data at 5-minute intervals
duration_hours = 72
sampling_interval_minutes = 5
samples = []
timestamps_seconds = []

sample_count = 0
for hour in range(duration_hours):
    for minute in range(0, 60, sampling_interval_minutes):
        state = sim.get_current_state()
        samples.append(state.light_intensity)
        timestamp_seconds = sample_count * sampling_interval_minutes * 60
        timestamps_seconds.append(timestamp_seconds)
        sample_count += 1
        sim.advance_time(sampling_interval_minutes * 60)

samples = np.array(samples)
timestamps_seconds = np.array(timestamps_seconds)
timestamps_hours = timestamps_seconds / 3600.0

# Find peaks
peaks, properties = find_peaks(samples, height=0.7, distance=100)

print(f"Found {len(peaks)} peaks in light intensity data")
print(f"\nPeak times (hours):")
for i, peak_idx in enumerate(peaks):
    print(f"  Peak {i+1}: {timestamps_hours[peak_idx]:.4f} hours (intensity={samples[peak_idx]:.4f})")

if len(peaks) >= 2:
    print(f"\nPeak-to-peak intervals:")
    peak_times = timestamps_hours[peaks]
    intervals = np.diff(peak_times)
    for i, interval in enumerate(intervals):
        print(f"  Peak {i+1} to Peak {i+2}: {interval:.4f} hours")
    
    mean_interval = np.mean(intervals)
    std_interval = np.std(intervals)
    print(f"\nMean interval: {mean_interval:.4f} hours")
    print(f"Std deviation: {std_interval:.4f} hours")
    
    if abs(mean_interval - 24.0) < 0.01:
        print("✅ Perfect 24-hour periods!")
    else:
        print(f"❌ Period error: {abs(mean_interval - 24.0):.4f} hours")
