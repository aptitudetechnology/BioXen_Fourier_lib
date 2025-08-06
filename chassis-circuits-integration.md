# Chassis and Circuits Integration Report

## 1. Current Integration Points

- **Chassis Classes:**
  - Chassis modules (`base.py`, `ecoli.py`, `yeast.py`, `orthogonal.py`) define resource management and VM isolation.
  - No direct import of `circuits.py` in chassis modules, but resource allocation and VM management are designed to support genetic circuit instantiation.
  - Chassis classes expose APIs like `allocate_resources(vm_id, resource_request)`, `deallocate_resources(vm_id)`, and `create_isolation_environment(vm_id)` for VM/circuit management.

- **Circuits System:**
  - Modular circuits (in `src/genetics/circuits/core/`, `library/`, `optimization/`, `exports/`) provide genetic elements, circuit templates, and resource-aware schedulers.
  - Scheduler circuits (e.g., round-robin, priority, resource-aware) are designed to allocate biological resources (ribosomes, ATP, memory) across VMs, matching chassis resource APIs.

- **APIs/Interfaces:**
  - Chassis exposes resource status and allocation APIs.
  - Circuits library provides functions to create scheduler circuits for VMs, which chassis can instantiate and manage.

---

## 2. Data Flow Analysis

- **Chassis → Circuits:**
  - Chassis modules manage VM lifecycles and allocate resources.
  - When a new VM/circuit is instantiated, chassis calls resource allocation methods and can select appropriate scheduler circuits from the circuits library.
  - Data structures passed: `resource_request` dicts (ribosomes, ATP, memory), VM IDs, and possibly genetic circuit objects.

- **Circuits → Chassis:**
  - Scheduler circuits monitor and regulate resource usage, reporting back to chassis via resource status APIs.
  - Circuits can be instantiated with VM-specific parameters, which chassis provides.

- **Resource Access:**
  - Chassis maintains `ChassisResources` (available ribosomes, ATP, memory).
  - Circuits use these resources via scheduler and monitoring circuits, adapting genetic element strengths (e.g., RBS) to match available resources.

---

## 3. Resource Management

- **Coordination:**
  - Chassis is the authority for resource allocation; circuits request resources via scheduler circuits.
  - VM boundaries are maintained by tracking active VMs and their resource allocations in chassis (`active_vms` dict).
  - Isolation mechanisms:
    - Chassis provides `create_isolation_environment(vm_id)` and `cleanup_vm_environment(vm_id)` for VM/circuit isolation.
    - Scheduler circuits in the library (e.g., round-robin, priority) enforce resource partitioning at the genetic level.

---

## 4. Plugin/Engineered Genome Loading

- **Engineered Genomes (FASTA):**
  - Chassis loads engineered genomes (e.g., `ol-fi-modem.fasta`) and coordinates circuit compilation.
  - Circuits system (BioCompiler, GeneticElement) parses FASTA files, assembles genetic circuits, and returns circuit objects to chassis.
  - Chassis allocates resources and instantiates isolation environments for each loaded genome/circuit.

- **Data Flow:**
  - FASTA file → Circuits/BioCompiler → GeneticCircuit object → Chassis resource allocation/isolation → Scheduler circuit selection.

---

## 5. Current Limitations

- **Coupling:**
  - Chassis and circuits are loosely coupled via resource APIs and VM management, but lack a unified plugin interface.
  - No direct chassis import of circuits modules; integration relies on external orchestration (e.g., workflow manager).
  - To support a generic plugin system, chassis should expose APIs for circuit registration, resource negotiation, and genome loading, and circuits should provide plugin hooks for chassis interaction.

- **Dependencies:**
  - Specific chassis types (e.g., orthogonal) may require custom circuit elements (e.g., MVOC synthesis) not present in standard circuits library.
  - Scheduler circuits are generic, but may need chassis-specific adaptation for advanced features (e.g., Ol-Fi modem support).

---

## 6. JCVI Integration

- **Coordination:**
  - JCVI genome formats are processed by circuits system (BioCompiler, GeneticElement) and passed to chassis for resource allocation and VM instantiation.
  - Data transformation occurs in circuits modules (e.g., `jcvi_format.py` in exports), converting JCVI data to genetic circuit objects.
  - Chassis manages VM lifecycles and resource allocation for JCVI-derived circuits.

---

## Code Examples

### Chassis Resource Allocation (orthogonal.py)
```python
def allocate_resources(self, vm_id: str, resource_request: Dict[str, Any]) -> bool:
    if self.current_resources.available_ribosomes >= resource_request.get("ribosomes", 1):
        self.current_resources.available_ribosomes -= resource_request.get("ribosomes", 1)
        self.active_vms[vm_id] = resource_request
        return True
    return False
```

### Scheduler Circuit Creation (schedulers.py)
```python
def create_round_robin_scheduler(vm_list: list) -> GeneticCircuit:
    # Add RBS for each VM with equal strength
    for vm_id in vm_list:
        # ...create RBS elements for each VM...
    # ...return GeneticCircuit object...
```

### Chassis Isolation Environment
```python
def create_isolation_environment(self, vm_id: str) -> bool:
    # Simulate isolation environment creation
    # ...existing code...
```

### Engineered Genome Loading (workflow manager, pseudocode)
```python
# Load FASTA, compile circuit, allocate resources
genome = load_fasta("ol-fi-modem.fasta")
circuit = BioCompiler.compile(genome)
chassis.allocate_resources(vm_id, circuit.resource_requirements)
chassis.create_isolation_environment(vm_id)
```

---

## Recommendations for Refactoring

- **Expose Chassis Plugin API:**
  - Methods for circuit registration, resource negotiation, genome loading.
- **Circuits Plugin Hooks:**
  - Allow circuits to register new element types, resource requirements, and isolation needs.
- **Unified Data Structures:**
  - Standardize resource request/response objects between chassis and circuits.
- **Workflow Manager:**
  - Centralize orchestration of genome loading, circuit compilation, and chassis resource management.

---

This analysis provides a roadmap for decoupling and refactoring both systems to support a generic plugin architecture, enabling any chassis to load engineered genomes and circuits.py to build appropriate genetic circuits for any plugin type.
