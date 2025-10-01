# Week 2 Testing Procedure - Wavelet Optimization

**Date:** October 1, 2025  
**Feature:** Phase 1 Feature 2 - Automatic Wavelet Selection  
**Branch:** dev  
**Estimated Time:** 10-15 minutes

---

## 🎯 What You're Testing

**Phase 1 Feature 2: Automatic Wavelet Selection**

This feature adds AI-powered wavelet selection to the BioXen Four-Lens Analysis System. The system now automatically picks the best wavelet transform for any biological signal.

**Key Capabilities:**
- Tests 7 different wavelets automatically
- Calculates 4 quality metrics for each
- Selects optimal wavelet based on weighted scoring
- Provides transparent reasoning (all scores visible)
- Lists alternative wavelets for exploration
- 100% backward compatible with MVP

---

## 📋 Prerequisites

Before you start, make sure you've completed:
- ✅ MVP testing (Steps 1-7 from main testing guide)
- ✅ Phase 1 Feature 1 testing (Steps 8-10)
- ✅ Virtual environment activated
- ✅ All dependencies installed

If not, run:
```bash
cd ~/BioXen_Fourier_lib
source venv/bin/activate
pip install -e .
```

---

## 🚀 Testing Procedure

### Step 1: Verify Environment

```bash
# Confirm you're in the right directory
pwd
# Should show: /home/chris/BioXen_Fourier_lib

# Confirm venv is active
which python
# Should show: .../BioXen_Fourier_lib/venv/bin/python

# Verify PyWavelets is installed
python -c "import pywt; print('PyWavelets version:', pywt.__version__)"
# Should show: PyWavelets version: 1.4.0 or higher
```

**Success Criteria:**
- ✅ In correct directory
- ✅ Virtual environment active
- ✅ PyWavelets installed

---

### Step 2: Run Week 2 Tests

Run the comprehensive test suite for wavelet optimization:

```bash
pytest tests/test_phase1_wavelet_optimization.py -v
```

**Expected Output:**
```
======================== test session starts =========================
platform linux -- Python 3.X.X, pytest-X.X.X, ...
collected 21 items

tests/test_phase1_wavelet_optimization.py::TestBackwardCompatibility::test_mvp_behavior_preserved PASSED [  4%]
tests/test_phase1_wavelet_optimization.py::TestBackwardCompatibility::test_default_parameters_no_breaking_changes PASSED [  9%]
tests/test_phase1_wavelet_optimization.py::TestAutomaticWaveletSelection::test_auto_select_picks_wavelet PASSED [ 14%]
tests/test_phase1_wavelet_optimization.py::TestAutomaticWaveletSelection::test_alternatives_provided PASSED [ 19%]
tests/test_phase1_wavelet_optimization.py::TestAutomaticWaveletSelection::test_auto_select_overrides_wavelet_name PASSED [ 23%]
tests/test_phase1_wavelet_optimization.py::TestSelectionMetrics::test_energy_concentration_metric PASSED [ 28%]
tests/test_phase1_wavelet_optimization.py::TestSelectionMetrics::test_time_localization_metric PASSED [ 33%]
tests/test_phase1_wavelet_optimization.py::TestSelectionMetrics::test_frequency_localization_metric PASSED [ 38%]
tests/test_phase1_wavelet_optimization.py::TestSelectionMetrics::test_edge_quality_metric PASSED [ 42%]
tests/test_phase1_wavelet_optimization.py::TestSignalTypeMatching::test_smooth_oscillation_prefers_morlet_or_mexh PASSED [ 47%]
tests/test_phase1_wavelet_optimization.py::TestSignalTypeMatching::test_sharp_transient_selection PASSED [ 52%]
tests/test_phase1_wavelet_optimization.py::TestEdgeCases::test_constant_signal PASSED [ 57%]
tests/test_phase1_wavelet_optimization.py::TestEdgeCases::test_very_short_signal PASSED [ 61%]
tests/test_phase1_wavelet_optimization.py::TestEdgeCases::test_noisy_signal PASSED [ 66%]
tests/test_phase1_wavelet_optimization.py::TestBiologicalRealism::test_circadian_rhythm_with_noise PASSED [ 71%]
tests/test_phase1_wavelet_optimization.py::TestBiologicalRealism::test_stress_response_signal PASSED [ 76%]
tests/test_phase1_wavelet_optimization.py::TestIntegration::test_works_with_validation PASSED [ 80%]
tests/test_phase1_wavelet_optimization.py::TestIntegration::test_consistent_results PASSED [ 85%]
tests/test_phase1_wavelet_optimization.py::TestIntegration::test_all_wavelets_available PASSED [ 90%]
tests/test_phase1_wavelet_optimization.py::TestPerformance::test_auto_select_completes_quickly PASSED [ 95%]
tests/test_phase1_wavelet_optimization.py::TestPerformance::test_scales_with_signal_length PASSED [100%]

======================== 21 passed in X.XXs =========================
```

**Success Criteria:**
- ✅ All 21 tests PASSED
- ✅ No FAILED tests
- ✅ No errors or warnings
- ✅ Completion time < 30 seconds

---

### Step 3: Run Week 2 Demo (Interactive)

Run the interactive demonstration script:

```bash
python examples/demo_phase1_wavelet_optimization.py
```

**What to Expect:**

The demo has **4 parts**. Press Enter to advance through each:

#### Demo 1: Smooth Circadian Oscillation
```
======================================================================
DEMO 1: Smooth Circadian Oscillation (ATP Levels)
======================================================================

[Description of signal...]

MVP Mode: Manual Wavelet Selection
-------------------------------------------------------------------
   Wavelet used: morl
   Transient events detected: X

Phase 1 Mode: Automatic Wavelet Selection
-------------------------------------------------------------------

✅ Optimal wavelet selected: morl (or mexh/gaus4)
   Description: Morlet - Good for smooth oscillations

📊 Selection Scores:
   Total Score:            0.XXX
   Energy Concentration:   0.XXX
   Time Localization:      0.XXX
   Frequency Localization: 0.XXX
   Edge Quality:           0.XXX

🎯 Top 3 Alternative Wavelets:
   1. morl   - Score: 0.XXX - Morlet - Good for smooth oscillations
   2. mexh   - Score: 0.XXX - Mexican Hat - Good for peak detection
   3. gaus4  - Score: 0.XXX - Gaussian 4 - Sharp features, smooth signal
```

**Verify:**
- ✅ Smooth wavelets (morl, mexh, gaus4) are in top 3
- ✅ All scores are between 0.0 and 1.0
- ✅ No errors

Press Enter to continue...

#### Demo 2: Sharp Stress Response
```
======================================================================
DEMO 2: Sharp Stress Response (Heat Shock)
======================================================================

[Description of stress event...]

✅ Optimal wavelet selected: [wavelet name]
   Description: [description]

📊 Selection Scores:
   Total Score:            0.XXX
   Energy Concentration:   0.XXX
   Time Localization:      0.XXX ⭐
   Frequency Localization: 0.XXX
   Edge Quality:           0.XXX

🎯 Transient Events Detected: X
   Event 1: t=36.Xh, intensity=XXX.X, duration=X samples
```

**Verify:**
- ✅ Time Localization score is highlighted (⭐)
- ✅ Stress event detected near t=36h
- ✅ Wavelet appropriate for sharp features
- ✅ No errors

Press Enter to continue...

#### Demo 3: Complex Mixed Signal
```
======================================================================
DEMO 3: Complex Mixed Signal (Cell Cycle + Stress)
======================================================================

[Description of complex signal...]

✅ Optimal wavelet selected: [wavelet name]
   Description: [description]

📊 Selection Scores (Balanced Performance):
   Total Score:            0.XXX
   Energy Concentration:   0.XXX
   Time Localization:      0.XXX
   Frequency Localization: 0.XXX
   Edge Quality:           0.XXX

🎯 Top 5 Alternative Wavelets:
   1. [name] - Score: 0.XXX
   2. [name] - Score: 0.XXX
   3. [name] - Score: 0.XXX
   4. [name] - Score: 0.XXX
   5. [name] - Score: 0.XXX
```

**Verify:**
- ✅ Balanced scores (no single metric dominates)
- ✅ Top 5 alternatives listed
- ✅ Scores decrease as you go down the list
- ✅ No errors

Press Enter to continue...

#### Demo 4: Comparison Across All Wavelets
```
======================================================================
DEMO 4: Comparison Across All Wavelets
======================================================================

Testing all wavelets...

Wavelet    Total    Energy   Time     Freq     Edge     Events  
----------------------------------------------------------------------
morl       0.XXX    0.XXX    0.XXX    0.XXX    0.XXX    X       
mexh       0.XXX    0.XXX    0.XXX    0.XXX    0.XXX    X       
gaus4      0.XXX    0.XXX    0.XXX    0.XXX    0.XXX    X       
db4        0.XXX    0.XXX    0.XXX    0.XXX    0.XXX    X       
db8        0.XXX    0.XXX    0.XXX    0.XXX    0.XXX    X       
sym4       0.XXX    0.XXX    0.XXX    0.XXX    0.XXX    X       
coif2      0.XXX    0.XXX    0.XXX    0.XXX    0.XXX    X       

======================================================================
🏆 Best Wavelet: [wavelet name]
   Total Score: 0.XXX
   Events Detected: X
```

**Verify:**
- ✅ All 7 wavelets tested (morl, mexh, gaus4, db4, db8, sym4, coif2)
- ✅ Table shows all scores
- ✅ Clear winner identified
- ✅ Different wavelets detect different numbers of events
- ✅ No errors

#### Final Summary
```
======================================================================
✅ PHASE 1 FEATURE 2 DEMO COMPLETE!
======================================================================

Summary:
  ✅ Automatic wavelet selection works
  ✅ Different signals get different wavelets
  ✅ Selection metrics provide transparency
  ✅ Alternative wavelets available for exploration
  ✅ Backward compatible (MVP mode still works)
```

**Overall Success Criteria:**
- ✅ All 4 demos completed without errors
- ✅ Different signal types got different optimal wavelets
- ✅ All scores in range [0.0, 1.0]
- ✅ Alternatives properly sorted
- ✅ Clear winner identified in comparison
- ✅ Biological interpretation makes sense

---

### Step 4: Quick Manual Test (Optional but Recommended)

Test the API directly to understand how it works:

```bash
python -c "
import numpy as np
from bioxen_fourier_vm_lib.analysis.system_analyzer import SystemAnalyzer

# Create analyzer
analyzer = SystemAnalyzer(sampling_rate=1.0)

# Generate smooth signal (circadian)
t = np.linspace(0, 48, 200)
signal = 100 + 30*np.sin(2*np.pi*t/24) + 2*np.random.randn(200)

# MVP mode
result_mvp = analyzer.wavelet_lens(signal, wavelet_name='morl')
print(f'MVP mode: {result_mvp.wavelet_used}')

# Phase 1 mode
result_phase1 = analyzer.wavelet_lens(signal, auto_select=True)
print(f'Phase 1 optimal: {result_phase1.wavelet_used}')
print(f'Score: {result_phase1.selection_score[\"total_score\"]:.3f}')
print(f'Top 3 alternatives:')
for name, scores in result_phase1.alternative_wavelets[:3]:
    print(f'  {name}: {scores[\"total_score\"]:.3f}')
"
```

**Expected Output:**
```
MVP mode: morl
Phase 1 optimal: morl (or mexh/gaus4)
Score: 0.XXX
Top 3 alternatives:
  morl: 0.XXX
  mexh: 0.XXX
  gaus4: 0.XXX
```

**Success Criteria:**
- ✅ MVP mode returns 'morl'
- ✅ Phase 1 mode returns valid wavelet
- ✅ Score is between 0.0 and 1.0
- ✅ Alternatives listed and sorted
- ✅ No errors

---

### Step 5: Test with Different Signal Types (Optional)

Verify the system adapts to different signal characteristics:

```bash
python -c "
import numpy as np
from bioxen_fourier_vm_lib.analysis.system_analyzer import SystemAnalyzer

analyzer = SystemAnalyzer(sampling_rate=1.0)

# Test 1: Smooth oscillation
print('Test 1: Smooth oscillation')
t = np.linspace(0, 48, 200)
smooth = 100 + 30*np.sin(2*np.pi*t/24)
result = analyzer.wavelet_lens(smooth, auto_select=True)
print(f'  Optimal: {result.wavelet_used}')
print(f'  Score: {result.selection_score[\"total_score\"]:.3f}')

# Test 2: Sharp spike
print('\nTest 2: Sharp spike')
spike = np.zeros(200)
spike[100] = 100
result = analyzer.wavelet_lens(spike, auto_select=True)
print(f'  Optimal: {result.wavelet_used}')
print(f'  Score: {result.selection_score[\"total_score\"]:.3f}')

# Test 3: Noise
print('\nTest 3: Random noise')
noise = np.random.randn(200)
result = analyzer.wavelet_lens(noise, auto_select=True)
print(f'  Optimal: {result.wavelet_used}')
print(f'  Score: {result.selection_score[\"total_score\"]:.3f}')

print('\n✅ System adapts to different signal types!')
"
```

**Expected Behavior:**
- Smooth signal → Likely gets morl, mexh, or gaus4
- Sharp spike → May get db4, db8, or sym4
- Noise → Gets any valid wavelet (scores may be lower)
- All run without errors

---

## ✅ Test Completion Checklist

Mark these off as you complete them:

- [ ] **Step 1:** Environment verified
  - [ ] Correct directory
  - [ ] Virtual environment active
  - [ ] PyWavelets installed

- [ ] **Step 2:** All 21 tests passed
  - [ ] Backward compatibility tests PASSED
  - [ ] Auto-selection tests PASSED
  - [ ] Metric tests PASSED
  - [ ] Signal matching tests PASSED
  - [ ] Edge case tests PASSED
  - [ ] Biological tests PASSED
  - [ ] Integration tests PASSED
  - [ ] Performance tests PASSED

- [ ] **Step 3:** All 4 demos completed successfully
  - [ ] Demo 1: Smooth oscillation (smooth wavelet selected)
  - [ ] Demo 2: Sharp transient (high time localization)
  - [ ] Demo 3: Complex signal (balanced scores)
  - [ ] Demo 4: Comparison (all 7 wavelets tested)

- [ ] **Step 4:** Manual test passed (optional)
  - [ ] MVP mode works
  - [ ] Phase 1 auto-select works
  - [ ] Scores valid
  - [ ] Alternatives listed

- [ ] **Step 5:** Different signal types tested (optional)
  - [ ] Smooth signals handled
  - [ ] Sharp signals handled
  - [ ] Noisy signals handled

---

## 📊 Expected Results Summary

### Test Results
| Test Category | Tests | Expected Result |
|--------------|-------|-----------------|
| Backward Compatibility | 2 | All PASS |
| Automatic Selection | 4 | All PASS |
| Selection Metrics | 4 | All PASS |
| Signal Type Matching | 2 | All PASS |
| Edge Cases | 3 | All PASS |
| Biological Realism | 2 | All PASS |
| Integration | 3 | All PASS |
| Performance | 2 | All PASS |
| **TOTAL** | **21** | **All PASS** |

### Demo Results
| Demo | Expected Behavior |
|------|-------------------|
| Demo 1 | Smooth wavelet (morl/mexh/gaus4) selected |
| Demo 2 | High time localization score, event detected |
| Demo 3 | Balanced scores across all metrics |
| Demo 4 | All 7 wavelets compared, clear winner |

---

## 🐛 Troubleshooting

### Issue: Import error for PyWavelets
```
ImportError: No module named 'pywt'
```
**Solution:**
```bash
pip install PyWavelets>=1.4.0
```

### Issue: Tests fail with "AttributeError: 'WaveletResult' has no attribute 'wavelet_used'"
**Solution:** You may need to reinstall the package:
```bash
pip install -e . --force-reinstall
```

### Issue: All wavelets get the same score
**Cause:** Signal is too simple (constant or pure noise)  
**Solution:** This is expected behavior. The algorithm will pick the first one alphabetically.

### Issue: Demo is very slow (>5 seconds per test)
**Cause:** Testing 7 wavelets requires computation  
**Solution:** This is normal. If it's >10 seconds, check CPU load.

### Issue: Unexpected wavelet selected
**Cause:** Different signals prefer different wavelets  
**Solution:** Not a bug! Review the selection scores to understand why. The algorithm is working as designed.

### Issue: Some tests are skipped
**Cause:** Missing dependencies or system limitations  
**Solution:** Check error messages. Most tests should run on any system.

---

## 📝 Recording Your Results

Create a results file:

```bash
cat > week2-test-results.md << 'EOF'
# Week 2 Test Results - Wavelet Optimization

**Date:** $(date)
**Tester:** Chris
**Platform:** $(uname -s) $(uname -m)
**Python:** $(python --version)

## Test Results

### Step 2: Unit Tests
- Total Tests: 21
- Passed: __/21
- Failed: __/21
- Time: __ seconds
- Notes: [Any observations]

### Step 3: Demo Tests
- Demo 1 (Smooth): PASS/FAIL - Optimal: ________
- Demo 2 (Sharp): PASS/FAIL - Optimal: ________
- Demo 3 (Complex): PASS/FAIL - Optimal: ________
- Demo 4 (Comparison): PASS/FAIL - Winner: ________
- Notes: [Any observations]

### Step 4: Manual Test (Optional)
- Status: PASS/FAIL
- Notes: [Any observations]

### Step 5: Signal Types (Optional)
- Status: PASS/FAIL
- Notes: [Any observations]

## Overall Assessment
- Feature 2 Working: YES/NO
- Ready for Production: YES/NO
- Comments: [Your assessment]

## Issues Found
[List any bugs or problems]

## Suggestions
[Any recommendations]

EOF

nano week2-test-results.md
```

---

## 🎉 Success Criteria

**Week 2 Feature 2 is SUCCESSFUL if:**

✅ All 21 unit tests pass  
✅ All 4 demos complete without errors  
✅ Different signals get different optimal wavelets  
✅ All scores are in range [0.0, 1.0]  
✅ Alternatives are sorted by score  
✅ MVP mode still works (backward compatible)  
✅ Performance is acceptable (<5s for medium signals)

**If all criteria met:** Week 2 Feature 2 is READY FOR PRODUCTION! 🚀

---

## 📚 Additional Resources

- **Feature Documentation:** `PHASE1_FEATURE2_COMPLETE.md`
- **Main Testing Guide:** `laptop-lib-test.md` (Steps 11-13)
- **Phase 1 Plan:** `PHASE1_PLAN.md`
- **Progress Tracker:** `PHASE1_STATUS.md`
- **Source Code:** `src/bioxen_fourier_vm_lib/analysis/system_analyzer.py`
- **Test Suite:** `tests/test_phase1_wavelet_optimization.py`
- **Demo Script:** `examples/demo_phase1_wavelet_optimization.py`

---

## 🚀 What's Next?

After successful Week 2 testing:

1. **Document your results** in `week2-test-results.md`
2. **Commit and push** your test results (optional)
3. **Try on real biological data** (optional)
4. **Move to Week 3:** Transfer Functions (if ready)

---

## 💡 Key Takeaways

### What You Just Tested:

1. **Intelligence Layer**
   - System automatically picks best wavelet
   - No more manual trial-and-error
   - Saves hours of research time

2. **Transparency**
   - See all 4 metric scores
   - Understand why each wavelet was chosen
   - Explore alternatives

3. **Adaptability**
   - Smooth signals → smooth wavelets
   - Sharp signals → sharp wavelets
   - Complex signals → balanced wavelets
   - Auto-adapts to your data

4. **Quality**
   - 21 comprehensive tests
   - 100% backward compatible
   - Research-grade results
   - Publication-ready

### The Power of Auto-Selection:

**Before:**
```python
# Try wavelet 1
result = analyzer.wavelet_lens(signal, 'morl')
# Check results... not ideal

# Try wavelet 2
result = analyzer.wavelet_lens(signal, 'mexh')
# Check results... better

# Try wavelet 3
result = analyzer.wavelet_lens(signal, 'db4')
# Check results... worse

# ... repeat for 7 wavelets
# Document your choice
# Total time: 2-3 hours
```

**After:**
```python
# One line - system picks best automatically
result = analyzer.wavelet_lens(signal, auto_select=True)
# Total time: 1 second
# See why it was chosen
# Ready for publication
```

---

**Happy Testing! 🧪**

If you encounter any issues, check the Troubleshooting section or refer to the documentation.

Good luck! 🚀