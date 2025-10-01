"""
Debug TimeSimulator light intensity calculation
"""

import sys
from pathlib import Path
import math
import time

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from bioxen_fourier_vm_lib.hypervisor.TimeSimulator import TimeSimulator

def debug_time_simulator():
    """Debug what the TimeSimulator is actually producing."""
    
    # Initialize TimeSimulator
    sim = TimeSimulator(
        latitude=37.7749,      # San Francisco
        longitude=-122.4194,
        time_acceleration=1.0
    )
    
    print("TimeSimulator Debug")
    print("=" * 40)
    print(f"Latitude: {37.7749}° ({math.radians(37.7749):.3f} rad)")
    print(f"Solar day length: {TimeSimulator.SOLAR_DAY_LENGTH:.2f} seconds")
    print()
    
    # Test a few states over 24 hours
    elapsed_times = [i * 3600 for i in range(0, 25, 3)]  # Every 3 hours for 24 hours
    
    for elapsed in elapsed_times:
        state = sim.get_current_state()
        
        # Manual calculation to debug
        solar_fraction = (elapsed % TimeSimulator.SOLAR_DAY_LENGTH) / TimeSimulator.SOLAR_DAY_LENGTH
        base_intensity = math.sin(math.pi * solar_fraction) if solar_fraction < 1.0 else 0.0
        latitude_factor = math.cos(math.radians(37.7749))
        manual_light = max(0.0, min(1.0, base_intensity * latitude_factor))
        
        hour = elapsed / 3600
        print(f"Hour {hour:2.0f}: "
              f"fraction={solar_fraction:.3f}, "
              f"base={base_intensity:.3f}, "
              f"lat_factor={latitude_factor:.3f}, "
              f"light={state.light_intensity:.3f}, "
              f"manual={manual_light:.3f}")
    
    print()
    print("Testing over short period...")
    
    # Test current moment
    for i in range(10):
        state = sim.get_current_state()
        print(f"Sample {i}: light_intensity = {state.light_intensity:.6f}")
        time.sleep(0.1)

if __name__ == "__main__":
    debug_time_simulator()