# BioXen Genetic Circuits Modularization Plan

## Overview
This document outlines the plan to refactor the monolithic `circuits.py` file into a modular architecture under the `circuits/` directory. The goal is to organize laboratory-ready genetic circuits by function while maintaining the groundbreaking capabilities that make BioXen's biological hypervisor implementable.

## Current State Analysis
The existing `circuits.py` contains:
- **ATP Monitoring Circuits**: Promoter sequences sensitive to cellular energy levels
- **Ribosome Scheduling**: RBS variants for resource prioritization
- **Orthogonal RNA Polymerase Systems**: Memory isolation mechanisms
- **Protein Tagging & Degradation**: VM-specific identification and cleanup
- **BioCompiler**: DNA sequence assembly and circuit generation

## Proposed Modular Structure

### 1. Core Modules

```
circuits/
├── __init__.py                 # Main exports and circuit registry
├── circuits.md                 # This planning document
├── core/
│   ├── __init__.py
│   ├── elements.py             # GeneticElement base classes
│   ├── compiler.py             # BioCompiler for DNA assembly
│   └── registry.py             # Circuit component registry
├── monitoring/
│   ├── __init__.py
│   ├── atp_sensors.py          # ATP monitoring circuits
│   ├── ribosome_sensors.py     # Ribosome utilization monitoring
│   └── biosensors.py           # General cellular state monitoring
├── scheduling/
│   ├── __init__.py
│   ├── rbs_variants.py         # Ribosome binding site variants
│   ├── promoter_strength.py    # Promoter-based scheduling
│   └── priority_systems.py     # Resource priority mechanisms
├── isolation/
│   ├── __init__.py
│   ├── orthogonal_rnap.py      # RNA polymerase variants
│   ├── genetic_codes.py        # Orthogonal translation systems
│   └── compartments.py         # Membrane compartmentalization
├── vm_management/
│   ├── __init__.py
│   ├── protein_tags.py         # VM-specific protein tagging
│   ├── degradation.py          # Protein cleanup systems
│   └── state_control.py        # VM state management circuits
└── presets/
    ├── __init__.py
    ├── hypervisor_core.py       # Complete hypervisor circuits
    ├── minimal_vm.py            # Basic VM circuit sets
    └── chassis_specific.py      # E.coli/Yeast optimized circuits
```

## Module Specifications

### 2.1 Core Module (`core/`)

**Purpose**: Foundational classes and compilation infrastructure

**Files**:
- `elements.py`: Base `GeneticElement` class, sequence validation
- `compiler.py`: `BioCompiler` class for DNA assembly and spacer management
- `registry.py`: Component discovery and validation system

**Key Classes**:
```python
class GeneticElement:
    name: str
    sequence: str
    element_type: str
    regulation_target: Optional[str]
    
class BioCompiler:
    def compile_hypervisor(self, vm_configs) -> Dict[str, str]
    def _assemble_circuit(self, circuit) -> str
```

### 2.2 Monitoring Module (`monitoring/`)

**Purpose**: Circuits for sensing cellular state and resource levels

**ATP Sensors** (`atp_sensors.py`):
- ATP-sensitive promoters
- Energy level reporters
- Metabolic state indicators

**Ribosome Sensors** (`ribosome_sensors.py`):
- Ribosome utilization reporters
- Translation bottleneck detection
- Protein synthesis rate monitoring

### 2.3 Scheduling Module (`scheduling/`)

**Purpose**: Resource allocation and prioritization mechanisms

**RBS Variants** (`rbs_variants.py`):
- Strong/Medium/Weak ribosome binding sites
- VM-specific translation initiation
- Natural time-slicing through binding affinity

**Priority Systems** (`priority_systems.py`):
- Essential vs. non-essential gene prioritization
- Stress-response triggered scheduling
- Dynamic resource reallocation

### 2.4 Isolation Module (`isolation/`)

**Purpose**: Preventing crosstalk between VMs

**Orthogonal RNA Polymerases** (`orthogonal_rnap.py`):
- VM-specific RNA polymerase variants
- Cognate promoter recognition
- Transcriptional isolation

**Genetic Codes** (`genetic_codes.py`):
- Standard genetic code
- Amber suppression systems
- Synthetic amino acid incorporation

### 2.5 VM Management Module (`vm_management/`)

**Purpose**: VM lifecycle and state control

**Protein Tags** (`protein_tags.py`):
- His6, FLAG, and composite tags
- VM-specific protein identification
- Purification and tracking systems

**Degradation** (`degradation.py`):
- SsrA-like degradation tags
- VM-specific proteases
- Cleanup and garbage collection

## Implementation Strategy

### Phase 1: Extract Core Infrastructure
1. Create `core/elements.py` with `GeneticElement` base class
2. Move `BioCompiler` to `core/compiler.py`
3. Establish module imports and registry system

### Phase 2: Functional Separation
1. Extract ATP monitoring circuits to `monitoring/atp_sensors.py`
2. Move RBS variants to `scheduling/rbs_variants.py`
3. Separate RNA polymerase systems to `isolation/orthogonal_rnap.py`
4. Organize protein tags in `vm_management/protein_tags.py`

### Phase 3: Advanced Features
1. Add ribosome utilization monitoring
2. Implement priority-based scheduling
3. Expand orthogonal genetic code systems
4. Create degradation and cleanup mechanisms

### Phase 4: Preset Configurations
1. Create complete hypervisor circuit packages
2. Develop minimal VM starter kits
3. Optimize for specific chassis (E.coli, Yeast)

## Benefits of Modularization

### 1. **Laboratory Implementation**
- Researchers can import only needed circuit types
- Easy to synthesize individual components
- Clear separation of functions for debugging

### 2. **Extensibility**
- New monitoring systems can be added independently
- Alternative scheduling mechanisms can be compared
- Novel isolation techniques can be integrated

### 3. **Maintainability**
- Smaller, focused files are easier to understand
- Changes to one circuit type don't affect others
- Clear testing boundaries for each module

### 4. **Collaboration**
- Different teams can work on different circuit types
- Easy to contribute new variants or improvements
- Clear API boundaries between modules

## Migration Strategy

### Backward Compatibility
- Maintain original `circuits.py` as a compatibility layer
- Import all components through main `__init__.py`
- Gradual deprecation with clear migration path

### Testing Strategy
- Unit tests for each circuit module
- Integration tests for complete hypervisor systems
- Laboratory validation of synthesized circuits

### Documentation
- Detailed API documentation for each module
- Usage examples for common circuit combinations
- Laboratory protocols for circuit synthesis

## Laboratory Readiness

### DNA Synthesis Preparation
- All sequences validated for synthesis compatibility
- Restriction enzyme sites catalogued
- Cloning strategies documented

### Implementation Protocols
- Step-by-step assembly instructions
- Transformation and testing procedures
- Validation assays for circuit function

### Chassis Integration
- E.coli-specific optimizations
- Yeast expression considerations
- Cross-chassis compatibility testing

## Success Metrics

1. **Modular Independence**: Each circuit type can be used standalone
2. **Laboratory Validation**: Circuits function as designed when synthesized
3. **Extensibility**: New circuit types can be added without breaking existing code
4. **Research Impact**: Framework enables novel synthetic biology experiments

This modular architecture will transform BioXen from a conceptual framework into a practical toolkit for building biological hypervisors in real laboratory settings.