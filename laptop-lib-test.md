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

## 🎉 After Successful Testing

1. **Commit test results:**
   ```bash
   git add laptop-test-results.md
   git commit -m "Add laptop test results for four-lens analysis"
   git push origin dev
   ```

2. **Create Pull Request** (if all tests pass):
   - Merge `dev` → `main`
   - Title: "Four-Lens Analysis System v2.1 MVP"
   - Include test results and IMPLEMENTATION_SUMMARY.md

3. **Next Steps:**
   - Phase 1: Add visualization (matplotlib plots)
   - Phase 1: Enhanced Lomb-Scargle features
   - Phase 1: Advanced wavelet detection
   - See `MASTER-PROMPT-MVP-FIRST-v2.1.md` for roadmap

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
