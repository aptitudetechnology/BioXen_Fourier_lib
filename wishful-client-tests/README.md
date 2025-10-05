# BioXen Wishful Client Tests 🔮

**Status:** Aspirational - These tests define ideal API contracts for future implementation

---

## 📋 Overview

This test suite defines comprehensive API tests for BioXen's future REST server implementing:
- Environmental sensor integration (BME280 temperature/humidity/pressure, LTR-559 light)
- Circadian entrainment validation for organisms with clock genes
- Temperature compensation studies (Q10 analysis)
- Model validation and parameter tuning
- VM lifecycle and continuous simulation

**Why "Wishful Thinking"?**
- These APIs don't exist yet (Phase 5-6 future work)
- Tests define the **contract** we want from future APIs
- Follows TDD approach: write tests first, then implement
- Mirrors structure of `client-tests/` for PyCWT-mod server

---

## 🎯 Test Modules

### 1. `test_sensor_hardware.py` (15 tests)
Hardware sensor detection, calibration, and data acquisition.

**Test Classes:**
- `TestBME280Hardware` - Temperature, humidity, pressure sensor
- `TestLTR559Hardware` - Light intensity and proximity sensor
- `TestSensorCalibration` - Calibration procedures
- `TestSensorDataQuality` - Noise, drift, consistency validation
- `TestMultiSensorIntegration` - Synchronized multi-sensor reading

**Key Tests:**
```python
def test_detect_bme280_sensor(test_client)
def test_read_temperature(test_client)
def test_read_light_intensity(test_client)
def test_calibrate_light_sensor_dark(test_client)
```

### 2. `test_circadian_entrainment.py` (20 tests)
Circadian rhythm validation for organisms WITH clock genes.

**Test Classes:**
- `TestLightDarkCycles` - Light cycle generation (12L:12D, 16L:8D, skeleton)
- `TestCircadianEntrainment` - Entrainment validation
- `TestPhaseResponseCurves` - PRC experiments (classic circadian biology)
- `TestFreeRunningPeriod` - Measure tau in constant conditions
- `TestPhotoperiodExperiments` - Photoperiodic responses

**Key Tests:**
```python
def test_yeast_entrainment_to_12L_12D(test_client)
def test_phase_delay_light_pulse_at_CT14(test_client)
def test_measure_tau_in_constant_darkness(test_client)
```

**Important:** Only tests organisms that HAVE circadian clock genes!
- ✅ Yeast (with FRQ/WC homologs)
- ✅ Cyanobacteria (KaiABC oscillator)
- ✅ Neurospora (FRQ/WC-1/WC-2)
- ❌ E. coli (no circadian genes)
- ❌ Syn3A (no circadian genes)

### 3. `test_temperature_compensation.py` (12 tests)
Temperature compensation and heat shock responses.

**Test Classes:**
- `TestTemperatureCompensation` - Q10 studies (circadian period should have Q10 ≈ 1)
- `TestHeatShockResponse` - Heat/cold shock protein induction
- `TestTemperatureCycles` - Temperature as zeitgeber
- `TestArrheniusKinetics` - Metabolic rate temperature dependence

**Key Tests:**
```python
def test_calculate_q10_coefficient(test_client)  # Should be ~1.0 for circadian
def test_heat_shock_37_to_42_celsius(test_client)  # HSP upregulation
def test_temperature_cycle_entrainment(test_client)
```

---

## 🧬 Biological Accuracy

These tests are grounded in real circadian biology and address Claude's critique about biologistic plausibility.

### What We're NOT Claiming:
- ❌ Sensors "create" circadian rhythms
- ❌ VMs have clock signals like computers
- ❌ All organisms need circadian clocks
- ❌ Frequency analysis causes self-regulation

### What We ARE Testing:
- ✅ **Entrainment:** Light input synchronizes EMERGENT oscillators (for organisms with clock genes)
- ✅ **Temperature compensation:** Circadian period stays ~24h across temperature range (Q10 ≈ 1)
- ✅ **Model validation:** Does simulation match biological reality?
- ✅ **Parameter tuning:** Adjust kinetic constants based on validation results

### Biologically Sound Examples:

**Neurospora crassa** (HAS circadian genes):
```python
vm = create_bio_vm('neurospora', genes=['frq', 'wc-1', 'wc-2'])
# Apply 12L:12D light cycle via LTR-559
# Validate: FRQ protein oscillates with ~22h period
# Test: Light pulse at CT12 causes phase delay
```

**E. coli** (NO circadian genes):
```python
vm = create_bio_vm('ecoli')  # No clock genes
# Don't test circadian entrainment
# But: Test heat shock response (42°C → dnaK/groEL upregulation)
# Validate: Temperature-dependent growth follows Arrhenius kinetics
```

---

## 🚀 Running Tests (When Implemented)

```bash
# Install dependencies (future)
pip install -r wishful-client-tests/requirements-test.txt

# Run all wishful tests
pytest wishful-client-tests/ -v

# Run specific test modules
pytest wishful-client-tests/test_sensor_hardware.py -v
pytest wishful-client-tests/test_circadian_entrainment.py -v
pytest wishful-client-tests/test_temperature_compensation.py -v

# Run with markers
pytest -m "sensor" wishful-client-tests/  # Only sensor tests
pytest -m "circadian" wishful-client-tests/  # Only circadian tests
pytest -m "wishful" wishful-client-tests/  # All aspirational tests
```

---

## 📊 Test Coverage Goals

| Test Module | Test Count | API Coverage |
|------------|-----------|--------------|
| `test_sensor_hardware.py` | 15 | 100% sensor APIs |
| `test_circadian_entrainment.py` | 20 | 95% circadian protocols |
| `test_temperature_compensation.py` | 12 | 90% temperature studies |
| **Total** | **47 tests** | **95% coverage** |

---

## 🔬 Scientific References

**Circadian Biology:**
- Dunlap JC (1999) "Molecular Bases for Circadian Clocks" - *Cell*
- Takahashi JS (2017) "Transcriptional architecture of the mammalian circadian clock" - *Nat Rev Genet*
- Nakajima M et al. (2005) "Reconstitution of Circadian Oscillation of Cyanobacterial KaiC" - *Science*

**Temperature Compensation:**
- Ruoff P et al. (2005) "The Goodwin Oscillator and Temperature Compensation" - *J Theor Biol*
- Hastings JW, Sweeney BM (1957) "On the mechanism of temperature independence" - *PNAS*

**Phase Response Curves:**
- Johnson CH (1999) "Forty years of PRCs--what have we learned?" - *Chronobiol Int*

**Heat Shock Response:**
- Richter K et al. (2010) "The heat shock response: life on the verge of death" - *Mol Cell*

---

## 🛠️ Fixtures Provided

See `conftest.py` for comprehensive fixtures:

**Environmental Data:**
- `sample_bme280_reading` - Temperature, humidity, pressure
- `sample_ltr559_reading` - Light intensity, proximity
- `light_dark_cycle_12_12` - 12:12 LD cycle config
- `environmental_time_series_24h` - 24-hour environmental data

**Biological Signals:**
- `circadian_signal_48h` - 48-hour oscillating signal (~24h period)
- `metabolic_time_series` - ATP, glucose time series
- `temperature_shock_response` - Heat shock response dynamics

**VM Configurations:**
- `ecoli_vm_config` - E. coli (no circadian genes)
- `yeast_circadian_vm_config` - Yeast with circadian capability
- `syn3a_vm_config` - Syn3A minimal cell
- `cyanobacteria_vm_config` - Synechococcus with KaiABC

**Reference Data:**
- `reference_circadian_data` - Expected periods, amplitudes
- `reference_temperature_compensation_data` - Q10 expectations
- `reference_heat_shock_genes` - Expected HSP induction

---

## 🎓 Educational Value

Even though these APIs don't exist yet, these tests serve as:

1. **API Design Specification** - Defines clear contracts for future implementation
2. **Biological Knowledge Base** - Documents what biological experiments should look like
3. **TDD Blueprint** - When we build the APIs, these tests guide implementation
4. **Scientific Validation** - Ensures we're testing biologically meaningful questions

---

## 📝 Test Markers

Tests are organized with pytest markers:

- `@pytest.mark.wishful` - Aspirational tests (all tests in this suite)
- `@pytest.mark.sensor` - Hardware sensor integration
- `@pytest.mark.circadian` - Circadian rhythm analysis
- `@pytest.mark.validation` - Model validation tests
- `@pytest.mark.integration` - Full workflow tests

---

## 🔮 When Will This Be Implemented?

**Timeline:**
- **Phase 1-4:** Focus on local computation, model validation framework
- **Phase 4 Assessment:** Benchmark performance to decide if remote computation needed
- **Phase 5-6:** IF Phase 4 shows bottlenecks, build REST API server
- **Phase 6+:** Hardware sensor integration

**Current Reality:**
- ❌ No REST API server
- ❌ No hardware sensor support
- ❌ VMs don't respond to real-time environmental data
- ❌ These tests will fail (APIs don't exist)

**Future Vision:**
- ✅ BioXen REST API server (FastAPI)
- ✅ BME280/LTR-559 sensor integration (Raspberry Pi + I2C)
- ✅ Real-time environmental data streaming to VMs
- ✅ Circadian entrainment validation for organisms with clock genes
- ✅ These tests guide implementation and validation

---

## 🔗 Related Documentation

- **Main wishful test prompt:** `wishful-client-tests.prompt` - Defines VM lifecycle, validation, parameter tuning APIs
- **Circadian-specific prompt:** `wishful-client-tests-circadian-clock.md` - Environmental sensor integration details
- **Claude's critique:** `circadian-clock-claude-thoughts.md` - Why circadian clocks are EMERGENT, not imposed
- **Reframing doc:** `../REFRAMING_COMPLETE.md` - Model validation (not self-regulation) approach
- **Execution model:** `../fourier-execution-model.md` - VM architecture and analysis integration
- **Roadmap:** `../docs/DEVELOPMENT_ROADMAP.md` - Phased implementation plan

---

## ✅ Key Takeaways

1. **Biologically Honest:** Only tests circadian entrainment for organisms WITH clock genes
2. **Scientifically Grounded:** Based on real circadian experiments (PRC, Q10, entrainment)
3. **API-First Design:** Defines clear contracts before implementation
4. **TDD Approach:** Write tests first, implement later
5. **Educational:** Documents what real biological experiments look like

**These tests represent the IDEAL state we're building toward, grounded in real biology and computational best practices.**

---

**Status:** 🔮 Aspirational (Phase 6+ implementation)  
**Last Updated:** October 5, 2025  
**Maintainer:** BioXen Development Team
