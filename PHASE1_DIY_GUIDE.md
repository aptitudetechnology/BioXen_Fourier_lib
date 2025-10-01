# Phase 1 Implementation Guide - DIY Edition

**Your Choice:** Option B - Self Implementation with AI Support  
**Date:** October 1, 2025  
**Status:** Ready to code!

---

## 🎯 Your Mission: Implement Phase 1 Features

You'll be implementing **4 major features** over the next 4 weeks. I've prepared everything you need to succeed!

---

## 📚 Your Support Package

### 1. Complete Specifications
- **PHASE1_PLAN.md** - 1,050 lines of detailed specs
  - Algorithm descriptions
  - Code examples
  - Test cases
  - Performance targets

### 2. Starting Point
- **Enhanced data structures** - Already done! ✅
  - `FourierResult` has harmonics fields
  - `WaveletResult` has wavelet selection fields
  - Backward compatible with MVP

### 3. This Guide
- Step-by-step implementation order
- Code snippets to copy/adapt
- Testing strategies
- Debugging tips

---

## 🗺️ Implementation Roadmap

### Week 1: Feature 1 - Advanced Lomb-Scargle
**Goal:** Detect multiple harmonics (24h + 12h + 8h)

**Files to modify:**
- `src/bioxen_fourier_vm_lib/analysis/system_analyzer.py`

**New methods to add:**
1. `_detect_harmonics()` - ~50 lines
2. `_estimate_phase()` - ~20 lines
3. `_estimate_amplitude()` - ~15 lines
4. `_calculate_bootstrap_confidence()` - ~40 lines (optional for week 1)

**Existing method to modify:**
- `fourier_lens()` - Add 2 parameters, ~30 lines added

**Tests to create:**
- `tests/test_phase1_harmonics.py` - ~200 lines

---

### Week 2: Feature 2 - Wavelet Optimization
**Goal:** Automatically select best wavelet for signal

**Files to modify:**
- `src/bioxen_fourier_vm_lib/analysis/system_analyzer.py`

**New methods to add:**
1. `_select_optimal_wavelet()` - ~80 lines
2. `_calculate_energy_concentration()` - ~20 lines
3. `_calculate_time_localization()` - ~25 lines
4. `_calculate_freq_localization()` - ~25 lines
5. `_calculate_edge_quality()` - ~25 lines

**Existing method to modify:**
- `wavelet_lens()` - Add wavelet selection logic, ~20 lines

**Tests to create:**
- `tests/test_phase1_wavelets.py` - ~150 lines

---

### Week 3: Feature 3 - Transfer Functions
**Goal:** System identification with ARMAX models

**Files to create:**
- `src/bioxen_fourier_vm_lib/analysis/transfer_function.py` (NEW)

**New class:**
- `TransferFunctionAnalyzer` - ~400 lines total

**Methods to implement:**
1. `identify_transfer_function()` - ~60 lines
2. `_estimate_armax_parameters()` - ~40 lines
3. `_armax_to_transfer_function()` - ~30 lines
4. `_calculate_fit_quality()` - ~35 lines
5. `convert_to_state_space()` - ~25 lines
6. `simulate_system_response()` - ~30 lines

**Tests to create:**
- `tests/test_phase1_transfer_functions.py` - ~200 lines

---

### Week 4: Feature 4 - Consensus Validation
**Goal:** Multi-method period detection with voting

**Files to create:**
- `src/bioxen_fourier_vm_lib/analysis/consensus.py` (NEW)

**New class:**
- `ConsensusAnalyzer` - ~350 lines total

**Methods to implement:**
1. `consensus_period_detection()` - ~50 lines
2. `_detect_period_lomb_scargle()` - ~20 lines
3. `_detect_period_fft()` - ~30 lines
4. `_detect_period_autocorrelation()` - ~40 lines
5. `_detect_period_fisher_g()` - ~30 lines
6. `_calculate_consensus()` - ~40 lines

**Tests to create:**
- `tests/test_phase1_consensus.py` - ~250 lines

---

## 🚀 Week 1 Detailed Guide: Advanced Lomb-Scargle

Let's start with Feature 1! Here's your step-by-step guide:

### Step 1: Implement `_detect_harmonics()`

**Location:** Add to `SystemAnalyzer` class in `system_analyzer.py`

**What it does:** Iteratively finds multiple periodic components

**Copy this and adapt:**

```python
def _detect_harmonics(
    self,
    ls: LombScargle,
    frequency: np.ndarray,
    power: np.ndarray,
    max_harmonics: int
) -> List[Dict[str, float]]:
    """
    Detect multiple harmonic components by iterative peak detection.
    
    Algorithm:
    1. Find dominant peak → record as harmonic
    2. Fit sinusoid at that frequency
    3. Subtract fitted component from signal
    4. Analyze residual for next harmonic
    5. Repeat until power < threshold or max_harmonics reached
    
    Args:
        ls: LombScargle object
        frequency: Frequency array from periodogram
        power: Power array from periodogram
        max_harmonics: Maximum number of harmonics to detect
    
    Returns:
        List of dictionaries with harmonic information
    """
    harmonics = []
    residual = self._current_signal.copy()  # Store in fourier_lens
    timestamps = self._current_timestamps.copy()
    
    for i in range(max_harmonics):
        # Analyze current residual
        ls_residual = LombScargle(timestamps, residual)
        freq, pwr = ls_residual.autopower(
            minimum_frequency=1.0/(100*3600),
            maximum_frequency=self.nyquist_freq
        )
        
        # Find peak
        peak_idx = np.argmax(pwr)
        peak_freq = freq[peak_idx]
        peak_power = pwr[peak_idx]
        
        # Stop if power too low (noise threshold)
        if peak_power < 0.1:
            break
        
        # Estimate amplitude and phase
        amplitude = self._estimate_amplitude(residual, timestamps, peak_freq)
        phase = self._estimate_phase(residual, timestamps, peak_freq)
        
        # Record harmonic
        harmonics.append({
            'frequency': peak_freq,
            'period': 1.0 / peak_freq / 3600,  # Convert to hours
            'power': peak_power,
            'amplitude': amplitude,
            'phase': phase
        })
        
        # Subtract this component from residual
        model = ls_residual.model(timestamps, peak_freq)
        residual = residual - model
    
    return harmonics
```

**⚠️ Important:** You need to store `self._current_signal` and `self._current_timestamps` in `fourier_lens()` before calling this method.

---

### Step 2: Implement `_estimate_phase()`

**Copy this:**

```python
def _estimate_phase(
    self,
    signal: np.ndarray,
    timestamps: np.ndarray,
    frequency: float
) -> float:
    """
    Estimate phase of sinusoidal component using least squares.
    
    Fits: signal = A*sin(2πft) + B*cos(2πft)
    Phase: θ = arctan2(B, A)
    
    Args:
        signal: Signal values
        timestamps: Time points (seconds)
        frequency: Frequency to analyze (Hz)
    
    Returns:
        Phase in radians [0, 2π)
    """
    # Build design matrix
    t = timestamps
    A_matrix = np.column_stack([
        np.sin(2 * np.pi * frequency * t),
        np.cos(2 * np.pi * frequency * t)
    ])
    
    # Least squares fit
    coeffs, _, _, _ = np.linalg.lstsq(A_matrix, signal, rcond=None)
    
    # Calculate phase from coefficients
    phase = np.arctan2(coeffs[1], coeffs[0])
    
    # Normalize to [0, 2π)
    return phase % (2 * np.pi)
```

---

### Step 3: Implement `_estimate_amplitude()`

**Copy this:**

```python
def _estimate_amplitude(
    self,
    signal: np.ndarray,
    timestamps: np.ndarray,
    frequency: float
) -> float:
    """
    Estimate amplitude of sinusoidal component.
    
    Args:
        signal: Signal values
        timestamps: Time points (seconds)
        frequency: Frequency to analyze (Hz)
    
    Returns:
        Amplitude (same units as signal)
    """
    # Build design matrix
    t = timestamps
    A_matrix = np.column_stack([
        np.sin(2 * np.pi * frequency * t),
        np.cos(2 * np.pi * frequency * t)
    ])
    
    # Least squares fit
    coeffs, _, _, _ = np.linalg.lstsq(A_matrix, signal, rcond=None)
    
    # Amplitude from Pythagorean theorem
    amplitude = np.sqrt(coeffs[0]**2 + coeffs[1]**2)
    
    return amplitude
```

---

### Step 4: Modify `fourier_lens()` Method

**Find this method** (around line 180-260) and modify it:

**Add these parameters to signature:**
```python
def fourier_lens(
    self, 
    time_series: np.ndarray, 
    timestamps: Optional[np.ndarray] = None,
    detect_harmonics: bool = False,  # NEW
    max_harmonics: int = 5  # NEW
) -> FourierResult:
```

**Add this BEFORE the LombScargle analysis:**
```python
# Store for harmonic detection (if needed)
self._current_signal = time_series.copy()
if timestamps is None:
    timestamps = np.arange(len(time_series)) / self.sampling_rate
self._current_timestamps = timestamps.copy()
```

**Add this AFTER finding dominant frequency (before return):**
```python
# Phase 1: Multi-harmonic detection
harmonics = None
harmonic_power = None

if detect_harmonics:
    harmonics = self._detect_harmonics(
        ls, frequency, power, max_harmonics
    )
    harmonic_power = sum(h['power'] for h in harmonics) if harmonics else 0.0
```

**Modify the return statement:**
```python
return FourierResult(
    frequencies=frequency,
    power_spectrum=power,
    dominant_frequency=dominant_freq,
    dominant_period=dominant_period / 3600.0,
    significance=significance,
    harmonics=harmonics,  # NEW
    harmonic_power=harmonic_power  # NEW
)
```

---

### Step 5: Create Tests

**Create:** `tests/test_phase1_harmonics.py`

**Copy this starter:**

```python
"""
Phase 1 Tests: Multi-Harmonic Detection
"""

import pytest
import numpy as np
from bioxen_fourier_vm_lib.analysis.system_analyzer import SystemAnalyzer


@pytest.fixture
def analyzer():
    """Standard analyzer for testing"""
    return SystemAnalyzer(sampling_rate=1.0)


def test_single_harmonic_backward_compatibility(analyzer):
    """Test that single harmonic still works (MVP compatibility)"""
    # 24h circadian signal
    t = np.linspace(0, 72, 300)
    signal = 100 + 30*np.sin(2*np.pi*t/24)
    
    # Without harmonics (MVP behavior)
    result = analyzer.fourier_lens(signal, t, detect_harmonics=False)
    
    assert result.harmonics is None
    assert result.harmonic_power is None
    assert 20 < result.dominant_period < 28


def test_multi_harmonic_detection(analyzer):
    """Test detection of 24h + 12h harmonics"""
    # Signal with two components
    t = np.linspace(0, 72, 300)
    signal = (100 + 
              30*np.sin(2*np.pi*t/24) +  # 24h fundamental
              10*np.sin(2*np.pi*t/12))   # 12h harmonic
    
    # With harmonics (Phase 1)
    result = analyzer.fourier_lens(signal, t, detect_harmonics=True)
    
    assert result.harmonics is not None
    assert len(result.harmonics) >= 2
    
    # Check periods detected
    periods = [h['period'] for h in result.harmonics]
    assert any(20 < p < 28 for p in periods), "Should detect 24h"
    assert any(10 < p < 14 for p in periods), "Should detect 12h"


def test_phase_estimation(analyzer):
    """Test phase estimation accuracy"""
    # Known phase signal
    t = np.linspace(0, 48, 200)
    phase_true = np.pi / 4  # 45 degrees
    signal = 100 + 30*np.sin(2*np.pi*t/24 + phase_true)
    
    result = analyzer.fourier_lens(signal, t, detect_harmonics=True)
    
    assert len(result.harmonics) >= 1
    phase_detected = result.harmonics[0]['phase']
    
    # Should be within 0.2 radians (~11 degrees)
    assert abs(phase_detected - phase_true) < 0.2


def test_amplitude_estimation(analyzer):
    """Test amplitude estimation accuracy"""
    t = np.linspace(0, 48, 200)
    amplitude_true = 30.0
    signal = 100 + amplitude_true*np.sin(2*np.pi*t/24)
    
    result = analyzer.fourier_lens(signal, t, detect_harmonics=True)
    
    assert len(result.harmonics) >= 1
    amplitude_detected = result.harmonics[0]['amplitude']
    
    # Should be within 10%
    assert abs(amplitude_detected - amplitude_true) / amplitude_true < 0.1


def test_harmonic_power_calculation(analyzer):
    """Test that harmonic power is calculated correctly"""
    t = np.linspace(0, 72, 300)
    signal = 100 + 30*np.sin(2*np.pi*t/24) + 10*np.sin(2*np.pi*t/12)
    
    result = analyzer.fourier_lens(signal, t, detect_harmonics=True)
    
    assert result.harmonic_power is not None
    assert result.harmonic_power > 0
    assert len(result.harmonics) >= 2


def test_max_harmonics_limit(analyzer):
    """Test that max_harmonics parameter works"""
    t = np.linspace(0, 72, 300)
    # Complex signal with many components
    signal = (100 + 
              30*np.sin(2*np.pi*t/24) +
              15*np.sin(2*np.pi*t/12) +
              8*np.sin(2*np.pi*t/8) +
              5*np.sin(2*np.pi*t/6))
    
    result = analyzer.fourier_lens(signal, t, detect_harmonics=True, max_harmonics=2)
    
    assert len(result.harmonics) <= 2


def test_noisy_signal_harmonics(analyzer):
    """Test robustness with noisy signal"""
    t = np.linspace(0, 72, 300)
    clean = 100 + 30*np.sin(2*np.pi*t/24) + 10*np.sin(2*np.pi*t/12)
    noise = 5*np.random.randn(len(t))
    signal = clean + noise
    
    result = analyzer.fourier_lens(signal, t, detect_harmonics=True)
    
    # Should still detect at least one harmonic
    assert len(result.harmonics) >= 1
    
    # Dominant should be around 24h
    assert 20 < result.harmonics[0]['period'] < 28


if __name__ == "__main__":
    pytest.main([__file__, '-v'])
```

---

### Step 6: Run Tests

```bash
# Activate environment
cd ~/BioXen_Fourier_lib
source venv/bin/activate

# Run your new tests
pytest tests/test_phase1_harmonics.py -v

# If tests pass, run full suite
pytest tests/ -v
```

---

### Step 7: Create Demo Script

**Create:** `examples/demo_phase1_harmonics.py`

```python
"""
Phase 1 Feature 1 Demo: Multi-Harmonic Detection

Demonstrates detection of multiple circadian rhythms in biological signals.
"""

import numpy as np
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from bioxen_fourier_vm_lib.analysis.system_analyzer import SystemAnalyzer


def main():
    print("=" * 70)
    print("Phase 1 Feature 1: Multi-Harmonic Detection Demo")
    print("=" * 70)
    
    # Create analyzer
    analyzer = SystemAnalyzer(sampling_rate=1.0)  # 1 sample/hour
    
    # Generate synthetic biological signal
    # Simulates ATP levels with circadian (24h) and ultradian (12h) rhythms
    print("\n📊 Generating synthetic ATP signal...")
    t = np.linspace(0, 72, 300)  # 72 hours, 300 samples
    
    atp_baseline = 100  # Arbitrary units
    circadian_component = 30 * np.sin(2*np.pi*t/24 + np.pi/6)  # 24h, phase shift
    ultradian_component = 15 * np.sin(2*np.pi*t/12)  # 12h
    noise = 3 * np.random.randn(len(t))
    
    atp_signal = atp_baseline + circadian_component + ultradian_component + noise
    
    print(f"   Duration: 72 hours")
    print(f"   Samples: {len(t)}")
    print(f"   Components: 24h (circadian) + 12h (ultradian) + noise")
    
    # Analyze WITHOUT harmonics (MVP mode)
    print("\n" + "=" * 70)
    print("MVP Mode (Single Period Detection)")
    print("=" * 70)
    
    result_mvp = analyzer.fourier_lens(atp_signal, t, detect_harmonics=False)
    
    print(f"   Dominant period: {result_mvp.dominant_period:.2f} hours")
    print(f"   Significance: {result_mvp.significance:.4f}")
    print(f"   Harmonics detected: None (MVP mode)")
    
    # Analyze WITH harmonics (Phase 1)
    print("\n" + "=" * 70)
    print("Phase 1 Mode (Multi-Harmonic Detection)")
    print("=" * 70)
    
    result_phase1 = analyzer.fourier_lens(atp_signal, t, 
                                          detect_harmonics=True,
                                          max_harmonics=5)
    
    print(f"   Dominant period: {result_phase1.dominant_period:.2f} hours")
    print(f"   Total harmonic power: {result_phase1.harmonic_power:.4f}")
    print(f"   Number of harmonics: {len(result_phase1.harmonics)}")
    
    print("\n   Detected Harmonics:")
    print("   " + "-" * 66)
    print(f"   {'#':<4} {'Period (h)':<12} {'Amplitude':<12} {'Phase (rad)':<12} {'Power':<12}")
    print("   " + "-" * 66)
    
    for i, h in enumerate(result_phase1.harmonics, 1):
        print(f"   {i:<4} {h['period']:<12.2f} {h['amplitude']:<12.2f} "
              f"{h['phase']:<12.4f} {h['power']:<12.4f}")
    
    # Biological interpretation
    print("\n" + "=" * 70)
    print("🔬 Biological Interpretation")
    print("=" * 70)
    
    for i, h in enumerate(result_phase1.harmonics, 1):
        period = h['period']
        amplitude = h['amplitude']
        phase_deg = h['phase'] * 180 / np.pi
        
        if 20 < period < 28:
            print(f"\n   Harmonic {i}: CIRCADIAN RHYTHM")
            print(f"   ├─ Period: ~24h (actual: {period:.1f}h)")
            print(f"   ├─ Amplitude: {amplitude:.1f} ATP units")
            print(f"   ├─ Phase: {phase_deg:.1f}° (peak at {phase_deg/15:.1f}h after midnight)")
            print(f"   └─ Interpretation: Primary biological clock")
            
        elif 10 < period < 14:
            print(f"\n   Harmonic {i}: ULTRADIAN RHYTHM")
            print(f"   ├─ Period: ~12h (actual: {period:.1f}h)")
            print(f"   ├─ Amplitude: {amplitude:.1f} ATP units")
            print(f"   ├─ Phase: {phase_deg:.1f}°")
            print(f"   └─ Interpretation: Metabolic oscillations, 2x per day")
            
        elif 6 < period < 10:
            print(f"\n   Harmonic {i}: SHORT ULTRADIAN")
            print(f"   ├─ Period: ~8h (actual: {period:.1f}h)")
            print(f"   ├─ Amplitude: {amplitude:.1f} ATP units")
            print(f"   └─ Interpretation: Cellular processes, 3x per day")
    
    print("\n" + "=" * 70)
    print("✅ Demo Complete!")
    print("=" * 70)
    print("\n💡 Key Insights:")
    print("   • Phase 1 reveals multiple rhythms in same signal")
    print("   • 24h circadian + 12h ultradian detected successfully")
    print("   • Phase information shows timing relationships")
    print("   • Amplitude shows relative strength of each rhythm")
    print("\n📖 Next: Try with real genomic data (examples/genomic_mvp_demo.py)")


if __name__ == "__main__":
    main()
```

---

## 🧪 Testing Workflow

### Standard Testing Process:

```bash
# 1. Run specific test file
pytest tests/test_phase1_harmonics.py -v

# 2. Run with coverage
pytest tests/test_phase1_harmonics.py -v --cov=src/bioxen_fourier_vm_lib/analysis

# 3. Run specific test
pytest tests/test_phase1_harmonics.py::test_multi_harmonic_detection -v

# 4. Run all tests
pytest tests/ -v

# 5. Run demo
python examples/demo_phase1_harmonics.py
```

---

## 🐛 Debugging Tips

### Common Issues:

**1. "AttributeError: 'SystemAnalyzer' object has no attribute '_current_signal'"**
- **Fix:** Add `self._current_signal = None` to `__init__()` method
- **Fix:** Store signal in `fourier_lens()` before calling `_detect_harmonics()`

**2. "LinAlgWarning: Ill-conditioned matrix"**
- **Cause:** Timestamps not in seconds, or very large/small values
- **Fix:** Normalize timestamps to reasonable range (0 to duration_seconds)

**3. "No harmonics detected"**
- **Cause:** Power threshold too high
- **Fix:** Lower threshold in `_detect_harmonics()` (try 0.05 instead of 0.1)

**4. "Phase estimation inaccurate"**
- **Cause:** Noisy signal or wrong frequency
- **Fix:** Add more samples, reduce noise, or fit over multiple periods

**5. Tests fail with "period not in expected range"**
- **Cause:** Fourier bug from MVP still present
- **Fix:** Check timestamp units (should be in seconds for Lomb-Scargle)

---

## 📊 Progress Tracking

### Week 1 Checklist:

- [ ] Step 1: Implement `_detect_harmonics()` (2 hours)
- [ ] Step 2: Implement `_estimate_phase()` (30 min)
- [ ] Step 3: Implement `_estimate_amplitude()` (30 min)
- [ ] Step 4: Modify `fourier_lens()` (1 hour)
- [ ] Step 5: Create tests (2 hours)
- [ ] Step 6: Run and debug tests (1 hour)
- [ ] Step 7: Create demo script (1 hour)
- [ ] Step 8: Test with real Syn3A genome (1 hour)
- [ ] Step 9: Update documentation (1 hour)
- [ ] Step 10: Commit and push (30 min)

**Total: ~10 hours**

---

## 💬 When You Need Help

### Ask me for:

✅ **Code review:** "Review my `_detect_harmonics()` implementation"  
✅ **Debugging:** "Test failing with error X"  
✅ **Clarification:** "What does energy concentration mean?"  
✅ **Best practices:** "Is this the right approach for X?"  
✅ **Optimization:** "How to make this faster?"  
✅ **Testing:** "What else should I test?"

### I can help with:

- Reviewing your code before committing
- Debugging test failures
- Explaining algorithms
- Suggesting optimizations
- Writing additional tests
- Creating documentation
- Validating biological interpretations

---

## 🚀 Let's Go!

### Your First Task (Right Now):

1. **Open:** `src/bioxen_fourier_vm_lib/analysis/system_analyzer.py`

2. **Find:** The `SystemAnalyzer` class

3. **Add:** The three new methods (`_detect_harmonics`, `_estimate_phase`, `_estimate_amplitude`)

4. **Test:** Run a simple test to see if it compiles

5. **Report back:** "Methods added" or "Got error X"

**I'm here to support you every step of the way!** 🎯

---

**Good luck! You've got this! 💪**

**Remember:** PHASE1_PLAN.md has all the details if you need more context.

---

**Status:** Ready to implement  
**Next:** Add the three helper methods to SystemAnalyzer  
**Support:** Ask me anything!
