# BioXen Fourier VM Library Execution Model

## Overview

The BioXen Fourier VM Library provides an execution model for creating virtualizations of biological cells from genomic data. This model enables computational simulation and management of biological systems through a factory-based architecture that abstracts cellular processes into programmable virtual machines (VMs).

## Core Components

### 1. Genomic Data Input
- **Format**: BioXen .genome files containing standardized gene records
- **Schema**: `BioXenGeneRecord` with fields for gene ID, start position, length, type, strand, etc.
- **Validation**: Genome parser validates structure and compatibility with supported chassis

### 2. Cellular Chassis
- **Types**: E. coli, Yeast, Orthogonal (synthetic), Syn3A (minimal cell)
- **Capabilities**: Defined by `ChassisCapabilities` including ribosomes, ATP, organelles, metabolic pathways
- **Architecture**: Prokaryotic vs eukaryotic memory models

### 3. Hypervisor Layer
- **BioXenHypervisor**: Manages VM lifecycle, resource allocation, and execution
- **VM States**: CREATED, RUNNING, PAUSED, STOPPED, ERROR
- **Resource Management**: ATP, ribosomes, tRNA, RNA polymerase, amino acids, nucleotides

### 4. Biological VM Abstraction
- **Classes**: `BiologicalVM`, `BasicBiologicalVM`, `XCPngBiologicalVM`
- **Operations**: Start, stop, destroy, allocate resources, execute biological processes
- **Infrastructure**: Basic (lightweight) or XCP-ng (advanced virtualization)

## Execution Workflow

### Step 1: Genome Loading and Parsing
```python
from bioxen_fourier_vm_lib.genome import GenomeParser

# Load genomic data
genome_data = GenomeParser.load_genome('path/to/genome.genome')
validated_records = GenomeParser.validate_records(genome_data)
```

### Step 2: Chassis Selection and Configuration
```python
from bioxen_fourier_vm_lib.chassis import ChassisType, EcoliChassis

# Select appropriate chassis
chassis = EcoliChassis()
chassis.configure_for_genome(validated_records)
```

### Step 3: VM Creation via Factory
```python
from bioxen_fourier_vm_lib.api import create_bio_vm

# Create biological VM
vm = create_bio_vm(
    vm_id='cell_simulation_001',
    biological_type='ecoli',
    vm_type='basic',
    config={'genome_data': validated_records}
)
```

### Step 4: Resource Allocation and Initialization
```python
# Allocate initial biological resources
vm.allocate_resources({
    'atp': 100.0,
    'ribosomes': 50,
    'amino_acids': 1000,
    'nucleotides': 2000
})

# Start the VM
vm.start()
```

### Step 5: Biological Process Execution
```python
# Execute biological processes
result = vm.execute_biological_process({
    'process_type': 'transcription',
    'gene_ids': ['gene_001', 'gene_002'],
    'conditions': {'temperature': 37.0, 'ph': 7.0}
})
```

### Step 6: Monitoring and Status Tracking
```python
# Monitor VM status
status = vm.get_status()
print(f"VM State: {status['state']}")
print(f"Resource Usage: {status['resources']}")
print(f"Active Processes: {status['processes']}")
```

## Data Flow

```
Genomic Data (.genome file)
    ↓
Genome Parser → Validation
    ↓
Chassis Selection → Configuration
    ↓
Factory API → VM Creation
    ↓
Hypervisor → Resource Allocation
    ↓
Biological VM → Process Execution
    ↓
Monitoring → Status/Output
```

## Supported Biological Processes

- **Transcription**: RNA synthesis from DNA templates
- **Translation**: Protein synthesis from mRNA
- **Metabolic Pathways**: Energy production and biochemical reactions
- **Genetic Circuits**: Regulatory networks and synthetic biology operations
- **Cell Division**: Simulation of cellular reproduction

## Resource Management

### Biological Resources
- **ATP**: Energy currency for cellular processes
- **Ribosomes**: Protein synthesis machinery
- **tRNA**: Transfer RNA for amino acid transport
- **RNA Polymerase**: Enzyme for transcription
- **Amino Acids**: Building blocks for proteins
- **Nucleotides**: Building blocks for nucleic acids

### Computational Resources
- **Memory**: Cellular memory architecture (prokaryotic/eukaryotic)
- **Processing Units**: Ribosomal capacity and concurrent operations
- **Storage**: Genome data and intermediate results

## Error Handling and Validation

- **Genome Validation**: Ensures compatibility with selected chassis
- **Resource Validation**: Checks availability before allocation
- **Process Validation**: Validates biological process parameters
- **VM State Validation**: Ensures proper state transitions

## Performance Considerations

- **Scalability**: Support for multiple concurrent VMs per chassis
- **Efficiency**: Optimized resource allocation algorithms
- **Monitoring**: Real-time performance metrics and profiling
- **Persistence**: VM state management across sessions

## Integration Points

- **JCVI Tools**: Genome acquisition and analysis integration
- **External Data Sources**: Live genome downloading and processing
- **Visualization**: Terminal-based monitoring interfaces
- **CLI**: Command-line interface for VM management

## Example Complete Workflow

```python
from bioxen_fourier_vm_lib.api import create_bio_vm
from bioxen_fourier_vm_lib.genome import GenomeParser

# 1. Load and validate genome
genome = GenomeParser.load_genome('ecoli_k12.genome')

# 2. Create biological VM
vm = create_bio_vm('ecoli_sim', 'ecoli', 'basic', {'genome': genome})

# 3. Initialize resources
vm.allocate_resources({'atp': 200, 'ribosomes': 100})

# 4. Start simulation
vm.start()

# 5. Run biological processes
transcription_result = vm.execute_biological_process({
    'type': 'transcription',
    'genes': ['lacZ', 'lacY'],
    'inducer': 'lactose'
})

# 6. Monitor and analyze
status = vm.get_status()
print(f"Simulation active: {status['active_processes']}")

# 7. Cleanup
vm.destroy()
```

This execution model provides a comprehensive framework for virtualizing biological cells, enabling computational biology research and synthetic biology applications through programmable cellular simulations.

---

## Integration with Four-Lens Analysis System

### Current State (October 2025)

The VM execution model above describes **discrete biological process execution**. The four-lens analysis system (`SystemAnalyzer`) exists as a separate, fully-functional component with 1,336 lines of production code, but is **not yet integrated** into the VM lifecycle.

**What works today:**
- ✅ VMs execute discrete processes (transcription, translation)
- ✅ SystemAnalyzer performs independent analysis of time-series data
- ✅ All four lenses fully implemented (Fourier, Wavelet, Laplace, Z-Transform)

**What's being built (Phases 2-3):**
- 🔄 VMs generating continuous metabolic time-series
- 🔄 VMs analyzing their own state automatically
- 🔄 Analysis triggering behavioral adjustments (self-regulation)

### Planned Integration (Phases 2-3)

VMs will be enhanced to support **continuous simulation** with **automatic self-regulation** using the four-lens analysis system.

#### Enhanced Workflow with Analysis Integration

```python
from bioxen_fourier_vm_lib.api import create_bio_vm

# 1. Create VM with continuous simulation capability (Phase 2)
vm = create_bio_vm('ecoli_sim', 'ecoli', 'basic')
vm.allocate_resources({'atp': 200, 'ribosomes': 100})

# 2. Start continuous simulation (NEW in Phase 2)
vm.start_continuous_simulation(
    duration_hours=48,
    update_interval=5.0  # Update metabolic state every 5 seconds
)

# Behind the scenes:
# - VM generates continuous time-series data (ATP, glucose, amino acids, gene expression)
# - History stored in rolling buffer (last 14 hours @ 5s resolution = ~10,000 samples)
# - Metabolic dynamics simulated with realistic biochemical equations

# 3. VM periodically analyzes its own state (NEW in Phase 3)
# Every 5 minutes, VM runs SystemAnalyzer on metabolic history:
#   - Fourier lens: Detects circadian rhythm drift
#   - Wavelet lens: Identifies stress transients
#   - Laplace lens: Monitors system stability
#   - Z-Transform lens: Filters measurement noise

# 4. VM adjusts behavior based on analysis (NEW in Phase 3)
# Analysis triggers automatic responses:
#   - Circadian drift → Adjust clock gene expression parameters
#   - System instability → Reduce metabolic rate to stabilize
#   - Stress transients → Activate stress response genes
#   - Low ATP → Upregulate glycolysis genes

# 5. Access historical data and analysis results
history = vm.get_metabolic_history(hours=1)
# Returns: {
#     'timestamps': [0, 5, 10, 15, ...],  # seconds
#     'atp': [100, 98, 95, 93, ...],
#     'glucose': [50, 48, 46, 44, ...],
#     'amino_acids': [1000, 995, 990, ...],
#     'gene_expression': {
#         'clock_gene': [50, 52, 54, ...],
#         'metabolic_gene': [40, 41, 39, ...]
#     }
# }

analysis_history = vm.get_analysis_history()
# Returns: List of analysis results with timestamps
# [
#     {
#         'timestamp': 300,
#         'fourier': FourierResult(...),
#         'wavelet': WaveletResult(...),
#         'laplace': LaplaceResult(...),
#         'ztransform': ZTransformResult(...)
#     },
#     ...
# ]

# 6. Stop simulation and cleanup
vm.stop_continuous_simulation()
vm.destroy()
```

#### Self-Regulation Example

```python
# VM detects circadian drift and self-corrects (Phase 3)
vm = create_bio_vm('ecoli_self_reg', 'ecoli', 'basic')
vm.start_continuous_simulation(duration_hours=48)

# Hour 12: VM analyzes metabolic state
# [VM ecoli_self_reg] Circadian drift detected: 26.3h (target: 24h)
# [VM ecoli_self_reg] Fourier analysis: dominant_period=26.3h, significance=0.95
# [VM ecoli_self_reg] Adjusting clock gene expression parameters...
# [VM ecoli_self_reg] Clock gene transcription rate: 1.0 → 1.15 (15% increase)

# Hour 24: Rhythm restored
# [VM ecoli_self_reg] Circadian rhythm stable: 24.1h (within tolerance)
# [VM ecoli_self_reg] System stability: stable, damping_ratio=0.65

# Hour 30: Stress event detected
# [VM ecoli_self_reg] High transient activity detected (8 events in 1 hour)
# [VM ecoli_self_reg] Wavelet analysis: transients at t=[1850s, 2100s, ...]
# [VM ecoli_self_reg] Activating stress response genes...
# [VM ecoli_self_reg] Heat shock protein expression: 10 → 45 (350% increase)

# Hour 36: Energy management
# [VM ecoli_self_reg] Low ATP detected: mean=38.2 (threshold=40)
# [VM ecoli_self_reg] Z-Transform filtering: noise_reduction=23%
# [VM ecoli_self_reg] Upregulating glycolysis genes...
# [VM ecoli_self_reg] Glucose metabolism rate: 1.0 → 1.5 (50% increase)
```

### Enhanced Data Flow with Analysis Integration

```
Genomic Data (.genome file)
    ↓
Genome Parser → Validation
    ↓
Chassis Selection → Configuration
    ↓
Factory API → VM Creation
    ↓
Hypervisor → Resource Allocation
    ↓
┌─────────────────────────────────────────────────────────┐
│ Continuous Simulation Loop (Phase 2)                   │
│                                                         │
│  1. Update Metabolic State (every 5s)                  │
│     - ATP regeneration from glucose                    │
│     - Ribosome activity and protein synthesis          │
│     - Gene expression with circadian oscillations      │
│     - Resource consumption                             │
│          ↓                                              │
│  2. Store in History Buffer                            │
│     - Rolling deque (maxlen=10,000)                    │
│     - Last ~14 hours of data                           │
│          ↓                                              │
│  3. Analyze State (every 5 min) (Phase 3) ←───────────┼─── SystemAnalyzer
│     - Extract time-series from history                 │     (4 lenses)
│     - Run all four lenses                              │     • Fourier
│     - Store results in analysis history                │     • Wavelet
│          ↓                                              │     • Laplace
│  4. Detect Anomalies                                   │     • Z-Transform
│     - Circadian drift (period ≠ 24h)                   │
│     - System instability (poles in right half-plane)   │
│     - Transient events (wavelet peaks)                 │
│     - Low resources (ATP < threshold)                  │
│          ↓                                              │
│  5. Adjust VM Behavior (feedback)                      │
│     - Tune gene expression parameters                  │
│     - Adjust metabolic rates                           │
│     - Activate/deactivate regulatory pathways          │
│          ↓                                              │
│  6. Loop continues...                                  │
└─────────────────────────────────────────────────────────┘
    ↓
Monitoring → Status/Output + Analysis Results + Self-Regulation Events
```

### Analysis-Driven Biological Processes

In the integrated system (Phase 3), analysis results trigger specific biological responses:

| Analysis Result | Detection Method | VM Response | Biological Mechanism |
|-----------------|------------------|-------------|---------------------|
| **Circadian drift** (period ≠ 24h) | Fourier lens: dominant_period check | Adjust clock gene parameters | Tune transcription rates to restore 24h rhythm |
| **System instability** | Laplace lens: pole locations | Reduce metabolic rate | Downregulate energy-intensive processes |
| **High transient activity** | Wavelet lens: event count | Activate stress response | Upregulate chaperones, heat shock proteins |
| **Low ATP levels** | Z-Transform lens: filtered mean | Upregulate glycolysis | Increase glucose metabolism genes |
| **Oscillation under-damping** | Laplace lens: damping ratio | Increase feedback strength | Enhance regulatory feedback loops |
| **Measurement noise** | Z-Transform lens: noise % | Apply filtering | Use filtered values for decisions |

### Implementation Timeline

- **Phase 1** (1-2 weeks): Automatic continuous analysis in profiler
- **Phase 2** (2-3 weeks): Continuous simulation with metabolic history
- **Phase 3** (2-3 weeks): VM self-regulation via analysis feedback

**Current Status:** Ready to start Phase 1  
**See:** [DEVELOPMENT_ROADMAP.md](docs/DEVELOPMENT_ROADMAP.md) for detailed implementation plan

### Benefits of Integration

1. **Homeostasis**: VMs automatically maintain stable metabolic states
2. **Robustness**: Self-correction when conditions change
3. **Realism**: Mimics real cellular regulation mechanisms
4. **Observability**: Complete history of metabolic state and analysis
5. **Research**: Study how analysis-driven feedback affects biological systems

This enhanced execution model will transform BioXen from a discrete process simulator into a **self-regulating biological system** that uses frequency domain analysis for autonomous homeostasis maintenance.

````
