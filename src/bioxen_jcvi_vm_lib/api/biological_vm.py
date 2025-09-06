from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from ..hypervisor.core import BioXenHypervisor, VirtualMachine

class BiologicalVM(ABC):
    """
    Abstract base class for all biological VMs.
    Hypervisor-focused implementation without JCVI dependencies.
    """
    
    def __init__(self, vm_id: str, biological_type: str, hypervisor: BioXenHypervisor, config: Dict[str, Any]):
        self.vm_id = vm_id
        self.biological_type = biological_type
        self.hypervisor = hypervisor
        self.config = config
        self._vm_instance: Optional[VirtualMachine] = None
    
    @abstractmethod
    def get_vm_type(self) -> str:
        """Return the VM infrastructure type (basic/xcpng)."""
        pass
    
    def get_biological_type(self) -> str:
        """Return the biological organism type."""
        return self.biological_type
    
    def start(self) -> bool:
        """Start the biological VM."""
        return self.hypervisor.start_vm(self.vm_id)
    
    def destroy(self) -> bool:
        """Destroy the biological VM."""
        return self.hypervisor.destroy_vm(self.vm_id)
    
    def get_status(self) -> Dict[str, Any]:
        """Get current VM status."""
        return self.hypervisor.get_vm_status(self.vm_id)
    
    def execute_biological_process(self, process_code: str) -> Dict[str, Any]:
        """Execute biological process."""
        return self._execute_biological_process_impl(process_code)
    
    def get_biological_metrics(self) -> Dict[str, Any]:
        """Get biological metrics."""
        return self._get_biological_metrics_impl()
    
    def allocate_resources(self, resources: Dict[str, Any]) -> bool:
        """Allocate resources to the VM."""
        return self.hypervisor.allocate_vm_resources(self.vm_id, resources)
    
    def get_resource_usage(self) -> Dict[str, Any]:
        """Get current resource usage."""
        return self.hypervisor.get_vm_resource_usage(self.vm_id)
    
    @abstractmethod
    def _execute_biological_process_impl(self, process_code: str) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def _get_biological_metrics_impl(self) -> Dict[str, Any]:
        pass


class BasicBiologicalVM(BiologicalVM):
    """Basic biological VM using direct hypervisor execution."""
    
    def get_vm_type(self) -> str:
        return "basic"
    
    def _execute_biological_process_impl(self, process_code: str) -> Dict[str, Any]:
        return self.hypervisor.execute_process(self.vm_id, process_code)
    
    def _get_biological_metrics_impl(self) -> Dict[str, Any]:
        status = self.get_status()
        if self.biological_type == "syn3a":
            return {
                'essential_genes': 473,
                'genome_size': '~580kb',
                'status': status.get('biological_status', {})
            }
        elif self.biological_type == "ecoli":
            return {
                'gene_count': 4377,
                'genome_size': '~4.6Mb',
                'status': status.get('biological_status', {})
            }
        else:
            return {
                'minimal_functions': ['dna_replication', 'protein_synthesis'],
                'status': status.get('biological_status', {})
            }


class XCPngBiologicalVM(BiologicalVM):
    """XCP-ng biological VM with SSH execution."""
    
    def __init__(self, vm_id: str, biological_type: str, hypervisor: BioXenHypervisor, config: Dict[str, Any]):
        super().__init__(vm_id, biological_type, hypervisor, config)
        self.xapi_config = config.get('xcpng_config', {})
    
    def get_vm_type(self) -> str:
        return "xcpng"
    
    def _execute_biological_process_impl(self, process_code: str) -> Dict[str, Any]:
        raise NotImplementedError("XCP-ng execution will be implemented in Phase 2")
    
    def _get_biological_metrics_impl(self) -> Dict[str, Any]:
        raise NotImplementedError("XCP-ng metrics will be implemented in Phase 2")
