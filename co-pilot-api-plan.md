# BioXen_jcvi_vm_lib Factory Pattern API Implementation Plan

## Executive Summary

Based on comprehensive codebase analysis and alignment with pylua_bioxen_vm_lib specification patterns, BioXen_jcvi_vm_lib is exceptionally well-positioned for factory pattern API implementation. The existing biological hypervisor infrastructure is mature and production-ready. This plan outlines a 4-week implementation strategy for adding a non-disruptive API layer that transforms the codebase into a reusable Python library while preserving all existing functionality.

**Key Insight**: The primary development effort focuses on API abstraction using proven pylua_bioxen_vm_lib VM class patterns rather than core functionality - the biological virtualization system is already sophisticated and complete.

**Critical Alignment**: This implementation directly follows the successful architectural patterns from pylua_bioxen_vm_lib v0.1.22, ensuring consistency across the BioXen ecosystem.

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
1. **Non-Disruptive Wrapper**: Pure API layer over existing functionality (pylua pattern)
2. **Delegation Pattern**: New classes delegate to existing hypervisor methods (XCPngVM pattern)
3. **Backward Compatibility**: All existing interfaces remain unchanged
4. **Type-Based Instantiation**: VM creation via string types ("syn3a", "ecoli") - exact pylua approach
5. **Unified Interface**: Consistent API across all VM types following pylua BiologicalVM pattern
6. **Configuration Management**: File-based configs with defaults (pylua ConfigManager pattern)

---

## Implementation Phases

### Phase 1: Foundation (Week 1)
**Objective**: Create core API structure and validate wrapper approach

#### Day 1-2: Directory Structure & Base Classes
```bash
# Create API directory structure
mkdir -p src/api
touch src/api/__init__.py
touch src/api/biological_vm.py
touch src/api/factory.py
touch src/api/resource_manager.py
touch src/api/config_manager.py
```

**`src/api/biological_vm.py` Implementation** (Following pylua_bioxen_vm_lib patterns):
```python
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from ..hypervisor.core import BioXenHypervisor, VirtualMachine

class BiologicalVM(ABC):
    """
    Abstract base class for all biological VMs.
    Mirrors pylua_bioxen_vm_lib VM class hierarchy pattern.
    """
    
    def __init__(self, vm_id: str, vm_type: str, hypervisor: BioXenHypervisor, config: Dict[str, Any]):
        self.vm_id = vm_id
        self.vm_type = vm_type  # "basic" or "xcpng" following pylua pattern
        self.hypervisor = hypervisor  # Reference to existing hypervisor (delegation pattern)
        self.config = config
        self._vm_instance: Optional[VirtualMachine] = None
    
    @abstractmethod
    def get_vm_type(self) -> str:
        """Return the VM type identifier - pylua pattern."""
        pass
    
    @abstractmethod
    def get_biological_type(self) -> str:
        """Return the biological organism type (syn3a, ecoli, minimal_cell)."""
        pass
    
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
    
    # Abstract methods for biological-specific operations
    @abstractmethod
    def execute_biological_process(self, process_code: str) -> Dict[str, Any]:
        """Execute biological process - equivalent to pylua execute_string()."""
        pass


class BasicBiologicalVM(BiologicalVM):
    """
    Basic biological VM running directly on BioXen hypervisor.
    Equivalent to pylua BasicLuaVM - direct process execution.
    """
    
    def __init__(self, vm_id: str, biological_type: str, hypervisor: BioXenHypervisor, config: Dict[str, Any]):
        super().__init__(vm_id, "basic", hypervisor, config)
        self.biological_type = biological_type  # syn3a, ecoli, minimal_cell
    
    def get_vm_type(self) -> str:
        return "basic"
    
    def get_biological_type(self) -> str:
        return self.biological_type
    
    def execute_biological_process(self, process_code: str) -> Dict[str, Any]:
        """Execute biological process directly on hypervisor."""
        # Direct delegation to existing hypervisor functionality
        return self.hypervisor.execute_process(self.vm_id, process_code)
    
    def install_biological_package(self, package_name: str) -> Dict[str, Any]:
        """Install biological analysis package."""
        return self.hypervisor.install_package(self.vm_id, package_name)


class XCPngBiologicalVM(BiologicalVM):
    """
    XCP-ng biological VM running basic VMs inside full virtual machines.
    Equivalent to pylua XCPngVM - template-based VM with SSH execution.
    Provides additional isolation by running BioXen VMs inside XCP-ng VMs.
    """
    
    def __init__(self, vm_id: str, biological_type: str, hypervisor: BioXenHypervisor, config: Dict[str, Any]):
        super().__init__(vm_id, "xcpng", hypervisor, config)
        self.biological_type = biological_type
        self.xcpng_vm_uuid = None
        self.vm_ip = None
        # XCP-ng specific configuration
        self.xapi_config = config.get('xcpng_config', {})
    
    def get_vm_type(self) -> str:
        return "xcpng"
    
    def get_biological_type(self) -> str:
        return self.biological_type
    
    def start(self) -> bool:
        """Start XCP-ng VM then start biological VM inside it."""
        # First create/start the XCP-ng VM (following pylua XCPngVM pattern)
        self.xcpng_vm_uuid = self._create_xcpng_vm()
        self._start_xcpng_vm()
        self.vm_ip = self._get_vm_ip()
        
        # Then start the biological VM inside the XCP-ng VM via SSH
        return self._start_biological_vm_via_ssh()
    
    def execute_biological_process(self, process_code: str) -> Dict[str, Any]:
        """Execute biological process via SSH in XCP-ng VM."""
        if not self.vm_ip:
            raise ValueError("XCP-ng VM not started or IP not available")
        
        # Execute biological process via SSH (pylua SSH execution pattern)
        return self._execute_via_ssh(process_code)
    
    def install_biological_package(self, package_name: str) -> Dict[str, Any]:
        """Install biological package via SSH in XCP-ng VM."""
        if not self.vm_ip:
            raise ValueError("XCP-ng VM not started or IP not available")
        
        return self._install_package_via_ssh(package_name)
    
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
```

#### Day 3-4: Concrete VM Classes
**Implement `Syn3AVM` class** (Following XCPngVM specialization pattern):
```python
class Syn3AVM(BiologicalVM):
    """
    Syn3A minimal genome biological VM.
    Mirrors XCPngVM specialization pattern from pylua_bioxen_vm_lib.
    """
    
    def get_vm_type(self) -> str:
        return "syn3a"
    
    def execute_biological_process(self, process_code: str) -> Dict[str, Any]:
        """Execute biological process - mirrors pylua execute_string() pattern."""
        # Delegate to existing hypervisor biological process execution
        return self.hypervisor.execute_biological_process(self.vm_id, process_code)
    
    def start_transcription(self, gene_ids: List[str]) -> bool:
        """
        Start transcription of specific genes.
        Biological equivalent of pylua XCPngVM.execute_string() specialization.
        """
        # Delegate to existing hypervisor gene expression logic
        return self.hypervisor.start_gene_expression(self.vm_id, gene_ids)
    
    def get_essential_genes(self) -> List[str]:
        """
        Get list of essential genes for Syn3A.
        Mirrors pylua VM-specific status methods.
        """
        vm = self.hypervisor.get_vm(self.vm_id)
        return vm.genome.essential_genes if vm else []
    
    def get_atp_level(self) -> float:
        """
        Get current ATP percentage.
        Biological resource monitoring - mirrors pylua resource tracking.
        """
        status = self.get_status()
        return status.get('atp_percent', 0.0)
    
    def get_ribosome_allocation(self) -> int:
        """Get current ribosome allocation - Syn3A specific method."""
        status = self.get_status()
        return status.get('allocated_ribosomes', 0)
    
    def optimize_minimal_metabolism(self) -> bool:
        """Optimize for minimal genome metabolism - Syn3A specific."""
        return self.hypervisor.optimize_minimal_metabolism(self.vm_id)
```

#### Day 5-7: Testing and Validation
- Create comprehensive test suite for wrapper pattern
- Validate delegation to existing hypervisor methods
- Test VM lifecycle management through new API
- Performance testing to measure wrapper overhead

### Phase 2: Core Implementation (Week 2)
**Objective**: Complete VM class hierarchy and implement factory function

#### Day 8-10: Additional VM Classes
**`EColiVM` Implementation** (Following BasicLuaVM pattern):
```python
class EColiVM(BiologicalVM):
    """
    E.coli bacterial VM with prokaryotic features.
    Mirrors BasicLuaVM pattern from pylua_bioxen_vm_lib.
    """
    
    def get_vm_type(self) -> str:
        return "ecoli"
    
    def execute_biological_process(self, process_code: str) -> Dict[str, Any]:
        """Execute biological process - standard delegation pattern."""
        return self.hypervisor.execute_biological_process(self.vm_id, process_code)
    
    def allocate_ribosomes(self, count: int) -> bool:
        """
        Allocate ribosomes for protein synthesis.
        E.coli specific resource management - mirrors pylua resource allocation.
        """
        return self.hypervisor.allocate_ribosomes(self.vm_id, count)
    
    def get_plasmid_count(self) -> int:
        """
        Get number of plasmids in the VM.
        E.coli specific functionality - mirrors pylua VM-specific features.
        """
        status = self.get_status()
        return status.get('plasmid_count', 0)
    
    def manage_operons(self, operon_ids: List[str], action: str) -> bool:
        """Manage E.coli operons - prokaryotic specific functionality."""
        return self.hypervisor.manage_operons(self.vm_id, operon_ids, action)
    
    def get_growth_phase(self) -> str:
        """Get current growth phase - E.coli specific monitoring."""
        status = self.get_status()
        return status.get('growth_phase', 'stationary')
```

**`MinimalCellVM` Implementation**:
```python
class MinimalCellVM(BiologicalVM):
    """
    Minimal cell VM with basic cellular functions.
    Mirrors pylua minimal VM pattern.
    """
    
    def get_vm_type(self) -> str:
        return "minimal_cell"
    
    def execute_biological_process(self, process_code: str) -> Dict[str, Any]:
        """Execute biological process with minimal cell constraints."""
        # Add minimal cell specific validation
        if not self._validate_minimal_process(process_code):
            raise ValueError("Process not supported in minimal cell")
        return self.hypervisor.execute_biological_process(self.vm_id, process_code)
    
    def get_minimal_functions(self) -> List[str]:
        """
        Get list of minimal cellular functions.
        Equivalent to pylua basic feature enumeration.
        """
        return ['dna_replication', 'protein_synthesis', 'energy_production', 'membrane_maintenance']
    
    def _validate_minimal_process(self, process_code: str) -> bool:
        """Validate process is compatible with minimal cell constraints."""
        minimal_functions = self.get_minimal_functions()
        # Implementation would check if process uses only minimal functions
        return True  # Simplified for example
```

#### Day 11-12: Factory Function Implementation
**`src/api/factory.py`** (Following exact pylua_bioxen_vm_lib create_vm pattern):
```python
from typing import Dict, Any, Optional
from .biological_vm import BiologicalVM, Syn3AVM, EColiVM, MinimalCellVM
from ..hypervisor.core import BioXenHypervisor, ChassisType

# Biological type mapping - updated to separate biological types from VM infrastructure
BIOLOGICAL_TYPE_MAPPING = {
    "syn3a": Syn3AVM,
    "ecoli": EColiVM, 
    "minimal_cell": MinimalCellVM
}

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
    if biological_type not in BIOLOGICAL_TYPE_MAPPING:
        raise ValueError(f"Unsupported biological type: {biological_type}. Supported: {list(BIOLOGICAL_TYPE_MAPPING.keys())}")
    
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
    
    # Create and return wrapper VM instance based on vm_type
    if vm_type == "basic":
        # For basic VMs, use the specific biological class directly
        biological_class = BIOLOGICAL_TYPE_MAPPING[biological_type]
        return biological_class(vm_id, biological_type, hypervisor, config)
    elif vm_type == "xcpng":
        # For XCP-ng VMs, use the XCP-ng wrapper regardless of biological type
        # The biological behavior is handled inside the XCP-ng VM
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
    
    # Fallback to default template
    return {"vm_type": vm_type, **config}

# Additional factory functions following pylua pattern
def get_supported_vm_types() -> List[str]:
    """Get list of supported VM types - mirrors pylua capability reporting."""
    return list(VM_TYPE_MAPPING.keys())

def validate_vm_type(vm_type: str) -> bool:
    """Validate VM type is supported - pylua validation pattern."""
    return vm_type in VM_TYPE_MAPPING
```

#### Day 13-14: Integration Testing
- Test factory function with all VM types
- Validate hypervisor registration works correctly
- Test config validation and error handling
- Integration testing with existing genome data

### Phase 3: Resource Management & Configuration (Week 3)
**Objective**: Implement unified resource management and configuration systems

#### Day 15-17: Resource Manager Implementation
**`src/api/resource_manager.py`** (Following pylua VMManager resource pattern):
```python
from typing import Dict, Any, List
from ..hypervisor.core import ResourceType, ResourceAllocation
from .biological_vm import BiologicalVM

class BioResourceManager:
    """
    Unified biological resource management interface.
    Mirrors pylua VMManager resource management pattern.
    """
    
    def __init__(self, vm: BiologicalVM):
        self.vm = vm
        self.hypervisor = vm.hypervisor
    
    def allocate_atp(self, percentage: float) -> bool:
        """
        Allocate ATP resources to the VM.
        Mirrors pylua resource allocation pattern.
        """
        return self.hypervisor.allocate_resource(
            self.vm.vm_id, 
            ResourceType.ATP, 
            percentage
        )
    
    def allocate_ribosomes(self, count: int) -> bool:
        """
        Allocate ribosome resources to the VM.
        Biological equivalent of pylua compute resource allocation.
        """
        return self.hypervisor.allocate_resource(
            self.vm.vm_id,
            ResourceType.RIBOSOMES,
            count
        )
    
    def allocate_memory(self, kb: int) -> bool:
        """
        Allocate memory resources to the VM.
        Mirrors pylua memory allocation pattern.
        """
        return self.hypervisor.allocate_resource(
            self.vm.vm_id,
            ResourceType.MEMORY,
            kb
        )
    
    def get_resource_usage(self) -> Dict[str, Any]:
        """
        Get current resource usage for the VM.
        Mirrors pylua VM resource monitoring.
        """
        return self.hypervisor.get_vm_resources(self.vm.vm_id)
    
    def get_available_resources(self) -> Dict[str, Any]:
        """
        Get available system resources.
        Mirrors pylua system resource reporting.
        """
        return self.hypervisor.get_system_resources()
    
    def optimize_allocation(self) -> bool:
        """
        Optimize resource allocation for the VM.
        Biological equivalent of pylua performance optimization.
        """
        # Use existing scheduler optimization logic
        return self.hypervisor.optimize_vm_resources(self.vm.vm_id)
    
    def get_resource_limits(self) -> Dict[str, Any]:
        """Get resource limits for VM type - mirrors pylua capability reporting."""
        vm_type = self.vm.get_vm_type()
        return self._get_vm_type_limits(vm_type)
    
    def _get_vm_type_limits(self, vm_type: str) -> Dict[str, Any]:
        """Get resource limits based on VM type - pylua VM-specific configuration."""
        limits = {
            "syn3a": {"max_ribosomes": 50, "max_atp": 80.0, "max_memory_kb": 200},
            "ecoli": {"max_ribosomes": 100, "max_atp": 90.0, "max_memory_kb": 500},
            "minimal_cell": {"max_ribosomes": 20, "max_atp": 60.0, "max_memory_kb": 100}
        }
        return limits.get(vm_type, {})

class BioVMManager:
    """
    Enhanced VM manager with multi-VM type support.
    Mirrors pylua VMManager pattern exactly.
    """
    
    def __init__(self, debug_mode: bool = False):
        self.debug_mode = debug_mode
        self.vms: Dict[str, BiologicalVM] = {}
        self.resource_managers: Dict[str, BioResourceManager] = {}
    
    def create_vm(self, vm_id: str, vm_type: str = "syn3a", config: Optional[Dict] = None) -> BiologicalVM:
        """
        Create VM with type selection - exact pylua pattern.
        """
        from .factory import create_bio_vm
        
        vm = create_bio_vm(vm_id, vm_type, config)
        self.vms[vm_id] = vm
        self.resource_managers[vm_id] = BioResourceManager(vm)
        return vm
    
    def execute_vm_sync(self, vm_id: str, biological_code: str) -> Dict[str, Any]:
        """
        Execute biological operation - mirrors pylua execute_vm_sync.
        """
        if vm_id not in self.vms:
            raise ValueError(f"VM {vm_id} not found")
        
        vm = self.vms[vm_id]
        return vm.execute_biological_process(biological_code)
    
    def get_vm_resource_manager(self, vm_id: str) -> BioResourceManager:
        """Get resource manager for VM - pylua resource access pattern."""
        if vm_id not in self.resource_managers:
            raise ValueError(f"VM {vm_id} not found")
        return self.resource_managers[vm_id]
    
    def list_vms(self) -> Dict[str, str]:
        """List all VMs and their types - mirrors pylua session listing."""
        return {vm_id: vm.get_vm_type() for vm_id, vm in self.vms.items()}
    
    def terminate_vm(self, vm_id: str) -> bool:
        """Terminate VM - mirrors pylua cleanup pattern."""
        if vm_id in self.vms:
            result = self.vms[vm_id].destroy()
            del self.vms[vm_id]
            del self.resource_managers[vm_id]
            return result
        return False
```

#### Day 18-19: Configuration Manager
**`src/api/config_manager.py`** (Following exact pylua ConfigManager pattern):
```python
from typing import Dict, Any, Optional
from dataclasses import dataclass
import json
from pathlib import Path

@dataclass
class VMConfig:
    """
    Standard VM configuration structure.
    Mirrors pylua VMConfig exactly.
    """
    vm_type: str
    chassis_type: str
    genome_file: Optional[str] = None
    resource_limits: Optional[Dict[str, Any]] = None
    custom_params: Optional[Dict[str, Any]] = None

class ConfigManager:
    """
    Centralized configuration management for biological VMs.
    Mirrors pylua ConfigManager pattern exactly.
    """
    
    DEFAULT_CONFIGS = {
        "syn3a": VMConfig(
            vm_type="syn3a",
            chassis_type="ecoli",
            genome_file="genomes/syn3a.genome",
            resource_limits={"max_ribosomes": 50, "max_atp": 80.0, "max_memory_kb": 200},
            custom_params={"essential_only": True, "optimization": "minimal_metabolism"}
        ),
        "ecoli": VMConfig(
            vm_type="ecoli", 
            chassis_type="ecoli",
            genome_file="genomes/ecoli.genome",
            resource_limits={"max_ribosomes": 100, "max_atp": 90.0, "max_memory_kb": 500},
            custom_params={"plasmid_support": True, "operon_management": True}
        ),
        "minimal_cell": VMConfig(
            vm_type="minimal_cell",
            chassis_type="ecoli", 
            resource_limits={"max_ribosomes": 20, "max_atp": 60.0, "max_memory_kb": 100},
            custom_params={"minimal_functions_only": True, "strict_validation": True}
        )
    }
    
    @classmethod
    def load_defaults(cls, vm_type: str) -> Dict[str, Any]:
        """
        Load default configuration for VM type.
        Mirrors pylua default configuration loading.
        """
        if vm_type not in cls.DEFAULT_CONFIGS:
            raise ValueError(f"No default config for VM type: {vm_type}")
        
        config = cls.DEFAULT_CONFIGS[vm_type]
        return {
            "vm_type": config.vm_type,
            "chassis_type": config.chassis_type,
            "genome_file": config.genome_file,
            "resource_limits": config.resource_limits or {},
            "custom_params": config.custom_params or {}
        }
    
    @classmethod
    def load_from_file(cls, config_path: str) -> Dict[str, Any]:
        """
        Load configuration from file - mirrors pylua file-based config.
        """
        config_file = Path(config_path)
        if not config_file.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        # Validate loaded config
        if "vm_type" in config:
            cls.validate_config(config["vm_type"], config)
        
        return config
    
    @classmethod
    def save_to_file(cls, config: Dict[str, Any], config_path: str) -> None:
        """Save configuration to file - pylua persistence pattern."""
        config_file = Path(config_path)
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    @classmethod
    def validate_config(cls, vm_type: str, config: Dict[str, Any]) -> bool:
        """
        Validate configuration for VM type.
        Mirrors pylua validation pattern.
        """
        required_fields = ["vm_type"]
        
        for field in required_fields:
            if field not in config:
                raise ValueError(f"Missing required config field: {field}")
        
        if config["vm_type"] != vm_type:
            raise ValueError(f"Config vm_type {config['vm_type']} doesn't match {vm_type}")
        
        # Validate resource limits
        if "resource_limits" in config:
            cls._validate_resource_limits(config["resource_limits"])
        
        # Validate biological constraints
        if "custom_params" in config:
            cls._validate_biological_params(vm_type, config["custom_params"])
        
        return True
    
    @classmethod
    def _validate_resource_limits(cls, limits: Dict[str, Any]) -> None:
        """Validate resource limit values - pylua resource validation."""
        if "max_ribosomes" in limits and limits["max_ribosomes"] <= 0:
            raise ValueError("max_ribosomes must be positive")
        
        if "max_atp" in limits and not (0 <= limits["max_atp"] <= 100):
            raise ValueError("max_atp must be between 0 and 100")
        
        if "max_memory_kb" in limits and limits["max_memory_kb"] <= 0:
            raise ValueError("max_memory_kb must be positive")
    
    @classmethod
    def _validate_biological_params(cls, vm_type: str, params: Dict[str, Any]) -> None:
        """Validate biological parameters for VM type."""
        # VM type specific validation
        if vm_type == "syn3a" and params.get("essential_only") is False:
            raise ValueError("Syn3A VMs require essential_only=True")
        
        if vm_type == "minimal_cell" and not params.get("minimal_functions_only", True):
            raise ValueError("Minimal cell VMs require minimal_functions_only=True")
    
    @classmethod
    def merge_configs(cls, base_config: Dict[str, Any], override_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge override config with base config.
        Mirrors pylua config merging pattern.
        """
        merged = base_config.copy()
        
        for key, value in override_config.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = {**merged[key], **value}
            else:
                merged[key] = value
        
        return merged
    
    @classmethod
    def get_supported_vm_types(cls) -> List[str]:
        """Get list of supported VM types - pylua capability reporting."""
        return list(cls.DEFAULT_CONFIGS.keys())
    
    @classmethod
    def create_config_template(cls, vm_type: str, output_path: str) -> None:
        """Create configuration template file - pylua template generation."""
        if vm_type not in cls.DEFAULT_CONFIGS:
            raise ValueError(f"Unsupported VM type: {vm_type}")
        
        template_config = cls.load_defaults(vm_type)
        template_config["_template"] = True
        template_config["_description"] = f"Configuration template for {vm_type} biological VM"
        
        cls.save_to_file(template_config, output_path)
```

#### Day 20-21: CLI Integration Updates
- Update `interactive_bioxen.py` to use factory pattern
- Add new VM type selection menus
- Preserve all existing functionality
- Test interactive workflows with new API

### Phase 4: Integration & Polish (Week 4)
**Objective**: Complete integration, testing, documentation, and optimization

#### Day 22-24: Comprehensive Testing
**Create `tests/test_api/` test suite**:
```python
# tests/test_api/test_factory.py
import pytest
from src.api.factory import create_bio_vm, VM_TYPE_MAPPING
from src.api.biological_vm import Syn3AVM, EColiVM, MinimalCellVM

class TestFactoryPattern:
    def test_create_syn3a_vm(self):
        vm = create_bio_vm("test_syn3a", "syn3a")
        assert isinstance(vm, Syn3AVM)
        assert vm.vm_id == "test_syn3a"
        assert vm.get_vm_type() == "syn3a"
    
    def test_create_ecoli_vm(self):
        vm = create_bio_vm("test_ecoli", "ecoli")
        assert isinstance(vm, EColiVM)
        assert vm.get_vm_type() == "ecoli"
    
    def test_unsupported_vm_type(self):
        with pytest.raises(ValueError, match="Unsupported VM type"):
            create_bio_vm("test", "unsupported_type")
    
    def test_vm_lifecycle(self):
        vm = create_bio_vm("lifecycle_test", "syn3a")
        assert vm.start()
        assert vm.pause()
        assert vm.resume()
        assert vm.destroy()

# tests/test_api/test_resource_manager.py
from src.api.resource_manager import BioResourceManager
from src.api.factory import create_bio_vm

class TestResourceManager:
    def test_resource_allocation(self):
        vm = create_bio_vm("resource_test", "syn3a")
        manager = BioResourceManager(vm)
        
        assert manager.allocate_atp(50.0)
        assert manager.allocate_ribosomes(10)
        assert manager.allocate_memory(100)
    
    def test_resource_monitoring(self):
        vm = create_bio_vm("monitor_test", "ecoli")
        manager = BioResourceManager(vm)
        
        usage = manager.get_resource_usage()
        assert isinstance(usage, dict)
        
        available = manager.get_available_resources()
        assert isinstance(available, dict)
```

#### Day 25-26: Documentation
**Create comprehensive API documentation**:
- API reference documentation
- Usage examples and tutorials
- Migration guide for existing users
- Integration patterns and best practices

**`docs/api/README.md`**:
```markdown
# BioXen Factory Pattern API

## Quick Start

### Basic VM Usage (Default)
```python
from src.api.factory import create_bio_vm
from src.api.resource_manager import BioResourceManager
from src.api.config_manager import ConfigManager

# Create a basic biological VM (runs directly on BioXen hypervisor)
vm = create_bio_vm("my_syn3a", "syn3a", "basic")  # vm_type="basic" is default

# Start the VM
vm.start()

# Manage resources
manager = BioResourceManager(vm)
manager.allocate_atp(75.0)
manager.allocate_ribosomes(20)

# Check status
status = vm.get_status()
print(f"VM Status: {status}")

# Clean up
vm.destroy()
```

### XCP-ng VM Usage (Enhanced Isolation)
```python
from src.api.factory import create_bio_vm

# XCP-ng configuration (required for vm_type="xcpng")
xcpng_config = {
    "xcpng_config": {
        "xapi_url": "https://xcpng-host:443",
        "username": "root",
        "password": "secure_password",
        "template_name": "bioxen-bio-template",
        "ssh_user": "root",
        "ssh_key_path": "/path/to/ssh/key",
        "vm_memory": "4GB",
        "vm_vcpus": 4
    }
}

# Create XCP-ng biological VM (runs basic VM inside full virtual machine)
vm = create_bio_vm("isolated_ecoli", "ecoli", "xcpng", xcpng_config)

# Start the VM (creates XCP-ng VM then starts biological VM inside it)
vm.start()

# Execute biological process via SSH
result = vm.execute_biological_process('start_transcription(["lacZ", "lacY"])')
print(f"Transcription result: {result}")

# Clean up
vm.destroy()
```

## Supported Configurations

### Biological Types
- `syn3a`: Minimal Syn3A genome VM
- `ecoli`: E.coli bacterial VM
- `minimal_cell`: Basic cellular functions VM

### VM Types
- `basic`: Direct execution on BioXen hypervisor (default)
  - Fastest performance
  - Direct integration with existing hypervisor
  - Suitable for development and standard workflows

- `xcpng`: BioXen VMs running inside XCP-ng virtual machines
  - Enhanced isolation and security
  - Remote execution via SSH
  - Suitable for production and distributed computing
  - Requires XCP-ng configuration
- `minimal_cell`: Basic minimal cell VM

## Configuration

```python
# Load default config
config = ConfigManager.load_defaults("syn3a")

# Create VM with custom config
custom_config = {
    "resource_limits": {"max_ribosomes": 30},
    "custom_params": {"debug_mode": True}
}
vm = create_bio_vm("custom_vm", "syn3a", "basic", custom_config)
```

### XCP-ng Configuration Example
```python
# Create XCP-ng config for enhanced isolation
xcpng_config = {
    "xcpng_config": {
        "xapi_url": "https://xcpng-host:443",
        "username": "root",
        "password": "secure_password",
        "template_name": "bioxen-bio-template",
        "ssh_user": "root",
        "ssh_key_path": "/path/to/ssh/key"
    }
}

# Create E.coli VM inside XCP-ng virtual machine
vm = create_bio_vm("isolated_ecoli", "ecoli", "xcpng", xcpng_config)
```

## Pattern Alignment with pylua_bioxen_vm_lib

This implementation directly mirrors the successful pylua patterns:

### pylua_bioxen_vm_lib Pattern
```python
# pylua usage
vm = create_vm("my_vm", vm_type="xcpng", config=xcpng_config)
result = vm.execute_string('return 2 + 2')
```

### BioXen_jcvi_vm_lib Pattern (This Implementation)
```python
# BioXen usage (same pattern)
vm = create_bio_vm("my_vm", "syn3a", vm_type="xcpng", config=xcpng_config)
result = vm.execute_biological_process('start_transcription(["gene1"])')
```

**Key Alignment Points:**
- Both use factory functions with `vm_type` parameter
- Both support "basic" (direct) and "xcpng" (virtualized) execution
- Both use delegation pattern to existing infrastructure
- Both require configuration for XCP-ng type
- Both provide specialized methods per VM type
```

#### Day 27-28: Performance Optimization & Future-Proofing
- Profile wrapper overhead and optimize hot paths
- Implement caching for frequently accessed data
- Add plugin system foundation for extensibility
- Prepare infrastructure for inter-VM communication

**Package Initialization (`src/api/__init__.py`)** (Following pylua package structure):
```python
"""
BioXen Factory Pattern API

This package provides a unified interface for creating and managing
biological virtual machines through a factory pattern.

Mirrors pylua_bioxen_vm_lib API structure and patterns.
"""

from .factory import create_bio_vm, get_supported_vm_types, validate_vm_type
from .biological_vm import BiologicalVM, Syn3AVM, EColiVM, MinimalCellVM
from .resource_manager import BioResourceManager, BioVMManager
from .config_manager import ConfigManager, VMConfig

# Public API exports - mirrors pylua package exports
__all__ = [
    # Factory functions
    'create_bio_vm',
    'get_supported_vm_types', 
    'validate_vm_type',
    
    # VM classes
    'BiologicalVM',
    'Syn3AVM', 
    'EColiVM',
    'MinimalCellVM',
    
    # Management classes
    'BioResourceManager',
    'BioVMManager',
    'ConfigManager',
    'VMConfig'
]

__version__ = '0.1.0'

# Quick start function - mirrors pylua convenience patterns
def quick_start_vm(vm_type: str = "syn3a", vm_id: str = "default") -> BiologicalVM:
    """
    Quick start function for simple VM creation.
    Mirrors pylua quick start patterns.
    """
    return create_bio_vm(vm_id, vm_type)

# Compatibility aliases - mirrors pylua backward compatibility
create_vm = create_bio_vm  # Alias for pylua compatibility
VMManager = BioVMManager   # Alias for consistency
```

---

## Success Metrics

### Week 1 Deliverables
- [ ] API directory structure created
- [ ] Abstract `BiologicalVM` class implemented
- [ ] `Syn3AVM` concrete implementation complete
- [ ] Basic wrapper functionality validated
- [ ] Initial test suite passing

### Week 2 Deliverables
- [ ] All VM classes implemented (`EColiVM`, `MinimalCellVM`)
- [ ] Factory function with type mapping complete
- [ ] VM creation and registration working
- [ ] Integration with existing hypervisor validated
- [ ] Config validation implemented

### Week 3 Deliverables
- [ ] `BioResourceManager` wrapper complete
- [ ] `ConfigManager` with defaults and validation
- [ ] CLI integration updated to use factory pattern
- [ ] All existing functionality preserved
- [ ] Performance testing completed

### Week 4 Deliverables
- [ ] Comprehensive test suite (90%+ coverage)
- [ ] Complete API documentation
- [ ] Migration guide for existing users
- [ ] Performance optimization completed
- [ ] Plugin system foundation ready

---

## Critical Implementation Insights (From pylua_bioxen_vm_lib Alignment)

### 1. **Delegation Pattern** (Key Learning from pylua)
The pylua VMs don't replace underlying functionality - they **delegate** to it:
- `XCPngVM.execute_string()` → delegates to SSH session
- `BiologicalVM.start()` → delegates to `hypervisor.start_vm()`
- **Critical**: Our VM classes should be **wrappers**, not replacements

### 2. **Type-Specific Behavior** (pylua Specialization Pattern)
Each VM type has specialized methods following pylua patterns:
- `XCPngVM` has XAPI-specific methods (`start()`, `get_status()`, `install_package()`)
- `Syn3AVM` should have biology-specific methods (`start_transcription()`, `get_atp_level()`, `optimize_minimal_metabolism()`)
- `EColiVM` should have prokaryotic methods (`manage_operons()`, `get_plasmid_count()`)

### 3. **Factory Pattern Implementation** (Exact pylua Approach)
```python
# pylua pattern that we must follow exactly:
VM_TYPE_MAPPING = {
    "syn3a": Syn3AVM,      # mirrors "xcpng": XCPngVM
    "ecoli": EColiVM,      # mirrors "basic": BasicLuaVM  
    "minimal_cell": MinimalCellVM
}

def create_bio_vm(vm_id: str, biological_type: str, vm_type: str = "basic", config: Optional[Dict] = None) -> BiologicalVM:
    """Mirrors pylua create_vm() function signature and behavior exactly with vm_type support."""
```

### 4. **Configuration Management** (pylua ConfigManager Pattern)
- File-based configs with JSON support (mirrors pylua xcpng_config.json)
- Default configurations per VM type
- Validation and merging capabilities  
- Template generation for users

### 5. **VMManager Integration** (pylua Multi-VM Pattern)
```python
# Must follow pylua VMManager pattern:
class BioVMManager:
    def create_vm(self, vm_id: str, vm_type: str = "basic", config: Optional[Dict] = None):
        """Exact pylua VMManager.create_vm() signature"""
    
    def execute_vm_sync(self, vm_id: str, code: str) -> Dict[str, Any]:
        """Mirrors pylua VMManager.execute_vm_sync()"""
```

### 6. **Error Handling** (pylua Exception Patterns)
- Specific exceptions for different error types
- ValueError for unsupported VM types
- SessionNotFoundError equivalents for biological VMs
- Graceful degradation and cleanup

### 7. **CLI Integration** (pylua Interactive Pattern)
- Update `interactive_bioxen.py` to use factory pattern
- VM type selection menus (mirrors pylua CLI workflow)
- Configuration management interface
- Session management with attach/detach

---

## Future Enhancements (Post-MVP)

### Inter-VM Communication
- Biological signal exchange protocols
- Message passing between VMs
- Resource sharing coordination
- Communication circuit implementation

### Advanced Features
- Real-time monitoring dashboards
- Batch operation support
- Multi-user session support
- Plugin system for custom VM types

### Performance Optimizations
- Async/await support for long-running operations
- Connection pooling for resource management
- Caching layer for genome data
- GPU acceleration for biological computations

---

## Conclusion

This implementation plan provides a comprehensive roadmap for transforming BioXen_jcvi_vm_lib into a factory pattern-based library following proven pylua_bioxen_vm_lib architectural patterns. The approach is:

- **Low Risk**: Non-disruptive wrapper pattern preserves existing functionality (proven by pylua)
- **High Value**: Provides clean, unified API for biological VM management
- **Pattern-Aligned**: Follows successful pylua_bioxen_vm_lib v0.1.22 architecture exactly
- **Well-Tested**: Comprehensive testing strategy ensures quality
- **Future-Ready**: Extensible architecture supports future enhancements
- **Ecosystem Consistent**: Maintains consistency across BioXen project family

**Critical Success Factor**: Strict adherence to pylua_bioxen_vm_lib patterns ensures:
- Proven architectural approach
- Consistent user experience across BioXen tools
- Reduced implementation risk through pattern reuse
- Easier maintenance and extension

The existing codebase provides an excellent foundation, and this plan leverages that strength while adding the requested factory pattern capabilities using battle-tested patterns from pylua_bioxen_vm_lib. The 4-week timeline is realistic given the mature underlying infrastructure and proven architectural patterns.

**Recommendation**: Begin implementation immediately following the pylua patterns. The codebase analysis confirms exceptional readiness for this enhancement, and the pylua specification provides a proven blueprint for success.
