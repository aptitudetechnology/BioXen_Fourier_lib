# Prompt: Refactor orthogonal.py into a Generic Modular Plugin Architecture

## Objective
Refactor the monolithic `orthogonal.py` chassis implementation into a generic, pluggable architecture that can load and execute ANY engineered genome (like `ol-fi-modem.fasta`) without hardcoding specific protocol logic. The chassis provides the infrastructure; the FASTA files contain the actual implementation.

## Current State Analysis
The existing `OrthogonalChassis` class needs to evolve from a simple synthetic cell platform into a **generic biological plugin host** that can dynamically load, validate, and execute engineered genomes without knowing their specific functionality beforehand.

## Required Modular Architecture

### 1. Core Chassis Structure (Generic Plugin Host)
```
src/chassis/orthogonal/
├── __init__.py                 # Main OrthogonalChassis class (plugin orchestrator)
├── base_genome.py             # Base genome loading/management (JCVI-Syn3A foundation)
├── plugin_loader.py           # Generic engineered genome loading and validation
├── resource_manager.py        # Resource allocation and VM management  
├── isolation_manager.py       # VM isolation and orthogonal code management
├── execution_engine.py        # Generic execution environment for loaded genomes
└── interfaces/
    ├── __init__.py
    ├── genome_interface.py    # Standard interface for engineered genomes
    ├── resource_interface.py  # Resource allocation interface
    └── communication_interface.py  # Generic communication abstraction
```

### 2. Plugin Architecture Specifications

#### 2.1 Main Orchestrator (`__init__.py` - OrthogonalChassis)
- **Generic Plugin Host**: Load ANY engineered genome without prior knowledge
- Inherit from `BaseChassis`
- Provide standardized interfaces for genome plugins
- Handle initialization sequence for unknown genomes
- Manage plugin lifecycle (load, validate, execute, cleanup)

#### 2.2 Base Genome Manager (`base_genome.py`) 
- Load foundational genomes (JCVI-Syn3A, minimal natural genomes)
- Provide **essential cellular services** that any plugin can use
- Manage base genome resource pool
- **Service Provider**: Offer ribosomes, ATP, basic metabolic pathways to plugins

#### 2.3 Plugin Loader (`plugin_loader.py`)
- **Generic FASTA Parser**: Load any `.fasta` engineered genome
- **Metadata Extraction**: Parse genome headers for resource requirements, interfaces
- **Validation Engine**: Ensure plugin compatibility with base genome
- **Dynamic Loading**: No hardcoded knowledge of specific protocols
- **Dependency Resolution**: Handle plugin requirements and conflicts

#### 2.4 Resource Manager (`resource_manager.py`)
- **Resource Allocation API**: Provide standardized resource allocation to any plugin
- **Quota Management**: Enforce resource limits per plugin
- **Resource Discovery**: Let plugins query available resources
- **Performance Monitoring**: Track resource usage across all loaded plugins

#### 2.5 Isolation Manager (`isolation_manager.py`)
- **Generic Isolation**: Provide orthogonal code isolation for any plugin type
- **Namespace Management**: Prevent conflicts between different loaded genomes
- **Security Boundaries**: Ensure plugins cannot interfere with each other
- **Code Assignment**: Dynamically assign orthogonal codes to plugins

#### 2.6 Execution Engine (`execution_engine.py`)
- **Generic Execution Environment**: Run any loaded genome's functionality
- **Event Loop**: Handle plugin lifecycle events, communication, resource requests
- **Plugin Coordination**: Manage interactions between multiple loaded plugins
- **Error Handling**: Generic error handling for any plugin type

### 3. Standardized Plugin Interfaces

#### 3.1 Genome Interface (`interfaces/genome_interface.py`)
- **Standard Plugin API**: Define how ANY engineered genome should expose its functionality
- **Metadata Format**: Standard format for genome headers describing capabilities
- **Lifecycle Hooks**: Initialize, execute, cleanup methods that any plugin must implement
- **Resource Declaration**: How plugins declare their resource needs

#### 3.2 Resource Interface (`interfaces/resource_interface.py`)
- **Resource Request API**: Standard way for plugins to request chassis resources
- **Resource Types**: Define standard resource types (ribosomes, ATP, memory, etc.)
- **Allocation Callbacks**: How plugins respond to resource allocation/deallocation

#### 3.3 Communication Interface (`interfaces/communication_interface.py`)
- **Generic Communication API**: Standard interface for ANY communication protocol
- **Signal Abstraction**: Generic chemical/molecular signal interface
- **Address Resolution**: Generic addressing scheme that works for any protocol
- **Protocol Agnostic**: Works for Ol-Fi, but also any future communication protocol

## Key Design Principles

### 4.1 Protocol Agnostic
- **Zero Hardcoding**: No specific knowledge of Ol-Fi, MVOC, or any particular protocol
- **Runtime Discovery**: Learn about loaded genome capabilities at runtime
- **Generic Interfaces**: All APIs work for ANY type of engineered genome
- **Future Proof**: Can load communication protocols, computation engines, sensors, etc.

### 4.2 FASTA-Driven Implementation
- **Code in FASTA**: All actual functionality encoded in the `.fasta` file
- **Metadata in Headers**: Resource requirements, interfaces, capabilities in FASTA headers
- **Self-Describing**: Genomes describe their own requirements and capabilities
- **Chassis Independence**: Same FASTA file should work on any compatible chassis

### 4.3 Plugin Ecosystem
- **Multiple Simultaneous Plugins**: Load multiple engineered genomes simultaneously
- **Plugin Composition**: Allow plugins to work together (e.g., communication + computation)
- **Plugin Discovery**: Runtime discovery of available engineered genomes
- **Plugin Markets**: Architecture supports sharing/distributing engineered genomes

### 4.4 Resource Management
- **Fair Allocation**: Distribute chassis resources fairly among plugins
- **Quality of Service**: Different resource priorities for different plugin types
- **Resource Pools**: Shared resource pools that any plugin can access
- **Monitoring**: Track resource usage for optimization and debugging

## FASTA File Requirements

### 5.1 Standard FASTA Header Format
```
>PLUGIN_METADATA|name=ol-fi-modem|version=1.0|type=communication|resources=ribosomes:50,atp:1000|interfaces=communication_interface
>RESOURCE_REQUIREMENTS|ribosomes=50|atp=1000|memory_kb=4096
>COMMUNICATION_METADATA|protocol=ol-fi|addressing=chemical|encoding=mvoc
[genetic sequence data]
```

### 5.2 Plugin Capability Declaration
- **Interface Compliance**: Declare which chassis interfaces the plugin implements
- **Resource Bounds**: Maximum and minimum resource requirements
- **Dependencies**: Other plugins or base genome features required
- **Compatibility**: Chassis versions and base genomes supported

## Implementation Deliverables

1. **Generic Plugin Architecture** - No protocol-specific code
2. **FASTA Loading Engine** - Parse any engineered genome format
3. **Resource Allocation Framework** - Generic resource management
4. **Execution Environment** - Run any loaded genome
5. **Standard Interfaces** - API definitions for plugin development
6. **Test Suite** - Test with multiple different FASTA files (not just Ol-Fi)
7. **Plugin Development Guide** - How to create new engineered genomes
8. **Migration Path** - Move from monolithic to plugin architecture

## Success Criteria
- Load and execute `ol-fi-modem.fasta` without hardcoded Ol-Fi knowledge
- Load multiple different engineered genomes simultaneously
- Generic enough to support future unknown protocols
- Clean plugin interfaces enabling third-party genome development
- Performance scalable with number of loaded plugins
- Comprehensive testing with diverse FASTA plugin types

The chassis should be like a **biological operating system** - it provides services and infrastructure, but the actual applications (engineered genomes) provide their own functionality. The chassis should work equally well with communication protocols, computational circuits, sensor networks, or any other type of engineered biological system.