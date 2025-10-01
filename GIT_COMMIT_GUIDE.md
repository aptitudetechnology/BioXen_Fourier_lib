# BioXen Four-Lens Analysis System - Git Commit Guide

## Files to Add to Git

Run these commands to stage all new files:

```bash
# Stage new analysis module
git add src/bioxen_fourier_vm_lib/analysis/

# Stage modified files
git add src/bioxen_fourier_vm_lib/monitoring/profiler.py
git add src/bioxen_fourier_vm_lib/hypervisor/core.py

# Stage demo scripts
git add examples/

# Stage tests
git add tests/

# Stage documentation
git add requirements-analysis.txt
git add IMPLEMENTATION_SUMMARY.md
git add GIT_COMMIT_GUIDE.md

# Check status
git status
```

## Suggested Commit Message

```bash
git commit -m "Add four-lens analysis system (v2.1 MVP)

Implement sophisticated time-series analysis for biological VM signals
using four complementary mathematical lenses:

New Features:
- SystemAnalyzer: Fourier, Wavelet, Laplace, Z-Transform analysis
- PerformanceProfiler integration: Auto-creates analyzer, adds 6 analysis methods
- BioXenHypervisor API: enable_performance_analysis(), analyze_system_dynamics()
- 3 demo scripts: MVP demo, TimeSimulator validation, profiler integration
- Comprehensive test suite: 20+ tests covering all lenses and integrations

Implementation Details:
- system_analyzer.py: ~650 lines implementing all four lenses
- profiler.py: +180 lines for analysis integration
- core.py: +150 lines for hypervisor API
- Demo scripts: ~730 lines total
- Test suite: ~400 lines with pytest

Dependencies Added:
- scipy>=1.11.0 (signal processing, Welch's method)
- astropy>=5.3.0 (Lomb-Scargle periodogram)
- PyWavelets>=1.4.0 (continuous wavelet transform)

Scientific Rationale:
- Lomb-Scargle: Gold standard for irregular biological sampling
- Wavelets: Essential for non-stationary biological signals
- Laplace: Reveals system stability via pole locations
- Z-Transform: Noise reduction with Butterworth filter

Integration Points:
1. PerformanceProfiler (primary): Analyzes real metrics (ATP, ribosomes)
2. BioXenHypervisor (API): High-level analysis interface
3. Standalone: SystemAnalyzer works with any numpy arrays

Ready for Testing:
- Create venv: python -m venv venv && source venv/bin/activate
- Install deps: pip install -r requirements-analysis.txt
- Run demos: python examples/mvp_demo.py
- Run tests: pytest tests/ -v

Status: ✅ Code complete, ready for validation
Follows: MASTER-PROMPT-MVP-FIRST-v2.1.md
Next: User testing, then Phase 1 enhancements"
```

## Files Modified

### New Files Created
```
src/bioxen_fourier_vm_lib/analysis/__init__.py          (35 lines)
src/bioxen_fourier_vm_lib/analysis/system_analyzer.py   (650 lines)
src/bioxen_fourier_vm_lib/analysis/README.md            (400 lines)
examples/mvp_demo.py                                     (280 lines)
examples/validate_time_simulator.py                     (180 lines)
examples/demo_profiler_integration.py                   (270 lines)
tests/test_system_analyzer_mvp.py                       (400 lines)
requirements-analysis.txt                                (18 lines)
IMPLEMENTATION_SUMMARY.md                                (400 lines)
GIT_COMMIT_GUIDE.md                                      (this file)
```

### Files Modified
```
src/bioxen_fourier_vm_lib/monitoring/profiler.py        (+180 lines)
src/bioxen_fourier_vm_lib/hypervisor/core.py           (+150 lines)
```

## Total Code Added
- **New code:** ~2,510 lines
- **Modified code:** ~330 lines  
- **Total:** ~2,840 lines
- **External library code leveraged:** ~500,000+ lines

## Quick Verification

Before committing, verify:
1. ✅ All demo scripts have proper imports
2. ✅ Test file uses pytest framework
3. ✅ Integration code added to profiler.py and core.py
4. ✅ Documentation complete (README, summary, requirements)
5. ✅ Following master prompt v2.1 specifications

## After Commit

Push to remote:
```bash
git push origin dev
```

Then user can:
1. Pull dev branch on laptop
2. Create venv
3. Install requirements-analysis.txt
4. Run demos and tests
5. Validate functionality
6. Merge to main when validated
