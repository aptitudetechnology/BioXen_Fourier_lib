# BioXen Execution Model Audit Prompt

## Audit Objective
Analyze the current BioXen_jcvi_vm_lib codebase to understand the existing execution model for biological processes and determine how genomic code is currently interpreted, processed, and executed within the biological VM framework.

## Key Questions to Investigate

### 1. Current Execution Architecture
**Analyze these core files:**
- `src/bioxen_jcvi_vm_lib/hypervisor/core.py` - BioXenHypervisor class
- `src/bioxen_jcvi_vm_lib/api/biological_vm.py` - BiologicalVM abstract interface
- `src/bioxen_jcvi_vm_lib/api/factory.py` - VM creation and configuration

**Critical Questions:**
- What does `execute_biological_process(process_code: str)` actually do?
- How is the `process_code` parameter interpreted and executed?
- What constitutes a "biological process" in the current implementation?
- Is there a biological instruction set or command vocabulary?

### 2. Genome Integration Points
**Analyze genome-related functionality:**
- `src/bioxen_jcvi_vm_lib/jcvi_integration/` - JCVI genome handling
- Any genome loading, parsing, or processing capabilities
- Chassis-specific implementations in `src/bioxen_jcvi_vm_lib/chassis/`

**Critical Questions:**
- How are genome files (.gbk, .fasta, .genome) currently processed?
- What happens when a genome is loaded into a biological VM?
- Is there any gene-to-function mapping or execution?
- How do chassis types (ecoli, yeast, orthogonal) differ in execution?

### 3. Resource Management and State
**Analyze resource handling:**
- Resource allocation methods (`allocate_resources()`)
- Resource usage tracking (`get_resource_usage()`)
- VM status and metrics (`get_status()`, `get_biological_metrics()`)

**Critical Questions:**
- What biological resources are currently modeled (ATP, ribosomes, etc.)?
- How are resources consumed during biological process execution?
- What state is maintained between process executions?
- Is there a cellular context or environment state?

### 4. Process Execution Model
**Analyze the execution flow:**
- How biological processes are initiated and managed
- What happens during VM lifecycle events (start, stop, pause, resume)
- Inter-process communication and dependencies

**Critical Questions:**
- Are biological processes executed sequentially or concurrently?
- Is there a scheduler for biological operations?
- How do processes interact with each other and shared resources?
- What is the granularity of biological operations (genes, pathways, reactions)?

### 5. Data Flow and Transformation
**Trace data from input to execution:**
- Input formats (genome files, process codes, configurations)
- Internal data representations
- Output formats and results

**Critical Questions:**
- How is biological data transformed from input files to executable operations?
- What intermediate representations are used?
- Is there compilation, interpretation, or direct mapping?
- How are execution results generated and returned?

## Specific Code Analysis Tasks

### Task 1: Method Signature Analysis
Document all methods related to biological execution:
```python
# Find and analyze all implementations of:
def execute_biological_process(self, process_code: str) -> Dict[str, Any]
def start(self) -> bool
def get_biological_metrics(self) -> Dict[str, Any]
def allocate_resources(self, resources: Dict[str, Any]) -> bool
```

### Task 2: Configuration Analysis
Examine how biological behavior is configured:
- Default configurations for different biological types
- How configurations affect execution behavior
- Resource limits and constraints

### Task 3: Chassis Implementation Analysis
Compare execution differences across chassis:
- E.coli vs yeast vs orthogonal chassis implementations
- Organism-specific behaviors and capabilities
- Resource requirements and constraints

### Task 4: Integration Points Analysis
Identify external system integrations:
- JCVI toolkit usage patterns
- File format handling and conversion
- External command execution

## Expected Deliverables

### 1. Execution Model Documentation
- Current biological process execution flow
- Data structures used for biological state
- Resource management implementation
- Process scheduling and lifecycle management

### 2. Gap Analysis
- What biological operations are currently supported?
- What genome information is utilized vs ignored?
- Where are simulation boundaries vs actual computation?
- What would need to change for direct genomic code execution?

### 3. Architecture Assessment
- Current abstraction layers and their purposes
- Extensibility points for new execution models
- Performance characteristics and bottlenecks
- Integration patterns with external tools

### 4. Recommendations
- How to extend current model for genomic virtualization
- Required architectural changes
- Implementation complexity assessment
- Compatibility considerations with existing functionality

## Analysis Guidelines

### Focus Areas
- **Concrete Implementation**: What actually executes, not just interfaces
- **Data Transformation**: How biological data becomes executable operations
- **Resource Modeling**: How biological constraints are enforced
- **State Management**: What persists between operations

### Avoid Assumptions
- Don't assume biological processes are simulated vs executed
- Don't assume genome files are used vs ignored
- Don't assume resource management is symbolic vs computational
- Verify actual implementation behavior through code analysis

## Output Format
Provide structured analysis with:
- Code excerpts demonstrating execution patterns
- Flow diagrams showing data transformation
- Concrete examples of current biological process execution
- Specific recommendations for genomic virtualization integration