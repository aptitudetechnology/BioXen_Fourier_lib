# Phase 1.5 MRA Testing Procedure - Laptop Validation
**Date:** October 1, 2025  
**Feature:** Multi-Resolution Analysis (MRA) Implementation  
**Environment:** Local Laptop Testing  
**Status:** Ready for Execution  

## 🎯 Testing Objectives

Validate that the Phase 1.5 Multi-Resolution Analysis (MRA) implementation works correctly on the laptop environment before deployment. This testing ensures:

- ✅ All MRA functionality works as designed
- ✅ Integration with existing features is seamless  
- ✅ Performance meets requirements
- ✅ Edge cases are handled properly
- ✅ Real biological data can be processed

## 📋 Pre-Test Setup

### 1. Environment Verification
```bash
# Verify Python environment
python --version  # Should be 3.8+

# Check required packages
python -c "import numpy; print('NumPy:', numpy.__version__)"
python -c "import pywt; print('PyWavelets:', pywt.__version__)"
python -c "import pytest; print('Pytest:', pytest.__version__)"

# Verify BioXen installation
python -c "from src.bioxen_fourier_vm_lib.analysis.system_analyzer import SystemAnalyzer; print('BioXen MRA: Ready')"
```

**Expected Output:**
- Python 3.8+ ✅
- NumPy 1.20+ ✅  
- PyWavelets 1.1+ ✅
- Pytest 6.0+ ✅
- BioXen import successful ✅

### 2. File Structure Check
```bash
# Verify all MRA files are present
ls -la src/bioxen_fourier_vm_lib/analysis/system_analyzer.py
ls -la tests/test_phase1_mra.py  
ls -la examples/demo_phase1_mra.py
ls -la PHASE1_5_MRA_COMPLETE.md
```

**Expected Output:** All files present ✅

---

## 🧪 Test Execution Plan

### TEST PHASE 1: Unit Test Validation ⚡ CRITICAL

Run the comprehensive MRA test suite to validate all functionality.

#### Command:
```bash
cd /home/chris/BioXen_Fourier_lib
python -m pytest tests/test_phase1_mra.py -v --tb=short
```

#### Expected Results:
```
tests/test_phase1_mra.py::TestBackwardCompatibility::test_mra_disabled_by_default PASSED
tests/test_phase1_mra.py::TestBackwardCompatibility::test_existing_functionality_unchanged PASSED
tests/test_phase1_mra.py::TestMRADecomposition::test_basic_decomposition PASSED
tests/test_phase1_mra.py::TestMRADecomposition::test_component_reconstruction PASSED
tests/test_phase1_mra.py::TestMRADecomposition::test_reconstruction_accuracy PASSED
tests/test_phase1_mra.py::TestMRADecomposition::test_wavelet_compatibility PASSED
tests/test_phase1_mra.py::TestDenoising::test_denoising_effectiveness PASSED
tests/test_phase1_mra.py::TestDenoising::test_signal_preservation PASSED
tests/test_phase1_mra.py::TestDenoising::test_noise_reduction_levels PASSED
tests/test_phase1_mra.py::TestEnergyConservation::test_energy_conservation PASSED
tests/test_phase1_mra.py::TestEnergyConservation::test_mra_summary_statistics PASSED
tests/test_phase1_mra.py::TestBiologicalRealism::test_atp_circadian_analysis PASSED
tests/test_phase1_mra.py::TestBiologicalRealism::test_stress_response_detection PASSED
tests/test_phase1_mra.py::TestIntegration::test_auto_selection_with_mra PASSED
tests/test_phase1_mra.py::TestIntegration::test_transient_detection_compatibility PASSED
tests/test_phase1_mra.py::TestIntegration::test_alternative_wavelets_with_mra PASSED
tests/test_phase1_mra.py::TestEdgeCases::test_short_signals PASSED
tests/test_phase1_mra.py::TestEdgeCases::test_constant_signal PASSED
tests/test_phase1_mra.py::TestEdgeCases::test_high_frequency_signal PASSED
tests/test_phase1_mra.py::TestPerformance::test_processing_speed PASSED
tests/test_phase1_mra.py::TestPerformance::test_memory_usage PASSED

========================= 21 PASSED in X.XXs =========================
```

#### Success Criteria:
- ✅ **All 21 tests PASS**
- ✅ **No failures or errors**  
- ✅ **Execution time < 30 seconds**
- ✅ **No memory warnings**

#### If Tests Fail:
1. **Record failure details** in this document
2. **Check Python environment** (versions, packages)
3. **Verify file integrity** (recent changes, syntax)
4. **Run individual failing tests** with `-vv` for details
5. **Report issues** for investigation

---

### TEST PHASE 2: Interactive Demo Validation 🎯 IMPORTANT

Run the interactive demo to validate real-world functionality and user experience.

#### Command:
```bash
python examples/demo_phase1_mra.py
```

#### Expected Demo Flow:
1. **Welcome Screen** with feature overview ✅
2. **Demo 1: Basic MRA** 
   - Signal generation: ATP with circadian + ultradian + noise
   - MRA decomposition into 6 components  
   - Energy distribution analysis
   - Denoising results showing 50-80% noise reduction
   - Signal preservation >95% correlation

3. **Demo 2: Denoising**
   - Multiple noise levels (2, 5, 10, 15 units)
   - SNR improvement across all levels
   - Detailed moderate noise example
   - Correlation improvements

4. **Demo 3: Stress Detection** 
   - Stress response signal generation
   - Component analysis identifying stress events
   - Peak detection accuracy within ±1 hour
   - Stress vs normal variation separation

5. **Demo 4: Mode Comparison**
   - MVP vs Phase 1 vs Phase 1.5 feature comparison
   - Capability progression demonstration
   - Usage recommendations

#### Success Criteria:
- ✅ **All 4 demos complete without errors**
- ✅ **Realistic biological signals generated**
- ✅ **MRA components show expected energy distribution**
- ✅ **Denoising achieves target performance**
- ✅ **Stress detection works accurately**
- ✅ **Mode comparisons show clear progression**

#### User Interaction Points:
- Press Enter between each demo section
- Review output for biological realism
- Verify numerical results make sense
- Note any unexpected behavior

---

### TEST PHASE 3: Integration Testing 🔧 CRITICAL

Verify MRA integrates properly with existing BioXen functionality.

#### Test 3A: Auto-Selection + MRA
```python
# Create test script: test_integration.py
from src.bioxen_fourier_vm_lib.analysis.system_analyzer import SystemAnalyzer
import numpy as np

# Generate test signal
t = np.linspace(0, 48, 200)
signal = 100 + 20*np.sin(2*np.pi*t/24) + 5*np.random.randn(len(t))

analyzer = SystemAnalyzer(sampling_rate=1.0)

# Test auto-selection + MRA
result = analyzer.wavelet_lens(signal, auto_select=True, enable_mra=True)

print(f"Auto-selected wavelet: {result.wavelet_used}")
print(f"Selection score: {result.selection_score['total_score']:.3f}")
print(f"MRA components: {len(result.mra_components)}")
print(f"Reconstruction error: {result.reconstruction_error:.4f}")
print("✅ Integration test passed!")
```

#### Expected Output:
```
Auto-selected wavelet: db4 (or similar optimal choice)
Selection score: >0.7
MRA components: 6 (approximation + 5 details)
Reconstruction error: <0.001
✅ Integration test passed!
```

#### Test 3B: Backward Compatibility
```python
# Test existing functionality unchanged
result_old = analyzer.wavelet_lens(signal, wavelet_name='morl')
result_new = analyzer.wavelet_lens(signal, wavelet_name='morl', enable_mra=False)

# Should be identical
assert result_old.wavelet_used == result_new.wavelet_used
assert len(result_old.transient_events) == len(result_new.transient_events)
assert result_old.mra_components is None
assert result_new.mra_components is None
print("✅ Backward compatibility confirmed!")
```

---

### TEST PHASE 4: Performance Validation ⚡ IMPORTANT

Verify MRA performance meets requirements across different signal sizes.

#### Performance Test Script:
```python
# Create performance_test.py
import time
import numpy as np
from src.bioxen_fourier_vm_lib.analysis.system_analyzer import SystemAnalyzer

analyzer = SystemAnalyzer(sampling_rate=1.0)

# Test different signal sizes
sizes = [100, 500, 1000, 2000, 5000]
print("Signal Size | Time (ms) | Memory OK | Result")
print("-" * 45)

for size in sizes:
    signal = np.random.randn(size)
    
    start_time = time.time()
    result = analyzer.wavelet_lens(signal, auto_select=True, enable_mra=True)
    end_time = time.time()
    
    duration_ms = (end_time - start_time) * 1000
    memory_ok = len(result.mra_components['approximation']) == size
    success = result.reconstruction_error < 0.01
    
    status = "✅" if (duration_ms < 1000 and memory_ok and success) else "❌"
    print(f"{size:>11} | {duration_ms:>8.1f} | {memory_ok:>9} | {status}")
```

#### Expected Performance:
- **100 samples**: <50ms ✅
- **500 samples**: <100ms ✅  
- **1000 samples**: <200ms ✅
- **2000 samples**: <400ms ✅
- **5000 samples**: <800ms ✅

#### Success Criteria:
- ✅ **All tests complete in <1000ms**
- ✅ **Memory usage scales linearly**
- ✅ **Reconstruction error <0.01 for all sizes**
- ✅ **No memory leaks or crashes**

---

### TEST PHASE 5: Real Data Validation 🧬 VALIDATION

Test MRA on realistic biological data scenarios.

#### Test 5A: Simulated Real ATP Data
```python
# realistic_data_test.py
import numpy as np
from src.bioxen_fourier_vm_lib.analysis.system_analyzer import SystemAnalyzer

# Simulate realistic ATP measurements
np.random.seed(42)  # Reproducible results
t = np.linspace(0, 96, 400)  # 96 hours, 400 samples

# Realistic ATP profile
baseline = 85 + 5*np.sin(2*np.pi*t/168)        # Weekly variation
circadian = 25*np.sin(2*np.pi*t/24 + np.pi/6)  # Circadian with phase
ultradian = 8*np.sin(2*np.pi*t/12)             # 12h ultradian
stress = np.zeros(len(t))
stress[200:220] = 30 * np.exp(-0.1*np.arange(20))  # Stress at t=48h
measurement_noise = 4 * np.random.randn(len(t))

atp_real = baseline + circadian + ultradian + stress + measurement_noise

analyzer = SystemAnalyzer(sampling_rate=1.0)
result = analyzer.wavelet_lens(atp_real, auto_select=True, enable_mra=True, mra_levels=6)

# Validate results
print(f"Dataset: 96h ATP with stress event")
print(f"Optimal wavelet: {result.wavelet_used}")
print(f"Reconstruction error: {result.reconstruction_error:.4f}")

# Check energy distribution
summary = analyzer.get_mra_summary(result.mra_components)
for component, stats in summary.items():
    if stats['energy'] > 5:
        print(f"{component}: {stats['energy']:.1f}% energy")

# Noise reduction check
correlation = np.corrcoef(atp_real, result.denoised_signal)[0,1]
print(f"Signal preservation: {correlation:.3f}")
print("✅ Real data test successful!")
```

#### Success Criteria:
- ✅ **Reconstruction error <0.005**
- ✅ **Circadian component identified (>15% energy)**
- ✅ **Stress event preserved in denoised signal**
- ✅ **Signal preservation >0.95 correlation**

---

## 📊 Test Results Documentation

### Test Execution Log

**Date Tested:** _______________  
**Environment:** _______________  
**Python Version:** _______________  

| Test Phase | Status | Duration | Notes |
|------------|--------|----------|--------|
| Unit Tests (21 tests) | ⬜ PASS / ⬜ FAIL | _____ | _________________________ |
| Demo Validation | ⬜ PASS / ⬜ FAIL | _____ | _________________________ |
| Integration Tests | ⬜ PASS / ⬜ FAIL | _____ | _________________________ |
| Performance Tests | ⬜ PASS / ⬜ FAIL | _____ | _________________________ |
| Real Data Tests | ⬜ PASS / ⬜ FAIL | _____ | _________________________ |

### Performance Metrics Achieved

| Signal Size | Processing Time | Memory Usage | Status |
|-------------|----------------|--------------|---------|
| 100 samples | _____ ms | _____ MB | ⬜ ✅ / ⬜ ❌ |
| 500 samples | _____ ms | _____ MB | ⬜ ✅ / ⬜ ❌ |
| 1000 samples | _____ ms | _____ MB | ⬜ ✅ / ⬜ ❌ |
| 2000 samples | _____ ms | _____ MB | ⬜ ✅ / ⬜ ❌ |
| 5000 samples | _____ ms | _____ MB | ⬜ ✅ / ⬜ ❌ |

### Key Functionality Validation

| Feature | Expected Result | Actual Result | Status |
|---------|----------------|---------------|---------|
| Signal Decomposition | 6 components (1 approx + 5 detail) | _____ | ⬜ ✅ / ⬜ ❌ |
| Reconstruction Error | <0.001 for synthetic signals | _____ | ⬜ ✅ / ⬜ ❌ |
| Noise Reduction | 50-80% noise removal | _____% | ⬜ ✅ / ⬜ ❌ |
| Signal Preservation | >95% correlation | _____% | ⬜ ✅ / ⬜ ❌ |
| Auto-Selection + MRA | Optimal wavelet works | _____ | ⬜ ✅ / ⬜ ❌ |
| Backward Compatibility | No breaking changes | _____ | ⬜ ✅ / ⬜ ❌ |

---

## 🚨 Troubleshooting Guide

### Common Issues & Solutions

#### Issue 1: Import Errors
**Symptom:** `ImportError: cannot import name 'SystemAnalyzer'`
**Solution:**
```bash
# Check PYTHONPATH
echo $PYTHONPATH
export PYTHONPATH="/home/chris/BioXen_Fourier_lib:$PYTHONPATH"

# Or run from project root
cd /home/chris/BioXen_Fourier_lib
python -m pytest tests/test_phase1_mra.py
```

#### Issue 2: PyWavelets Missing
**Symptom:** `ModuleNotFoundError: No module named 'pywt'`
**Solution:**
```bash
pip install PyWavelets>=1.1.0
```

#### Issue 3: Test Failures
**Symptom:** Tests fail with numerical errors
**Solution:**
```bash
# Run specific failing test with verbose output
python -m pytest tests/test_phase1_mra.py::TestMRADecomposition::test_reconstruction_accuracy -vv

# Check numpy/pywt versions
python -c "import numpy; import pywt; print(f'NumPy: {numpy.__version__}, PyWavelets: {pywt.__version__}')"
```

#### Issue 4: Performance Issues  
**Symptom:** Tests run very slowly (>30s)
**Solution:**
- Check available memory
- Close other applications
- Use smaller test signals initially

#### Issue 5: Demo Crashes
**Symptom:** Demo script exits with error
**Solution:**
```bash
# Run with error handling
python examples/demo_phase1_mra.py 2>&1 | tee demo_log.txt

# Check specific error location
python -c "
import sys; sys.path.insert(0, 'src')
from bioxen_fourier_vm_lib.analysis.system_analyzer import SystemAnalyzer
analyzer = SystemAnalyzer(sampling_rate=1.0)
print('Basic import works')
"
```

---

## ✅ Test Completion Checklist

### Before Testing:
- ⬜ Environment setup complete
- ⬜ All files present and verified
- ⬜ Dependencies installed
- ⬜ Project path configured

### During Testing:
- ⬜ Unit tests executed and documented
- ⬜ Interactive demo completed
- ⬜ Integration tests passed
- ⬜ Performance benchmarks recorded
- ⬜ Real data scenarios validated

### After Testing:
- ⬜ All test results documented
- ⬜ Performance metrics recorded  
- ⬜ Issues identified and noted
- ⬜ Success criteria met or deviations explained
- ⬜ Next steps determined

### Sign-Off:
- ⬜ **Phase 1.5 MRA implementation VALIDATED** ✅
- ⬜ **Ready for production use** ✅
- ⬜ **Documentation updated** ✅
- ⬜ **Ready to proceed to Phase 1 Week 3** ✅

---

## 📝 Final Notes

**Testing Completed By:** _______________  
**Date:** _______________  
**Overall Status:** ⬜ ✅ PASS - Ready for Week 3 / ⬜ ❌ ISSUES - Needs fixes  

**Summary Comments:**
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

**Recommendation:**
⬜ Proceed to Phase 1 Week 3 (Transfer Functions)  
⬜ Address issues first, then retest  
⬜ Additional validation needed  

---

**This comprehensive testing procedure ensures Phase 1.5 MRA is fully validated and ready for research use! 🚀**