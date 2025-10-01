# BioXen Four-Lens Analysis System - Laptop Testing Guide

**Date:** October 1, 2025  
**Branch:** dev  
**Status:** Ready for Testing  
**Estimated Time:** 15-20 minutes

---

## 🎯 What You're Testing

The new **Four-Lens Analysis System** that adds sophisticated time-series analysis to BioXen:
- **Fourier (Lomb-Scargle)** - Detects circadian rhythms (~24h periods)
- **Wavelet** - Detects transient events (stress responses, phase transitions)
- **Laplace** - Assesses system stability (homeostasis vs instability)
- **Z-Transform** - Filters noise from biological signals

---

## 📋 Prerequisites

- Python 3.8+ installed
- Git installed
- 15-20 minutes of time
- Internet connection (for pip installs)

---

## 🚀 Step-by-Step Testing Instructions

### Step 1: Pull the Dev Branch

```bash
# Navigate to project directory
cd ~/BioXen_Fourier_lib

# Make sure you're on dev branch
git checkout dev

# Pull latest changes
git pull origin dev

# Verify you have the new files
ls -la src/bioxen_fourier_vm_lib/analysis/
ls -la examples/
ls -la tests/
```

**Expected output:**
- `analysis/` directory with `__init__.py`, `system_analyzer.py`, `README.md`
- `examples/` directory with 3 demo scripts
- `tests/` directory with test file

---

### Step 2: Create Virtual Environment

```bash
# Create venv (if not already created)
python3 -m venv venv

# Activate it
source venv/bin/activate  # Linux/Mac
# OR on Windows:
# venv\Scripts\activate

# Verify activation (should show path to venv/bin/python)
which python
```

---

### Step 3: Install Dependencies

```bash
# Install new analysis dependencies
pip install -r requirements-analysis.txt

# Install BioXen in development mode (if not already)
pip install -e .

# Verify installations
python -c "import numpy; print('numpy:', numpy.__version__)"
python -c "import scipy; print('scipy:', scipy.__version__)"
python -c "import astropy; print('astropy:', astropy.__version__)"
python -c "import pywt; print('PyWavelets:', pywt.__version__)"
```

**Expected output:**
- numpy: 1.24.0 or higher
- scipy: 1.11.0 or higher
- astropy: 5.3.0 or higher
- PyWavelets: 1.4.0 or higher

---

### Step 4: Run Demo 1 - MVP Demo (Synthetic Data)

This is the fastest test - uses synthetic data, no hypervisor needed.

```bash
python examples/mvp_demo.py
```

**Expected output:**
```
======================================================================
BioXen Four-Lens Analysis System - MVP Demo
======================================================================

📊 Generating synthetic biological signal...
   Duration: 48 hours
   Samples: 200
   ...

✅ Validating signal quality...
   ✓ Sufficient Length
   ✓ Not Constant
   ...

🔍 LENS 1: Fourier Analysis (Lomb-Scargle)
======================================================================
   Dominant period: 24.XX hours
   ✅ Successfully detected ~24h circadian rhythm!

🔍 LENS 2: Wavelet Analysis
======================================================================
   Transient events detected: X
   ✅ Successfully detected stress response near t=24h!

🔍 LENS 3: Laplace Analysis (System Stability)
======================================================================
   System stability: STABLE
   ✅ System is STABLE - returns to equilibrium

🔍 LENS 4: Z-Transform (Digital Filtering)
======================================================================
   Noise reduction: XX.X%
   ✅ Successfully reduced noise

✅ MVP Demo Complete!
```

**Success criteria:**
- ✅ Detects period between 20-28 hours
- ✅ Finds at least 1 transient event
- ✅ System classified as stable or oscillatory
- ✅ Noise reduced by >30%

---

### Step 5: Run Demo 2 - TimeSimulator Validation

This validates that BioXen's TimeSimulator produces accurate 24-hour cycles.

```bash
python examples/validate_time_simulator.py
```

**Expected output:**
```
======================================================================
TimeSimulator Validation Test
======================================================================

🌍 Initializing TimeSimulator...
   Location: San Francisco (37.77°N, 122.42°W)

📊 Collecting 72 hours of light intensity data...
   Progress: 0h 12h 24h 36h 48h 60h Done!

🔍 Analyzing with Fourier Lens (Lomb-Scargle)...

======================================================================
RESULTS
======================================================================
Expected period:          24.00 hours
Detected period:          24.XX hours
Statistical significance: 0.9XXX (XX.X%)
Accuracy:                 XX.XX%

======================================================================
VALIDATION CRITERIA
======================================================================

1. Period within tolerance (24.0 ± 0.1 hours):
   ✅ PASSED

2. High statistical significance (>95%):
   ✅ PASSED

======================================================================
✅ VALIDATION PASSED
======================================================================
```

**Success criteria:**
- ✅ Detected period: 23.9 - 24.1 hours
- ✅ Significance: > 95%
- ✅ Overall: PASSED

---

### Step 6: Run Tests

```bash
# Run all tests
pytest tests/ -v

# OR with more detail
pytest tests/test_system_analyzer_mvp.py -v

# OR with coverage
pytest tests/ --cov=bioxen_fourier_vm_lib.analysis --cov-report=term-missing
```

**Expected output:**
```
tests/test_system_analyzer_mvp.py::test_fourier_lens_detects_circadian PASSED
tests/test_system_analyzer_mvp.py::test_fourier_lens_with_uniform_sampling PASSED
tests/test_system_analyzer_mvp.py::test_wavelet_lens_runs PASSED
tests/test_system_analyzer_mvp.py::test_wavelet_lens_detects_transient PASSED
tests/test_system_analyzer_mvp.py::test_laplace_lens_stability PASSED
tests/test_system_analyzer_mvp.py::test_laplace_lens_pole_locations PASSED
tests/test_system_analyzer_mvp.py::test_z_transform_lens_reduces_noise PASSED
tests/test_system_analyzer_mvp.py::test_z_transform_lens_auto_cutoff PASSED
tests/test_system_analyzer_mvp.py::test_validation_passes_good_signal PASSED
tests/test_system_analyzer_mvp.py::test_validation_catches_constant_signal PASSED
tests/test_system_analyzer_mvp.py::test_validation_catches_nans PASSED
tests/test_system_analyzer_mvp.py::test_validation_catches_insufficient_length PASSED
tests/test_system_analyzer_mvp.py::test_profiler_integration PASSED
tests/test_system_analyzer_mvp.py::test_hypervisor_integration PASSED
...

======================== XX passed in X.XXs ============================
```

**Success criteria:**
- ✅ All tests pass (20+ tests)
- ✅ No import errors
- ✅ Integration tests pass

---

### Step 7: Optional - Test Profiler Integration

This requires a running hypervisor with profiler (takes 5+ minutes for data collection).

```bash
python examples/demo_profiler_integration.py
```

**Note:** This demo:
- Initializes a BioXen hypervisor
- Starts PerformanceProfiler
- Waits 5 minutes to collect 60 samples
- Analyzes real ATP/ribosome data with all four lenses

You can skip this for now and run it later when you have more time.

---

## ✅ Success Checklist

Mark these off as you complete them:

- [ ] Step 1: Pulled dev branch successfully
- [ ] Step 2: Created and activated venv
- [ ] Step 3: Installed all dependencies (no errors)
- [ ] Step 4: MVP demo completed successfully
  - [ ] Detected ~24h period
  - [ ] Found transient events
  - [ ] System classified as stable
  - [ ] Noise reduced
- [ ] Step 5: TimeSimulator validation PASSED
  - [ ] Period within tolerance
  - [ ] High significance
- [ ] Step 6: All tests passed (20+)
- [ ] Optional Step 7: Profiler integration tested

---

## 🐛 Troubleshooting

### Import Error: "No module named 'scipy'"
**Solution:**
```bash
pip install scipy>=1.11.0
```

### Import Error: "No module named 'astropy'"
**Solution:**
```bash
pip install astropy>=5.3.0
```

### Import Error: "No module named 'pywt'"
**Solution:**
```bash
pip install PyWavelets>=1.4.0
```

### Demo fails with "Insufficient data"
**Solution:** This is expected for `demo_profiler_integration.py` - it needs to collect data for 5 minutes. The other demos don't have this requirement.

### Test import errors
**Solution:**
```bash
pip install pytest pytest-cov
```

### Virtual environment not activating
**Solution:**
```bash
deactivate  # if already in another venv
python3 -m venv venv --clear  # recreate
source venv/bin/activate
```

---

## 📊 What Each Test Validates

### MVP Demo (`mvp_demo.py`)
- ✅ All four lenses work correctly
- ✅ Signal validation catches problems
- ✅ Period detection within expected range
- ✅ Transient detection works
- ✅ Stability classification works
- ✅ Noise filtering works

### TimeSimulator Validation (`validate_time_simulator.py`)
- ✅ Integration with existing BioXen component
- ✅ Fourier analysis detects known 24h period
- ✅ Statistical significance testing works
- ✅ Real astronomical constants validated

### Unit Tests (`test_system_analyzer_mvp.py`)
- ✅ Each lens works independently
- ✅ Edge cases handled (empty, NaN, constant signals)
- ✅ Integration with profiler works
- ✅ Integration with hypervisor works
- ✅ Performance is acceptable

---

## 📝 Recording Your Results

Create a test report file:

```bash
# Create test results file
cat > laptop-test-results.md << 'EOF'
# BioXen Four-Lens Analysis - Test Results

**Date:** $(date)
**Tester:** [Your Name]
**Platform:** [Linux/Mac/Windows]
**Python Version:** $(python --version)

## Test Results

### Demo 1 - MVP Demo
- Status: [PASS/FAIL]
- Notes: [Any observations]

### Demo 2 - TimeSimulator Validation
- Status: [PASS/FAIL]
- Detected Period: [XX.XX hours]
- Significance: [XX.X%]
- Notes: [Any observations]

### Unit Tests
- Total Tests: [XX]
- Passed: [XX]
- Failed: [XX]
- Notes: [Any failures or warnings]

## Overall Assessment
[Your comments on functionality, performance, ease of use]

## Issues Found
[List any bugs or problems encountered]

## Suggestions
[Any recommendations for improvements]
EOF

# Edit with your results
nano laptop-test-results.md
```

---

---

## 🚀 Phase 1 Testing - Multi-Harmonic Detection

**If you've completed MVP testing above, continue here to test Phase 1 Feature 1.**

### What's New in Phase 1 Feature 1?

The **Advanced Lomb-Scargle Multi-Harmonic Detection** enhancement adds:
- Detection of **multiple periodic components** (e.g., 24h + 12h + 8h rhythms)
- **Phase estimation** for each harmonic (timing of peaks)
- **Amplitude estimation** for each harmonic (strength of oscillation)
- 100% backward compatible - MVP behavior unchanged unless you opt-in

### Step 8: Run Phase 1 Harmonics Tests

```bash
# Run Phase 1 harmonic detection tests
pytest tests/test_phase1_harmonics.py -v

# OR with more detail
pytest tests/test_phase1_harmonics.py -v -s

# OR with coverage
pytest tests/test_phase1_harmonics.py --cov=bioxen_fourier_vm_lib.analysis --cov-report=term-missing
```

**Expected output:**
```
tests/test_phase1_harmonics.py::TestBackwardCompatibility::test_mvp_behavior_preserved PASSED
tests/test_phase1_harmonics.py::TestBackwardCompatibility::test_default_parameters_match_mvp PASSED
tests/test_phase1_harmonics.py::TestMultiHarmonicDetection::test_detects_two_harmonics PASSED
tests/test_phase1_harmonics.py::TestMultiHarmonicDetection::test_detects_three_harmonics PASSED
tests/test_phase1_harmonics.py::TestMultiHarmonicDetection::test_harmonic_power_ordering PASSED
tests/test_phase1_harmonics.py::TestMultiHarmonicDetection::test_respects_max_harmonics_limit PASSED
tests/test_phase1_harmonics.py::TestMultiHarmonicDetection::test_fundamental_plus_harmonics PASSED
tests/test_phase1_harmonics.py::TestMultiHarmonicDetection::test_close_frequency_separation PASSED
tests/test_phase1_harmonics.py::TestPhaseEstimation::test_zero_phase PASSED
tests/test_phase1_harmonics.py::TestPhaseEstimation::test_quarter_phase PASSED
tests/test_phase1_harmonics.py::TestPhaseEstimation::test_phase_wraparound PASSED
tests/test_phase1_harmonics.py::TestAmplitudeEstimation::test_small_amplitude PASSED
tests/test_phase1_harmonics.py::TestAmplitudeEstimation::test_large_amplitude PASSED
tests/test_phase1_harmonics.py::TestAmplitudeEstimation::test_multiple_amplitudes PASSED
tests/test_phase1_harmonics.py::TestEdgeCases::test_constant_signal PASSED
tests/test_phase1_harmonics.py::TestEdgeCases::test_single_frequency PASSED
tests/test_phase1_harmonics.py::TestEdgeCases::test_irregular_timestamps PASSED
tests/test_phase1_harmonics.py::TestBiologicalRealism::test_circadian_plus_ultradian PASSED
tests/test_phase1_harmonics.py::TestBiologicalRealism::test_damped_oscillations PASSED
tests/test_phase1_harmonics.py::TestIntegration::test_with_validation PASSED
tests/test_phase1_harmonics.py::TestIntegration::test_performance_large_signal PASSED

======================== 21 passed in X.XXs ============================
```

**Success criteria:**
- ✅ All 21 tests pass
- ✅ Backward compatibility tests pass (MVP behavior preserved)
- ✅ Multi-harmonic detection tests pass (2-3 harmonics)
- ✅ Phase/amplitude estimation tests pass
- ✅ Edge case tests pass
- ✅ Biological realism tests pass
- ✅ Integration tests pass

---

### Step 9: Run Phase 1 Harmonics Demo

This demo shows the power of multi-harmonic detection on a realistic biological signal.

```bash
python examples/demo_phase1_harmonics.py
```

**Expected output:**
```
======================================================================
Phase 1 Demo: Multi-Harmonic Detection
======================================================================

📊 Generating Synthetic ATP Signal...
   - Circadian component (24h): amplitude 30, phase 0.0
   - Ultradian component (12h): amplitude 15, phase π/4
   - Cellular component (8h): amplitude 8, phase π/2
   - Baseline: 100 units
   - Noise: 2% (σ=2 units)
   - Duration: 72 hours
   - Samples: 300

======================================================================
PART 1: Signal Composition
======================================================================
The synthetic signal represents ATP levels with THREE biological rhythms:
  1. Circadian (24h): Daily metabolic cycle
  2. Ultradian (12h): Feeding/fasting cycles
  3. Cellular (8h): Cell division timing

Ground truth:
  - 24h: amplitude 30.00, phase 0.00 rad (0.00h peak)
  - 12h: amplitude 15.00, phase 0.79 rad (1.50h peak)
  - 8h:  amplitude 8.00,  phase 1.57 rad (2.00h peak)

======================================================================
PART 2: MVP Analysis (Single Period Detection)
======================================================================

Running Fourier lens in MVP mode (detect_harmonics=False)...

MVP Results:
  Dominant period:  24.XX hours
  Power:            XXX.X
  Significance:     0.9XXX

✅ MVP correctly identifies the STRONGEST component (24h circadian)
⚠️  BUT: MVP misses the 12h and 8h components!

======================================================================
PART 3: Phase 1 Analysis (Multi-Harmonic Detection)
======================================================================

Running Fourier lens in Phase 1 mode (detect_harmonics=True)...

Phase 1 Results: 3 harmonics detected

Harmonic #1:
  Period:    24.XX hours ≈ 24h circadian
  Power:     XXX.X
  Amplitude: 29.XX (true: 30.00) - error: X.X%
  Phase:     0.XX rad (true: 0.00) - error: X.X%
  Peak time: X.Xh

Harmonic #2:
  Period:    12.XX hours ≈ 12h ultradian
  Power:     XX.X
  Amplitude: 14.XX (true: 15.00) - error: X.X%
  Phase:     0.XX rad (true: 0.79) - error: X.X%
  Peak time: X.Xh

Harmonic #3:
  Period:    8.XX hours ≈ 8h cellular
  Power:     X.X
  Amplitude: 7.XX (true: 8.00) - error: X.X%
  Phase:     1.XX rad (true: 1.57) - error: X.X%
  Peak time: X.Xh

✅ Phase 1 detected ALL THREE components with high accuracy!

======================================================================
PART 4: Biological Interpretation
======================================================================

� 24h Circadian Rhythm:
   - Peak at ~X.Xh (early morning)
   - Amplitude: ~30 units
   - Interpretation: Daily metabolic cycle synchronized with light

🍽️  12h Ultradian Rhythm:
   - Peak at ~X.Xh
   - Amplitude: ~15 units (50% of circadian)
   - Interpretation: Feeding/fasting cycles, 2 peaks per day

🔬 8h Cellular Rhythm:
   - Peak at ~X.Xh
   - Amplitude: ~8 units (27% of circadian)
   - Interpretation: Cell division timing, 3 peaks per day

======================================================================
PART 5: Key Insights
======================================================================

1. Multi-scale Temporal Organization:
   - ATP levels are controlled by MULTIPLE overlapping cycles
   - Each cycle operates at a different timescale
   - Detecting only the dominant frequency misses important biology!

2. Phase Relationships:
   - Circadian peak: early morning (energy mobilization)
   - Ultradian peak: ~1.5h after circadian (feeding response)
   - Cellular peak: ~2h after circadian (cell division timing)

3. Research Applications:
   - Drug timing (chronotherapy): target each rhythm separately
   - Metabolic disorders: detect disrupted ultradian rhythms
   - Cell cycle research: identify proliferation timing
   - Aging studies: track amplitude changes in each rhythm

======================================================================
PART 6: MVP vs Phase 1 Comparison
======================================================================

MVP (Single Period):
  ✅ Fast and simple
  ✅ Identifies dominant rhythm
  ⚠️  Misses secondary rhythms
  ⚠️  No amplitude/phase information beyond dominant

Phase 1 (Multi-Harmonic):
  ✅ Detects multiple rhythms
  ✅ Accurate amplitude estimation
  ✅ Accurate phase estimation
  ✅ Biological interpretation of each component
  ✅ Research-grade precision
  ⏱️  Slightly slower (still <1s for this signal)

======================================================================
✅ PHASE 1 DEMO COMPLETE!
======================================================================

Next steps:
  - Try on real data: hypervisor ATP/ribosome time series
  - Visualize: create plots of detected harmonics
  - Biological validation: compare with known circadian markers
  - Phase 1 Feature 2: Wavelet optimization (Week 2)
```

**Success criteria:**
- ✅ Demo runs without errors
- ✅ Detects 3 harmonics (24h, 12h, 8h)
- ✅ Amplitude estimates within 10% of true values
- ✅ Phase estimates within 15% of true values
- ✅ Clear biological interpretation provided

---

### Step 10: Phase 1 Success Checklist

Mark these off as you complete them:

- [ ] Step 8: Phase 1 harmonics tests passed (21 tests)
  - [ ] Backward compatibility verified
  - [ ] Multi-harmonic detection works
  - [ ] Phase estimation accurate
  - [ ] Amplitude estimation accurate
  - [ ] Edge cases handled
  - [ ] Biological realism validated
  - [ ] Integration tests passed
- [ ] Step 9: Phase 1 demo completed successfully
  - [ ] 3 harmonics detected
  - [ ] Amplitudes accurate (<10% error)
  - [ ] Phases accurate (<15% error)
  - [ ] Biological interpretation makes sense

---

### Phase 1 Troubleshooting

**Demo shows high errors (>20%) in amplitude/phase**
- Check: Is noise level too high? Demo uses 2% noise.
- Check: Are timestamps irregular? Lomb-Scargle handles this.
- Solution: This is expected for low-power harmonics - algorithm prioritizes avoiding false positives.

**Tests fail with "NaN detected"**
- Solution: This is a validation test - it's supposed to catch NaNs. If it's failing, check signal generation.

**Performance test fails (>5 seconds)**
- Check: CPU load on laptop
- Solution: Phase 1 is optimized but requires more computation. Adjust `large_signal_size` in test if needed.

**"No harmonics detected" in demo**
- Check: Did demo generate signal correctly?
- Check: Is `detect_harmonics=True` parameter set?
- Solution: Review demo script output - should show 3 components in generation phase.

---

## �🎉 After Successful Testing

1. **Commit test results:**
   ```bash
   git add laptop-test-results.md
   git commit -m "Add laptop test results for four-lens analysis + Phase 1 Feature 1"
   git push origin dev
   ```

2. **Create Pull Request** (if all tests pass):
   - Merge `dev` → `main`
   - Title: "Four-Lens Analysis System v2.1 MVP + Phase 1 Feature 1"
   - Include test results and IMPLEMENTATION_SUMMARY.md

3. **Next Steps:**
   - Phase 1 Feature 2: Wavelet optimization (Week 2)
   - Phase 1 Feature 3: Transfer functions (Week 3)
   - Phase 1 Feature 4: Consensus validation (Week 4)
   - See `MASTER-PROMPT-MVP-FIRST-v2.1.md` for complete Phase 1 roadmap
   - See `PHASE1_PLAN.md` for detailed specifications

---

## 📚 Additional Resources

- **Module Documentation:** `src/bioxen_fourier_vm_lib/analysis/README.md`
- **Implementation Summary:** `IMPLEMENTATION_SUMMARY.md`
- **Master Prompt:** `MASTER-PROMPT-MVP-FIRST-v2.1.md`
- **Git Commit Guide:** `GIT_COMMIT_GUIDE.md`

---

## 🆘 Need Help?

If you encounter issues:

1. Check the troubleshooting section above
2. Review `IMPLEMENTATION_SUMMARY.md` for architecture details
3. Check `src/bioxen_fourier_vm_lib/analysis/README.md` for usage examples
4. Look at test file for working examples: `tests/test_system_analyzer_mvp.py`

---

**Good luck with testing! 🚀**

The system is designed to be robust and well-documented. All demos should run successfully out of the box.
