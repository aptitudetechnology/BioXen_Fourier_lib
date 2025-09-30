"""
Circuit library module for BioXen genetic circuits.

This package contains specialized circuit implementations organized by function:
- monitors: Resource monitoring circuits
- schedulers: Resource scheduling circuits  
- isolation: VM isolation circuits
- memory: Memory management circuits
"""

from .monitors import (
    get_atp_monitor_circuit,
    get_ribosome_monitor_circuit,
    get_metabolic_monitor_circuit,
    get_resource_stress_circuit,
    create_custom_monitor,
    MONITOR_CIRCUITS
)

from .schedulers import (
    get_ribosome_scheduler_circuit,
    get_metabolic_scheduler_circuit,
    get_time_division_circuit,
    get_priority_scheduler_circuit,
    get_load_balancer_circuit,
    create_custom_scheduler,
    SCHEDULER_CIRCUITS
)

from .isolation import (
    get_memory_isolation_circuit,
    get_namespace_isolation_circuit,
    get_membrane_isolation_circuit,
    get_transcriptional_isolation_circuit,
    get_protein_isolation_circuit,
    create_vm_isolation_circuit,
    ISOLATION_CIRCUITS
)

from .memory import (
    get_protein_degradation_circuit,
    get_rna_cleanup_circuit,
    get_metabolite_recycling_circuit,
    get_garbage_collection_circuit,
    get_memory_compaction_circuit,
    get_memory_allocation_circuit,
    create_vm_memory_manager,
    MEMORY_CIRCUITS
)

__all__ = [
    # Monitor circuits
    "get_atp_monitor_circuit",
    "get_ribosome_monitor_circuit", 
    "get_metabolic_monitor_circuit",
    "get_resource_stress_circuit",
    "create_custom_monitor",
    "MONITOR_CIRCUITS",
    
    # Scheduler circuits
    "get_ribosome_scheduler_circuit",
    "get_metabolic_scheduler_circuit",
    "get_time_division_circuit",
    "get_priority_scheduler_circuit",
    "get_load_balancer_circuit",
    "create_custom_scheduler",
    "SCHEDULER_CIRCUITS",
    
    # Isolation circuits
    "get_memory_isolation_circuit",
    "get_namespace_isolation_circuit",
    "get_membrane_isolation_circuit",
    "get_transcriptional_isolation_circuit", 
    "get_protein_isolation_circuit",
    "create_vm_isolation_circuit",
    "ISOLATION_CIRCUITS",
    
    # Memory management circuits
    "get_protein_degradation_circuit",
    "get_rna_cleanup_circuit",
    "get_metabolite_recycling_circuit",
    "get_garbage_collection_circuit",
    "get_memory_compaction_circuit",
    "get_memory_allocation_circuit",
    "create_vm_memory_manager",
    "MEMORY_CIRCUITS",
]

# Combined circuit registry for easy access
ALL_CIRCUITS = {
    **MONITOR_CIRCUITS,
    **SCHEDULER_CIRCUITS,
    **ISOLATION_CIRCUITS,
    **MEMORY_CIRCUITS,
}
