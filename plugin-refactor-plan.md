# BioXen Plugin Architecture Refactoring Plan

Based on the chassis-circuits integration analysis, here's a comprehensive refactoring plan to transform the current loose coupling into a robust plugin architecture.

## Phase 1: Standardize Integration (Foundation)

### 1.1 Create Plugin Interface System
```
src/plugin_system/
├── __init__.py
├── interfaces/
│   ├── __init__.py
│   ├── plugin_interface.py      # Base plugin contract
│   ├── resource_interface.py    # Standardized resource requests
│   ├── signal_interface.py      # Generic communication abstraction
│   └── lifecycle_interface.py   # Plugin lifecycle management
├── registry/
│   ├── __init__.py
│   ├── plugin_registry.py       # Central plugin management
│   ├── capability_registry.py   # Track plugin capabilities
│   └── metadata_parser.py       # FASTA header parsing
└── orchestrator/
    ├── __init__.py
    ├── plugin_orchestrator.py   # Automate FASTA→Circuit→Chassis pipeline
    └── workflow_coordinator.py  # Replace manual workflow manager
```

### 1.2 Standardize Resource Data Structures
**Current:** Ad-hoc dictionaries passed between chassis and circuits
**New:** Formal resource contract classes

```python
# src/plugin_system/interfaces/resource_interface.py
@dataclass
class ResourceRequest:
    plugin_id: str
    ribosomes: int
    atp: float
    memory_kb: int
    custom_resources: Dict[str, Any]  # For plugin-specific needs
    isolation_level: IsolationLevel
    
@dataclass
class ResourceAllocation:
    allocated: ResourceRequest
    scheduler_circuit: GeneticCircuit
    isolation_environment: str
    vm_id: str
```

### 1.3 Formalize Plugin Lifecycle
**Replace:** Manual `load_fasta() → compile() → allocate()` with automated plugin lifecycle

```python
# src/plugin_system/interfaces/lifecycle_interface.py
class PluginLifecycle:
    def discover(self, fasta_path: str) -> PluginMetadata
    def validate(self, plugin_metadata: PluginMetadata) -> ValidationResult
    def compile(self, plugin_metadata: PluginMetadata) -> GeneticCircuit
    def allocate(self, circuit: GeneticCircuit, chassis: BaseChassis) -> ResourceAllocation
    def initialize(self, allocation: ResourceAllocation) -> bool
    def execute(self, allocation: ResourceAllocation) -> ExecutionContext
    def cleanup(self, allocation: ResourceAllocation) -> bool
```

## Phase 2: Plugin Discovery and Management

### 2.1 Enhanced FASTA Metadata System
**Extend:** Current basic FASTA loading to include rich plugin metadata

```
# Enhanced FASTA header format
>PLUGIN_METADATA|name=ol-fi-modem|version=1.0|type=communication
>CAPABILITIES|interfaces=signal_interface,resource_interface|protocols=mvoc,chemical
>RESOURCES|ribosomes=50|atp=1000|memory_kb=4096|isolation=orthogonal
>DEPENDENCIES|base_genome=syn3a|chassis_types=orthogonal|circuits=scheduler,monitor
>SIGNALS|input=mvoc_chemical|output=mvoc_response|addressing=chemical_gradient
[genetic sequence data]
```

### 2.2 Dynamic Circuit Compilation
**Replace:** Static BioCompiler with dynamic plugin-aware compiler

```python
# Enhanced src/genetics/circuits/core/compiler.py
class PluginAwareBioCompiler:
    def compile_for_plugin(self, plugin_metadata: PluginMetadata, 
                          chassis_capabilities: ChassisCapabilities) -> GeneticCircuit:
        # Dynamic compilation based on plugin requirements
        # Select appropriate circuit elements for plugin type
        # Optimize for target chassis capabilities
        # Generate plugin-specific scheduler circuits
```

### 2.3 Plugin Registry System
**New:** Central registry managing all loaded plugins

```python
# src/plugin_system/registry/plugin_registry.py
class PluginRegistry:
    def register_plugin(self, plugin_path: str) -> PluginID
    def get_plugin_capabilities(self, plugin_id: PluginID) -> CapabilitySet
    def find_compatible_plugins(self, requirements: PluginRequirements) -> List[PluginID]
    def get_plugin_dependencies(self, plugin_id: PluginID) -> DependencyGraph
    def validate_plugin_compatibility(self, plugin_ids: List[PluginID]) -> ValidationResult
```

## Phase 3: Chassis Modernization

### 3.1 Refactor Chassis for Plugin Support
**Extend:** Current chassis classes to support plugin architecture

```python
# src/chassis/orthogonal/__init__.py - Refactored OrthogonalChassis
class OrthogonalChassis(BaseChassis):
    def __init__(self):
        super().__init__()
        self.plugin_orchestrator = PluginOrchestrator(self)
        self.plugin_registry = PluginRegistry()
        
    def load_plugin(self, fasta_path: str) -> PluginExecution:
        return self.plugin_orchestrator.load_and_execute(fasta_path)
        
    def get_compatible_plugins(self) -> List[PluginMetadata]:
        return self.plugin_registry.find_compatible_plugins(self.get_capabilities())
```

### 3.2 Enhanced Resource Management
**Upgrade:** Current simple resource allocation to plugin-aware system

```python
# src/chassis/orthogonal/resource_manager.py
class PluginResourceManager:
    def allocate_for_plugin(self, plugin_metadata: PluginMetadata) -> ResourceAllocation
    def deallocate_plugin(self, plugin_id: PluginID) -> bool
    def rebalance_resources(self) -> None  # Dynamic rebalancing between plugins
    def get_resource_utilization(self) -> ResourceUtilization
    def enforce_resource_quotas(self) -> None
```

### 3.3 Plugin Isolation Management
**Enhance:** Current VM isolation for multi-plugin environments

```python
# src/chassis/orthogonal/isolation_manager.py
class PluginIsolationManager:
    def create_plugin_environment(self, plugin_metadata: PluginMetadata) -> IsolationEnvironment
    def enforce_plugin_boundaries(self) -> None
    def handle_cross_plugin_communication(self, sender: PluginID, receiver: PluginID, signal: Signal) -> bool
    def detect_plugin_conflicts(self) -> List[ConflictReport]
```

## Phase 4: Circuit System Enhancement

### 4.1 Plugin-Aware Circuit Library
**Restructure:** Current circuit library for plugin modularity

```
src/genetics/circuits/
├── plugin_support/
│   ├── plugin_circuit_factory.py    # Generate circuits for any plugin type
│   ├── dynamic_scheduler.py         # Plugin-aware resource scheduling
│   └── signal_router.py            # Route signals between plugins
├── core/
│   ├── elements.py                 # Enhanced for plugin building blocks
│   ├── compiler.py                 # Plugin-aware compilation
│   └── validation.py               # Plugin circuit validation
└── library/
    ├── communication/              # Generic communication circuits
    ├── computation/               # Generic computational circuits
    ├── sensing/                  # Generic sensor circuits
    └── protocols/               # Protocol-specific implementations
```

### 4.2 Generic Signal Abstraction
**Abstract:** Current MVOC-specific logic to generic signal interface

```python
# src/genetics/circuits/plugin_support/signal_router.py
class GenericSignalRouter:
    def route_signal(self, signal: GenericSignal, addressing: AddressingScheme) -> RoutingResult
    def register_signal_handler(self, plugin_id: PluginID, signal_type: SignalType) -> bool
    def broadcast_signal(self, signal: GenericSignal, scope: BroadcastScope) -> None
    def create_signal_isolation(self, plugin_id: PluginID) -> SignalIsolation
```

## Phase 5: Integration and Testing

### 5.1 Automated Integration Testing
**New:** Comprehensive testing framework for plugin system

```
tests/plugin_system/
├── integration/
│   ├── test_plugin_lifecycle.py
│   ├── test_multi_plugin_loading.py
│   └── test_chassis_plugin_integration.py
├── plugins/
│   ├── test_ol_fi_modem.py         # Validate ol-fi-modem.fasta
│   ├── test_communication_plugins.py
│   └── test_computation_plugins.py
└── performance/
    ├── test_resource_allocation.py
    ├── test_plugin_isolation.py
    └── test_scalability.py
```

### 5.2 Migration Strategy
**Gradual:** Maintain backward compatibility during transition

1. **Phase 1-2:** New plugin system runs alongside existing manual workflow
2. **Phase 3:** Chassis classes support both old and new interfaces
3. **Phase 4:** Circuit library maintains backward compatibility
4. **Phase 5:** Full migration with deprecation of old interfaces

### 5.3 Plugin Development Kit
**New:** Tools for creating new plugins

```
tools/plugin_dev/
├── plugin_template_generator.py    # Generate FASTA templates
├── plugin_validator.py            # Validate plugin compliance
├── resource_estimator.py          # Estimate plugin resource needs
└── compatibility_checker.py       # Check chassis compatibility
```

## Success Metrics

1. **ol-fi-modem.fasta loads automatically** without manual orchestration
2. **Multiple plugins run simultaneously** with proper isolation
3. **New plugin types** can be created without modifying core chassis code
4. **Resource utilization** is optimized across all loaded plugins
5. **Plugin development** is streamlined with clear interfaces and tools

## Implementation Timeline

- **Week 1-2:** Phase 1 - Plugin interfaces and basic registry
- **Week 3-4:** Phase 2 - FASTA metadata parsing and dynamic compilation  
- **Week 5-6:** Phase 3 - Chassis refactoring for plugin support
- **Week 7-8:** Phase 4 - Circuit library enhancement
- **Week 9-10:** Phase 5 - Integration testing and migration tools

This plan transforms the current loose coupling into a robust plugin architecture while maintaining the excellent foundation that already exists.