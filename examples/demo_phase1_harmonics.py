"""
Phase 1 Feature 1 Demo: Multi-Harmonic Detection

Demonstrates detection of multiple circadian rhythms in biological signals.

This demo shows the power of Phase 1's multi-harmonic detection:
- Detects fundamental + harmonics (24h + 12h + 8h)
- Estimates amplitude and phase for each component
- Provides biological interpretation

Scientific Context:
    Real biological systems exhibit multiple periodicities:
    - 24h circadian: Master clock (SCN, clock genes)
    - 12h ultradian: Metabolic oscillations (2x per day)
    - 8h rhythms: Cellular processes (3x per day)
    
    Single-frequency analysis (MVP) misses this complexity.
    Multi-harmonic detection (Phase 1) reveals full picture.
"""

import numpy as np
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from bioxen_fourier_vm_lib.analysis.system_analyzer import SystemAnalyzer


def print_header(text, char="="):
    """Print formatted header"""
    width = 70
    print("\n" + char * width)
    print(text.center(width))
    print(char * width)


def format_phase_time(phase_rad, period_hours):
    """Convert phase in radians to time of peak"""
    # Phase 0 = peak at t=0
    # Convert to hours after midnight
    hours = (phase_rad / (2 * np.pi)) * period_hours
    return hours


def main():
    print_header("Phase 1 Feature 1: Multi-Harmonic Detection Demo")
    
    # Create analyzer
    analyzer = SystemAnalyzer(sampling_rate=1.0)  # 1 sample/hour
    
    # =========================================================================
    # Part 1: Generate Synthetic Biological Signal
    # =========================================================================
    print_header("Part 1: Generating Synthetic ATP Signal", "-")
    
    print("\n📊 Simulating ATP levels over 4 days (96 hours)...")
    t = np.linspace(0, 96, 400)  # 96 hours, 400 samples
    
    # Biological components
    atp_baseline = 100  # Arbitrary units
    
    # 24h circadian rhythm (master clock)
    circadian_amplitude = 30
    circadian_phase = np.pi / 6  # Peak at 4am (π/6 * 24/2π = 4h)
    circadian = circadian_amplitude * np.sin(2*np.pi*t/24 + circadian_phase)
    
    # 12h ultradian rhythm (metabolism)
    ultradian_amplitude = 15
    ultradian = ultradian_amplitude * np.sin(2*np.pi*t/12)
    
    # 8h rhythm (cellular processes)
    cellular_amplitude = 8
    cellular = cellular_amplitude * np.sin(2*np.pi*t/8)
    
    # Biological noise
    np.random.seed(42)  # Reproducible
    noise = 3 * np.random.randn(len(t))
    
    # Combined signal
    atp_signal = atp_baseline + circadian + ultradian + cellular + noise
    
    print(f"   Duration: 96 hours (4 days)")
    print(f"   Samples: {len(t)}")
    print(f"   Sampling rate: {len(t)/96:.1f} samples/hour")
    print(f"\n   Signal components:")
    print(f"   ├─ Baseline: {atp_baseline} ATP units")
    print(f"   ├─ 24h circadian: amplitude {circadian_amplitude}, phase {circadian_phase:.3f} rad")
    print(f"   ├─ 12h ultradian: amplitude {ultradian_amplitude}")
    print(f"   ├─ 8h cellular: amplitude {cellular_amplitude}")
    print(f"   └─ Noise: σ = 3 units")
    
    # =========================================================================
    # Part 2: MVP Analysis (Single Period Detection)
    # =========================================================================
    print_header("Part 2: MVP Mode (Single Period Detection)", "-")
    
    result_mvp = analyzer.fourier_lens(atp_signal, t, detect_harmonics=False)
    
    print(f"\n   Dominant period: {result_mvp.dominant_period:.2f} hours")
    print(f"   Dominant frequency: {result_mvp.dominant_frequency:.6f} Hz")
    print(f"   Statistical significance: {result_mvp.significance:.4f}")
    print(f"   Harmonics detected: None (MVP mode)")
    
    print(f"\n   ℹ️  MVP detects strongest component but misses others")
    
    # =========================================================================
    # Part 3: Phase 1 Analysis (Multi-Harmonic Detection)
    # =========================================================================
    print_header("Part 3: Phase 1 Mode (Multi-Harmonic Detection)", "-")
    
    result_phase1 = analyzer.fourier_lens(atp_signal, t, 
                                          detect_harmonics=True,
                                          max_harmonics=5)
    
    print(f"\n   Dominant period: {result_phase1.dominant_period:.2f} hours")
    print(f"   Total harmonic power: {result_phase1.harmonic_power:.4f}")
    print(f"   Number of harmonics: {len(result_phase1.harmonics)}")
    
    print("\n   📊 Detected Harmonics:")
    print("   " + "-" * 66)
    print(f"   {'#':<4} {'Period (h)':<12} {'Amplitude':<12} {'Phase (rad)':<12} {'Power':<12}")
    print("   " + "-" * 66)
    
    for i, h in enumerate(result_phase1.harmonics, 1):
        print(f"   {i:<4} {h['period']:<12.2f} {h['amplitude']:<12.2f} "
              f"{h['phase']:<12.4f} {h['power']:<12.4f}")
    
    # =========================================================================
    # Part 4: Biological Interpretation
    # =========================================================================
    print_header("Part 4: Biological Interpretation", "-")
    
    for i, h in enumerate(result_phase1.harmonics, 1):
        period = h['period']
        amplitude = h['amplitude']
        phase = h['phase']
        power = h['power']
        phase_deg = phase * 180 / np.pi
        peak_time = format_phase_time(phase, period)
        
        if 20 < period < 28:
            print(f"\n   🔬 Harmonic {i}: CIRCADIAN RHYTHM")
            print(f"   ├─ Period: ~24h (detected: {period:.1f}h)")
            print(f"   ├─ Amplitude: {amplitude:.1f} ATP units (true: {circadian_amplitude})")
            print(f"   ├─ Phase: {phase:.4f} rad ({phase_deg:.1f}°)")
            print(f"   ├─ Peak occurs at: ~{peak_time:.1f}h after midnight")
            print(f"   ├─ Spectral power: {power:.4f}")
            print(f"   │")
            print(f"   └─ Biological interpretation:")
            print(f"      • Primary biological clock (SCN in mammals)")
            print(f"      • Drives sleep/wake cycles")
            print(f"      • Regulates hormone secretion")
            print(f"      • Controls ~40% of genome expression")
            
            # Compare to true values
            amp_error = abs(amplitude - circadian_amplitude) / circadian_amplitude * 100
            phase_error = abs(phase - circadian_phase)
            phase_error = min(phase_error, 2*np.pi - phase_error) * 180/np.pi
            print(f"      • Detection accuracy: amplitude {amp_error:.1f}% error, "
                  f"phase {phase_error:.1f}° error")
            
        elif 10 < period < 14:
            print(f"\n   🔬 Harmonic {i}: ULTRADIAN RHYTHM")
            print(f"   ├─ Period: ~12h (detected: {period:.1f}h)")
            print(f"   ├─ Amplitude: {amplitude:.1f} ATP units (true: {ultradian_amplitude})")
            print(f"   ├─ Phase: {phase:.4f} rad ({phase_deg:.1f}°)")
            print(f"   ├─ Spectral power: {power:.4f}")
            print(f"   │")
            print(f"   └─ Biological interpretation:")
            print(f"      • Metabolic oscillations")
            print(f"      • 2 peaks per day (often at mealtimes)")
            print(f"      • ATP synthesis/consumption cycles")
            print(f"      • Coordinated with feeding behavior")
            
            amp_error = abs(amplitude - ultradian_amplitude) / ultradian_amplitude * 100
            print(f"      • Detection accuracy: amplitude {amp_error:.1f}% error")
            
        elif 6 < period < 10:
            print(f"\n   🔬 Harmonic {i}: SHORT ULTRADIAN RHYTHM")
            print(f"   ├─ Period: ~8h (detected: {period:.1f}h)")
            print(f"   ├─ Amplitude: {amplitude:.1f} ATP units (true: {cellular_amplitude})")
            print(f"   ├─ Phase: {phase:.4f} rad ({phase_deg:.1f}°)")
            print(f"   ├─ Spectral power: {power:.4f}")
            print(f"   │")
            print(f"   └─ Biological interpretation:")
            print(f"      • Cellular process cycles")
            print(f"      • 3 peaks per day")
            print(f"      • May reflect cell cycle phases")
            print(f"      • Stress response kinetics")
            
            amp_error = abs(amplitude - cellular_amplitude) / cellular_amplitude * 100
            print(f"      • Detection accuracy: amplitude {amp_error:.1f}% error")
        else:
            print(f"\n   ℹ️  Harmonic {i}: Period {period:.1f}h (possibly noise)")
    
    # =========================================================================
    # Part 5: Key Insights and Biological Impact
    # =========================================================================
    print_header("Part 5: Key Insights", "-")
    
    print("\n   💡 What Phase 1 Reveals:")
    print("   ├─ Multiple rhythms coexist in biological systems")
    print("   ├─ Each rhythm has distinct amplitude and phase")
    print("   ├─ Harmonics indicate temporal organization")
    print("   └─ Phase relationships show process coordination")
    
    print("\n   🔬 Research Applications:")
    print("   ├─ Drug timing optimization (chronotherapy)")
    print("   ├─ Disease diagnosis (rhythm disruption)")
    print("   ├─ Circadian clock gene analysis")
    print("   ├─ Metabolic syndrome studies")
    print("   └─ Aging and rhythm amplitude decline")
    
    print("\n   ⚕️  Clinical Relevance:")
    print("   ├─ Cancer cells show disrupted rhythms")
    print("   ├─ Diabetes affects ultradian insulin pulses")
    print("   ├─ Depression linked to phase shifts")
    print("   ├─ Jet lag = temporary desynchronization")
    print("   └─ Shift work = chronic rhythm disruption")
    
    # =========================================================================
    # Part 6: Comparison and Summary
    # =========================================================================
    print_header("Part 6: MVP vs Phase 1 Comparison", "-")
    
    print("\n   📊 Detection Summary:")
    print("   " + "-" * 66)
    print(f"   {'Mode':<15} {'Harmonics':<15} {'Information':<36}")
    print("   " + "-" * 66)
    print(f"   {'MVP':<15} {'1 (dominant)':<15} {'Single period only':<36}")
    print(f"   {'Phase 1':<15} {f'{len(result_phase1.harmonics)}':<15} "
          f"{'Multiple periods + amplitude + phase':<36}")
    print("   " + "-" * 66)
    
    print("\n   ✨ Phase 1 Advantages:")
    print("   ✓ Reveals complete temporal structure")
    print("   ✓ Quantifies multiple rhythms simultaneously")
    print("   ✓ Provides phase information (timing)")
    print("   ✓ Measures relative amplitude (importance)")
    print("   ✓ Publication-ready analysis")
    
    print_header("Demo Complete!", "=")
    
    print("\n🎓 What You Learned:")
    print("   • How multi-harmonic detection works")
    print("   • Biological significance of multiple rhythms")
    print("   • Phase and amplitude interpretation")
    print("   • Research and clinical applications")
    
    print("\n📚 Next Steps:")
    print("   • Try with real genomic data: examples/genomic_mvp_demo.py")
    print("   • Analyze TimeSimulator: examples/validate_time_simulator.py")
    print("   • Run tests: pytest tests/test_phase1_harmonics.py -v")
    print("   • Explore Week 2 features: Wavelet optimization")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
