# BioXen JCVI VM Library - Phase 1.3: Hypervisor-Focused Library

**Date:** September 5, 2025  
**Phase:** 1.3 - Hypervisor-Focused Production Library  
**Status:** Planning  
**Goal:** Deliver production-ready hypervisor library excluding JCVI/genome features

---

## Executive Summary

Phase 1.3 represents a strategic pivot toward a focused, production-ready biological virtualization library. Based on the analysis in `lib-ver0.0.04-report.md`, we will concentrate on delivering robust hypervisor functionality while excluding JCVI tools and genome downloaders to create a clean, maintainable package.

## Strategic Direction

### ✅ **Include: Core Hypervisor Features**
- Complete `src/hypervisor/` module suite
- VM lifecycle management (create, start, stop, destroy, monitor)
- Resource allocation and management
- Biological chassis selection (ecoli, yeast, orthogonal)
- System monitoring and profiling
- Factory pattern API for VM creation
- Interactive CLI for VM operations

### ❌ **Exclude: JCVI and Acquisition Features**
- JCVI integration modules (`src/jcvi_integration/`)
- Genome download functionality (`download_genomes.py`)
- JCVI format conversion tools
- Enhanced JCVI CLI workflows
- Genome acquisition pipelines

## Implementation Plan

### **Phase 1.3.1: Core Module Packaging**

#### **Hypervisor Module Suite**
```python
src/
├── hypervisor/              # ✅ Core virtualization engine
│   ├── core.py             # Main hypervisor functionality
│   ├── vm_manager.py       # VM lifecycle operations
│   └── resource_pool.py    # Resource allocation
├── chassis/                 # ✅ Biological chassis support
│   ├── ecoli.py            # E. coli chassis
│   ├── yeast.py            # Yeast chassis
│   └── orthogonal.py       # Orthogonal chassis
├── monitoring/              # ✅ System profiling
│   ├── metrics.py          # Performance metrics
│   └── profiler.py         # Resource profiling
└── api/                     # ✅ Factory pattern API (hypervisor-only)
    ├── factory.py          # VM creation factory
    ├── biological_vm.py    # VM abstractions
    └── resource_manager.py # Resource management API
```

#### **Excluded Modules**
```python
# These will NOT be included in v0.0.5:
src/jcvi_integration/        # ❌ JCVI workflows
download_genomes.py          # ❌ Genome acquisition
bioxen_jcvi_integration.py   # ❌ JCVI integration
bioxen_to_jcvi_converter.py  # ❌ Format conversion
enhanced_jcvi_cli.py         # ❌ JCVI CLI tools
```

### **Phase 1.3.2: Factory Pattern API (Hypervisor-Only)**

#### **Simplified Factory Functions**
```python
# Core factory interface (no JCVI modes)
def create_bio_vm(vm_id: str, biological_type: str, vm_type: str = "basic", 
                  config: Optional[Dict[str, Any]] = None) -> BiologicalVM:
    """
    Create biological VM with hypervisor support only.
    
    Args:
        vm_id: Unique VM identifier
        biological_type: "syn3a", "ecoli", "minimal_cell"
        vm_type: "basic", "xcpng"  # No "jcvi_optimized"
        config: VM configuration options
    """

def create_biological_vm(vm_type: str = "basic", 
                        config: Optional[Dict[str, Any]] = None) -> BiologicalVM:
    """Simplified factory for basic VM creation."""
```

#### **VM Interface (Hypervisor-Focused)**
```python
class BiologicalVM(ABC):
    # Core VM operations
    def start(self) -> bool
    def pause(self) -> bool
    def resume(self) -> bool
    def destroy(self) -> bool
    def get_status(self) -> Dict[str, Any]
    
    # Biological operations (hypervisor-level)
    def execute_biological_process(self, process_code: str) -> Dict[str, Any]
    def install_biological_package(self, package_name: str) -> Dict[str, Any]
    def get_biological_metrics(self) -> Dict[str, Any]
    
    # Resource management
    def allocate_resources(self, resources: Dict[str, Any]) -> bool
    def get_resource_usage(self) -> Dict[str, Any]
    
    # REMOVED: JCVI-specific methods
    # - analyze_genome()
    # - run_comparative_analysis()
    # - convert_genome_format()
```

### **Phase 1.3.3: Interactive CLI (VM Management Only)**

#### **Simplified Menu Structure**
```python
# Hypervisor-focused CLI options
MENU_OPTIONS = [
    "🏭 Create Biological VM",
    "🖥️ List Active VMs", 
    "▶️ Start VM",
    "⏸️ Pause VM",
    "⏹️ Stop VM",
    "🗑️ Delete VM",
    "📊 VM Status & Metrics",
    "⚙️ Resource Management",
    "🧬 Chassis Selection",
    "🚪 Exit"
]

# REMOVED: JCVI and genome options
# - "📥 Acquire Genome"
# - "🔄 JCVI Workflow"
# - "🧪 Format Conversion"
```

### **Phase 1.3.4: Dependencies (Minimal Set)**

#### **Required Dependencies Only**
```python
install_requires = [
    "pylua-bioxen-vm-lib>=0.1.22",  # Core VM functionality
    "questionary>=2.1.0",           # Interactive CLI
    "rich>=13.0.0",                 # Enhanced terminal output
]

# REMOVED: JCVI and genome dependencies
# - "jcvi>=1.5.6"
# - "ncbi-genome-download>=0.3.3"
# - "biopython>=1.80"
# - "matplotlib>=3.5.0"
# - "numpy>=1.21.0"
# - "scipy>=1.7.0"
```

### **Phase 1.3.5: Testing Strategy**

#### **Hypervisor Test Coverage**
```python
tests/
├── test_hypervisor/         # ✅ Core hypervisor tests
│   ├── test_vm_lifecycle.py
│   ├── test_resource_mgmt.py
│   └── test_chassis.py
├── test_api/                # ✅ Factory pattern tests
│   ├── test_factory.py
│   └── test_biological_vm.py
└── test_cli/                # ✅ CLI interaction tests
    └── test_interactive.py

# REMOVED: JCVI test modules
# - test_jcvi_integration/
# - test_genome_acquisition/
# - test_format_conversion/
```

## Documentation Updates

### **README.md - Hypervisor Focus**
```markdown
# BioXen JCVI VM Library v0.0.5

A production-ready biological virtualization library focused on hypervisor 
functionality and VM management.

## Features
✅ Biological VM creation and lifecycle management
✅ Resource allocation and monitoring  
✅ Multi-chassis support (E. coli, yeast, orthogonal)
✅ Interactive CLI for VM operations
✅ Factory pattern API for type-safe VM creation

## Not Included
❌ JCVI integration (available separately)
❌ Genome download functionality  
❌ Format conversion tools

## Quick Start
```python
from bioxen_jcvi_vm_lib import create_bio_vm

# Create biological VM
vm = create_bio_vm("my_vm", "ecoli", "basic")
vm.start()
status = vm.get_status()
```

### **Specification Document Updates**
- Update `specification-document-bioxen_jcvi_vm_lib_ver0.0.05.md`
- Remove all JCVI acquisition and integration sections
- Focus on hypervisor architecture and VM management
- Document extension points for future JCVI integration

## Migration Path

### **From v0.0.4 to v0.0.5**
```python
# v0.0.4 (JCVI features available but incomplete)
vm = create_biological_vm(vm_type="jcvi_optimized")  # ❌ No longer available
stats = vm.analyze_genome("genome.fasta")            # ❌ Removed

# v0.0.5 (Hypervisor-focused)
vm = create_biological_vm(vm_type="basic")           # ✅ Clean hypervisor
metrics = vm.get_biological_metrics()               # ✅ VM-level metrics
```

### **Extension Point for Future JCVI Package**
```python
# Future separate package: bioxen-jcvi-tools
from bioxen_jcvi_tools import JCVIExtension

vm = create_bio_vm("my_vm", "ecoli", "basic")
jcvi_ext = JCVIExtension(vm)  # External extension
jcvi_ext.analyze_genome("genome.fasta")
```

## Success Metrics

### **Phase 1.3 Deliverables**
- ✅ Production-ready hypervisor library (no JCVI dependencies)
- ✅ Complete VM lifecycle management
- ✅ Resource allocation and monitoring
- ✅ Multi-chassis biological support
- ✅ Interactive CLI for VM operations
- ✅ Comprehensive test coverage for hypervisor features
- ✅ Clean API documentation and examples

### **Quality Gates**
- All hypervisor tests passing (100%)
- VM creation/destruction cycles stable
- Resource management validated
- CLI interface fully functional
- Zero JCVI/genome dependencies
- Documentation complete and accurate

## Timeline

**Phase 1.3 Duration:** 2 weeks
**Target Completion:** September 19, 2025

**Week 1:** Core module packaging and API cleanup
**Week 2:** Testing, documentation, and PyPI release

## Conclusion

Phase 1.3 delivers a focused, production-ready biological virtualization library that provides robust hypervisor functionality without the complexity of JCVI integration. This creates a stable foundation for biological VM management while enabling future JCVI capabilities through separate packages.

The strategic separation allows:
- Faster development cycles for hypervisor features
- Cleaner dependency management
- Easier maintenance and testing
- Clear upgrade paths for users

**Next Steps:** Begin implementation of hypervisor-focused v0.0.5 following this plan.

---

**Generated:** September 5, 2025  
**Phase:** 1.3 Planning Complete  
**Ready for Implementation:** ✅
