# BioXen_jcvi_vm_lib Factory Pattern API - Phase 1: Foundation

## Phase 1 Overview: Core Infrastructure (Weeks 1-2)

**Objective**: Create the foundational API structure following pylua_bioxen_vm_lib patterns with infrastructure-focused VM classes.

**Duration**: 2 weeks
**Priority**: Critical foundation for entire project
**Dependencies**: None (pure wrapper over existing hypervisor)

---

## Architecture Vision

### Target API Structure
```
src/api/
├── __init__.py              # Package initialization and public exports
├── biological_vm.py         # Abstract BiologicalVM + concrete VM classes
├── factory.py              # create_bio_vm() factory function
├── resource_manager.py     # BioResourceManager unified wrapper
└── config_manager.py       # ConfigManager centralized config handling
```

### Design Principles
1. **Infrastructure-Focused**: Primary classes based on execution method ("basic" vs "xcpng")
2. **Non-Disruptive Wrapper**: Pure API layer over existing functionality (pylua pattern)
3. **Delegation Pattern**: New classes delegate to existing hypervisor methods (XCPngVM pattern)
4. **Backward Compatibility**: All existing interfaces remain unchanged
5. **Biological Type Composition**: Organism type ("syn3a", "ecoli") handled as parameter
6. **Configuration Management**: File-based configs with defaults (pylua ConfigManager pattern)

---

## Week 1: Core VM Class Implementation

### Day 1-2: Directory Structure & Base Classes

#### Create API Directory Structure
```bash
# Create API directory structure
mkdir -p src/api
touch src/api/__init__.py
touch src/api/biological_vm.py
touch src/api/factory.py
touch src/api/resource_manager.py
touch src/api/config_manager.py
```

#### `src/api/biological_vm.py` Implementation

**Abstract Base Class Following pylua Pattern**:
```python
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from ..hypervisor.core import BioXenHypervisor, VirtualMachine

class BiologicalVM(ABC):
    """
    Abstract base class for all biological VMs.
    Mirrors pylua_bioxen_vm_lib VM class hierarchy pattern.
    """
    
    def __init__(self, vm_id: str, biological_type: str, hypervisor: BioXenHypervisor, config: Dict[str, Any]):
        self.vm_id = vm_id
        self.biological_type = biological_type  # syn3a, ecoli, minimal_cell
        self.hypervisor = hypervisor  # Reference to existing hypervisor (delegation pattern)
        self.config = config
        self._vm_instance: Optional[VirtualMachine] = None
    
    @abstractmethod
    def get_vm_type(self) -> str:
        """Return the VM infrastructure type (basic/xcpng) - pylua pattern."""
        pass
    
    def get_biological_type(self) -> str:
        """Return the biological organism type (syn3a, ecoli, minimal_cell)."""
        return self.biological_type
    
    # Common interface methods that delegate to hypervisor (pylua delegation pattern)
    def start(self) -> bool:
        """Start the biological VM - mirrors pylua VM.start()."""
        return self.hypervisor.start_vm(self.vm_id)
    
    def pause(self) -> bool:
        """Pause the biological VM."""
        return self.hypervisor.pause_vm(self.vm_id)
    
    def resume(self) -> bool:
        """Resume the biological VM."""
        return self.hypervisor.resume_vm(self.vm_id)
    
    def destroy(self) -> bool:
        """Destroy the biological VM - mirrors pylua cleanup pattern."""
        return self.hypervisor.destroy_vm(self.vm_id)
    
    def get_status(self) -> Dict[str, Any]:
        """Get current VM status - mirrors pylua VM.get_status()."""
        return self.hypervisor.get_vm_status(self.vm_id)
    
    # Biological-specific methods (same interface for all VM types)
    def execute_biological_process(self, process_code: str) -> Dict[str, Any]:
        """Execute biological process - equivalent to pylua execute_string()."""
        return self._execute_biological_process_impl(process_code)
    
    def install_biological_package(self, package_name: str) -> Dict[str, Any]:
        """Install biological analysis package."""
        return self._install_biological_package_impl(package_name)
    
    def get_biological_metrics(self) -> Dict[str, Any]:
        """Get biological metrics based on organism type."""
        return self._get_biological_metrics_impl()
    
    # Abstract implementation methods - infrastructure-specific
    @abstractmethod
    def _execute_biological_process_impl(self, process_code: str) -> Dict[str, Any]:
        """Implementation-specific biological process execution."""
        pass
    
    @abstractmethod
    def _install_biological_package_impl(self, package_name: str) -> Dict[str, Any]:
        """Implementation-specific package installation."""
        pass
    
    @abstractmethod
    def _get_biological_metrics_impl(self) -> Dict[str, Any]:
        """Implementation-specific metrics gathering."""
        pass
    
    # Biological-specific helper methods (available for all VM types)
    def start_transcription(self, gene_ids: List[str]) -> bool:
        """Start transcription - available for all VM types."""
        if self.biological_type == "syn3a":
            return self.hypervisor.start_gene_expression(self.vm_id, gene_ids)
        else:
            raise ValueError(f"Transcription not supported for {self.biological_type}")

    def get_essential_genes(self) -> List[str]:
        """Get essential genes - Syn3A specific."""
        if self.biological_type == "syn3a":
            vm = self.hypervisor.get_vm(self.vm_id)
            return vm.genome.essential_genes if vm else []
        return []

    def manage_operons(self, operon_ids: List[str], action: str) -> bool:
        """Manage operons - E.coli specific."""
        if self.biological_type == "ecoli":
            return self.hypervisor.manage_operons(self.vm_id, operon_ids, action)
        else:
            raise ValueError(f"Operons not supported for {self.biological_type}")

    def get_plasmid_count(self) -> int:
        """Get plasmid count - E.coli specific."""
        if self.biological_type == "ecoli":
            status = self.get_status()
            return status.get('plasmid_count', 0)
        return 0
```

### Day 3-4: Concrete Infrastructure VM Classes

#### BasicBiologicalVM Implementation
```python
class BasicBiologicalVM(BiologicalVM):
    """
    Basic biological VM running directly on BioXen hypervisor.
    Equivalent to pylua BasicLuaVM - direct process execution.
    """
    
    def __init__(self, vm_id: str, biological_type: str, hypervisor: BioXenHypervisor, config: Dict[str, Any]):
        super().__init__(vm_id, biological_type, hypervisor, config)
    
    def get_vm_type(self) -> str:
        return "basic"
    
    def _execute_biological_process_impl(self, process_code: str) -> Dict[str, Any]:
        """Execute biological process directly on hypervisor."""
        return self.hypervisor.execute_biological_process(self.vm_id, process_code, self.biological_type)

    def _install_biological_package_impl(self, package_name: str) -> Dict[str, Any]:
        """Install biological analysis package."""
        return self.hypervisor.install_package(self.vm_id, package_name)

    def _get_biological_metrics_impl(self) -> Dict[str, Any]:
        """Get biological metrics based on organism type."""
        if self.biological_type == "syn3a":
            return self._get_syn3a_metrics()
        elif self.biological_type == "ecoli":
            return self._get_ecoli_metrics()
        elif self.biological_type == "minimal_cell":
            return self._get_minimal_cell_metrics()
        else:
            return {}

    def _get_syn3a_metrics(self) -> Dict[str, Any]:
        """Get Syn3A-specific metrics."""
        status = self.get_status()
        return {
            'atp_level': status.get('atp_percent', 0.0),
            'essential_genes': status.get('essential_genes', []),
            'ribosome_allocation': status.get('allocated_ribosomes', 0)
        }

    def _get_ecoli_metrics(self) -> Dict[str, Any]:
        """Get E.coli-specific metrics."""
        status = self.get_status()
        return {
            'plasmid_count': status.get('plasmid_count', 0),
            'growth_phase': status.get('growth_phase', 'stationary'),
            'operon_status': status.get('operon_status', {})
        }

    def _get_minimal_cell_metrics(self) -> Dict[str, Any]:
        """Get minimal cell-specific metrics."""
        status = self.get_status()
        return {
            'minimal_functions': ['dna_replication', 'protein_synthesis', 'energy_production'],
            'function_status': status.get('function_status', {})
        }
```

#### XCPngBiologicalVM Implementation
```python
class XCPngBiologicalVM(BiologicalVM):
    """
    XCP-ng biological VM running basic VMs inside full virtual machines.
    Equivalent to pylua XCPngVM - template-based VM with SSH execution.
    Provides additional isolation by running BioXen VMs inside XCP-ng VMs.
    """
    
    def __init__(self, vm_id: str, biological_type: str, hypervisor: BioXenHypervisor, config: Dict[str, Any]):
        super().__init__(vm_id, biological_type, hypervisor, config)
        self.xcpng_vm_uuid = None
        self.vm_ip = None
        # XCP-ng specific configuration
        self.xapi_config = config.get('xcpng_config', {})
    
    def get_vm_type(self) -> str:
        return "xcpng"
    
    def start(self) -> bool:
        """Start XCP-ng VM then start biological VM inside it."""
        # First create/start the XCP-ng VM (following pylua XCPngVM pattern)
        self.xcpng_vm_uuid = self._create_xcpng_vm()
        self._start_xcpng_vm()
        self.vm_ip = self._get_vm_ip()
        
        # Then start the biological VM inside the XCP-ng VM via SSH
        return self._start_biological_vm_via_ssh()
    
    def _execute_biological_process_impl(self, process_code: str) -> Dict[str, Any]:
        """Execute biological process via SSH in XCP-ng VM."""
        if not self.vm_ip:
            raise ValueError("XCP-ng VM not started or IP not available")
        
        # Execute biological process via SSH (pylua SSH execution pattern)
        return self._execute_via_ssh(process_code)
    
    def _install_biological_package_impl(self, package_name: str) -> Dict[str, Any]:
        """Install biological package via SSH in XCP-ng VM."""
        if not self.vm_ip:
            raise ValueError("XCP-ng VM not started or IP not available")
        
        return self._install_package_via_ssh(package_name)
    
    def _get_biological_metrics_impl(self) -> Dict[str, Any]:
        """Get biological metrics via SSH."""
        if not self.vm_ip:
            raise ValueError("XCP-ng VM not started or IP not available")
        
        # Get metrics via SSH and parse based on biological type
        ssh_result = self._execute_via_ssh("get_biological_status()")
        return self._parse_biological_metrics(ssh_result)
    
    # XCP-ng specific implementation methods
    def _create_xcpng_vm(self) -> str:
        """Create XCP-ng VM from template (following pylua XAPI pattern)."""
        # Implementation details for XCP-ng VM creation
        pass
    
    def _start_xcpng_vm(self) -> bool:
        """Start the XCP-ng VM."""
        # Implementation details for starting XCP-ng VM
        pass
    
    def _get_vm_ip(self) -> str:
        """Get IP address of started XCP-ng VM."""
        # Implementation details for getting VM IP
        pass
    
    def _start_biological_vm_via_ssh(self) -> bool:
        """Start biological VM inside XCP-ng VM via SSH."""
        # SSH into XCP-ng VM and start BioXen hypervisor
        pass
    
    def _execute_via_ssh(self, process_code: str) -> Dict[str, Any]:
        """Execute biological process via SSH."""
        # SSH execution following pylua pattern
        pass
    
    def _install_package_via_ssh(self, package_name: str) -> Dict[str, Any]:
        """Install package via SSH."""
        # SSH package installation following pylua pattern
        pass
    
    def _parse_biological_metrics(self, ssh_result: Dict[str, Any]) -> Dict[str, Any]:
        """Parse SSH result into biological metrics based on organism type."""
        # Parse based on self.biological_type
        pass
```

### Day 5-7: Factory Function Implementation

#### `src/api/factory.py` Implementation
```python
from typing import Dict, Any, Optional, List
from .biological_vm import BiologicalVM, BasicBiologicalVM, XCPngBiologicalVM
from ..hypervisor.core import BioXenHypervisor, ChassisType

def create_bio_vm(vm_id: str, biological_type: str, vm_type: str = "basic", config: Optional[Dict[str, Any]] = None) -> BiologicalVM:
    """
    Factory function to create biological VMs with VM type support.
    Mirrors pylua_bioxen_vm_lib create_vm() function exactly with vm_type parameter.
    
    Args:
        vm_id: Unique identifier for the VM
        biological_type: Type of biological organism ("syn3a", "ecoli", "minimal_cell")
        vm_type: VM infrastructure type ("basic", "xcpng") - default "basic"
        config: Optional configuration dictionary (required for xcpng)
    
    Returns:
        BiologicalVM instance of the appropriate type
    
    Raises:
        ValueError: If biological_type or vm_type is not supported
    """
    supported_biological_types = ["syn3a", "ecoli", "minimal_cell"]
    if biological_type not in supported_biological_types:
        raise ValueError(f"Unsupported biological type: {biological_type}. Supported: {supported_biological_types}")
    
    if vm_type not in ["basic", "xcpng"]:
        raise ValueError(f"Unsupported VM type: {vm_type}. Supported: ['basic', 'xcpng']")
    
    if vm_type == "xcpng" and not config:
        raise ValueError("XCP-ng VM type requires config parameter with xcpng_config")
    
    config = config or {}
    
    # Create hypervisor with appropriate chassis (mirrors pylua XCP-ng setup)
    chassis_type = _get_chassis_for_biological_type(biological_type)
    hypervisor = BioXenHypervisor(chassis_type=chassis_type)
    
    # Create VM in hypervisor first (mirrors pylua template creation)
    vm_template = _create_vm_template(biological_type, vm_type, config)
    hypervisor.create_vm(vm_id, template=vm_template)
    
    # Create and return wrapper VM instance based on vm_type (infrastructure-focused)
    if vm_type == "basic":
        # For basic VMs, use BasicBiologicalVM with biological_type parameter
        return BasicBiologicalVM(vm_id, biological_type, hypervisor, config)
    elif vm_type == "xcpng":
        # For XCP-ng VMs, use XCPngBiologicalVM with biological_type parameter  
        return XCPngBiologicalVM(vm_id, biological_type, hypervisor, config)

def _get_chassis_for_biological_type(biological_type: str) -> ChassisType:
    """Map biological type to appropriate chassis - mirrors pylua config mapping."""
    chassis_mapping = {
        "syn3a": ChassisType.ECOLI,  # Syn3A runs on E.coli chassis
        "ecoli": ChassisType.ECOLI,
        "minimal_cell": ChassisType.ECOLI
    }
    return chassis_mapping.get(biological_type, ChassisType.ECOLI)

def _create_vm_template(biological_type: str, vm_type: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create VM template based on biological type, VM type and config.
    Mirrors pylua template creation pattern with XCP-ng support.
    """
    # Delegate to existing genome integration logic
    from ..genome.parser import BioXenRealGenomeIntegrator
    
    genome_mapping = {
        "syn3a": "genomes/syn3a.genome",
        "ecoli": "genomes/ecoli.genome", 
        "minimal_cell": "genomes/minimal.genome"
    }
    
    genome_file = genome_mapping.get(biological_type)
    if not genome_file:
        raise ValueError(f"No genome file mapping for biological type: {biological_type}")
    
    integrator = BioXenRealGenomeIntegrator(genome_file)
    template = integrator.create_vm_template()
    
    # Add VM type specific configuration
    template['vm_type'] = vm_type
    template['biological_type'] = biological_type
    
    if vm_type == "xcpng":
        # Add XCP-ng specific template parameters
        xcpng_config = config.get('xcpng_config', {})
        template.update({
            'xcpng_template': xcpng_config.get('template_name', 'bioxen-bio-template'),
            'xcpng_network': xcpng_config.get('network_uuid'),
            'xcpng_storage': xcpng_config.get('storage_repository'),
            'vm_memory': xcpng_config.get('vm_memory', '2GB'),
            'vm_vcpus': xcpng_config.get('vm_vcpus', 2)
        })
    
    return template

# Additional factory functions following pylua pattern
def get_supported_biological_types() -> List[str]:
    """Get list of supported biological types."""
    return ["syn3a", "ecoli", "minimal_cell"]

def get_supported_vm_types() -> List[str]:
    """Get list of supported VM infrastructure types - mirrors pylua capability reporting."""
    return ["basic", "xcpng"]

def validate_biological_type(biological_type: str) -> bool:
    """Validate biological type is supported."""
    return biological_type in get_supported_biological_types()

def validate_vm_type(vm_type: str) -> bool:
    """Validate VM infrastructure type is supported - pylua validation pattern."""
    return vm_type in get_supported_vm_types()
```

---

## Week 2: Basic Resource Management & Testing

### Day 8-10: Basic Resource Manager

#### `src/api/resource_manager.py` Implementation
```python
from typing import Dict, Any, Optional
from .biological_vm import BiologicalVM

class BioResourceManager:
    """
    Unified resource management wrapper for biological VMs.
    Mirrors pylua resource management patterns.
    """
    
    def __init__(self, vm: BiologicalVM):
        self.vm = vm
        self.hypervisor = vm.hypervisor
    
    def allocate_atp(self, percentage: float) -> bool:
        """Allocate ATP resources - universal biological resource."""
        return self.hypervisor.allocate_atp(self.vm.vm_id, percentage)
    
    def allocate_ribosomes(self, count: int) -> bool:
        """Allocate ribosomes for protein synthesis."""
        return self.hypervisor.allocate_ribosomes(self.vm.vm_id, count)
    
    def get_resource_usage(self) -> Dict[str, Any]:
        """Get current resource usage."""
        return self.hypervisor.get_resource_usage(self.vm.vm_id)
    
    def get_available_resources(self) -> Dict[str, Any]:
        """Get available resources for allocation."""
        return self.hypervisor.get_available_resources(self.vm.vm_id)
    
    def optimize_resources_for_biological_type(self) -> bool:
        """Optimize resource allocation based on biological organism type."""
        if self.vm.biological_type == "syn3a":
            return self._optimize_for_minimal_genome()
        elif self.vm.biological_type == "ecoli":
            return self._optimize_for_prokaryote()
        elif self.vm.biological_type == "minimal_cell":
            return self._optimize_for_minimal_cell()
        return False
    
    def _optimize_for_minimal_genome(self) -> bool:
        """Optimize resources for minimal genome (Syn3A)."""
        # Minimal resource allocation for essential functions only
        return (self.allocate_atp(60.0) and 
                self.allocate_ribosomes(10))
    
    def _optimize_for_prokaryote(self) -> bool:
        """Optimize resources for prokaryotic organism (E.coli)."""
        # Standard bacterial resource allocation
        return (self.allocate_atp(80.0) and 
                self.allocate_ribosomes(25))
    
    def _optimize_for_minimal_cell(self) -> bool:
        """Optimize resources for minimal cellular functions."""
        # Basic cellular function resource allocation
        return (self.allocate_atp(50.0) and 
                self.allocate_ribosomes(8))
```

### Day 11-12: Basic Configuration Manager

#### `src/api/config_manager.py` Implementation
```python
from typing import Dict, Any, Optional
import json
import os

class ConfigManager:
    """
    Configuration management for biological VMs.
    Mirrors pylua configuration patterns.
    """
    
    @staticmethod
    def load_defaults(biological_type: str) -> Dict[str, Any]:
        """Load default configuration for biological type."""
        default_configs = {
            "syn3a": {
                "resource_limits": {
                    "max_atp": 70.0,
                    "max_ribosomes": 15
                },
                "genome_optimization": True,
                "minimal_mode": True
            },
            "ecoli": {
                "resource_limits": {
                    "max_atp": 90.0,
                    "max_ribosomes": 30
                },
                "operon_management": True,
                "plasmid_support": True
            },
            "minimal_cell": {
                "resource_limits": {
                    "max_atp": 60.0,
                    "max_ribosomes": 12
                },
                "basic_functions_only": True,
                "function_validation": True
            }
        }
        return default_configs.get(biological_type, {})
    
    @staticmethod
    def load_from_file(config_path: str) -> Dict[str, Any]:
        """Load configuration from file - mirrors pylua file loading."""
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_path, 'r') as f:
            return json.load(f)
    
    @staticmethod
    def validate_config(config: Dict[str, Any], vm_type: str) -> bool:
        """Validate configuration for VM type."""
        if vm_type == "xcpng":
            return ConfigManager._validate_xcpng_config(config)
        elif vm_type == "basic":
            return ConfigManager._validate_basic_config(config)
        return False
    
    @staticmethod
    def _validate_xcpng_config(config: Dict[str, Any]) -> bool:
        """Validate XCP-ng specific configuration."""
        xcpng_config = config.get('xcpng_config', {})
        required_fields = ['xapi_url', 'username', 'password', 'ssh_user']
        return all(field in xcpng_config for field in required_fields)
    
    @staticmethod
    def _validate_basic_config(config: Dict[str, Any]) -> bool:
        """Validate basic VM configuration."""
        # Basic VMs have minimal config requirements
        return True
    
    @staticmethod
    def merge_configs(base_config: Dict[str, Any], override_config: Dict[str, Any]) -> Dict[str, Any]:
        """Merge configurations with override priority."""
        merged = base_config.copy()
        merged.update(override_config)
        return merged
```

### Day 13-14: Package Initialization & Basic Testing

#### `src/api/__init__.py` Implementation
```python
"""
BioXen Factory Pattern API

Infrastructure-focused biological VM management following pylua_bioxen_vm_lib patterns.
"""

from .biological_vm import BiologicalVM, BasicBiologicalVM, XCPngBiologicalVM
from .factory import create_bio_vm, get_supported_biological_types, get_supported_vm_types, validate_biological_type, validate_vm_type
from .resource_manager import BioResourceManager
from .config_manager import ConfigManager

# Public API exports (mirrors pylua exports)
__all__ = [
    # Core VM classes
    'BiologicalVM',
    'BasicBiologicalVM', 
    'XCPngBiologicalVM',
    
    # Factory functions
    'create_bio_vm',
    'get_supported_biological_types',
    'get_supported_vm_types',
    'validate_biological_type',
    'validate_vm_type',
    
    # Management classes
    'BioResourceManager',
    'ConfigManager'
]

# Convenience functions (mirrors pylua convenience patterns)
def quick_start_vm(biological_type: str, vm_id: Optional[str] = None) -> BiologicalVM:
    """Quick start a basic biological VM with default settings."""
    vm_id = vm_id or f"quick_{biological_type}"
    return create_bio_vm(vm_id, biological_type)

# Alias for pylua compatibility
create_vm = create_bio_vm  # Alias for pylua compatibility
```

#### Basic Testing Suite
```python
# tests/test_api/test_phase1.py
import pytest
from src.api import create_bio_vm, BasicBiologicalVM, XCPngBiologicalVM

class TestPhase1Foundation:
    def test_create_basic_syn3a_vm(self):
        vm = create_bio_vm("test_syn3a", "syn3a", "basic")
        assert isinstance(vm, BasicBiologicalVM)
        assert vm.vm_id == "test_syn3a"
        assert vm.get_vm_type() == "basic"
        assert vm.get_biological_type() == "syn3a"
    
    def test_create_basic_ecoli_vm(self):
        vm = create_bio_vm("test_ecoli", "ecoli", "basic")
        assert isinstance(vm, BasicBiologicalVM)
        assert vm.get_vm_type() == "basic" 
        assert vm.get_biological_type() == "ecoli"
    
    def test_xcpng_requires_config(self):
        with pytest.raises(ValueError, match="XCP-ng VM type requires config"):
            create_bio_vm("test", "syn3a", "xcpng")
    
    def test_unsupported_biological_type(self):
        with pytest.raises(ValueError, match="Unsupported biological type"):
            create_bio_vm("test", "unsupported_bio_type", "basic")
    
    def test_unsupported_vm_type(self):
        with pytest.raises(ValueError, match="Unsupported VM type"):
            create_bio_vm("test", "syn3a", "unsupported_vm_type")
```

---

## Phase 1 Success Criteria

### Week 1 Deliverables
- [ ] Complete API directory structure created
- [ ] `BiologicalVM` abstract base class implemented
- [ ] `BasicBiologicalVM` class fully functional
- [ ] `XCPngBiologicalVM` class structure complete
- [ ] Factory function `create_bio_vm()` implemented
- [ ] Basic wrapper functionality validated
- [ ] Initial test suite passing

### Week 2 Deliverables
- [ ] `BioResourceManager` basic functionality implemented
- [ ] `ConfigManager` with default configs
- [ ] Package initialization (`__init__.py`) complete
- [ ] Comprehensive test suite for Phase 1
- [ ] Integration with existing hypervisor validated
- [ ] Performance baseline established

### Critical Validation Points
1. **Delegation Pattern Working**: All VM methods successfully delegate to existing hypervisor
2. **Infrastructure Focus**: "basic" vs "xcpng" distinction clear and functional
3. **Biological Type Composition**: All biological types work with both VM infrastructures
4. **Pylua Pattern Alignment**: Factory function signature matches pylua exactly
5. **Non-Disruptive**: Existing hypervisor functionality unmodified
6. **Error Handling**: Proper validation and error messages for invalid inputs

---

## Next Phase Preview

**Phase 2 (Weeks 3-4)**: Complete XCP-ng integration, advanced resource management, and configuration validation.

**Phase 3 (Weeks 5-6)**: CLI integration, comprehensive testing, documentation, and production readiness.

---

## Notes

- **Priority**: Foundation phase is critical - must be solid before proceeding
- **Testing**: Test each component as it's built, not at the end
- **Documentation**: Document decisions and patterns for future phases
- **Performance**: Measure wrapper overhead to ensure minimal impact
- **Compatibility**: Validate existing code continues to work unchanged
