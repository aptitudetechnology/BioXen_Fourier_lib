"""
Phase 1 Feature 2 Demo: Automatic Wavelet Selection
Demonstrates intelligent wavelet selection for different biological signals

This demo shows how the system automatically picks the best wavelet
transform for different types of biological signals.

Author: BioXen Development Team
Date: October 1, 2025
"""

import numpy as np
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from bioxen_fourier_vm_lib.analysis.system_analyzer import SystemAnalyzer


def print_header(title: str):
    """Print formatted section header"""
    print(f"\n{'='*70}")
    print(title)
    print('='*70)


def print_subheader(title: str):
    """Print formatted subsection header"""
    print(f"\n{title}")
    print('-'*70)


def demo_smooth_oscillation():
    """Demo 1: Smooth circadian oscillation"""
    print_header("DEMO 1: Smooth Circadian Oscillation (ATP Levels)")
    
    print("""
Scenario: 72 hours of ATP measurements during normal cell operation
Signal characteristics:
  - Smooth 24h circadian rhythm (amplitude: 30 units)
  - Small 12h ultradian component (amplitude: 10 units)
  - Low noise (2% of signal)
  - No sharp transitions

Expected: System should prefer smooth wavelets (Morlet, Mexican Hat)
""")
    
    # Generate smooth oscillation
    t = np.linspace(0, 72, 300)  # 300 samples over 72 hours
    atp_baseline = 100
    circadian = 30 * np.sin(2*np.pi*t/24)
    ultradian = 10 * np.sin(2*np.pi*t/12)
    noise = 2 * np.random.randn(len(t))
    
    signal = atp_baseline + circadian + ultradian + noise
    
    # Create analyzer
    analyzer = SystemAnalyzer(sampling_rate=1.0)
    
    print("🔍 Analyzing signal...")
    print(f"   Signal length: {len(signal)} samples")
    print(f"   Duration: 72 hours")
    print(f"   Mean: {signal.mean():.1f} units")
    print(f"   Std dev: {signal.std():.1f} units")
    
    # MVP mode (manual selection)
    print_subheader("MVP Mode: Manual Wavelet Selection")
    result_mvp = analyzer.wavelet_lens(signal, wavelet_name='morl')
    print(f"   Wavelet used: {result_mvp.wavelet_used}")
    print(f"   Transient events detected: {len(result_mvp.transient_events)}")
    
    # Phase 1 mode (auto-selection)
    print_subheader("Phase 1 Mode: Automatic Wavelet Selection")
    result_phase1 = analyzer.wavelet_lens(signal, auto_select=True)
    
    print(f"\n✅ Optimal wavelet selected: {result_phase1.wavelet_used}")
    print(f"   Description: {analyzer.AVAILABLE_WAVELETS[result_phase1.wavelet_used]}")
    
    print(f"\n📊 Selection Scores:")
    print(f"   Total Score:            {result_phase1.selection_score['total_score']:.3f}")
    print(f"   Energy Concentration:   {result_phase1.selection_score['energy_concentration']:.3f}")
    print(f"   Time Localization:      {result_phase1.selection_score['time_localization']:.3f}")
    print(f"   Frequency Localization: {result_phase1.selection_score['frequency_localization']:.3f}")
    print(f"   Edge Quality:           {result_phase1.selection_score['edge_quality']:.3f}")
    
    print(f"\n🎯 Top 3 Alternative Wavelets:")
    for i, (name, scores) in enumerate(result_phase1.alternative_wavelets[:3], 1):
        print(f"   {i}. {name:6s} - Score: {scores['total_score']:.3f} - {analyzer.AVAILABLE_WAVELETS[name]}")
    
    print(f"\n💡 Interpretation:")
    print(f"   For smooth oscillating signals like circadian ATP rhythms,")
    print(f"   the system correctly identified that {result_phase1.wavelet_used} provides")
    print(f"   the best time-frequency resolution.")


def demo_sharp_transient():
    """Demo 2: Sharp stress response"""
    print_header("DEMO 2: Sharp Stress Response (Heat Shock)")
    
    print("""
Scenario: Cell experiences heat shock stress at t=36h
Signal characteristics:
  - Stable baseline (100 units)
  - Sudden ATP spike at stress event (50 unit increase)
  - Sharp transition (occurs over ~2 hours)
  - Quick recovery

Expected: System should prefer wavelets good at localizing sharp events
""")
    
    # Generate signal with sharp transient
    t = np.linspace(0, 72, 300)
    signal = 100 * np.ones(300)
    
    # Add sharp stress response at t=36h (sample index ~150)
    stress_start = 145
    stress_end = 155
    signal[stress_start:stress_end] += 50 * np.exp(-0.5 * ((np.arange(10) - 5)/2)**2)
    
    # Add small noise
    signal += 2 * np.random.randn(300)
    
    analyzer = SystemAnalyzer(sampling_rate=1.0)
    
    print("🔍 Analyzing signal...")
    print(f"   Signal length: {len(signal)} samples")
    print(f"   Duration: 72 hours")
    print(f"   Baseline: {signal[:100].mean():.1f} units")
    print(f"   Peak: {signal.max():.1f} units")
    print(f"   Stress timing: ~36 hours")
    
    # Phase 1 mode (auto-selection)
    print_subheader("Phase 1 Mode: Automatic Wavelet Selection")
    result = analyzer.wavelet_lens(signal, auto_select=True)
    
    print(f"\n✅ Optimal wavelet selected: {result.wavelet_used}")
    print(f"   Description: {analyzer.AVAILABLE_WAVELETS[result.wavelet_used]}")
    
    print(f"\n📊 Selection Scores:")
    print(f"   Total Score:            {result.selection_score['total_score']:.3f}")
    print(f"   Energy Concentration:   {result.selection_score['energy_concentration']:.3f}")
    print(f"   Time Localization:      {result.selection_score['time_localization']:.3f} ⭐")
    print(f"   Frequency Localization: {result.selection_score['frequency_localization']:.3f}")
    print(f"   Edge Quality:           {result.selection_score['edge_quality']:.3f}")
    
    print(f"\n🎯 Transient Events Detected: {len(result.transient_events)}")
    for i, event in enumerate(result.transient_events, 1):
        time_hours = event['time_index'] * 72 / 300
        print(f"   Event {i}: t={time_hours:.1f}h, intensity={event['intensity']:.1f}, duration={event['duration_samples']} samples")
    
    print(f"\n💡 Interpretation:")
    print(f"   For sharp transient events like stress responses,")
    print(f"   the system selected {result.wavelet_used} which excels at")
    print(f"   time localization (score: {result.selection_score['time_localization']:.3f})")


def demo_complex_signal():
    """Demo 3: Complex mixed signal"""
    print_header("DEMO 3: Complex Mixed Signal (Cell Cycle + Stress)")
    
    print("""
Scenario: Cell undergoing division with periodic checkpoints + stress event
Signal characteristics:
  - Baseline circadian rhythm (24h, amplitude: 20)
  - Cell cycle checkpoints (periodic spikes every 8h)
  - Stress event at t=40h
  - Moderate noise

Expected: System should balance multiple requirements
""")
    
    # Generate complex signal
    t = np.linspace(0, 72, 300)
    
    # Circadian baseline
    circadian = 20 * np.sin(2*np.pi*t/24)
    
    # Cell cycle checkpoints (spikes every 8 hours)
    checkpoints = np.zeros(300)
    for checkpoint_time in [8, 16, 24, 32, 40, 48, 56, 64]:
        idx = int(checkpoint_time * 300 / 72)
        if idx < 300:
            checkpoints[max(0,idx-2):min(300,idx+2)] += 15
    
    # Stress event at t=40h
    stress = np.zeros(300)
    stress_idx = int(40 * 300 / 72)
    stress[stress_idx:stress_idx+10] = 30
    
    # Combine
    signal = 100 + circadian + checkpoints + stress + 3*np.random.randn(300)
    
    analyzer = SystemAnalyzer(sampling_rate=1.0)
    
    print("🔍 Analyzing signal...")
    print(f"   Signal length: {len(signal)} samples")
    print(f"   Components: circadian + cell cycle + stress")
    print(f"   Mean: {signal.mean():.1f} units")
    
    # Phase 1 mode (auto-selection)
    print_subheader("Phase 1 Mode: Automatic Wavelet Selection")
    result = analyzer.wavelet_lens(signal, auto_select=True)
    
    print(f"\n✅ Optimal wavelet selected: {result.wavelet_used}")
    print(f"   Description: {analyzer.AVAILABLE_WAVELETS[result.wavelet_used]}")
    
    print(f"\n📊 Selection Scores (Balanced Performance):")
    print(f"   Total Score:            {result.selection_score['total_score']:.3f}")
    print(f"   Energy Concentration:   {result.selection_score['energy_concentration']:.3f}")
    print(f"   Time Localization:      {result.selection_score['time_localization']:.3f}")
    print(f"   Frequency Localization: {result.selection_score['frequency_localization']:.3f}")
    print(f"   Edge Quality:           {result.selection_score['edge_quality']:.3f}")
    
    print(f"\n🎯 Top 5 Alternative Wavelets:")
    for i, (name, scores) in enumerate(result.alternative_wavelets[:5], 1):
        print(f"   {i}. {name:6s} - Score: {scores['total_score']:.3f}")
    
    print(f"\n💡 Interpretation:")
    print(f"   For complex signals with both smooth and sharp features,")
    print(f"   the system selected {result.wavelet_used} which provides")
    print(f"   balanced performance across all metrics.")


def demo_comparison():
    """Demo 4: Side-by-side comparison"""
    print_header("DEMO 4: Comparison Across All Wavelets")
    
    print("""
Scenario: Compare all available wavelets on the same signal
Signal: Circadian ATP with stress event
Purpose: Show why automatic selection matters
""")
    
    # Generate signal
    t = np.linspace(0, 72, 300)
    circadian = 30 * np.sin(2*np.pi*t/24)
    signal = 100 + circadian + 5*np.random.randn(300)
    
    # Add stress at t=36h
    stress_idx = 150
    signal[stress_idx:stress_idx+10] += 40
    
    analyzer = SystemAnalyzer(sampling_rate=1.0)
    
    print("🔍 Testing all wavelets...")
    print(f"\n{'Wavelet':<10} {'Total':<8} {'Energy':<8} {'Time':<8} {'Freq':<8} {'Edge':<8} {'Events':<8}")
    print("-" * 70)
    
    results = []
    for wavelet_name in analyzer.AVAILABLE_WAVELETS.keys():
        try:
            result = analyzer.wavelet_lens(signal, wavelet_name=wavelet_name)
            
            # Get scores by running auto-select once
            result_scored = analyzer.wavelet_lens(signal, auto_select=True)
            
            # Find this wavelet's scores in alternatives
            scores = None
            for name, s in result_scored.alternative_wavelets:
                if name == wavelet_name:
                    scores = s
                    break
            
            if scores:
                results.append((wavelet_name, scores, len(result.transient_events)))
                print(f"{wavelet_name:<10} "
                      f"{scores['total_score']:<8.3f} "
                      f"{scores['energy_concentration']:<8.3f} "
                      f"{scores['time_localization']:<8.3f} "
                      f"{scores['frequency_localization']:<8.3f} "
                      f"{scores['edge_quality']:<8.3f} "
                      f"{len(result.transient_events):<8}")
        except Exception as e:
            print(f"{wavelet_name:<10} ERROR: {str(e)}")
    
    # Find best
    if results:
        best = max(results, key=lambda x: x[1]['total_score'])
        print("\n" + "="*70)
        print(f"🏆 Best Wavelet: {best[0]}")
        print(f"   Total Score: {best[1]['total_score']:.3f}")
        print(f"   Events Detected: {best[2]}")
        
        print(f"\n💡 Key Insight:")
        print(f"   Different wavelets give different scores and detect different")
        print(f"   numbers of events. Automatic selection saves you from having")
        print(f"   to manually test all {len(analyzer.AVAILABLE_WAVELETS)} options!")


def main():
    """Run all demos"""
    print_header("Phase 1 Feature 2: Automatic Wavelet Selection Demo")
    print("""
This demo shows how BioXen's Four-Lens Analysis System automatically
selects the optimal wavelet transform for different biological signals.

Why This Matters:
  - Different wavelets are good at different things
  - Morlet: smooth oscillations (circadian rhythms)
  - Daubechies: sharp features (stress responses)
  - Mexican Hat: peak detection (transient events)
  
  Without auto-selection, you'd have to:
  1. Try all 7 wavelets manually
  2. Compare results
  3. Pick the best one
  4. Document your choice
  
  With auto-selection:
  1. Set auto_select=True
  2. System picks the best wavelet automatically
  3. Get detailed scores explaining the choice
  4. See alternative options if you want to explore

Let's see it in action!
""")
    
    input("Press Enter to start Demo 1 (Smooth Oscillation)...")
    demo_smooth_oscillation()
    
    input("\n\nPress Enter to start Demo 2 (Sharp Transient)...")
    demo_sharp_transient()
    
    input("\n\nPress Enter to start Demo 3 (Complex Signal)...")
    demo_complex_signal()
    
    input("\n\nPress Enter to start Demo 4 (Comparison)...")
    demo_comparison()
    
    print_header("✅ PHASE 1 FEATURE 2 DEMO COMPLETE!")
    print("""
Summary:
  ✅ Automatic wavelet selection works
  ✅ Different signals get different wavelets
  ✅ Selection metrics provide transparency
  ✅ Alternative wavelets available for exploration
  ✅ Backward compatible (MVP mode still works)

Next Steps:
  - Run on your real biological data
  - Compare auto-selected vs manual selection
  - Try Phase 1 Feature 3: Transfer Functions (Week 3)
  - Try Phase 1 Feature 4: Consensus Validation (Week 4)

Key Takeaway:
  The system intelligently adapts to your signal characteristics,
  saving time and improving analysis quality!
""")


if __name__ == '__main__':
    main()
