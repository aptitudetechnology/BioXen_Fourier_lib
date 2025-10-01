# Fourier Period Bug - Debug Instructions

## Quick Start

Run this on your laptop to diagnose the Fourier period calculation issue:

```bash
cd ~/BioXen_Fourier_lib
source venv/bin/activate  # Make sure venv is active
python debug_fourier.py
```

## What the Debug Script Tests

The script will test **3 scenarios** to identify where the unit conversion breaks:

### Test 1: Timestamps in HOURS
- Passes time values like `0.0, 0.1, 0.2, ... 48.0` (hours)
- Should detect: 24.0 hour period
- This tests if Lomb-Scargle can handle non-second units

### Test 2: Timestamps in SECONDS  
- Passes time values like `0, 360, 720, ... 172800` (seconds)
- Should detect: 24.0 hour period
- This is the **correct** usage per documentation

### Test 3: No Timestamps (Auto-generated)
- Analyzer creates timestamps internally based on sampling rate
- Should detect: 24.0 hour period
- Tests if auto-generation works correctly

### Test 4: TimeSimulator-like Data
- Simulates 72 hours of light intensity (5-min sampling)
- Exactly matches validate_time_simulator.py usage
- Should detect: 24.0 hour period

## Expected Output

```
======================================================================
Fourier Period Calculation Debug
======================================================================

📊 Generated Signal:
   Duration: 48.0 hours
   Samples: 480
   Expected period: 24.0 hours

----------------------------------------------------------------------
TEST 1: Timestamps in HOURS
----------------------------------------------------------------------
...
   Dominant period: XX.XX hours
   Expected: 24.0 hours

----------------------------------------------------------------------
TEST 2: Timestamps in SECONDS
----------------------------------------------------------------------
...
   Dominant period: XX.XX hours  ← Should be ~24.0 hours
   Expected: 24.0 hours

----------------------------------------------------------------------
DIAGNOSIS SUMMARY
----------------------------------------------------------------------
Hours          → XX.XX hours (error: XX.XXh) [✅ or ❌]
Seconds        → XX.XX hours (error: XX.XXh) [✅ or ❌]
None (auto)    → XX.XX hours (error: XX.XXh) [✅ or ❌]

🔍 ROOT CAUSE ANALYSIS:
[Diagnostic message will appear here]
```

## Interpreting Results

### If Test 2 (Seconds) shows 24.0h:
✅ **Lomb-Scargle working correctly**
- Issue is in demo scripts passing wrong timestamp units
- Fix: Ensure all demos convert timestamps to seconds

### If Test 2 (Seconds) shows 0.00h or wrong value:
❌ **Internal calculation issue**
- Problem in `system_analyzer.py` line 254-259
- Need to fix frequency-to-period conversion
- Possible issues:
  - Frequency range too narrow/wide
  - Period calculation formula wrong
  - Unit conversion happening twice

### If Test 3 (Auto) works but Test 2 fails:
⚠️ **Timestamp interpretation issue**
- Lomb-Scargle may not be handling timestamps correctly
- Check timestamp preprocessing

## Likely Fixes

Based on results, you'll need to fix ONE of these:

### Fix A: Demo Script Timestamps
If Test 2 works, fix the demo scripts:

```python
# In examples/validate_time_simulator.py
# WRONG:
result = analyzer.fourier_lens(samples, timestamps_hours)

# RIGHT:
timestamps_seconds = timestamps_hours * 3600.0
result = analyzer.fourier_lens(samples, timestamps_seconds)
```

### Fix B: Period Conversion
If Test 2 fails with small values (< 1.0h), fix conversion:

```python
# In system_analyzer.py, line 254
# Current:
dominant_period = 1.0 / dominant_freq if dominant_freq > 0 else float('inf')
# ...
# Line 259:
dominant_period=dominant_period / 3600.0,  # Convert seconds to hours

# Possible issue: Check if frequency is already in wrong units
# Add debug print to see actual values
```

### Fix C: Frequency Range
If Test 2 fails with huge values (> 1000h), fix range:

```python
# In system_analyzer.py, line 239-242
# Current:
frequency, power = ls.autopower(
    minimum_frequency=1.0/(100*3600),  # Max period: 100 hours
    maximum_frequency=self.nyquist_freq,
    samples_per_peak=10
)

# Check if nyquist_freq is calculated correctly
# Should be: sampling_rate / 2.0
```

## After Running Debug Script

1. **Share the output** - Post the console output or save to file:
   ```bash
   python debug_fourier.py > fourier_debug_output.txt
   ```

2. **Note which test passed** - Record results for each test scenario

3. **Identify the fix needed** - Based on which tests passed/failed

4. **Apply the fix** - Modify either:
   - Demo scripts (if Test 2 passed)
   - `system_analyzer.py` (if Test 2 failed)

5. **Re-test** - Run validation again:
   ```bash
   python examples/validate_time_simulator.py
   pytest tests/test_system_analyzer_mvp.py -v -k fourier
   ```

## Questions to Answer

When you run the debug script, note:

1. What is the detected period in Test 2 (seconds)? **______ hours**
2. What is the dominant frequency in Test 2? **______ Hz**
3. Does Test 2 pass (20-28h range)? **Yes / No**
4. Does Test 4 (TimeSimulator-like) pass? **Yes / No**
5. What does "ROOT CAUSE ANALYSIS" say? **______________**

---

**This debug run will definitively identify whether the bug is:**
- A) In demo scripts (timestamp units)
- B) In analyzer (period conversion)
- C) In analyzer (frequency range)

Then we can apply the precise fix! 🎯
