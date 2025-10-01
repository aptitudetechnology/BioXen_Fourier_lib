# BioXen Fourier VM Library

[![Version](https://img.shields.io/badge/version-0.0.0.01-blue.svg)](https://github.com/aptitudetechnology/BioXen_Fourier_lib)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A Python library for virtualizing biological cells using a factory pattern, enabling programmatic creation and management of biological virtual machines (VMs) for research and simulation. Features advanced time simulation for circadian rhythm studies and Fourier analysis of metabolic oscillations.

## ✨ Features

- **Biological VM Virtualization**: Create synthetic cell simulations
- **Four-Lens Analysis System**: Multi-method frequency domain analysis optimized for biological signals
  - **Fourier (Lomb-Scargle)**: Industry standard for irregular sampling in biology
  - **Wavelet**: Essential for non-stationary signals and time-frequency localization
  - **Laplace**: Control theory and system stability analysis
  - **Z-Transform**: Digital signal processing for sampled data
- **Time Simulation**: Accurate solar/lunar cycles for circadian studies
- **Hypervisor System**: Manage multiple biological VMs
- **Factory Pattern API**: Clean, extensible architecture
- **Interactive Learning Tools**: Web-based demos with decision trees and validation

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

## 📋 API Overview

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

## 📚 Documentation

- [Specification Document](specification-document_bioxen_fourier_vm_lib_ver0.0.0.01.md)
- [Execution Model](execution-model.md)
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