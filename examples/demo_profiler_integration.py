"""
Real PerformanceProfiler Integration Demo

Demonstrates four-lens analysis on REAL data from PerformanceProfiler.

This demo requires:
- BioXen hypervisor running
- PerformanceProfiler collecting data
- At least 50 samples collected (250+ seconds of runtime @ 5s intervals)

This shows the complete integration path:
  PerformanceProfiler → SystemAnalyzer → Four-Lens Results
"""

import sys
from pathlib import Path
import time

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from bioxen_fourier_vm_lib.hypervisor.core import BioXenHypervisor
from bioxen_fourier_vm_lib.monitoring.profiler import PerformanceProfiler
from bioxen_fourier_vm_lib.chassis import ChassisType


def main():
    print("=" * 70)
    print("Four-Lens Analysis on Real PerformanceProfiler Data")
    print("=" * 70)
    print("\nThis demo analyzes REAL time-series data collected by")
    print("PerformanceProfiler from a running BioXen hypervisor.")
    
    # Initialize hypervisor
    print("\n🧬 Initializing BioXen Hypervisor...")
    try:
        hypervisor = BioXenHypervisor(
            max_vms=4,
            chassis_type=ChassisType.ECOLI
        )
        chassis_info = hypervisor.get_chassis_info()
        print(f"   ✓ Hypervisor initialized")
        print(f"   Chassis: {chassis_info.get('type', 'unknown')}")
        print(f"   Max VMs: {hypervisor.max_vms}")
    except Exception as e:
        print(f"   ❌ Error initializing hypervisor: {e}")
        return 1
    
    # Initialize profiler
    print("\n📊 Starting PerformanceProfiler...")
    try:
        profiler = PerformanceProfiler(hypervisor, monitoring_interval=5.0)
        profiler.start_monitoring()
        print("   ✓ Profiler started")
        print("   Monitoring interval: 5.0 seconds")
        print("   Storage capacity: 1000 samples (max)")
    except Exception as e:
        print(f"   ❌ Error starting profiler: {e}")
        return 1
    
    # Check if analyzer was created
    if not hasattr(profiler, 'analyzer'):
        print("\n❌ ERROR: PerformanceProfiler missing 'analyzer' attribute")
        print("   The integration code may not be applied yet.")
        print("   Please ensure profiler.py has been modified per master prompt.")
        profiler.stop_monitoring()
        return 1
    
    print("   ✓ SystemAnalyzer integrated (sampling_rate: 0.2 Hz)")
    
    # Wait for sufficient data collection
    print("\n⏳ Collecting data...")
    print("   Need at least 50 samples for meaningful analysis")
    print("   @ 5-second intervals = 250 seconds minimum")
    
    wait_time = 300  # 5 minutes = 60 samples
    print(f"\n   Collecting for {wait_time} seconds ({wait_time//60} minutes)...")
    
    start_time = time.time()
    last_count = 0
    
    while time.time() - start_time < wait_time:
        time.sleep(10)  # Check every 10 seconds
        current_samples = len(profiler.system_metrics)
        elapsed = int(time.time() - start_time)
        remaining = wait_time - elapsed
        
        print(f"   [{elapsed}s/{wait_time}s] Samples: {current_samples}/60 "
              f"(remaining: {remaining}s)    ", end='\r', flush=True)
        
        last_count = current_samples
    
    print()  # New line after progress
    final_count = len(profiler.system_metrics)
    print(f"\n   ✓ Collected {final_count} samples")
    
    if final_count < 50:
        print(f"\n   ⚠️  Warning: Only {final_count} samples (minimum 50 recommended)")
        print("   Results may be less reliable with limited data")
    
    # Analyze ATP levels with all four lenses
    print("\n🔍 Analyzing ATP levels with all four lenses...")
    print("   This may take a few seconds...")
    
    try:
        results = profiler.analyze_metric_all('atp_level')
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        print("\nTroubleshooting:")
        print("  - Check that PerformanceProfiler has analyze_metric_all() method")
        print("  - Verify integration code from master prompt is applied")
        profiler.stop_monitoring()
        return 1
    
    # Check for errors in results
    if 'error' in results:
        print(f"\n❌ Analysis error: {results['error']}")
        if 'checks' in results:
            print("\nValidation checks:")
            for check, passed in results['checks'].items():
                status = "✓" if passed else "✗"
                print(f"   {status} {check}")
        profiler.stop_monitoring()
        return 1
    
    # Display results
    print("\n" + "="*70)
    print("ANALYSIS RESULTS")
    print("="*70)
    
    print(f"\nMetric: {results.get('metric', 'unknown')}")
    print(f"Samples: {results.get('samples', 0)}")
    print(f"Duration: {results.get('duration_seconds', 0):.1f} seconds")
    
    # Fourier results
    if 'fourier' in results:
        print("\n" + "-"*70)
        print("🔍 LENS 1: FOURIER (Lomb-Scargle)")
        print("-"*70)
        fourier = results['fourier']
        print(f"   Dominant frequency: {fourier.dominant_frequency:.8f} Hz")
        print(f"   Dominant period: {fourier.dominant_period:.2f} hours")
        print(f"   Statistical significance: {fourier.significance:.4f} ({fourier.significance*100:.1f}%)")
        
        # Interpretation
        if 20 < fourier.dominant_period < 28:
            print("\n   💡 Interpretation: Circadian rhythm detected (~24h)")
        elif 0.1 < fourier.dominant_period < 4:
            print("\n   💡 Interpretation: Ultradian rhythm detected (<4h)")
        else:
            print(f"\n   💡 Interpretation: {fourier.dominant_period:.1f}h periodicity")
    
    # Wavelet results
    if 'wavelet' in results:
        print("\n" + "-"*70)
        print("🔍 LENS 2: WAVELET")
        print("-"*70)
        wavelet = results['wavelet']
        print(f"   Scales analyzed: {len(wavelet.scales)}")
        print(f"   Time-frequency map shape: {wavelet.time_frequency_map.shape}")
        print(f"   Transient events detected: {len(wavelet.transient_events)}")
        
        if wavelet.transient_events:
            print("\n   Detected events:")
            for i, event in enumerate(wavelet.transient_events[:5]):  # Show first 5
                print(f"   Event {i+1}:")
                print(f"      Time index: {event['time_index']}")
                print(f"      Intensity: {event['intensity']:.2f}")
                print(f"      Duration: {event.get('duration_samples', 'N/A')} samples")
        else:
            print("\n   💡 No significant transient events (system stable)")
    
    # Laplace results
    if 'laplace' in results:
        print("\n" + "-"*70)
        print("🔍 LENS 3: LAPLACE (Stability)")
        print("-"*70)
        laplace = results['laplace']
        print(f"   System stability: {laplace.stability.upper()}")
        print(f"   Natural frequency: {laplace.natural_frequency:.8f} Hz")
        print(f"   Damping ratio: {laplace.damping_ratio:.4f}")
        print(f"   Poles: {laplace.poles}")
        
        # Interpretation
        print("\n   💡 Interpretation:")
        if laplace.stability == 'stable':
            print("      System is STABLE - healthy homeostasis")
            print("      Returns to equilibrium after perturbations")
        elif laplace.stability == 'oscillatory':
            print("      System is OSCILLATORY - sustained rhythms")
            print("      Natural biological cycles present")
        else:
            print("      System is UNSTABLE - homeostasis compromised!")
            print("      ⚠️  Potential resource exhaustion or runaway process")
    
    # Z-Transform results
    if 'ztransform' in results:
        print("\n" + "-"*70)
        print("🔍 LENS 4: Z-TRANSFORM (Filtering)")
        print("-"*70)
        zt = results['ztransform']
        print(f"   Cutoff frequency: {zt.cutoff_frequency:.8f} Hz")
        print(f"   Noise reduction: {zt.noise_reduction_percent:.1f}%")
        
        # Show signal statistics
        from bioxen_fourier_vm_lib.analysis.system_analyzer import SystemAnalyzer
        import numpy as np
        
        values, _ = profiler.extract_time_series('atp_level')
        if len(values) > 0:
            print(f"\n   Original signal:")
            print(f"      Mean: {np.mean(values):.2f}")
            print(f"      Std: {np.std(values):.2f}")
            print(f"   Filtered signal:")
            print(f"      Mean: {np.mean(zt.filtered_signal):.2f}")
            print(f"      Std: {np.std(zt.filtered_signal):.2f}")
    
    # Summary
    print("\n" + "="*70)
    print("✅ Analysis Complete!")
    print("="*70)
    
    print("\n📊 Summary:")
    if 'fourier' in results:
        print(f"   • Dominant period: {results['fourier'].dominant_period:.1f} hours")
    if 'wavelet' in results:
        print(f"   • Transient events: {len(results['wavelet'].transient_events)}")
    if 'laplace' in results:
        print(f"   • System stability: {results['laplace'].stability}")
    if 'ztransform' in results:
        print(f"   • Noise reduction: {results['ztransform'].noise_reduction_percent:.1f}%")
    
    # Cleanup
    print("\n🧹 Stopping profiler...")
    profiler.stop_monitoring()
    print("   ✓ Profiler stopped")
    
    print("\n" + "="*70)
    print("Demo completed successfully!")
    print("="*70)
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        exit_code = 130
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        exit_code = 1
    
    exit(exit_code)
