# Factory Pattern API Implementation Report - Prompt 4

## Project Context

This project is a fork of BioXen-jcvi (https://github.com/aptitudetechnology/BioXen-jcvi) and is now called BioXen_jcvi_vm_lib (https://github.com/aptitudetechnology/BioXen_jcvi_vm_lib).

## Objective

Transform the codebase into a Python library that can be used by BioXen-jcvi by implementing a factory pattern API layer as a **non-disruptive wrapper** over existing functionality.

## Implementation Plan

### 1. Core API Components

#### `src/api/biological_vm.py`
- **Abstract `BiologicalVM` base class**
  - Delegates to existing hypervisor methods
  - Maintains compatibility with current architecture
- **Concrete VM classes:**
  - `Syn3AVM` - Wraps genome-specific logic for Syn3A
  - `EColiVM` - Wraps genome-specific logic for E.coli
  - Each class maintains references to existing hypervisor and genome integrator instances

#### `src/api/factory.py`
- **`create_bio_vm(vm_id, vm_type, config)`** function
  - Instantiates VM classes and registers with existing hypervisor
  - **VM type mapping:**
    - "syn3a" → `Syn3AVM`
    - "ecoli" → `EColiVM`
    - "minimal_cell" → `MinimalCellVM`

#### `src/api/resource_manager.py`
- **`BioResourceManager` class**
  - Wraps existing ribosome/ATP/memory management
  - Interfaces with current resource tracking without replacing it
  - Maintains backward compatibility

#### `src/api/config_manager.py`
- **Unified config handling**
  - Works with existing dictionary patterns
  - Config validation and defaults for different VM types
  - Seamless integration with current configuration system

### 2. Integration Strategy

#### Integration Points
- Add registration mechanisms in existing files to register VMs created via factory
- Ensure factory-created VMs work with current hypervisor system
- Maintain all existing functionality without modification

#### Key Constraints
- **Non-disruptive implementation**: All existing functionality in `src/hypervisor/core.py` and `interactive_bioxen.py` must remain unchanged
- **Pure API layer addition**: No modification to core business logic
- **Backward compatibility**: Existing interfaces and workflows must continue to work

### 3. Architecture Benefits

#### Modularity
- Clean separation between API layer and core functionality
- Factory pattern enables easy extension for new VM types
- Resource management abstraction simplifies usage

#### Maintainability
- Wrapper pattern preserves existing code stability
- Clear separation of concerns
- Easy to test and validate

#### Extensibility
- Simple addition of new biological VM types
- Configurable resource allocation patterns
- Flexible configuration management

## Implementation Status

- [ ] Create `src/api/` directory structure
- [ ] Implement `BiologicalVM` abstract base class
- [ ] Implement concrete VM classes (`Syn3AVM`, `EColiVM`)
- [ ] Create factory function with type mapping
- [ ] Implement `BioResourceManager` wrapper
- [ ] Create unified config management system
- [ ] Add integration points to existing hypervisor
- [ ] Test factory pattern with existing workflows
- [ ] Validate non-disruptive integration
- [ ] Document API usage patterns

## Next Steps

1. Begin with creating the directory structure: `src/api/`
2. Implement the abstract `BiologicalVM` class
3. Create the first concrete implementation (`Syn3AVM`)
4. Test integration with existing hypervisor system
5. Incrementally add remaining components while ensuring compatibility

This approach ensures a smooth transition to a library-based architecture while preserving all existing functionality and maintaining the project's current operational capabilities.