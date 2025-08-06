"""
BioXen Hypervisor Core - Main hypervisor control logic

This module implements the core biological hypervisor functionality,
managing virtual machines running bacterial genomes on configurable cellular chassis.
"""

import time
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

# Import chassis support
try:
    from ..chassis import ChassisType, BaseChassis, EcoliChassis, YeastChassis
except ImportError:
    # Fallback for direct execution
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent))
    from chassis import ChassisType, BaseChassis, EcoliChassis, YeastChassis

class VMState(Enum):
    """Virtual Machine states"""
    CREATED = "created"
    RUNNING = "running" 
    PAUSED = "paused"
    STOPPED = "stopped"
    ERROR = "error"

class ResourceType(Enum):
    """Types of biological resources"""
    RIBOSOMES = "ribosomes"
    ATP = "atp"
    TRNA = "trna"
    RNA_POLYMERASE = "rna_polymerase"
    AMINO_ACIDS = "amino_acids"
    NUCLEOTIDES = "nucleotides"

@dataclass
class ResourceAllocation:
    """Resource allocation for a VM"""
    ribosomes: int = 0
    atp_percentage: float = 0.0
    rna_polymerase: int = 0
    memory_kb: int = 0  # DNA/RNA space in "kilobases"
    priority: int = 1   # 1=low, 5=high
    boot_time: Optional[float] = None  # Boot time in seconds

@dataclass
class VirtualMachine:
    """Represents a virtualized Syn3A instance"""
    vm_id: str
    state: VMState = VMState.CREATED
    genome_template: str = "syn3a_minimal"
    resources: ResourceAllocation = field(default_factory=ResourceAllocation)
    start_time: Optional[float] = None
    last_context_switch: Optional[float] = None
    cpu_time_used: float = 0.0
    health_status: str = "unknown"
    
    def __post_init__(self):
        if self.start_time is None:
            self.start_time = time.time()

class BioXenHypervisor:
    """
    Main hypervisor class implementing biological virtualization
    
    Manages multiple virtual machines on configurable cellular chassis,
    handling resource allocation, scheduling, and isolation.
    """
    
    def __init__(self, max_vms: int = 4, chassis_type: ChassisType = ChassisType.ECOLI, 
                 chassis_config: Optional[Dict[str, Any]] = None):
        self.max_vms = max_vms
        self.chassis_type = chassis_type
        self.chassis_config = chassis_config or {}
        
        # Initialize chassis
        self.chassis = self._initialize_chassis()
        if not self.chassis or not self.chassis.initialize():
            raise RuntimeError(f"Failed to initialize {chassis_type.value} chassis")
        
        self.vms: Dict[str, VirtualMachine] = {}
        self.active_vm: Optional[str] = None
        self.resource_monitor = ResourceMonitor()
        self.scheduler = RoundRobinScheduler()
        
        # Get chassis-specific resource limits
        capabilities = self.chassis.get_capabilities()
        self.total_ribosomes = capabilities.max_ribosomes
        
        # Hypervisor overhead tracking
        self.hypervisor_overhead = 0.15  # 15% overhead
        self.available_ribosomes = int(self.total_ribosomes * (1 - self.hypervisor_overhead))
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"BioXen Hypervisor initialized with {chassis_type.value} chassis")
    
    def _initialize_chassis(self) -> Optional[BaseChassis]:
        """Initialize the appropriate chassis based on type"""
        chassis_id = self.chassis_config.get("chassis_id", f"{self.chassis_type.value}_primary")
        
        if self.chassis_type == ChassisType.ECOLI:
            return EcoliChassis(chassis_id)
        elif self.chassis_type == ChassisType.YEAST:
            return YeastChassis(chassis_id)
        else:
            raise ValueError(f"Unsupported chassis type: {self.chassis_type}")
    
    def get_chassis_info(self) -> Dict[str, Any]:
        """Get information about the current chassis"""
        if self.chassis:
            return self.chassis.get_chassis_info()
        return {"error": "No chassis initialized"}
        
    def create_vm(self, vm_id: str, genome_template: str = "syn3a_minimal", 
                  resource_allocation: Optional[ResourceAllocation] = None) -> bool:
        """Create a new virtual machine"""
        
        if len(self.vms) >= self.max_vms:
            self.logger.error(f"Cannot create VM {vm_id}: Maximum VMs ({self.max_vms}) reached")
            return False
            
        if vm_id in self.vms:
            self.logger.error(f"VM {vm_id} already exists")
            return False
            
        if resource_allocation is None:
            # Default resource allocation based on chassis
            capabilities = self.chassis.get_capabilities()
            default_ribosomes = self.available_ribosomes // 4  # Fair share
            default_memory = 120 if self.chassis_type == ChassisType.ECOLI else 500  # KB
            
            resource_allocation = ResourceAllocation(
                ribosomes=default_ribosomes,
                atp_percentage=25.0,  # 25% of ATP
                rna_polymerase=10,
                memory_kb=default_memory,
                priority=1
            )
        
        # Prepare resource request for chassis
        resource_request = {
            "ribosomes": resource_allocation.ribosomes,
            "atp_percentage": resource_allocation.atp_percentage,
            "memory_kb": resource_allocation.memory_kb,
            "rna_polymerase": resource_allocation.rna_polymerase
        }
        
        # Try to allocate resources through chassis
        if not self.chassis.allocate_resources(vm_id, resource_request):
            self.logger.error(f"Failed to allocate chassis resources for VM {vm_id}")
            return False
        
        # Create VM instance
        vm = VirtualMachine(
            vm_id=vm_id,
            genome_template=genome_template,
            resources=resource_allocation
        )
        
        # Create isolation environment
        if not self.chassis.create_isolation_environment(vm_id):
            self.logger.warning(f"Failed to create isolation environment for VM {vm_id}")
            # Continue anyway - isolation is best-effort
        
        self.vms[vm_id] = vm
        
        # Create concise genome description for logging
        if hasattr(genome_template, 'organism'):
            genome_desc = f"{genome_template.organism} ({len(genome_template.genes)} genes)"
        elif isinstance(genome_template, str):
            genome_desc = genome_template
        else:
            genome_desc = f"{type(genome_template).__name__}"
            
        self.logger.info(f"VM {vm_id} created successfully with {genome_desc} on {self.chassis_type.value} chassis")
        return True
        
    def start_vm(self, vm_id: str) -> bool:
        """Start a virtual machine"""
        if vm_id not in self.vms:
            self.logger.error(f"VM {vm_id} does not exist")
            return False
            
        vm = self.vms[vm_id]
        if vm.state != VMState.CREATED and vm.state != VMState.STOPPED:
            self.logger.error(f"VM {vm_id} cannot be started from state {vm.state}")
            return False
            
        # Simulate boot sequence
        self._boot_vm(vm)
        vm.state = VMState.RUNNING
        vm.start_time = time.time()
        
        self.logger.info(f"Started VM {vm_id}")
        return True
        
    def pause_vm(self, vm_id: str) -> bool:
        """Pause a running virtual machine"""
        if vm_id not in self.vms:
            return False
            
        vm = self.vms[vm_id]
        if vm.state != VMState.RUNNING:
            return False
            
        vm.state = VMState.PAUSED
        self.logger.info(f"Paused VM {vm_id}")
        return True
        
    def resume_vm(self, vm_id: str) -> bool:
        """Resume a paused virtual machine"""
        if vm_id not in self.vms:
            return False
            
        vm = self.vms[vm_id]
        if vm.state != VMState.PAUSED:
            return False
            
        vm.state = VMState.RUNNING
        self.logger.info(f"Resumed VM {vm_id}")
        return True
        
    def destroy_vm(self, vm_id: str) -> bool:
        """Destroy a virtual machine and free its resources"""
        if vm_id not in self.vms:
            return False
            
        vm = self.vms[vm_id]
        
        # Cleanup chassis resources
        if not self.chassis.deallocate_resources(vm_id):
            self.logger.warning(f"Failed to deallocate chassis resources for VM {vm_id}")
        
        # Cleanup chassis environment
        if not self.chassis.cleanup_vm_environment(vm_id):
            self.logger.warning(f"Failed to cleanup chassis environment for VM {vm_id}")
        
        # Cleanup VM-specific resources
        self._cleanup_vm(vm)
        
        # Remove from scheduler if active
        if self.active_vm == vm_id:
            self.active_vm = None
            
        del self.vms[vm_id]
        self.logger.info(f"Destroyed VM {vm_id} and cleaned up {self.chassis_type.value} chassis resources")
        return True
        
    def get_vm_status(self, vm_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed status of a virtual machine"""
        if vm_id not in self.vms:
            return None
            
        vm = self.vms[vm_id]
        uptime = time.time() - vm.start_time if vm.start_time else 0
        
        return {
            "vm_id": vm.vm_id,
            "state": vm.state.value,
            "uptime_seconds": uptime,
            "cpu_time_used": vm.cpu_time_used,
            "ribosome_allocation": vm.resources.ribosomes,
            "atp_percentage": vm.resources.atp_percentage,
            "memory_kb": vm.resources.memory_kb,
            "health_status": vm.health_status,
            "priority": vm.resources.priority
        }
        
    def list_vms(self) -> List[Dict[str, Any]]:
        """List all virtual machines"""
        return [self.get_vm_status(vm_id) for vm_id in self.vms.keys()]
        
    def run_scheduler(self) -> None:
        """Run one iteration of the VM scheduler"""
        running_vms = [vm_id for vm_id, vm in self.vms.items() 
                      if vm.state == VMState.RUNNING]
        
        if not running_vms:
            return
            
        # Context switch if needed
        next_vm = self.scheduler.select_next_vm(running_vms, self.active_vm)
        
        if next_vm != self.active_vm:
            self._context_switch(self.active_vm, next_vm)
            self.active_vm = next_vm
            
    def get_system_resources(self) -> Dict[str, Any]:
        """Get current system resource usage"""
        allocated_ribosomes = sum(vm.resources.ribosomes for vm in self.vms.values())
        allocated_atp = sum(vm.resources.atp_percentage for vm in self.vms.values())
        
        return {
            "total_ribosomes": self.total_ribosomes,
            "available_ribosomes": self.available_ribosomes,
            "allocated_ribosomes": allocated_ribosomes,
            "free_ribosomes": self.available_ribosomes - allocated_ribosomes,
            "total_atp_allocated": allocated_atp,
            "hypervisor_overhead": self.hypervisor_overhead,
            "active_vms": len([vm for vm in self.vms.values() if vm.state == VMState.RUNNING])
        }
        
    def _boot_vm(self, vm: VirtualMachine) -> None:
        """Simulate the VM boot sequence"""
        self.logger.info(f"Booting VM {vm.vm_id}...")
        # 1. Load genome template
        # 2. Initialize core genes  
        # 3. Allocate resources
        # 4. Start transcription/translation
        vm.health_status = "healthy"
        
    def _cleanup_vm(self, vm: VirtualMachine) -> None:
        """Clean up VM resources"""
        self.logger.info(f"Cleaning up VM {vm.vm_id}...")
        # 1. Stop all processes
        # 2. Degrade VM-specific proteins
        # 3. Free allocated memory
        # 4. Release resources
        
    def _context_switch(self, current_vm: Optional[str], next_vm: str) -> None:
        """Perform context switch between VMs"""
        context_switch_time = 30.0  # 30 seconds as specified in readme
        
        if current_vm:
            # Save current VM state
            current = self.vms[current_vm]
            current.last_context_switch = time.time()
            current.cpu_time_used += context_switch_time
            self.logger.info(f"Context switch: {current_vm} -> {next_vm}")
        
        # Load next VM state  
        next_vm_obj = self.vms[next_vm]
        next_vm_obj.last_context_switch = time.time()


class ResourceMonitor:
    """Monitors biological resource usage"""
    
    def __init__(self):
        self.atp_level = 100.0  # Percentage
        self.ribosome_utilization = 0.0
        
    def get_atp_level(self) -> float:
        """Get current ATP level (0-100%)"""
        # In real implementation, this would read from biosensors
        return self.atp_level
        
    def get_ribosome_utilization(self) -> float:
        """Get current ribosome utilization (0-100%)"""
        return self.ribosome_utilization


class RoundRobinScheduler:
    """Simple round-robin scheduler for VMs"""
    
    def __init__(self, time_quantum: float = 60.0):
        self.time_quantum = time_quantum  # seconds
        self.last_switch_time = time.time()
        
    def select_next_vm(self, running_vms: List[str], current_vm: Optional[str]) -> str:
        """Select next VM to run"""
        if not running_vms:
            return current_vm
            
        if current_vm is None:
            return running_vms[0]
            
        # Check if time quantum expired
        if time.time() - self.last_switch_time >= self.time_quantum:
            try:
                current_index = running_vms.index(current_vm)
                next_index = (current_index + 1) % len(running_vms)
                self.last_switch_time = time.time()
                return running_vms[next_index]
            except ValueError:
                return running_vms[0]
                
        return current_vm
