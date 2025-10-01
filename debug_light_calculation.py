import math

# Simulate the TimeSimulator calculation
latitude = 37.7749  # San Francisco
latitude_rad = math.radians(latitude)

SOLAR_DAY_LENGTH = 86164.0905

# Test at different times
test_times = [0, 21541, 43082, 64623]  # 0h, 6h, 12h, 18h

print("=" * 70)
print("TimeSimulator Light Intensity Debug")
print("=" * 70)
print(f"Latitude: {latitude}° ({latitude_rad:.4f} rad)")
print(f"Solar Day Length: {SOLAR_DAY_LENGTH} seconds")
print()

for elapsed in test_times:
    hours = elapsed / 3600
    solar_fraction = (elapsed % SOLAR_DAY_LENGTH) / SOLAR_DAY_LENGTH
    
    # Original calculation
    phase_shifted = (solar_fraction + 0.75) % 1.0
    base_intensity = max(0.0, math.sin(2 * math.pi * phase_shifted - math.pi/2))
    latitude_factor = math.cos(latitude_rad)
    result = max(0.0, min(1.0, base_intensity * latitude_factor))
    
    print(f"Time: {hours:5.1f}h ({elapsed:6d}s)")
    print(f"  solar_fraction:  {solar_fraction:.6f}")
    print(f"  phase_shifted:   {phase_shifted:.6f}")
    print(f"  sin argument:    {(2 * math.pi * phase_shifted - math.pi/2):.6f}")
    print(f"  base_intensity:  {base_intensity:.6f}")
    print(f"  latitude_factor: {latitude_factor:.6f}")
    print(f"  result:          {result:.6f}")
    print()

# Now test what happens with cos(latitude) in radians
print("=" * 70)
print("Latitude Factor Analysis")
print("=" * 70)
print(f"cos({latitude_rad:.4f} rad) = {math.cos(latitude_rad):.6f}")
print(f"cos({latitude}°) using degrees = {math.cos(math.radians(latitude)):.6f}")
print()

# The issue: if we use degrees instead of radians
bad_result = math.cos(latitude)  # Using degrees as radians!
print(f"ERROR: cos({latitude} without conversion) = {bad_result:.6f}")
