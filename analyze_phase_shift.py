import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

SOLAR_DAY_LENGTH = 86164.0905
latitude_rad = math.radians(37.7749)

# Calculate for a full day
times = np.linspace(0, SOLAR_DAY_LENGTH, 100)
original_intensity = []
fixed_intensity = []

for elapsed in times:
    solar_fraction = (elapsed % SOLAR_DAY_LENGTH) / SOLAR_DAY_LENGTH
    
    # ORIGINAL (broken) calculation
    phase_shifted = (solar_fraction + 0.75) % 1.0
    base = max(0.0, math.sin(2 * math.pi * phase_shifted - math.pi/2))
    original_intensity.append(base * math.cos(latitude_rad))
    
    # FIXED calculation - sun should be high at solar_fraction=0.5 (noon)
    # Use simple sine wave: 0 at midnight, peak at noon
    angle = 2 * math.pi * (solar_fraction - 0.25)  # Shift so 0.25=sunrise
    fixed_base = max(0.0, math.sin(angle))
    fixed_intensity.append(fixed_base * math.cos(latitude_rad))

# Convert times to hours
hours = times / 3600

# Create visualization
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

ax1.plot(hours, original_intensity, 'r-', linewidth=2, label='Original (Broken)')
ax1.axhline(y=0, color='k', linestyle='--', alpha=0.3)
ax1.set_xlabel('Time (hours)', fontsize=12)
ax1.set_ylabel('Light Intensity', fontsize=12)
ax1.set_title('ORIGINAL: Light Intensity Over 24 Hours (BROKEN)', fontsize=14)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(0, 24)
ax1.set_ylim(-0.1, 1.1)
ax1.legend()

# Add time markers
for h in [0, 6, 12, 18, 24]:
    ax1.axvline(x=h, color='gray', linestyle=':', alpha=0.5)
    ax1.text(h, 1.05, f'{h}h', ha='center', fontsize=10)

ax2.plot(hours, fixed_intensity, 'g-', linewidth=2, label='Fixed')
ax2.axhline(y=0, color='k', linestyle='--', alpha=0.3)
ax2.set_xlabel('Time (hours)', fontsize=12)
ax2.set_ylabel('Light Intensity', fontsize=12)
ax2.set_title('FIXED: Light Intensity Over 24 Hours', fontsize=14)
ax2.grid(True, alpha=0.3)
ax2.set_xlim(0, 24)
ax2.set_ylim(-0.1, 1.1)
ax2.legend()

# Add time markers
for h in [0, 6, 12, 18, 24]:
    ax2.axvline(x=h, color='gray', linestyle=':', alpha=0.5)
    ax2.text(h, 1.05, f'{h}h', ha='center', fontsize=10)

plt.tight_layout()
plt.savefig('light_intensity_comparison.png', dpi=150)
print("Saved comparison to light_intensity_comparison.png")

# Print key values
print("\n" + "=" * 70)
print("Key Time Points Comparison")
print("=" * 70)
print(f"{'Time':<12} {'Original':<15} {'Fixed':<15}")
print("-" * 70)
for h in [0, 3, 6, 9, 12, 15, 18, 21]:
    idx = int(h * len(times) / 24)
    print(f"{h:2d}:00 ({h/24:.3f}) {original_intensity[idx]:8.6f}       {fixed_intensity[idx]:8.6f}")
