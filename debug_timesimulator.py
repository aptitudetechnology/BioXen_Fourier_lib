"""
Debug TimeSimulator Light Intensity Issue

Tests the TimeSimulator to see what's causing constant 0.000 values.
"""

import sys
from pathlib import Path
import math
import time as time_module

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from bioxen_fourier_vm_lib.hypervisor.TimeSimulator import TimeSimulator

def test_light_intensity_calculation():
    """Test light intensity calculation directly"""
    print("="*70)
    print("TimeSimulator Light Intensity Debug Test")
    print("="*70)
    
    # Initialize TimeSimulator
    print("\n📍 Initializing TimeSimulator...")
    sim = TimeSimulator(
        latitude=37.7749,      # San Francisco
        longitude=-122.4194,
        time_acceleration=1.0
    )
    print(f"   Latitude: {math.degrees(sim.latitude):.4f}° (radians: {sim.latitude:.4f})")
    print(f"   Longitude: {math.degrees(sim.longitude):.4f}° (radians: {sim.longitude:.4f})")
    print(f"   Solar day length: {sim.SOLAR_DAY_LENGTH:.2f} seconds")
    
    # Test internal calculation directly
    print("\n🔍 Testing _calculate_light_intensity() directly...")
    
    # Test at various points in the day
    test_times = [
        (0, "00:00 - Midnight"),
        (sim.SOLAR_DAY_LENGTH * 0.25, "06:00 - Sunrise"),
        (sim.SOLAR_DAY_LENGTH * 0.5, "12:00 - Noon"),
        (sim.SOLAR_DAY_LENGTH * 0.75, "18:00 - Sunset"),
        (sim.SOLAR_DAY_LENGTH, "24:00 - Midnight again")
    ]
    
    print("\nDirect calculation tests:")
    for elapsed, description in test_times:
        intensity = sim._calculate_light_intensity(elapsed)
        solar_fraction = (elapsed % sim.SOLAR_DAY_LENGTH) / sim.SOLAR_DAY_LENGTH
        print(f"   {description:20} elapsed={elapsed:8.0f}s, fraction={solar_fraction:.3f}, intensity={intensity:.6f}")
    
    # Test get_current_state() method
    print("\n🔍 Testing get_current_state() method...")
    print("\nCollecting 24 samples over one solar day:")
    
    samples = []
    for hour in range(24):
        # Manually advance time
        sim.start_time = time_module.time() - (hour * 3600)  # Go back in time
        state = sim.get_current_state()
        samples.append((hour, state.light_intensity))
        print(f"   Hour {hour:2d}: light_intensity={state.light_intensity:.6f}, "
              f"phase={state.solar_phase.value}, elapsed={state.simulation_time_elapsed:.0f}s")
    
    # Statistics
    print("\n📊 Statistics:")
    intensities = [s[1] for s in samples]
    print(f"   Min: {min(intensities):.6f}")
    print(f"   Max: {max(intensities):.6f}")
    print(f"   Mean: {sum(intensities)/len(intensities):.6f}")
    print(f"   Non-zero count: {sum(1 for i in intensities if i > 0)}")
    
    # Check latitude correction
    print("\n🧮 Latitude correction check:")
    latitude_factor = math.cos(sim.latitude)
    print(f"   cos({math.degrees(sim.latitude):.2f}°) = {latitude_factor:.6f}")
    print(f"   This is {'GOOD' if latitude_factor > 0.5 else 'PROBLEMATIC'} for light intensity")
    
    # Test base intensity calculation
    print("\n🔍 Testing base intensity formula:")
    for fraction in [0.0, 0.25, 0.5, 0.75, 1.0]:
        phase_shifted = (fraction + 0.75) % 1.0
        base_intensity = max(0.0, math.sin(2 * math.pi * phase_shifted - math.pi/2))
        result = base_intensity * latitude_factor
        print(f"   fraction={fraction:.2f}, phase_shifted={phase_shifted:.3f}, "
              f"base={base_intensity:.6f}, result={result:.6f}")
    
    # Diagnosis
    print("\n"+ "="*70)
    print("DIAGNOSIS")
    print("="*70)
    
    if max(intensities) == 0:
        print("❌ PROBLEM CONFIRMED: All light intensities are zero!")
        print("\nPossible causes:")
        print("1. Latitude factor is causing zeroing (cos value too small)")
        print("2. Phase calculation is wrong")
        print("3. sine wave formula is broken")
        
        # Check specific issue
        if latitude_factor < 0.1:
            print(f"\n⚠️  FOUND: Latitude factor ({latitude_factor:.6f}) is very small!")
            print("   This is crushing all light values to near zero.")
        
    elif max(intensities) < 0.01:
        print("⚠️  PROBLEM: Light intensities are too small")
        print(f"   Maximum value: {max(intensities):.6f}")
    else:
        print("✅ Light intensity calculation appears to be working")
        print(f"   Range: {min(intensities):.6f} to {max(intensities):.6f}")
    
    return samples


def test_suggested_fix():
    """Test a suggested fix for the light intensity calculation"""
    print("\n" + "="*70)
    print("TESTING SUGGESTED FIX")
    print("="*70)
    
    class FixedTimeSimulator(TimeSimulator):
        def _calculate_light_intensity(self, elapsed: float) -> float:
            """
            Fixed version with proper day/night cycle.
            """
            solar_fraction = (elapsed % self.SOLAR_DAY_LENGTH) / self.SOLAR_DAY_LENGTH
            
            # Simple sine wave: peak at noon (0.5), zero at midnight (0.0 and 1.0)
            # sin(2π * fraction) shifted to be positive during day
            base_intensity = max(0.0, math.sin(2 * math.pi * solar_fraction))
            
            # Latitude correction (don't make it too aggressive)
            # Use absolute value and add baseline to avoid total darkness
            latitude_factor = 0.5 + 0.5 * abs(math.cos(self.latitude))
            
            result = base_intensity * latitude_factor
            return result
    
    sim = FixedTimeSimulator(latitude=37.7749, longitude=-122.4194)
    
    print("\nTesting fixed version over 24 hours:")
    samples = []
    for hour in range(24):
        sim.start_time = time_module.time() - (hour * 3600)
        state = sim.get_current_state()
        samples.append(state.light_intensity)
        print(f"   Hour {hour:2d}: {state.light_intensity:.6f}")
    
    print(f"\n   Min: {min(samples):.6f}")
    print(f"   Max: {max(samples):.6f}")
    print(f"   Mean: {sum(samples)/len(samples):.6f}")
    
    if max(samples) > 0.5:
        print("\n✅ FIXED! Light intensity now shows proper day/night cycle")
    else:
        print("\n⚠️  Still has issues")
    
    return samples


if __name__ == "__main__":
    # Run original test
    original_samples = test_light_intensity_calculation()
    
    # Run fixed version test
    fixed_samples = test_suggested_fix()
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Original max intensity: {max(s[1] for s in original_samples):.6f}")
    print(f"Fixed max intensity:    {max(fixed_samples):.6f}")
