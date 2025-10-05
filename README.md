# BioXen Fourier VM Library

[![Version](https://img.shields.io/badge/version-0.0.0.01-blue.svg)](https://github.com/aptitudetechnology/BioXen_Fourier_lib)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A Python library for virtualizing biological cells using a factory pattern, enabling programmatic creation and management of biological virtual machines (VMs) for research and simulation. Features advanced time simulation for circadian rhythm studies and Fourier analysis of metabolic oscillations.

## 🚦 Project Status (October 2025)

**What works today:**
- ✅ **VM Engine**: Create, manage, and run biological VMs (syn3a, ecoli, minimal_cell)
- ✅ **SystemAnalyzer**: All 4 lenses fully implemented (1,336 lines - Fourier, Wavelet, Laplace, Z-Transform)
- ✅ **Basic biological process execution** (transcription, translation)
- ✅ **Resource management** (ATP, ribosomes, amino acids)
- ✅ **Performance Profiler**: Time-series data collection from VMs

**What we're building** (see [DEVELOPMENT_ROADMAP.md](docs/DEVELOPMENT_ROADMAP.md)):
- 🔄 **Phase 1 (Ready to Start)**: Automatic continuous analysis in profiler
- 🔄 **Phase 2 (2-3 weeks)**: Continuous simulation mode with metabolic history
- 🔄 **Phase 3 (Core Goal)**: VM self-regulation using analysis feedback
- 🔄 **Phase 4 (1-2 weeks)**: Performance validation and optimization decisions
- 🔄 **Phase 5-6 (Optional)**: Remote computation and hardware acceleration

**Current Focus:** Phase 1 - Adding automatic analysis to the performance profiler.

---

## 🎯 The BioXen Vision

BioXen is building toward **self-regulating biological VMs** that maintain homeostasis through continuous frequency domain analysis:

1. **VMs simulate** cellular processes (metabolism, gene expression, protein synthesis)
2. **VMs generate** continuous time-series data (ATP levels, metabolite concentrations)
3. **VMs analyze** their own state using four complementary analytical methods:
   - **Fourier Lens:** Detect circadian rhythm drift
   - **Wavelet Lens:** Identify transient stress responses
   - **Laplace Lens:** Monitor system stability and feedback control
   - **Z-Transform Lens:** Filter noise and smooth measurements
4. **VMs adapt** behavior based on analysis (adjust clock genes, regulate metabolism)

This creates biological simulations that **self-regulate like real cells**.

---

## ✨ Features

### Current Features (Working Today)

- **✅ Biological VM Virtualization**: Create, start, stop, and manage synthetic cell simulations
- **✅ Four-Lens Analysis System**: Complete implementation of frequency domain analysis
  - **Fourier (Lomb-Scargle)**: Detect circadian rhythms and periodic patterns
  - **Wavelet (CWT/DWT)**: Localize transient events with automatic wavelet selection and multi-resolution analysis
  - **Laplace**: Transfer function analysis and system stability assessment
  - **Z-Transform**: Digital filtering and noise reduction
- **✅ Time Simulation**: Accurate solar/lunar cycles for circadian studies
- **✅ Hypervisor System**: Manage multiple biological VMs with resource allocation
- **✅ Factory Pattern API**: Clean, extensible architecture for VM creation
- **✅ Performance Profiler**: Real-time monitoring with time-series data collection
- **✅ Interactive Learning Tools**: Web-based demos with decision trees and validation

### Planned Features (In Development)

- **🔄 Continuous VM Simulation**: VMs will generate continuous metabolic time-series (ATP, glucose, gene expression)
- **🔄 VM Self-Regulation**: VMs will use four-lens analysis to detect anomalies and adjust behavior
- **🔄 Automatic Real-Time Analysis**: Profiler will continuously analyze and trigger alerts
- **🔄 Hardware Acceleration**: REST API server (PyCWT-mod) for FPGA/GPU-accelerated wavelet analysis

**See:** `docs/DEVELOPMENT_ROADMAP.md` for implementation timeline

## 📦 Installation

### Requirements
- Python >= 3.6
- Dependencies: pylua-bioxen-vm-lib >= 0.1.22, questionary >= 2.1.0, rich >= 13.0.0

### Install from Source
```bash
git clone https://github.com/aptitudetechnology/BioXen_Fourier_lib.git
cd BioXen_Fourier_lib
pip install -e .
```

## 🚀 Quick Start

```python
from bioxen_fourier_vm_lib.api import create_bio_vm
from bioxen_fourier_vm_lib.hypervisor import BioXenHypervisor

# Create a biological VM
vm = create_bio_vm('my_cell', 'syn3a', 'basic')

# Start the VM
vm.start()

# Allocate resources
vm.allocate_resources({
    'atp': 100.0,
    'ribosomes': 50,
    'amino_acids': 1000
})

# Check status
status = vm.get_status()
print(f"VM State: {status['state']}")

# Execute biological process
result = vm.execute_biological_process({
    'type': 'transcription',
    'genes': ['gene_001']
})

# Get environmental state for circadian rhythm modeling
hypervisor = BioXenHypervisor()
env_state = hypervisor.get_environmental_state()
print(f"Light intensity: {env_state.light_intensity}")
print(f"Seasonal phase: {env_state.seasonal_phase.value}")

# Clean up
vm.destroy()
```

## � What Works Today vs. What's Planned

### ✅ Working Now: VM Management & Analysis

You can create and manage biological VMs, and analyze time-series data with the four-lens system:

```python
# ✅ VM Creation and Management (WORKS)
from bioxen_fourier_vm_lib.api import create_bio_vm

vm = create_bio_vm('ecoli_001', 'ecoli', 'basic')
vm.start()
vm.allocate_resources({'atp': 100, 'ribosomes': 50})
result = vm.execute_biological_process({'type': 'transcription', 'genes': ['gene_001']})
status = vm.get_status()
vm.destroy()
```

```python
# ✅ Four-Lens Analysis (WORKS)
from bioxen_fourier_vm_lib.analysis.system_analyzer import SystemAnalyzer
import numpy as np

analyzer = SystemAnalyzer(sampling_rate=0.2)

# Example: Analyze ATP levels over time
atp_data = np.random.normal(100, 10, size=720)  # 1 hour of data
timestamps = np.arange(len(atp_data)) * 5.0

# Detect circadian rhythms
fourier = analyzer.fourier_lens(atp_data, timestamps, detect_harmonics=True)
print(f"Dominant period: {fourier.dominant_period:.1f} hours")

# Detect transient events
wavelet = analyzer.wavelet_lens(atp_data, dt=5.0)
print(f"Transient events: {len(wavelet.transient_events)}")

# Assess system stability
laplace = analyzer.laplace_lens(atp_data, dt=5.0)
print(f"System stability: {laplace.stability}")

# Filter noise
ztransform = analyzer.z_transform_lens(atp_data, dt=5.0)
print(f"Noise reduced by: {ztransform.noise_reduction_percent:.1f}%")
```

### 🔄 Coming Soon: Self-Regulating VMs (Phases 2-3)

The vision is for VMs to continuously simulate metabolic processes and self-regulate using analysis:

```python
# 🔄 PLANNED (not yet implemented)
vm = create_bio_vm('cell', 'ecoli', 'basic')

# Continuous simulation with metabolic tracking
vm.start_continuous_simulation(duration_hours=48)

# Get historical metabolic data
history = vm.get_metabolic_history()
# Returns: {'timestamps': [...], 'atp': [...], 'glucose': [...], 'gene_expression': {...}}

# VM analyzes its own state and self-regulates
analysis = vm.analyze_metabolic_state()
if analysis.circadian_drift_detected:
    vm.adjust_clock_genes()  # Automatic homeostasis!

# Profiler with automatic continuous analysis
from bioxen_fourier_vm_lib.monitoring.profiler import PerformanceProfiler

profiler = PerformanceProfiler(hypervisor, monitoring_interval=5.0, analysis_interval=60.0)
profiler.start_monitoring()  # Will analyze data every 60 seconds automatically

# Get analysis results
recent_analysis = profiler.get_latest_analysis()
print(f"System stability: {recent_analysis['laplace'].stability}")
```

**Status:** See `docs/IMPLEMENTATION_STATUS.md` for detailed audit of what exists  
**Roadmap:** See `docs/DEVELOPMENT_ROADMAP.md` for implementation plan (Phases 1-6)

## �📋 API Overview

### Core Functions
- `create_bio_vm(vm_id, biological_type, vm_type, config=None)`: Create a biological VM
- `get_supported_biological_types()`: List available organism types
- `get_supported_vm_types()`: List available VM infrastructures

### VM Operations
- `vm.start()`: Start the biological VM
- `vm.get_status()`: Get current VM status
- `vm.allocate_resources(resources)`: Allocate biological resources
- `vm.execute_biological_process(process)`: Run biological processes
- `vm.destroy()`: Destroy the VM

### Hypervisor Operations
- `hypervisor.get_environmental_state()`: Get current temporal state for circadian modeling
- `hypervisor.create_vm(vm_id, genome_template)`: Create VM with hypervisor control
- `hypervisor.start_vm(vm_id)`: Start VM through hypervisor
- `hypervisor.get_system_resources()`: Monitor system-wide resource usage

---

## 🔬 The Four-Lens Analysis System

BioXen's analysis engine uses four complementary methods because biological signals present unique challenges:

| Challenge | Lens | Method | Best For | Library | Status |
|-----------|------|--------|----------|---------|--------|
| Irregular sampling | **Fourier** | Lomb-Scargle periodogram | Circadian rhythms, dominant frequencies | `astropy.timeseries.LombScargle` | ✅ Working |
| Non-stationary signals | **Wavelet** | CWT/DWT with auto-selection | Transients, stress responses, time-frequency | `pywt` (PyWavelets) | ✅ Working |
| System stability | **Laplace** | Transfer functions, pole analysis | Feedback control, homeostasis | `scipy.signal`, `python-control` | ✅ Working |
| Discrete measurements | **Z-Transform** | Digital filters, noise reduction | Sampled data, filtering | `scipy.signal` | ✅ Working |

### Why Four Lenses?

- **Biological signals are non-stationary** (conditions change over time) → Wavelet essential
- **Biological sampling is irregular** (real-world constraints) → Lomb-Scargle is the standard
- **Different biological questions** require different analytical approaches
- **Multi-lens validation** increases confidence in findings

**All four lenses are fully implemented in `SystemAnalyzer`** (1,336 lines) and can be used independently for signal analysis. VM integration (automatic self-regulation) is in active development (Phases 2-3).

**Learn more:**
- Research background: `research/Frequency Domain Analysis in Biology.md`
- Interactive demos: `research/interactive-fourier-series/lenses/`
- Implementation details: `docs/IMPLEMENTATION_STATUS.md`
- Integration plan: `docs/DEVELOPMENT_ROADMAP.md`

### Four-Lens Analysis

```python
from astropy.timeseries import LombScargle
import pywt
import numpy as np

# Example: Analyze circadian gene expression with irregular sampling
time = np.array([0, 1, 3, 6, 10, 15, 21, 28])  # Irregular hours
expression = np.array([1.0, 1.5, 0.8, 0.3, 0.5, 1.2, 1.8, 1.3])

# Lens 1: Lomb-Scargle (handles irregular sampling - biology standard)
frequency, power = LombScargle(time, expression).autopower()
dominant_freq = frequency[np.argmax(power)]
print(f"Dominant period: {1/dominant_freq:.2f} hours")

# Lens 2: Wavelet (for time-frequency localization)
coefficients, frequencies = pywt.cwt(expression, scales=np.arange(1,10), wavelet='morl')

# See research/interactive-fourier-series/lenses/ for interactive web demos
# - bioxen-lenses.html: Four-lens comparison with decision tree
# - bio-signal.html: Method selection guide for 5 signal types
```

## 🏗️ Architecture

## 🏗️ Architecture

```
src/bioxen_fourier_vm_lib/
├── api/                   # Public API layer
│   └── factory.py         # Factory pattern implementation
├── hypervisor/            # Hypervisor layer
│   ├── core.py           # Main hypervisor logic
│   └── TimeSimulator.py  # Astronomical time cycles
├── analysis/              # Four-lens frequency domain analysis
│   ├── fourier.py        # Lomb-Scargle periodogram
│   ├── wavelet.py        # Wavelet transforms
│   ├── laplace.py        # Transfer functions
│   └── ztransform.py     # Digital signal processing
├── genetics/              # Genetic circuits
├── monitoring/            # Performance monitoring
└── visualization/         # Terminal interfaces
```

## 🔬 Supported Biological Types

- **syn3a**: Minimal cell (JCVI-Syn3A)
- **ecoli**: Escherichia coli
- **yeast**: Saccharomyces cerevisiae
- **orthogonal**: Synthetic cell chassis
- Future: mammalian, plant

## 🖥️ VM Types

- **basic**: Lightweight virtualization

## ⏰ Temporal Modeling

The library includes sophisticated time simulation for accurate biological rhythm studies:

- **Solar Cycles**: Day/night simulation with light intensity (0.0-1.0)
- **Lunar Phases**: Full moon cycle with illumination levels
- **Seasonal Variations**: Orbital seasons affecting resource availability and temperature
- **Gravitational Tides**: Lunar gravitational effects on cellular processes
- **Circadian Rhythms**: Enable Fourier analysis of metabolic oscillations

```python
# Access temporal state for rhythm studies
from bioxen_fourier_vm_lib.hypervisor import BioXenHypervisor

hypervisor = BioXenHypervisor()
state = hypervisor.get_environmental_state()

# Use in biological process timing
light_level = state.light_intensity  # 0.0 (night) to 1.0 (day)
season = state.seasonal_phase        # spring, summer, autumn, winter
tide_factor = state.gravitational_tide_factor  # 0.95-1.05
```
- **xcpng**: Advanced XCP-ng infrastructure

## �️ Development Roadmap

We're following a phased approach to build self-regulating biological VMs:

- **✅ Phase 0: Foundation** - Complete (documentation alignment, codebase audit)
- **🔄 Phase 1: Profiler Analysis** (1-2 weeks, Ready to Start)
  - Automatic continuous analysis in performance profiler
  - Anomaly detection and alerting
  - Analysis result history tracking
- **⏳ Phase 2: Continuous Simulation** (2-3 weeks, Depends on Phase 1)
  - VMs generate continuous metabolic time-series
  - Historical data buffers (ATP, glucose, gene expression)
  - Realistic metabolic dynamics
- **⏳ Phase 3: VM Self-Regulation** (2-3 weeks, Depends on Phase 1+2)
  - VMs analyze their own metabolic state
  - Analysis triggers behavioral adjustments
  - Feedback loops: circadian correction, stability management, energy regulation
- **⏳ Phase 4: Performance Validation** (1-2 weeks, Depends on Phase 1+2+3)
  - Benchmark analysis overhead and latency
  - Memory profiling and leak detection
  - Decide: local computation sufficient or need remote?
- **⏳ Phase 5-6: Architecture Refactor & Remote Computation** (6-10 weeks, Conditional)
  - Execute ONLY if Phase 4 shows performance bottlenecks
  - PyCWT-mod REST API server for hardware acceleration
  - FPGA/GPU support for wavelet analysis

**Current Focus:** Phase 1 - Implementing automatic analysis loop in profiler  
**See:** [DEVELOPMENT_ROADMAP.md](docs/DEVELOPMENT_ROADMAP.md) for detailed task breakdown

---

## �📚 Documentation

- **[Implementation Status](docs/IMPLEMENTATION_STATUS.md)** - What exists vs. what's planned
- **[Development Roadmap](docs/DEVELOPMENT_ROADMAP.md)** - 6-phase implementation plan
- **[Quick Reference](docs/QUICK_REFERENCE.md)** - Working examples and recipes
- [Specification Document](specification-document_bioxen_fourier_vm_lib_ver0.0.0.01.md)
- [Execution Model](fourier-execution-model.md)
- [Research](research/)

## 🧪 Research Foundation

This library builds on peer-reviewed frequency domain analysis techniques for biological systems:

### Four-Lens Analysis System

BioXen uses a **research-backed four-lens approach** for comprehensive biological signal analysis:

| Lens | Primary Use | Key Library | Biology Application |
|------|-------------|-------------|---------------------|
| **Fourier (Lomb-Scargle)** | Irregular sampling, dominant frequencies | `astropy.timeseries.LombScargle` | Circadian rhythms, gene expression cycles |
| **Wavelet** | Non-stationary signals, time-frequency | `pywt` (PyWavelets) | Transient responses, cell cycle analysis |
| **Laplace** | Stability, control theory | `scipy.signal.TransferFunction` | Metabolic pathway control, system stability |
| **Z-Transform** | Discrete sampling, digital filters | `python-control` | Experimental time-series, sampled data |

**Why Four Lenses?**
- Biological signals are **non-stationary** (conditions change over time) → Wavelet essential
- Biological sampling is **irregular** (real-world constraints) → Lomb-Scargle is the standard
- Different biological questions require different analytical approaches
- Multi-lens validation increases confidence in findings

### Research Background

- **Spectral dynamics** in systems biology (Van Dongen 1999, Hughes et al. 2009)
- **Lomb-Scargle Periodogram**: Gold standard for biological rhythms (Scargle 1982, Ruf 1999)
- **Wavelet analysis**: Essential for non-stationary biological signals (Wu et al. 2016)
- **Higher-order spectral analysis**: Nonlinear interactions (Nikias & Petropulu 1993)
- **Circadian Rhythm Modeling**: Astronomical time cycles for accurate biological timing
- **Metabolic Oscillation Analysis**: Frequency domain studies of cellular processes

See `research/Frequency Domain Analysis in Biology.md` and interactive demos in `research/interactive-fourier-series/lenses/` for detailed research background.

## 🔧 Development

### Setup Development Environment
```bash
# Install in development mode
pip install -e .

# Run tests
python -m pytest tests/

# Check dependencies
./check_dependencies.sh
```

### Project Structure
- `src/`: Main library code
- `tests/`: Unit tests
- `examples/`: Usage examples
- `research/`: Research materials and analysis
- `recycle-bin/`: Archived legacy code

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Based on research in computational biology and systems biology
- Inspired by JCVI Syn3A and minimal cell research
- Built with modern Python practices and factory patterns

## 📞 Support

For questions, issues, or contributions:
- GitHub Issues: [Report bugs or request features](https://github.com/aptitudetechnology/BioXen_Fourier_lib/issues)
- Documentation: See specification document and code docstrings

---

**BioXen Fourier VM Library** - Virtualizing biology for research and simulation with advanced temporal modeling and frequency domain analysis.