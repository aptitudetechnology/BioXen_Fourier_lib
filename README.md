# BioXen Fourier VM Library

[![Version](https://img.shields.io/badge/version-0.0.0.01-blue.svg)](https://github.com/aptitudetechnology/BioXen_Fourier_lib)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A Python library for virtualizing biological cells using a factory pattern, enabling programmatic creation and management of biological virtual machines (VMs) for research and simulation. Features advanced time simulation for circadian rhythm studies and Fourier analysis of metabolic oscillations.

## 🌟 Features

- **Factory Pattern API**: Create and manage biological VMs with simple, consistent interfaces
- **Multiple Biological Types**: Support for syn3a, ecoli, yeast, orthogonal, and future mammalian/plant chassis
- **VM Infrastructures**: Basic and XCP-ng virtualization options
- **Genome Schema**: Standardized format for biological genome files with validation
- **Resource Management**: Allocate and monitor biological resources (ATP, ribosomes, etc.)
- **Hypervisor Control**: Full lifecycle management of biological VMs
- **Time Simulation**: Pure Earth astronomical cycles for circadian rhythm modeling
- **Fourier Analysis**: Frequency domain analysis of metabolic oscillations and gene expression
- **Extensible Architecture**: Modular design for adding new chassis and capabilities

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

## 🏗️ Architecture

```
src/bioxen_fourier_vm_lib/
├── api/                    # Factory API and VM classes
├── chassis/               # Cellular chassis implementations
├── genome/                # Genome schema and parsing
├── hypervisor/            # VM lifecycle management
│   ├── core.py           # Main hypervisor logic
│   └── TimeSimulator.py  # Astronomical time cycles
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

This library builds on frequency domain analysis techniques for biological systems:

- Spectral dynamics in systems biology
- Fourier analysis of gene regulatory networks
- Wavelet analysis for non-stationary signals
- Higher-order spectral analysis for nonlinear interactions
- **Circadian Rhythm Modeling**: Astronomical time cycles for accurate biological timing
- **Metabolic Oscillation Analysis**: Frequency domain studies of cellular processes

See `research/Frequency Domain Analysis in Biology.md` for detailed research background.

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