# BioXen_jcvi_vm_lib Factory Pattern API Implementation Plan
## ARCHITECTURAL DECISION: Infrastructure-Focused Following pylua_bioxen_vm_lib Exactly

**RESOLVED**: We will follow the **Infrastructure-focused approach** to maintain exact alignment with pylua_bioxen_vm_lib patterns.

---

## **Final VM Class Architecture** (Infrastructure-Focused):

### Primary VM Classes (Infrastructure Dimension)

1. **`BiologicalVM`** - Abstract base class
   - Common interface for all biological VMs
   - Mirrors pylua's base VM pattern

2. **`BasicBiologicalVM`** - Direct execution on BioXen hypervisor
   - Equivalent to pylua's `BasicLuaVM`
   - Fast, direct integration with existing hypervisor
   - Biological type handled as constructor parameter

3. **`XCPngBiologicalVM`** - Execution inside XCP-ng virtual machines
   - Equivalent to pylua's `XCPngVM`
   - Enhanced isolation via SSH execution
   - Biological type handled as constructor parameter

### Biological Type Handling (Composition Pattern)

Instead of separate `Syn3AVM`, `EColiVM` classes, biological behavior is handled through:
- **Constructor parameter**: `biological_type` ("syn3a", "ecoli", "minimal_cell")
- **Composition**: VM classes delegate to biological-specific modules
- **Configuration**: Biological-specific settings in config dictionaries

---

## **Factory Function Signature** (Final):

```python
def create_bio_vm(vm_id: str, biological_type: str, vm_type: str = "basic", config: Optional[Dict[str, Any]] = None) -> BiologicalVM:
    """
    Create biological VM following pylua pattern exactly.
    
    Args:
        vm_id: Unique identifier for the VM
        biological_type: Organism type ("syn3a", "ecoli", "minimal_cell")
        vm_type: Infrastructure type ("basic", "xcpng") - mirrors pylua exactly
        config: Optional configuration (required for xcpng)
    
    Returns:
        BasicBiologicalVM or XCPngBiologicalVM instance
    """
```

**Key Benefits of Infrastructure-Focused Approach:**

1. **Perfect pylua Alignment**: Matches pylua_bioxen_vm_lib architecture exactly
2. **Clean Separation**: Infrastructure concerns separate from biological concerns  
3. **Scalable**: Easy to add new biological types without new VM classes
4. **Consistent**: Same pattern users already know from pylua
5. **Maintainable**: Fewer classes, clearer responsibilities

---

## **Updated Implementation Examples**:

### Basic Biological VM Usage
```python
from src.api.factory import create_bio_vm

# Create basic Syn3A VM (direct hypervisor execution)
vm = create_bio_vm("my_syn3a", "syn3a", "basic")  # vm_type="basic" is default
vm.start()

# Create basic E.coli VM  
vm = create_bio_vm("my_ecoli", "ecoli")  # defaults to basic
vm.start()
```

### XCP-ng Biological VM Usage
```python
# XCP-ng configuration
xcpng_config = {
    "xcpng_config": {
        "xapi_url": "https://xcpng-host:443",
        "username": "root",
        "template_name": "bioxen-bio-template",
        "ssh_user": "root",
        "ssh_key_path": "/path/to/ssh/key"
    }
}

# Create XCP-ng Syn3A VM (enhanced isolation)
vm = create_bio_vm("isolated_syn3a", "syn3a", "xcpng", xcpng_config)
vm.start()

# Create XCP-ng E.coli VM
vm = create_bio_vm("isolated_ecoli", "ecoli", "xcpng", xcpng_config)  
vm.start()
```

---

## **Class Implementation Details**:

### BasicBiologicalVM Class
```python
class BasicBiologicalVM(BiologicalVM):
    """
    Basic biological VM running directly on BioXen hypervisor.
    Mirrors pylua BasicLuaVM pattern exactly.
    """
    
    def __init__(self, vm_id: str, biological_type: str, hypervisor: BioXenHypervisor, config: Dict[str, Any]):
        super().__init__(vm_id, "basic", hypervisor, config)
        self.biological_type = biological_type  # "syn3a", "ecoli", "minimal_cell"
        self.biological_module = self._load_biological_module(biological_type)
    
    def execute_biological_process(self, process_code: str) -> Dict[str, Any]:
        """Execute biological process directly on hypervisor."""
        return self.hypervisor.execute_process(self.vm_id, process_code)
    
    def _load_biological_module(self, biological_type: str):
        """Load biological-specific behavior module."""
        # Delegate to existing biological modules
        if biological_type == "syn3a":
            from ..biology.syn3a import Syn3ABehavior
            return Syn3ABehavior(self.hypervisor, self.vm_id)
        elif biological_type == "ecoli":
            from ..biology.ecoli import EColiBehavior  
            return EColiBehavior(self.hypervisor, self.vm_id)
        # ... etc
```

### XCPngBiologicalVM Class  
```python
class XCPngBiologicalVM(BiologicalVM):
    """
    XCP-ng biological VM running basic VMs inside virtual machines.
    Mirrors pylua XCPngVM pattern exactly.
    """
    
    def __init__(self, vm_id: str, biological_type: str, hypervisor: BioXenHypervisor, config: Dict[str, Any]):
        super().__init__(vm_id, "xcpng", hypervisor, config)
        self.biological_type = biological_type
        self.biological_module = self._load_biological_module(biological_type)
        self.xcpng_vm_uuid = None
        self.vm_ip = None
    
    def start(self) -> bool:
        """Start XCP-ng VM then start biological VM inside it."""
        # Create XCP-ng VM from template
        self.xcpng_vm_uuid = self._create_xcpng_vm()
        self._start_xcpng_vm()
        self.vm_ip = self._get_vm_ip()
        
        # Start biological VM inside XCP-ng VM via SSH
        return self._start_biological_vm_via_ssh()
    
    def execute_biological_process(self, process_code: str) -> Dict[str, Any]:
        """Execute biological process via SSH in XCP-ng VM."""
        return self._execute_via_ssh(process_code)
```

---

## **Why This Approach is Correct**:

### 1. **Exact pylua Pattern Match**
- `vm_type` parameter controls infrastructure (`"basic"` vs `"xcpng"`)  
- Biological concerns handled through composition, not inheritance
- Same factory function signature style as pylua

### 2. **Clean Architecture**
- Infrastructure and biological concerns properly separated
- Easy to add new biological types without new VM classes
- Consistent with established patterns users know

### 3. **Implementation Benefits**
- Fewer classes to maintain
- Clear responsibility boundaries  
- Scalable for future biological types
- Perfect alignment with existing pylua ecosystem

This infrastructure-focused approach ensures our BioXen_jcvi_vm_lib factory pattern API will be consistent, maintainable, and familiar to users already using pylua_bioxen_vm_lib.