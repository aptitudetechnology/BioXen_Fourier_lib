"""
Scheduling circuit implementations for resource allocation.

This module contains genetic circuits for scheduling and time-slicing
biological resources like ribosomes and metabolic pathways.
"""

from ..core.elements import GeneticCircuit, GeneticElement, CircuitType, ElementType


def get_ribosome_scheduler_circuit() -> GeneticCircuit:
    """Get the ribosome scheduling circuit"""
    return GeneticCircuit(
        circuit_id="ribosome_scheduler",
        circuit_type=CircuitType.SCHEDULER,
        elements=[
            GeneticElement(
                name="vm1_rbs",
                sequence="AGGAGGACAACATG",  # Strong RBS
                element_type=ElementType.RBS,
                vm_specific=True
            ),
            GeneticElement(
                name="vm2_rbs", 
                sequence="AGGAGAAACATG",    # Medium RBS
                element_type=ElementType.RBS,
                vm_specific=True
            ),
            GeneticElement(
                name="vm3_rbs",
                sequence="AGGACATG",        # Weak RBS
                element_type=ElementType.RBS, 
                vm_specific=True
            ),
            GeneticElement(
                name="scheduler_sRNA",
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
                name="glycolysis_promoter",
                sequence="TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGAGC",
                element_type=ElementType.PROMOTER,
                regulation_target="glycolysis_genes"
            ),
            GeneticElement(
                name="tca_promoter",
                sequence="TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGACC",
                element_type=ElementType.PROMOTER,
                regulation_target="tca_genes"
            ),
            GeneticElement(
                name="metabolic_switch_rna",
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
            name="timing_master_rna",
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
                name="high_priority_rbs",
                sequence="AGGAGGACAACATG",
                element_type=ElementType.RBS,
                vm_specific=True
            ),
            GeneticElement(
                name="high_priority_promoter",
                sequence="TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGAGC",
                element_type=ElementType.PROMOTER,
                vm_specific=True,
                regulation_target="high_priority_genes"
            ),
            
            # Medium priority VM
            GeneticElement(
                name="medium_priority_rbs",
                sequence="AGGAGAAACATG",
                element_type=ElementType.RBS,
                vm_specific=True
            ),
            GeneticElement(
                name="medium_priority_promoter",
                sequence="TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGACC",
                element_type=ElementType.PROMOTER,
                vm_specific=True,
                regulation_target="medium_priority_genes"
            ),
            
            # Low priority VM (weakest RBS)
            GeneticElement(
                name="low_priority_rbs",
                sequence="AGGACATG",
                element_type=ElementType.RBS,
                vm_specific=True
            ),
            GeneticElement(
                name="low_priority_promoter",
                sequence="TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGGCC",
                element_type=ElementType.PROMOTER,
                vm_specific=True,
                regulation_target="low_priority_genes"
            ),
            
            # Priority control RNA
            GeneticElement(
                name="priority_control_rna",
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
                name="load_sensor_promoter",
                sequence="TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGAAA",
                element_type=ElementType.PROMOTER,
                regulation_target="load_reporter"
            ),
            GeneticElement(
                name="load_reporter",
                sequence="ATGAAAGCAATTTTCGTACTGAAAGGTTGGTGGCGCACTTCCTGAA",
                element_type=ElementType.GENE
            ),
            
            # Balancing regulatory RNAs
            GeneticElement(
                name="balance_rna_1",
                sequence="GCAAGCUGGUCGGCAUC",
                element_type=ElementType.SRNA,
                regulation_target="vm1_resources"
            ),
            GeneticElement(
                name="balance_rna_2",
                sequence="GCAAGCUGGUCGGCGCC",
                element_type=ElementType.SRNA,
                regulation_target="vm2_resources"
            ),
            GeneticElement(
                name="balance_rna_3",
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
