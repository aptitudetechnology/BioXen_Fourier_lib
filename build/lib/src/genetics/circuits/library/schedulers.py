"""
Scheduling circuit implementations for resource allocation.

This module contains genetic circuits for scheduling and time-slicing
biological resources like ribosomes and metabolic pathways.
"""

from ..core.elements import GeneticCircuit, GeneticElement, CircuitType, ElementType


# Factory functions for creating scheduling circuits
def create_round_robin_scheduler(vm_list: list) -> GeneticCircuit:
    """Create round-robin scheduler circuit for VMs"""
    elements = []
    
    # Add master scheduler promoter
    elements.append(GeneticElement(
        element_id="rr_scheduler_promoter",
        sequence="TTGACAGCTAGCTCAGTCCTAGGTATAATGCTAGC",
        element_type=ElementType.PROMOTER,
        regulation_target="scheduler_controller"
    ))
    
    # Add scheduler controller gene
    elements.append(GeneticElement(
        element_id="scheduler_controller",
        sequence="ATGAAAGCAATTTTCGTACTGAAAGGTTGGTGGCGCACTTCCTGAA",
        element_type=ElementType.GENE
    ))
    
    # Add RBS for each VM with equal strength
    rbs_sequence = "AGGAGAAACATG"  # Medium strength for fair allocation
    for vm_id in vm_list:
        elements.append(GeneticElement(
            element_id=f"{vm_id}_rbs",
            sequence=rbs_sequence,
            element_type=ElementType.RBS,
            vm_specific=True
        ))
    
    # Add scheduler RNA
    elements.append(GeneticElement(
        element_id="rr_scheduler_rna",
        sequence="GCAAGCUGGUCGGCAUC",
        element_type=ElementType.SRNA,
        regulation_target="vm_genes"
    ))
    
    # Add terminator
    elements.append(GeneticElement(
        element_id="rr_scheduler_terminator",
        sequence="GCCTCTTCGCTATTACGCCAGCTGGCGAAAGGGGGATGTGCTGCAAGGCG",
        element_type=ElementType.TERMINATOR
    ))
    
    return GeneticCircuit(
        circuit_id="round_robin_scheduler",
        circuit_type=CircuitType.SCHEDULER,
        elements=elements,
        description=f"Round-robin scheduler for VMs: {', '.join(vm_list)}"
    )


def create_priority_scheduler(vm_priorities: dict) -> GeneticCircuit:
    """Create priority-based scheduler circuit"""
    elements = []
    
    # Add scheduler promoter
    elements.append(GeneticElement(
        element_id="priority_scheduler_promoter",
        sequence="TTGACAGCTAGCTCAGTCCTAGGTATAATGCTAGC",
        element_type=ElementType.PROMOTER,
        regulation_target="priority_controller"
    ))
    
    # Add priority controller
    elements.append(GeneticElement(
        element_id="priority_controller",
        sequence="ATGAAAGCAATTTTCGTACTGAAAGGTTGGTGGCGCACTTCCTGCC",
        element_type=ElementType.GENE
    ))
    
    # Define RBS strengths based on priority
    rbs_strengths = {
        1: "AGGAGGACAACATG",    # Strong (high priority)
        2: "AGGAGAAACATG",      # Medium
        3: "AGGACATG"           # Weak (low priority)
    }
    
    # Add RBS for each VM based on priority
    for vm_id, priority in vm_priorities.items():
        rbs_seq = rbs_strengths.get(priority, rbs_strengths[2])  # Default to medium
        
        elements.append(GeneticElement(
            element_id=f"{vm_id}_priority_rbs",
            sequence=rbs_seq,
            element_type=ElementType.RBS,
            vm_specific=True
        ))
    
    # Add priority scheduler RNA
    elements.append(GeneticElement(
        element_id="priority_scheduler_rna",
        sequence="GCAAGCUGGUCGGCAUCAAG",
        element_type=ElementType.SRNA,
        regulation_target="vm_genes"
    ))
    
    # Add terminator
    elements.append(GeneticElement(
        element_id="priority_scheduler_terminator",
        sequence="GCCTCTTCGCTATTACGCCAGCTGGCGAAAGGGGGATGTGCTGCAAGGCG",
        element_type=ElementType.TERMINATOR
    ))
    
    return GeneticCircuit(
        circuit_id="priority_scheduler",
        circuit_type=CircuitType.SCHEDULER,
        elements=elements,
        description=f"Priority scheduler for VMs with priorities: {vm_priorities}"
    )


def create_resource_aware_scheduler(vm_list: list, resource_limits: dict = None) -> GeneticCircuit:
    """Create resource-aware scheduler circuit"""
    elements = []
    
    # Add resource-aware promoter
    elements.append(GeneticElement(
        element_id="resource_scheduler_promoter",
        sequence="TTGACAGCTAGCTCAGTCCTAGGTATAATGCTAGCAACCTG",
        element_type=ElementType.PROMOTER,
        regulation_target="resource_controller"
    ))
    
    # Add resource monitoring controller
    elements.append(GeneticElement(
        element_id="resource_controller",
        sequence="ATGAAAGCAATTTTCGTACTGAAAGGTTGGTGGCGCACTTCCTGGG",
        element_type=ElementType.GENE
    ))
    
    # Add adaptive RBS for each VM
    for vm_id in vm_list:
        # Resource-aware RBS that can be modulated
        elements.append(GeneticElement(
            element_id=f"{vm_id}_adaptive_rbs",
            sequence="AGGAGAAACATGCC",  # Slightly modified for resource responsiveness
            element_type=ElementType.RBS,
            vm_specific=True
        ))
    
    # Add resource monitoring genes
    if resource_limits:
        for resource, limit in resource_limits.items():
            elements.append(GeneticElement(
                element_id=f"{resource}_monitor",
                sequence="ATGAAAGCAATTTTCGTACTGAAAGGTTGGTGGCGCACTTCCTGAG",
                element_type=ElementType.GENE
            ))
    
    # Add adaptive scheduler RNA
    elements.append(GeneticElement(
        element_id="adaptive_scheduler_rna",
        sequence="GCAAGCUGGUCGGCAUCAAGCCU",
        element_type=ElementType.SRNA,
        regulation_target="vm_genes"
    ))
    
    # Add terminator
    elements.append(GeneticElement(
        element_id="resource_scheduler_terminator",
        sequence="GCCTCTTCGCTATTACGCCAGCTGGCGAAAGGGGGATGTGCTGCAAGGCG",
        element_type=ElementType.TERMINATOR
    ))
    
    return GeneticCircuit(
        circuit_id="resource_aware_scheduler",
        circuit_type=CircuitType.SCHEDULER,
        elements=elements,
        description=f"Resource-aware scheduler for VMs: {', '.join(vm_list)}"
    )


# Legacy functions (keeping for backward compatibility)
def get_ribosome_scheduler_circuit() -> GeneticCircuit:
    """Get the ribosome scheduling circuit"""
    return GeneticCircuit(
        circuit_id="ribosome_scheduler",
        circuit_type=CircuitType.SCHEDULER,
        elements=[
            GeneticElement(
                element_id="vm1_rbs",
                sequence="AGGAGGACAACATG",  # Strong RBS
                element_type=ElementType.RBS,
                vm_specific=True
            ),
            GeneticElement(
                element_id="vm2_rbs", 
                sequence="AGGAGAAACATG",    # Medium RBS
                element_type=ElementType.RBS,
                vm_specific=True
            ),
            GeneticElement(
                element_id="vm3_rbs",
                sequence="AGGACATG",        # Weak RBS
                element_type=ElementType.RBS, 
                vm_specific=True
            ),
            GeneticElement(
                element_id="scheduler_sRNA",
                sequence="GCAAGCUGGUCGGCAUC",  # Small regulatory RNA
                element_type=ElementType.SRNA,
                regulation_target="vm_rbs"
            )
        ],
        description="Time-sliced ribosome allocation using RBS variants"
    )


def get_metabolic_scheduler_circuit() -> GeneticCircuit:
    """Get the metabolic pathway scheduling circuit"""
    return GeneticCircuit(
        circuit_id="metabolic_scheduler",
        circuit_type=CircuitType.SCHEDULER,
        elements=[
            GeneticElement(
                element_id="glycolysis_promoter",
                sequence="TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGAGC",
                element_type=ElementType.PROMOTER,
                regulation_target="glycolysis_genes"
            ),
            GeneticElement(
                element_id="tca_promoter",
                sequence="TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGACC",
                element_type=ElementType.PROMOTER,
                regulation_target="tca_genes"
            ),
            GeneticElement(
                element_id="metabolic_switch_rna",
                sequence="GCAAGCUGGUCGGCAUCGGAUCCGCAUC",
                element_type=ElementType.SRNA,
                regulation_target="metabolic_promoters"
            )
        ],
        description="Scheduling circuit for metabolic pathway switching"
    )


def get_time_division_circuit(time_slots: int = 3) -> GeneticCircuit:
    """Get a time-division multiplexing circuit for VM scheduling"""
    elements = []
    
    # Create time-slot specific elements
    for i in range(time_slots):
        slot_id = f"slot{i+1}"
        
        # Add RBS for this time slot
        rbs_strength = ["AGGAGGACAACATG", "AGGAGAAACATG", "AGGACATG", "AGGAATG"][i % 4]
        elements.append(
            GeneticElement(
                name=f"{slot_id}_rbs",
                sequence=rbs_strength,
                element_type=ElementType.RBS,
                vm_specific=True
            )
        )
        
        # Add promoter for this time slot
        promoter_seq = f"TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTG{chr(65+i)}GC"
        elements.append(
            GeneticElement(
                name=f"{slot_id}_promoter",
                sequence=promoter_seq,
                element_type=ElementType.PROMOTER,
                vm_specific=True,
                regulation_target=f"{slot_id}_genes"
            )
        )
    
    # Add master timing RNA
    elements.append(
        GeneticElement(
            element_id="timing_master_rna",
            sequence="GCAAGCUGGUCGGCAUCGGCAUCGCAUCGGAUC",
            element_type=ElementType.SRNA,
            regulation_target="time_slots"
        )
    )
    
    return GeneticCircuit(
        circuit_id=f"time_division_{time_slots}",
        circuit_type=CircuitType.SCHEDULER,
        elements=elements,
        description=f"Time-division multiplexing for {time_slots} VM slots"
    )


def get_priority_scheduler_circuit() -> GeneticCircuit:
    """Get a priority-based scheduling circuit"""
    return GeneticCircuit(
        circuit_id="priority_scheduler",
        circuit_type=CircuitType.SCHEDULER,
        elements=[
            # High priority VM (strongest RBS)
            GeneticElement(
                element_id="high_priority_rbs",
                sequence="AGGAGGACAACATG",
                element_type=ElementType.RBS,
                vm_specific=True
            ),
            GeneticElement(
                element_id="high_priority_promoter",
                sequence="TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGAGC",
                element_type=ElementType.PROMOTER,
                vm_specific=True,
                regulation_target="high_priority_genes"
            ),
            
            # Medium priority VM
            GeneticElement(
                element_id="medium_priority_rbs",
                sequence="AGGAGAAACATG",
                element_type=ElementType.RBS,
                vm_specific=True
            ),
            GeneticElement(
                element_id="medium_priority_promoter",
                sequence="TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGACC",
                element_type=ElementType.PROMOTER,
                vm_specific=True,
                regulation_target="medium_priority_genes"
            ),
            
            # Low priority VM (weakest RBS)
            GeneticElement(
                element_id="low_priority_rbs",
                sequence="AGGACATG",
                element_type=ElementType.RBS,
                vm_specific=True
            ),
            GeneticElement(
                element_id="low_priority_promoter",
                sequence="TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGGCC",
                element_type=ElementType.PROMOTER,
                vm_specific=True,
                regulation_target="low_priority_genes"
            ),
            
            # Priority control RNA
            GeneticElement(
                element_id="priority_control_rna",
                sequence="GCAAGCUGGUCGGCAUCGGCAUCGCAUC",
                element_type=ElementType.SRNA,
                regulation_target="priority_system"
            )
        ],
        description="Priority-based scheduling with high/medium/low priority VMs"
    )


def get_load_balancer_circuit() -> GeneticCircuit:
    """Get a load balancing circuit for resource distribution"""
    return GeneticCircuit(
        circuit_id="load_balancer",
        circuit_type=CircuitType.SCHEDULER,
        elements=[
            # Load sensing elements
            GeneticElement(
                element_id="load_sensor_promoter",
                sequence="TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGAAA",
                element_type=ElementType.PROMOTER,
                regulation_target="load_reporter"
            ),
            GeneticElement(
                element_id="load_reporter",
                sequence="ATGAAAGCAATTTTCGTACTGAAAGGTTGGTGGCGCACTTCCTGAA",
                element_type=ElementType.GENE
            ),
            
            # Balancing regulatory RNAs
            GeneticElement(
                element_id="balance_rna_1",
                sequence="GCAAGCUGGUCGGCAUC",
                element_type=ElementType.SRNA,
                regulation_target="vm1_resources"
            ),
            GeneticElement(
                element_id="balance_rna_2",
                sequence="GCAAGCUGGUCGGCGCC",
                element_type=ElementType.SRNA,
                regulation_target="vm2_resources"
            ),
            GeneticElement(
                element_id="balance_rna_3",
                sequence="GCAAGCUGGUCGGCTCC",
                element_type=ElementType.SRNA,
                regulation_target="vm3_resources"
            )
        ],
        description="Load balancing circuit for dynamic resource distribution"
    )


def create_custom_scheduler(scheduler_name: str, vm_count: int, 
                          scheduling_strategy: str = "round_robin") -> GeneticCircuit:
    """Create a custom scheduling circuit"""
    elements = []
    
    # RBS strengths for different strategies
    rbs_variants = {
        "round_robin": ["AGGAGGACAACATG", "AGGAGAAACATG", "AGGACATG"] * ((vm_count // 3) + 1),
        "priority": ["AGGAGGACAACATG"] + ["AGGAGAAACATG"] * (vm_count - 2) + ["AGGACATG"],
        "fair": ["AGGAGAAACATG"] * vm_count
    }
    
    rbs_list = rbs_variants.get(scheduling_strategy, rbs_variants["round_robin"])
    
    for i in range(vm_count):
        vm_id = f"vm{i+1}"
        
        elements.append(
            GeneticElement(
                name=f"{vm_id}_rbs",
                sequence=rbs_list[i % len(rbs_list)],
                element_type=ElementType.RBS,
                vm_specific=True
            )
        )
    
    # Add scheduler control RNA
    elements.append(
        GeneticElement(
            name=f"{scheduler_name}_control_rna",
            sequence="GCAAGCUGGUCGGCAUCGGCAUC",
            element_type=ElementType.SRNA,
            regulation_target="scheduler_system"
        )
    )
    
    return GeneticCircuit(
        circuit_id=f"{scheduler_name}_scheduler",
        circuit_type=CircuitType.SCHEDULER,
        elements=elements,
        description=f"Custom {scheduling_strategy} scheduler for {vm_count} VMs"
    )


# Circuit library for easy access
SCHEDULER_CIRCUITS = {
    "ribosome_scheduler": get_ribosome_scheduler_circuit,
    "metabolic_scheduler": get_metabolic_scheduler_circuit,
    "priority_scheduler": get_priority_scheduler_circuit,
    "load_balancer": get_load_balancer_circuit,
}
