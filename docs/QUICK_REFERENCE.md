# BioXen Quick Reference - What Works Now

**Last Updated:** October 5, 2025  
**For:** Developers wanting to use BioXen today

---

## ✅ What You Can Do Right Now

### 1. Create and Manage Biological VMs

```python
from bioxen_fourier_vm_lib.api import create_bio_vm

# Create VM
vm = create_bio_vm('my_ecoli', 'ecoli', 'basic')

# Start VM
vm.start()

# Allocate resources
vm.allocate_resources({
    'atp': 100.0,
    'ribosomes': 50,
    'amino_acids': 1000
})

# Execute biological process
result = vm.execute_biological_process({
    'type': 'transcription',
    'genes': ['gene_001']
})

# Check status
status = vm.get_status()
print(f"State: {status['state']}")

# Clean up
vm.destroy()
```

**Supported Organisms:**
- `'syn3a'` - JCVI-Syn3A minimal cell
- `'ecoli'` - E. coli
- `'minimal_cell'` - Generic minimal cell

**VM Types:**
- `'basic'` - Lightweight (recommended)
- `'xcpng'` - Advanced (requires config)

---

### 2. Analyze Biological Time-Series Data

```python
from bioxen_fourier_vm_lib.analysis.system_analyzer import SystemAnalyzer
import numpy as np

# Create analyzer (sampling_rate = samples per second)
analyzer = SystemAnalyzer(sampling_rate=0.2)  # 5-second intervals

# Example: ATP levels over 48 hours
atp_data = np.random.normal(100, 10, size=34560)  # 48h * 720 samples/h
timestamps = np.arange(len(atp_data)) * 5.0  # Every 5 seconds

# Lens 1: Fourier - Detect circadian rhythms
fourier = analyzer.fourier_lens(atp_data, timestamps, detect_harmonics=True)
print(f"Dominant period: {fourier.dominant_period:.1f} hours")
if 20 < fourier.dominant_period < 28:
    print("✓ Circadian rhythm detected!")

for harmonic in fourier.harmonics:
    print(f"  Period: {harmonic['period']:.1f}h, Power: {harmonic['power']:.3f}")

# Lens 2: Wavelet - Detect transient events
wavelet = analyzer.wavelet_lens(atp_data, dt=5.0)
print(f"Transient events detected: {len(wavelet.transient_events)}")
print(f"Optimal wavelet used: {wavelet.wavelet_used}")

for event in wavelet.transient_events:
    print(f"  Event at t={event['time']:.0f}s, intensity={event['intensity']:.2f}")

# Lens 3: Laplace - Assess system stability
laplace = analyzer.laplace_lens(atp_data, dt=5.0)
print(f"System stability: {laplace.stability}")
print(f"Damping ratio: {laplace.damping_ratio:.3f}")

if laplace.stability == 'unstable':
    print("⚠️  WARNING: System homeostasis compromised!")

# Lens 4: Z-Transform - Filter noise
ztransform = analyzer.z_transform_lens(atp_data, dt=5.0)
print(f"Noise reduced by: {ztransform.noise_reduction_percent:.1f}%")

# Get filtered signal
clean_signal = ztransform.filtered_signal
```

---

### 3. Monitor VM Performance

```python
from bioxen_fourier_vm_lib.monitoring.profiler import PerformanceProfiler
from bioxen_fourier_vm_lib.hypervisor import BioXenHypervisor
import time

# Create hypervisor and profiler
hypervisor = BioXenHypervisor()
profiler = PerformanceProfiler(hypervisor, monitoring_interval=5.0)

# Start monitoring
profiler.start_monitoring()

# ... create and run VMs ...
vm1 = create_bio_vm('vm1', 'ecoli', 'basic')
vm1.start()

# Let it run and collect data
time.sleep(300)  # 5 minutes

# Manually analyze collected data
fourier_result = profiler.analyze_with_fourier()
print(f"System rhythm period: {fourier_result.dominant_period:.1f}h")

wavelet_result = profiler.analyze_with_wavelet()
print(f"Transient events: {len(wavelet_result.transient_events)}")

laplace_result = profiler.analyze_with_laplace()
print(f"System stability: {laplace_result.stability}")

ztransform_result = profiler.analyze_with_ztransform()
print(f"Noise reduction: {ztransform_result.noise_reduction_percent:.1f}%")

# Stop monitoring
profiler.stop_monitoring()
vm1.destroy()
```

---

### 4. Access Environmental State for Circadian Studies

```python
from bioxen_fourier_vm_lib.hypervisor import BioXenHypervisor

hypervisor = BioXenHypervisor()
state = hypervisor.get_environmental_state()

# Access temporal information
print(f"Light intensity: {state.light_intensity:.2f}")  # 0.0 (night) to 1.0 (day)
print(f"Seasonal phase: {state.seasonal_phase.value}")  # spring/summer/autumn/winter
print(f"Lunar phase: {state.lunar_phase.value}")  # new/waxing/full/waning
print(f"Tidal factor: {state.gravitational_tide_factor:.3f}")  # 0.95-1.05

# Use in biological process timing
if state.light_intensity > 0.5:
    print("Daylight - upregulate photosynthesis genes")
else:
    print("Nighttime - activate circadian clock genes")
```

---

## ❌ What You Cannot Do Yet

### Continuous Simulation Mode
```python
# ❌ NOT IMPLEMENTED
vm.start_continuous_simulation(duration_hours=48)
history = vm.get_metabolic_history()
```

### VM Self-Regulation
```python
# ❌ NOT IMPLEMENTED
analysis = vm.analyze_metabolic_state()
if analysis.circadian_drift_detected:
    vm.adjust_clock_genes()
```

### Automatic Real-Time Analysis
```python
# ❌ Profiler doesn't analyze automatically yet
profiler.start_monitoring()  # Collects data but doesn't analyze
# Must manually call profiler.analyze_with_fourier(), etc.
```

### Remote Hardware Acceleration
```python
# ❌ PyCWT-mod server not implemented yet
# Test suite exists, server pending
```

---

## 📚 Complete Examples

### Example 1: Analyze Simulated Circadian Gene Expression

```python
from bioxen_fourier_vm_lib.analysis.system_analyzer import SystemAnalyzer
import numpy as np

# Generate realistic circadian gene expression data
hours = np.linspace(0, 72, 1000)  # 72 hours
timestamps = hours * 3600  # Convert to seconds

# Circadian rhythm (24h) + noise
expression = 50 + 30 * np.sin(2 * np.pi * hours / 24) + np.random.normal(0, 5, len(hours))

# Analyze
analyzer = SystemAnalyzer(sampling_rate=1.0/((timestamps[1] - timestamps[0])))
result = analyzer.fourier_lens(expression, timestamps, detect_harmonics=True)

print(f"Dominant period: {result.dominant_period:.1f}h")
print(f"Confidence: {result.significance*100:.1f}%")

if 20 < result.dominant_period < 28:
    print("✓ Strong circadian rhythm detected!")
```

### Example 2: Detect Stress Response with Wavelets

```python
from bioxen_fourier_vm_lib.analysis.system_analyzer import SystemAnalyzer
import numpy as np

# Generate ATP levels with stress event at t=1800s (30 min)
timestamps = np.arange(0, 7200, 5)  # 2 hours, 5s intervals
atp = np.ones(len(timestamps)) * 100

# Stress event: ATP drops rapidly then recovers
stress_start = 360  # Index at 30 min
stress_duration = 60  # 60 samples = 5 minutes
atp[stress_start:stress_start+stress_duration] *= 0.6  # 40% drop

# Gradual recovery
for i in range(stress_duration):
    recovery_idx = stress_start + stress_duration + i
    if recovery_idx < len(atp):
        atp[recovery_idx] = 0.6 + 0.4 * (i / stress_duration)

# Add noise
atp += np.random.normal(0, 2, len(atp))

# Analyze
analyzer = SystemAnalyzer(sampling_rate=0.2)
result = analyzer.wavelet_lens(atp, dt=5.0)

print(f"Transient events detected: {len(result.transient_events)}")
print(f"Wavelet used: {result.wavelet_used}")

for event in result.transient_events:
    time_minutes = event['time'] / 60
    print(f"  Event at t={time_minutes:.1f} min, intensity={event['intensity']:.2f}")
```

### Example 3: Full VM Workflow with Monitoring

```python
from bioxen_fourier_vm_lib.api import create_bio_vm
from bioxen_fourier_vm_lib.monitoring.profiler import PerformanceProfiler
from bioxen_fourier_vm_lib.hypervisor import BioXenHypervisor
import time

# Setup
hypervisor = BioXenHypervisor()
profiler = PerformanceProfiler(hypervisor, monitoring_interval=5.0)
profiler.start_monitoring()

# Create multiple VMs
vms = []
for i in range(3):
    vm = create_bio_vm(f'cell_{i}', 'ecoli', 'basic')
    vm.start()
    vm.allocate_resources({'atp': 100, 'ribosomes': 30})
    vms.append(vm)

# Run workload
print("Running biological processes...")
for _ in range(10):
    for vm in vms:
        vm.execute_biological_process({'type': 'transcription', 'genes': [f'gene_{_}']})
    time.sleep(2)

# Analyze
print("\nAnalyzing collected metrics...")
fourier = profiler.analyze_with_fourier()
print(f"System period: {fourier.dominant_period:.1f}h")

wavelet = profiler.analyze_with_wavelet()
print(f"Transient events: {len(wavelet.transient_events)}")

laplace = profiler.analyze_with_laplace()
print(f"Stability: {laplace.stability}")

# Cleanup
profiler.stop_monitoring()
for vm in vms:
    vm.destroy()

print("\n✓ Workflow complete!")
```

---

## 🔍 Debugging & Validation

### Check if SystemAnalyzer is Working

```python
from bioxen_fourier_vm_lib.analysis.system_analyzer import SystemAnalyzer
import numpy as np

analyzer = SystemAnalyzer(sampling_rate=1.0)

# Test signal validation
test_signal = np.random.normal(0, 1, 100)
validation = analyzer.validate_signal(test_signal)

print(f"Signal valid: {validation['all_passed']}")
if not validation['all_passed']:
    print("Issues:", validation)
```

### Check VM Status

```python
vm = create_bio_vm('test', 'ecoli', 'basic')
vm.start()

status = vm.get_status()
print(f"State: {status['state']}")
print(f"Biological status: {status.get('biological_status', {})}")

resource_usage = vm.get_resource_usage()
print(f"Resource usage: {resource_usage}")
```

---

## 📖 Where to Learn More

- **Implementation Status:** `docs/IMPLEMENTATION_STATUS.md`
- **Development Roadmap:** `docs/DEVELOPMENT_ROADMAP.md`
- **Full Specification:** `specification-document_bioxen_fourier_vm_lib_ver0.0.0.01.md`
- **Research Background:** `research/Frequency Domain Analysis in Biology.md`
- **Interactive Demos:** `research/interactive-fourier-series/lenses/`

---

## 💡 Tips & Best Practices

1. **Always validate signals** before analysis
2. **Use appropriate sampling rates** for your data (e.g., 0.2 Hz for 5s intervals)
3. **Lomb-Scargle is mandatory** for irregular biological sampling
4. **Wavelets detect transients** that Fourier misses
5. **Check system stability** with Laplace lens for homeostasis studies
6. **Filter before analyzing** if your signal is noisy

---

## 🐛 Common Issues

**Issue:** "SystemAnalyzer not found"  
**Fix:** `pip install -e .` from repository root

**Issue:** "No module named 'astropy'"  
**Fix:** `pip install astropy pywt scipy numpy`

**Issue:** "VM won't start"  
**Fix:** Check hypervisor status: `hypervisor.get_system_resources()`

**Issue:** "Analysis returns None"  
**Fix:** Ensure you have enough data points (minimum 100 samples)

---

**Ready to build?** Start with the examples above! 🚀  
**Want to contribute?** See the Development Roadmap for Phase 1 tasks.
