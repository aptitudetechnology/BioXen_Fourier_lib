# BioXen Fourier VM Library: MVP Execution Model Enhancement

## Executive Summary

This is the **Minimum Viable Prototype (MVP)** implementation plan for integrating three-lens system analysis into the BioXen execution model. This plan focuses on delivering a working proof-of-concept in **2 weeks** that demonstrates the core value proposition while maintaining scientific validity.

**Goal:** Transform biological VM execution from passive process running to active dynamics analysis with Fourier, Laplace, and Z-transform insights.

**Timeline:** 2 weeks (80 hours)  
**Deliverable:** Working prototype demonstrating all three lenses on simulated VM data

---

## MVP Scope: What's In vs. Out

### ✅ In Scope (MVP)

**Core Features:**
- Basic `SystemAnalyzer` class with three lens methods
- Simple Fourier analysis (FFT for uniform sampling)
- Basic Laplace analysis (pole estimation from frequency response)
- Simple Z-transform filtering (lowpass Butterworth filter)
- Integration point in `BioXenHypervisor`
- Demo script showing all three lenses working
- Basic unit tests (happy path only)

**Simplifications:**
- Assume uniform sampling (skip Lomb-Scargle for MVP)
- Use 2nd-order system approximation for Laplace
- Single filter type (lowpass only)
- Synthetic test data (no real biosensor integration)
- Terminal text output (no plots for MVP)

### ❌ Out of Scope (Post-MVP)

**Deferred to Production:**
- Lomb-Scargle for irregular sampling
- Full transfer function system identification
- Multiple filter types (highpass, bandpass)
- Real-time plotting/visualization
- Comprehensive error handling
- Performance optimization
- Advanced control system design
- Integration with actual VM metrics
- Extensive documentation

---

## Week 1: Core Implementation (40 hours)

### Day 1-2: SystemAnalyzer Foundation (16 hours)

**File:** `src/bioxen_fourier_vm_lib/analysis/system_analyzer.py`

```python
"""
BioXen System Analyzer - MVP Implementation

Three-lens analysis for biological VM time series:
- Fourier: Frequency domain spectral analysis
- Laplace: Transfer function and stability analysis  
- Z-Transform: Discrete-time filtering

MVP simplifications:
- Uniform sampling only (no Lomb-Scargle)
- 2nd order Laplace approximation
- Lowpass filtering only
"""

from scipy import signal
from scipy.fft import fft, fftfreq
import numpy as np
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class FourierResult:
    """Simplified Fourier analysis results"""
    frequencies: np.ndarray
    power_spectrum: np.ndarray
    dominant_frequency: float
    dominant_period: float


@dataclass
class LaplaceResult:
    """Simplified Laplace analysis results"""
    poles: np.ndarray
    stability: str  # 'stable', 'oscillatory', 'unstable'
    natural_frequency: float


@dataclass
class ZTransformResult:
    """Simplified Z-transform results"""
    filtered_signal: np.ndarray
    noise_reduction_percent: float


class SystemAnalyzer:
    """
    MVP System Analyzer for biological time series.
    
    Example:
        >>> analyzer = SystemAnalyzer(sampling_rate=1.0)
        >>> fourier = analyzer.fourier_lens(atp_data)
        >>> print(f"Dominant period: {fourier.dominant_period:.1f} hours")
    """
    
    def __init__(self, sampling_rate: float = 1.0):
        """
        Initialize analyzer.
        
        Args:
            sampling_rate: Samples per hour (default: 1.0 = hourly samples)
        """
        self.sampling_rate = sampling_rate
        self.nyquist = sampling_rate / 2.0
    
    def fourier_lens(self, time_series: np.ndarray) -> FourierResult:
        """
        Fourier transform analysis - MVP version with standard FFT.
        
        Args:
            time_series: Uniformly sampled biological signal
        
        Returns:
            FourierResult with frequency spectrum
        """
        # Compute FFT
        n = len(time_series)
        yf = fft(time_series)
        xf = fftfreq(n, 1/self.sampling_rate)
        
        # Keep positive frequencies only
        positive_freqs = xf[:n//2]
        power = np.abs(yf[:n//2])
        
        # Find dominant frequency
        peak_idx = np.argmax(power[1:]) + 1  # Skip DC component
        dominant_freq = positive_freqs[peak_idx]
        dominant_period = 1.0 / dominant_freq if dominant_freq > 0 else float('inf')
        
        return FourierResult(
            frequencies=positive_freqs,
            power_spectrum=power,
            dominant_frequency=dominant_freq,
            dominant_period=dominant_period
        )
    
    def laplace_lens(self, time_series: np.ndarray) -> LaplaceResult:
        """
        Laplace transform analysis - MVP version with 2nd order approximation.
        
        Args:
            time_series: Uniformly sampled biological signal
        
        Returns:
            LaplaceResult with pole locations and stability
        """
        # Estimate natural frequency from power spectrum
        freqs, psd = signal.welch(time_series, fs=self.sampling_rate)
        peak_freq = freqs[np.argmax(psd[1:]) + 1]  # Skip DC
        omega_n = 2 * np.pi * peak_freq
        
        # Estimate damping from signal decay
        # Simplified: assume moderate damping for MVP
        zeta = 0.3  # Underdamped oscillator (typical for biological rhythms)
        
        # Calculate 2nd order poles: s = -ζω_n ± jω_n√(1-ζ²)
        real_part = -zeta * omega_n
        imag_part = omega_n * np.sqrt(max(0, 1 - zeta**2))
        poles = np.array([
            real_part + 1j*imag_part,
            real_part - 1j*imag_part
        ])
        
        # Classify stability
        if real_part < -0.01:
            stability = 'oscillatory' if imag_part > 0.01 else 'stable'
        elif real_part > 0.01:
            stability = 'unstable'
        else:
            stability = 'marginally_stable'
        
        return LaplaceResult(
            poles=poles,
            stability=stability,
            natural_frequency=omega_n
        )
    
    def z_transform_lens(
        self, 
        time_series: np.ndarray,
        cutoff_freq: Optional[float] = None
    ) -> ZTransformResult:
        """
        Z-transform analysis - MVP version with simple lowpass filter.
        
        Args:
            time_series: Uniformly sampled biological signal
            cutoff_freq: Filter cutoff (Hz), default = Nyquist/4
        
        Returns:
            ZTransformResult with filtered signal
        """
        if cutoff_freq is None:
            cutoff_freq = self.nyquist / 4.0
        
        # Design 4th order Butterworth lowpass filter
        sos = signal.butter(4, cutoff_freq, 'lowpass', fs=self.sampling_rate, output='sos')
        
        # Apply filter
        filtered = signal.sosfilt(sos, time_series)
        
        # Calculate noise reduction
        original_var = np.var(time_series)
        filtered_var = np.var(filtered)
        noise_reduction = (1.0 - filtered_var/original_var) * 100
        
        return ZTransformResult(
            filtered_signal=filtered,
            noise_reduction_percent=noise_reduction
        )
    
    def analyze_all(self, time_series: np.ndarray) -> Dict[str, Any]:
        """
        Apply all three lenses to signal.
        
        Args:
            time_series: Uniformly sampled biological signal
        
        Returns:
            Dictionary with 'fourier', 'laplace', 'z_transform' results
        """
        return {
            'fourier': self.fourier_lens(time_series),
            'laplace': self.laplace_lens(time_series),
            'z_transform': self.z_transform_lens(time_series)
        }
```

**Tasks:**
- [ ] Create `src/bioxen_fourier_vm_lib/analysis/` directory
- [ ] Create `__init__.py` with exports
- [ ] Implement `SystemAnalyzer` class (above code)
- [ ] Test with synthetic sine wave (24h period)

**Time Estimate:** 16 hours
- Design: 2 hours
- Implementation: 10 hours
- Testing: 4 hours

### Day 3-4: Hypervisor Integration (16 hours)

**File:** `src/bioxen_fourier_vm_lib/hypervisor/core.py`

```python
# Add to imports
from ..analysis import SystemAnalyzer

class BioXenHypervisor:
    def __init__(self, ...):
        # ...existing code...
        
        # MVP: Add system analyzer
        self.system_analyzer = SystemAnalyzer(sampling_rate=1.0)  # 1 sample/hour
        
        # MVP: Simple time series storage
        self._vm_metrics: Dict[str, List[float]] = {}
    
    def record_vm_metric(self, vm_id: str, value: float) -> None:
        """
        MVP: Record single metric value for VM.
        
        Args:
            vm_id: Virtual machine identifier
            value: Metric value (e.g., ATP percentage)
        """
        if vm_id not in self._vm_metrics:
            self._vm_metrics[vm_id] = []
        self._vm_metrics[vm_id].append(value)
    
    def analyze_vm(self, vm_id: str) -> Optional[Dict[str, Any]]:
        """
        MVP: Analyze VM dynamics using three lenses.
        
        Args:
            vm_id: Virtual machine to analyze
        
        Returns:
            Analysis results or None if insufficient data
        """
        if vm_id not in self._vm_metrics:
            self.logger.warning(f"No metrics recorded for VM {vm_id}")
            return None
        
        metrics = self._vm_metrics[vm_id]
        if len(metrics) < 10:
            self.logger.warning(f"Insufficient data for VM {vm_id}: {len(metrics)} points (need ≥10)")
            return None
        
        # Convert to numpy array
        time_series = np.array(metrics)
        
        # Apply three-lens analysis
        try:
            results = self.system_analyzer.analyze_all(time_series)
            
            # MVP: Log interesting findings
            fourier = results['fourier']
            laplace = results['laplace']
            
            self.logger.info(f"VM {vm_id} Analysis:")
            self.logger.info(f"  Dominant period: {fourier.dominant_period:.1f} hours")
            self.logger.info(f"  Stability: {laplace.stability}")
            
            # Check for circadian synchronization
            if abs(fourier.dominant_period - 24.0) < 2.0:
                self.logger.info(f"  ✓ VM synchronized with 24h circadian cycle")
            else:
                self.logger.warning(f"  ⚠ VM desynchronized (period = {fourier.dominant_period:.1f}h)")
            
            return results
            
        except Exception as e:
            self.logger.error(f"Analysis failed for VM {vm_id}: {e}")
            return None
```

**Tasks:**
- [ ] Add `system_analyzer` to `__init__`
- [ ] Implement `record_vm_metric()` method
- [ ] Implement `analyze_vm()` method
- [ ] Add logging for analysis results

**Time Estimate:** 16 hours
- Design: 2 hours
- Implementation: 10 hours
- Integration testing: 4 hours

### Day 5: Demo Script (8 hours)

**File:** `examples/mvp_three_lens_demo.py`

```python
"""
MVP Demo: Three-Lens Analysis of Biological VM Dynamics

Demonstrates Fourier, Laplace, and Z-transform analysis
on simulated circadian ATP oscillations.
"""

import numpy as np
import sys
from pathlib import Path

# Add src to path for demo
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from bioxen_fourier_vm_lib.analysis import SystemAnalyzer


def generate_circadian_atp_data(hours: int = 72, noise_level: float = 5.0) -> np.ndarray:
    """
    Generate synthetic circadian ATP data.
    
    Args:
        hours: Duration in hours (default: 72 = 3 days)
        noise_level: Percentage noise (default: 5%)
    
    Returns:
        Hourly ATP percentage values
    """
    t = np.arange(hours)
    
    # Circadian rhythm: 24h period
    circadian = 50 + 30 * np.sin(2 * np.pi * t / 24.0)
    
    # Add noise
    noise = np.random.normal(0, noise_level, hours)
    
    return circadian + noise


def demo_fourier_lens():
    """Demo: Fourier analysis detects circadian rhythm"""
    print("\n" + "="*60)
    print("DEMO 1: Fourier Lens - Circadian Rhythm Detection")
    print("="*60)
    
    # Generate 3 days of circadian ATP data
    atp_data = generate_circadian_atp_data(hours=72, noise_level=5.0)
    
    # Analyze with Fourier lens
    analyzer = SystemAnalyzer(sampling_rate=1.0)  # 1 sample/hour
    fourier = analyzer.fourier_lens(atp_data)
    
    print(f"\n📊 Results:")
    print(f"  Dominant Frequency: {fourier.dominant_frequency:.4f} Hz")
    print(f"  Dominant Period:    {fourier.dominant_period:.1f} hours")
    print(f"  Power:              {fourier.power_spectrum[np.argmax(fourier.power_spectrum[1:])+1]:.1f}")
    
    if abs(fourier.dominant_period - 24.0) < 2.0:
        print(f"\n✓ SUCCESS: 24-hour circadian rhythm detected!")
    else:
        print(f"\n✗ WARNING: Period deviates from 24h circadian cycle")


def demo_laplace_lens():
    """Demo: Laplace analysis classifies system stability"""
    print("\n" + "="*60)
    print("DEMO 2: Laplace Lens - Stability Analysis")
    print("="*60)
    
    # Generate stable oscillator data
    atp_data = generate_circadian_atp_data(hours=72, noise_level=3.0)
    
    # Analyze with Laplace lens
    analyzer = SystemAnalyzer(sampling_rate=1.0)
    laplace = analyzer.laplace_lens(atp_data)
    
    print(f"\n📊 Results:")
    print(f"  Poles:              {laplace.poles}")
    print(f"  Stability:          {laplace.stability}")
    print(f"  Natural Frequency:  {laplace.natural_frequency:.4f} rad/s")
    
    if laplace.stability == 'oscillatory':
        print(f"\n✓ SUCCESS: System is a stable oscillator (genetic clock)")
    elif laplace.stability == 'stable':
        print(f"\n✓ System is stable (homeostatic)")
    else:
        print(f"\n✗ WARNING: System is {laplace.stability}")


def demo_z_transform_lens():
    """Demo: Z-transform filters measurement noise"""
    print("\n" + "="*60)
    print("DEMO 3: Z-Transform Lens - Noise Filtering")
    print("="*60)
    
    # Generate noisy data
    atp_data = generate_circadian_atp_data(hours=72, noise_level=15.0)
    
    # Analyze with Z-transform lens
    analyzer = SystemAnalyzer(sampling_rate=1.0)
    z_result = analyzer.z_transform_lens(atp_data, cutoff_freq=0.1)
    
    print(f"\n📊 Results:")
    print(f"  Original variance:  {np.var(atp_data):.2f}")
    print(f"  Filtered variance:  {np.var(z_result.filtered_signal):.2f}")
    print(f"  Noise reduction:    {z_result.noise_reduction_percent:.1f}%")
    
    if z_result.noise_reduction_percent > 30:
        print(f"\n✓ SUCCESS: Significant noise reduction achieved")
    else:
        print(f"\n⚠ Moderate noise reduction")


def demo_all_lenses():
    """Demo: Apply all three lenses to same dataset"""
    print("\n" + "="*60)
    print("DEMO 4: Three-Lens Integrated Analysis")
    print("="*60)
    
    # Generate realistic noisy circadian data
    atp_data = generate_circadian_atp_data(hours=72, noise_level=8.0)
    
    # Analyze with all lenses
    analyzer = SystemAnalyzer(sampling_rate=1.0)
    results = analyzer.analyze_all(atp_data)
    
    print(f"\n🔬 Fourier Lens:")
    print(f"   Period: {results['fourier'].dominant_period:.1f}h")
    
    print(f"\n⚙️  Laplace Lens:")
    print(f"   Stability: {results['laplace'].stability}")
    
    print(f"\n📊 Z-Transform Lens:")
    print(f"   Noise reduction: {results['z_transform'].noise_reduction_percent:.1f}%")
    
    print(f"\n✓ All three lenses successfully analyzed VM dynamics!")


if __name__ == '__main__':
    print("\n" + "🔬 BioXen Three-Lens System Analysis MVP Demo")
    print("Demonstrating Fourier, Laplace, and Z-transform analysis")
    print("on simulated circadian ATP oscillations\n")
    
    demo_fourier_lens()
    demo_laplace_lens()
    demo_z_transform_lens()
    demo_all_lenses()
    
    print("\n" + "="*60)
    print("MVP Demo Complete!")
    print("="*60 + "\n")
```

**Tasks:**
- [ ] Create `examples/` directory
- [ ] Implement demo script
- [ ] Test all four demos
- [ ] Add usage instructions

**Time Estimate:** 8 hours
- Implementation: 4 hours
- Testing: 2 hours
- Documentation: 2 hours

---

## Week 2: Testing & Documentation (40 hours)

### Day 6-7: Unit Tests (16 hours)

**File:** `tests/test_system_analyzer.py`

```python
"""
Unit tests for SystemAnalyzer MVP implementation.
"""

import pytest
import numpy as np
from bioxen_fourier_vm_lib.analysis import SystemAnalyzer


class TestFourierLens:
    """Test Fourier analysis"""
    
    def test_detects_24h_period(self):
        """Should detect 24-hour circadian period"""
        # Generate 3 days of hourly data with 24h period
        t = np.arange(72)
        signal = 50 + 30 * np.sin(2 * np.pi * t / 24.0)
        
        analyzer = SystemAnalyzer(sampling_rate=1.0)
        result = analyzer.fourier_lens(signal)
        
        # Should detect ~24h period
        assert abs(result.dominant_period - 24.0) < 1.0
        assert result.dominant_frequency > 0
    
    def test_returns_correct_structure(self):
        """Should return FourierResult with all fields"""
        signal = np.random.randn(50)
        analyzer = SystemAnalyzer()
        result = analyzer.fourier_lens(signal)
        
        assert hasattr(result, 'frequencies')
        assert hasattr(result, 'power_spectrum')
        assert hasattr(result, 'dominant_frequency')
        assert hasattr(result, 'dominant_period')


class TestLaplaceLens:
    """Test Laplace analysis"""
    
    def test_classifies_oscillator_as_oscillatory(self):
        """Should classify stable oscillator correctly"""
        # Generate damped oscillation
        t = np.linspace(0, 100, 100)
        signal = np.exp(-0.1*t) * np.sin(2*np.pi*t/24)
        
        analyzer = SystemAnalyzer(sampling_rate=1.0)
        result = analyzer.laplace_lens(signal)
        
        assert result.stability in ['oscillatory', 'stable']
        assert len(result.poles) == 2
    
    def test_returns_correct_structure(self):
        """Should return LaplaceResult with all fields"""
        signal = np.random.randn(50)
        analyzer = SystemAnalyzer()
        result = analyzer.laplace_lens(signal)
        
        assert hasattr(result, 'poles')
        assert hasattr(result, 'stability')
        assert hasattr(result, 'natural_frequency')


class TestZTransformLens:
    """Test Z-transform analysis"""
    
    def test_reduces_noise(self):
        """Should reduce noise through filtering"""
        # Clean signal + noise
        t = np.arange(100)
        clean = np.sin(2 * np.pi * t / 24)
        noisy = clean + 0.5 * np.random.randn(100)
        
        analyzer = SystemAnalyzer(sampling_rate=1.0)
        result = analyzer.z_transform_lens(noisy)
        
        # Should reduce noise
        assert result.noise_reduction_percent > 20
        assert len(result.filtered_signal) == len(noisy)
    
    def test_returns_correct_structure(self):
        """Should return ZTransformResult with all fields"""
        signal = np.random.randn(50)
        analyzer = SystemAnalyzer()
        result = analyzer.z_transform_lens(signal)
        
        assert hasattr(result, 'filtered_signal')
        assert hasattr(result, 'noise_reduction_percent')


class TestAnalyzeAll:
    """Test integrated analysis"""
    
    def test_returns_all_three_lenses(self):
        """Should return results from all three lenses"""
        signal = np.random.randn(50)
        analyzer = SystemAnalyzer()
        results = analyzer.analyze_all(signal)
        
        assert 'fourier' in results
        assert 'laplace' in results
        assert 'z_transform' in results
```

**Tasks:**
- [ ] Create `tests/` directory
- [ ] Set up pytest configuration
- [ ] Write unit tests for each lens
- [ ] Achieve >80% code coverage

**Time Estimate:** 16 hours
- Test design: 4 hours
- Implementation: 8 hours
- Debugging: 4 hours

### Day 8-9: Documentation (16 hours)

**File:** `docs/mvp_three_lens_guide.md`

```markdown
# Three-Lens System Analysis MVP Guide

## Overview

The BioXen Three-Lens System Analyzer provides frequency-domain analysis
of biological VM dynamics using three complementary mathematical transforms:

1. **Fourier Transform**: Detects periodic patterns (circadian rhythms)
2. **Laplace Transform**: Analyzes system stability and response
3. **Z-Transform**: Filters noise from discrete measurements

## Quick Start

### Installation

```bash
pip install -e .
```

### Basic Usage

```python
from bioxen_fourier_vm_lib.analysis import SystemAnalyzer
import numpy as np

# Create analyzer
analyzer = SystemAnalyzer(sampling_rate=1.0)  # 1 sample/hour

# Generate sample data (72 hours of ATP measurements)
atp_data = np.array([...])  # Your VM metrics

# Analyze with all three lenses
results = analyzer.analyze_all(atp_data)

# Check results
print(f"Dominant period: {results['fourier'].dominant_period} hours")
print(f"Stability: {results['laplace'].stability}")
print(f"Noise reduction: {results['z_transform'].noise_reduction_percent}%")
```

## API Reference

### SystemAnalyzer

Main class for three-lens analysis.

**Constructor:**
```python
SystemAnalyzer(sampling_rate: float = 1.0)
```

**Methods:**

- `fourier_lens(time_series)` → FourierResult
- `laplace_lens(time_series)` → LaplaceResult
- `z_transform_lens(time_series)` → ZTransformResult
- `analyze_all(time_series)` → Dict[str, Any]

### Hypervisor Integration

```python
from bioxen_fourier_vm_lib.hypervisor import BioXenHypervisor

hypervisor = BioXenHypervisor()

# Record metrics over time
for hour in range(72):
    hypervisor.record_vm_metric('vm1', atp_value)

# Analyze dynamics
results = hypervisor.analyze_vm('vm1')
```

## Examples

See `examples/mvp_three_lens_demo.py` for complete demonstrations.

## Limitations (MVP)

- **Uniform sampling only**: Requires evenly-spaced measurements
- **2nd order Laplace**: Simplified pole estimation
- **Lowpass filtering only**: Single filter type
- **No visualization**: Text output only

## Next Steps

See `new-prompt-update-execution-model-claude.md` for full production roadmap.
```

**Tasks:**
- [ ] Write user guide
- [ ] Document API
- [ ] Add examples
- [ ] List MVP limitations

**Time Estimate:** 16 hours
- Writing: 10 hours
- Review/editing: 4 hours
- Examples: 2 hours

### Day 10: Integration & Polish (8 hours)

**Tasks:**
- [ ] Update main README with three-lens section
- [ ] Add `analysis` module to package exports
- [ ] Create release notes for MVP
- [ ] Final testing of demo script
- [ ] Prepare demo for stakeholders

**Time Estimate:** 8 hours
- Integration: 3 hours
- Testing: 3 hours
- Documentation: 2 hours

---

## MVP Success Criteria

### Functional Requirements

✅ **Must Have:**
- [ ] SystemAnalyzer class with three working lens methods
- [ ] Fourier lens detects 24h period in synthetic circadian data
- [ ] Laplace lens classifies oscillator as 'oscillatory' or 'stable'
- [ ] Z-transform lens achieves >30% noise reduction
- [ ] Integration point exists in BioXenHypervisor
- [ ] Demo script runs without errors
- [ ] Basic unit tests pass

### Non-Functional Requirements

✅ **Performance:**
- Analysis completes in <5 seconds for 100 data points

✅ **Code Quality:**
- PEP 8 compliant
- Type hints on public methods
- Docstrings on all classes/methods

✅ **Testing:**
- >80% code coverage
- All critical paths tested

---

## MVP Deliverables Checklist

### Code Artifacts
- [ ] `src/bioxen_fourier_vm_lib/analysis/system_analyzer.py`
- [ ] `src/bioxen_fourier_vm_lib/analysis/__init__.py`
- [ ] Updates to `src/bioxen_fourier_vm_lib/hypervisor/core.py`
- [ ] `examples/mvp_three_lens_demo.py`
- [ ] `tests/test_system_analyzer.py`

### Documentation
- [ ] `docs/mvp_three_lens_guide.md`
- [ ] Updated README.md
- [ ] Inline code documentation (docstrings)

### Demo Materials
- [ ] Working demo script
- [ ] Sample output
- [ ] 2-minute demo video/screenshots

---

## Risk Mitigation

### Risk 1: FFT insufficient for real data
**Mitigation:** Document limitation, plan Lomb-Scargle for v2

### Risk 2: Laplace pole estimation inaccurate
**Mitigation:** Use conservative 2nd order approximation, validate on known systems

### Risk 3: Integration breaks existing code
**Mitigation:** Make analysis opt-in, keep existing methods unchanged

### Risk 4: Timeline slip
**Mitigation:** Cut Z-transform if needed (keep Fourier + Laplace as core)

---

## Post-MVP Roadmap

**Week 3-4: Production Polish**
- Implement Lomb-Scargle for irregular sampling
- Add multiple filter types
- Create visualization module

**Week 5-6: Scientific Validation**
- Compare Fourier results vs. MetaCycle
- Validate Laplace against Del Vecchio examples
- Benchmark performance

**Week 7-8: Documentation & Release**
- Write comprehensive user guide
- Create tutorial notebooks
- Publish v0.1.0

---

## Claude Implementation Prompt (Copy-Paste Ready)

```
I need to implement an MVP three-lens system analyzer for the BioXen Fourier VM Library.

GOAL: Working prototype in 2 weeks demonstrating Fourier, Laplace, and Z-transform analysis.

MVP SCOPE:
✅ Basic SystemAnalyzer class with three methods
✅ Standard FFT for Fourier (uniform sampling)
✅ 2nd order Laplace approximation
✅ Simple Butterworth lowpass filter for Z-transform
✅ Integration point in BioXenHypervisor
✅ Demo script showing all three lenses
✅ Basic unit tests

SIMPLIFIED ASSUMPTIONS:
- Uniform sampling (skip Lomb-Scargle for MVP)
- 2nd order system approximation
- Single filter type
- Synthetic test data
- Text output (no plots)

IMPLEMENTATION PRIORITY:
1. SystemAnalyzer core (Day 1-2)
2. Hypervisor integration (Day 3-4)
3. Demo script (Day 5)
4. Unit tests (Day 6-7)
5. Documentation (Day 8-9)
6. Polish (Day 10)

Please implement the SystemAnalyzer class first with these three methods:
- fourier_lens(time_series) using scipy.fft
- laplace_lens(time_series) using scipy.signal.welch for frequency estimation
- z_transform_lens(time_series) using scipy.signal.butter

Each should return a simple dataclass with essential results only.

Code should be production-quality but deliberately simplified for MVP speed.
Include docstrings with examples.
Use type hints.
Keep it under 200 lines total.
```

---

## Summary

**Timeline:** 2 weeks (10 days)  
**Effort:** 80 hours  
**Team:** 1 developer  

**Deliverable:** Working three-lens analyzer demonstrating:
- ✓ 24-hour rhythm detection via Fourier
- ✓ Stability classification via Laplace  
- ✓ Noise filtering via Z-transform

**Philosophy:** Ship early, validate concept, iterate based on feedback.

The MVP proves the value proposition before investing in production-grade implementation.
