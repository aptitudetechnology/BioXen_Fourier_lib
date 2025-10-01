# Phase 1 Quick Reference Card

```
╔════════════════════════════════════════════════════════════╗
║     BioXen Phase 1 - Quick Reference for Developers       ║
╚════════════════════════════════════════════════════════════╝

📚 DOCUMENTATION FILES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PHASE1_PLAN.md          Complete specification (1050 lines)
PHASE1_DIY_GUIDE.md     Step-by-step implementation guide
PHASE1_SUMMARY.md       Technical overview
PHASE1_STATUS.md        Visual progress tracker

🎯 WEEK 1: ADVANCED LOMB-SCARGLE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FILE TO MODIFY:
└─ src/bioxen_fourier_vm_lib/analysis/system_analyzer.py

METHODS TO ADD (in SystemAnalyzer class):
├─ _detect_harmonics()           ~50 lines
├─ _estimate_phase()              ~20 lines  
├─ _estimate_amplitude()          ~15 lines
└─ _calculate_bootstrap_conf()    ~40 lines (optional)

METHOD TO MODIFY:
└─ fourier_lens()                 Add 2 params, ~30 lines

TEST FILE TO CREATE:
└─ tests/test_phase1_harmonics.py ~200 lines

DEMO TO CREATE:
└─ examples/demo_phase1_harmonics.py ~150 lines

⏱️  ESTIMATED TIME: 10 hours

📝 CODE SNIPPETS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NEW PARAMETERS TO fourier_lens():
───────────────────────────────────────────────────────────
detect_harmonics: bool = False
max_harmonics: int = 5

BEFORE LOMB-SCARGLE (in fourier_lens):
───────────────────────────────────────────────────────────
self._current_signal = time_series.copy()
self._current_timestamps = timestamps.copy()

AFTER FINDING DOMINANT FREQ (in fourier_lens):
───────────────────────────────────────────────────────────
harmonics = None
harmonic_power = None

if detect_harmonics:
    harmonics = self._detect_harmonics(
        ls, frequency, power, max_harmonics
    )
    harmonic_power = sum(h['power'] for h in harmonics)

UPDATE RETURN STATEMENT:
───────────────────────────────────────────────────────────
return FourierResult(
    # ... existing fields ...
    harmonics=harmonics,
    harmonic_power=harmonic_power
)

🧪 TESTING COMMANDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Run Phase 1 tests only
pytest tests/test_phase1_harmonics.py -v

# Run specific test
pytest tests/test_phase1_harmonics.py::test_multi_harmonic_detection -v

# Run with coverage
pytest tests/test_phase1_harmonics.py --cov=src/bioxen_fourier_vm_lib

# Run demo
python examples/demo_phase1_harmonics.py

# Run all tests
pytest tests/ -v

🐛 COMMON ERRORS & FIXES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ERROR: AttributeError: '_current_signal'
FIX: Add to __init__():
     self._current_signal = None
     self._current_timestamps = None

ERROR: LinAlgWarning: Ill-conditioned matrix
FIX: Ensure timestamps in seconds, not hours

ERROR: No harmonics detected
FIX: Lower threshold in _detect_harmonics() to 0.05

ERROR: Tests fail with period outside range
FIX: Check Fourier bug from MVP (timestamp units)

📊 VALIDATION CHECKLIST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

□ Methods compile without syntax errors
□ Tests run without import errors
□ test_single_harmonic_backward_compatibility PASSES
□ test_multi_harmonic_detection PASSES
□ test_phase_estimation PASSES
□ test_amplitude_estimation PASSES
□ test_harmonic_power_calculation PASSES
□ test_max_harmonics_limit PASSES
□ test_noisy_signal_harmonics PASSES
□ Demo script runs successfully
□ Real genome analysis works with harmonics
□ Documentation updated

🎓 KEY CONCEPTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HARMONICS: Integer multiples of fundamental frequency
  Example: 24h → 12h (2x) → 8h (3x) → 6h (4x)

PHASE: When signal peaks occur (0 to 2π radians)
  Example: 0° = midnight, 90° = 6am, 180° = noon

AMPLITUDE: Signal strength (same units as input)
  Example: ATP varies ±30 units around 100

ITERATIVE DETECTION: Subtract dominant → find next
  1. Find 24h (strongest) → subtract → residual
  2. Find 12h (next) → subtract → residual
  3. Continue until noise level

💡 BIOLOGICAL CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

24h CIRCADIAN:
  • Master biological clock
  • Sleep/wake, hormones
  • Most genes show this

12h ULTRADIAN:
  • Metabolic oscillations
  • 2 peaks per day
  • ATP, glucose cycling

8h RHYTHM:
  • Cellular processes
  • 3 peaks per day
  • Less common

PHASE RELATIONSHIPS:
  • Liver peaks 6h after brain
  • Synchronization = health
  • Desynchrony = disease

🔍 WHERE TO GET HELP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CODE REVIEW:      "Review my implementation"
DEBUGGING:        "Test failing with error X"
CLARIFICATION:    "What does X mean?"
BEST PRACTICES:   "Is this the right approach?"
OPTIMIZATION:     "How to make faster?"
TESTING:          "What else to test?"

📞 ASK ME ANYTIME!

🚀 NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 1: Open system_analyzer.py
STEP 2: Add 3 methods (_detect_harmonics, _estimate_phase, _estimate_amplitude)
STEP 3: Modify fourier_lens() method
STEP 4: Create test file
STEP 5: Run tests
STEP 6: Create demo
STEP 7: Validate with real data
STEP 8: Commit and push

START HERE: PHASE1_DIY_GUIDE.md (detailed instructions)

═══════════════════════════════════════════════════════════

Status: Ready to code! 🎯
Support: Full AI assistance available
Timeline: Week 1 = 10 hours
Goal: Multi-harmonic detection working

YOU'VE GOT THIS! 💪

═══════════════════════════════════════════════════════════
```
