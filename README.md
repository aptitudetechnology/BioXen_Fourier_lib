# BioXen_jcvi_vm_lib

**Interactive Biological Hypervisor Library for Real Bacterial Genomes**

---

## Project Overview

BioXen_jcvi_vm_lib is a Python library forked from [BioXen-jcvi](https://github.com/aptitudetechnology/BioXen-jcvi), designed to provide an interactive biological hypervisor for virtualizing real bacterial genomes. This project introduces a modular API layer using the factory pattern, enabling seamless integration and extension of biological VM types.

> **Educational Sandbox:** This library is for educational use only. Results are not biologically validated and should not be used for professional research.

---

## Key Features

- **Factory Pattern API Layer:**
  - Non-disruptive wrapper over existing hypervisor and genome integrator logic
  - Easily instantiate and register biological VMs
- **Modular VM Classes:**
  - Abstract `BiologicalVM` base class
  - Concrete implementations: `Syn3AVM`, `EColiVM`, `MinimalCellVM`
- **Resource Management:**
  - `BioResourceManager` wraps ribosome/ATP/memory management
- **Unified Configuration:**
  - Centralized config manager for VM types
- **Backward Compatibility:**
  - All existing functionality remains unchanged

---

## Quickstart

1. **Create a Biological VM:**
   ```python
   from src.api.factory import create_bio_vm

   vm = create_bio_vm(vm_id="demo1", vm_type="syn3a", config={"genome": "NC_000000"})
   # VM is registered with the hypervisor automatically
   ```
2. **Manage Resources:**
   ```python
   from src.api.resource_manager import BioResourceManager

   resource_mgr = BioResourceManager(vm)
   resource_mgr.allocate_atp(100)
   ```
3. **Configure VM:**
   ```python
   from src.api.config_manager import ConfigManager

   config = ConfigManager.load_defaults(vm_type="syn3a")
   ```

---

## Architecture

- `src/api/biological_vm.py`: Abstract and concrete VM classes
- `src/api/factory.py`: Factory function for VM instantiation
- `src/api/resource_manager.py`: Resource management wrapper
- `src/api/config_manager.py`: Unified config handling

---

## Status & Roadmap

- [x] MVP API design
- [ ] Implement all core API modules
- [ ] Integrate with existing hypervisor
- [ ] Add documentation and usage examples

---

## License

MIT License

---

For more details, see `factory-pattern-api-prompt4-report.md` and `factory-pattern-api.prompt4`.
