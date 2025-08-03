"""
Monitoring circuit implementations for resource tracking.

This module contains genetic circuits for monitoring cellular resources
like ATP levels, ribosome usage, and metabolic activity.
"""

from ..core.elements import GeneticCircuit, GeneticElement, CircuitType, ElementType


# Factory functions for creating monitoring circuits
def create_atp_monitor(vm_id: str) -> GeneticCircuit:
    """Create ATP monitoring circuit for a specific VM"""
    return GeneticCircuit(
        circuit_id=f"{vm_id}_atp_monitor",
        circuit_type=CircuitType.RESOURCE_MONITOR,
        elements=[
            GeneticElement(
                element_id=f"{vm_id}_atp_promoter",
                sequence="TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGAGC",
                element_type=ElementType.PROMOTER,
                vm_specific=True,
                regulation_target=f"{vm_id}_atp_reporter"
            ),
            GeneticElement(
                element_id=f"{vm_id}_rbs",
                sequence="AAGGAGGTGATCCATG",
                element_type=ElementType.RBS,
                vm_specific=True
            ),
            GeneticElement(
                element_id=f"{vm_id}_atp_reporter",
                sequence="ATGAAAGCAATTTTCGTACTGAAAGGTTGGTGGCGCACTTCCTGAA",
                element_type=ElementType.GENE,
                vm_specific=True
            ),
            GeneticElement(
                element_id=f"{vm_id}_terminator",
                sequence="GCCTCTTCGCTATTACGCCAGCTGGCGAAAGGGGGATGTGCTGCAAGGCG",
                element_type=ElementType.TERMINATOR,
                vm_specific=True
            )
        ],
        description=f"ATP monitoring circuit for VM {vm_id}"
    )


def create_ph_monitor(vm_id: str) -> GeneticCircuit:
    """Create pH monitoring circuit for a specific VM"""
    return GeneticCircuit(
        circuit_id=f"{vm_id}_ph_monitor",
        circuit_type=CircuitType.RESOURCE_MONITOR,
        elements=[
            GeneticElement(
                element_id=f"{vm_id}_ph_promoter",
                sequence="TTGACAGCTAGCTCAGTCCTAGGTATAATGCTAGCAACCTGGATC",
                element_type=ElementType.PROMOTER,
                vm_specific=True,
                regulation_target=f"{vm_id}_ph_reporter"
            ),
            GeneticElement(
                element_id=f"{vm_id}_ph_rbs",
                sequence="AAGGAGGTGATCCATG",
                element_type=ElementType.RBS,
                vm_specific=True
            ),
            GeneticElement(
                element_id=f"{vm_id}_ph_reporter",
                sequence="ATGAAAGCAATTTTCGTACTGAAAGGTTGGTGGCGCACTTCCTGCC",
                element_type=ElementType.GENE,
                vm_specific=True
            ),
            GeneticElement(
                element_id=f"{vm_id}_ph_terminator",
                sequence="GCCTCTTCGCTATTACGCCAGCTGGCGAAAGGGGGATGTGCTGCAAGGCG",
                element_type=ElementType.TERMINATOR,
                vm_specific=True
            )
        ],
        description=f"pH monitoring circuit for VM {vm_id}"
    )


def create_temperature_monitor(vm_id: str) -> GeneticCircuit:
    """Create temperature monitoring circuit for a specific VM"""
    return GeneticCircuit(
        circuit_id=f"{vm_id}_temp_monitor",
        circuit_type=CircuitType.RESOURCE_MONITOR,
        elements=[
            GeneticElement(
                element_id=f"{vm_id}_temp_promoter",
                sequence="TTGACAGCTAGCTCAGTCCTAGGTATAATGCTAGCAACCTGGAAT",
                element_type=ElementType.PROMOTER,
                vm_specific=True,
                regulation_target=f"{vm_id}_temp_reporter"
            ),
            GeneticElement(
                element_id=f"{vm_id}_temp_rbs",
                sequence="AAGGAGGTGATCCATG",
                element_type=ElementType.RBS,
                vm_specific=True
            ),
            GeneticElement(
                element_id=f"{vm_id}_temp_reporter",
                sequence="ATGAAAGCAATTTTCGTACTGAAAGGTTGGTGGCGCACTTCCTGGG",
                element_type=ElementType.GENE,
                vm_specific=True
            ),
            GeneticElement(
                element_id=f"{vm_id}_temp_terminator",
                sequence="GCCTCTTCGCTATTACGCCAGCTGGCGAAAGGGGGATGTGCTGCAAGGCG",
                element_type=ElementType.TERMINATOR,
                vm_specific=True
            )
        ],
        description=f"Temperature monitoring circuit for VM {vm_id}"
    )


def create_resource_monitor(vm_id: str, resources: list) -> GeneticCircuit:
    """Create general resource monitoring circuit for specified resources"""
    elements = []
    
    # Add promoter
    elements.append(GeneticElement(
        element_id=f"{vm_id}_resource_promoter",
        sequence="TTGACAGCTAGCTCAGTCCTAGGTATAATGCTAGC",
        element_type=ElementType.PROMOTER,
        vm_specific=True,
        regulation_target=f"{vm_id}_resource_monitor"
    ))
    
    # Add RBS
    elements.append(GeneticElement(
        element_id=f"{vm_id}_resource_rbs", 
        sequence="AAGGAGGTGATCCATG",
        element_type=ElementType.RBS,
        vm_specific=True
    ))
    
    # Add monitoring genes for each resource
    base_sequence = "ATGAAAGCAATTTTCGTACTGAAAGGTTGGTGGCGCACTTCCTG"
    for i, resource in enumerate(resources):
        # Vary sequence slightly for each resource
        sequence = base_sequence + ("AA" if i % 2 == 0 else "GG")
        
        elements.append(GeneticElement(
            element_id=f"{vm_id}_{resource}_monitor",
            sequence=sequence,
            element_type=ElementType.GENE,
            vm_specific=True
        ))
    
    # Add terminator
    elements.append(GeneticElement(
        element_id=f"{vm_id}_resource_terminator",
        sequence="GCCTCTTCGCTATTACGCCAGCTGGCGAAAGGGGGATGTGCTGCAAGGCG",
        element_type=ElementType.TERMINATOR,
        vm_specific=True
    ))
    
    return GeneticCircuit(
        circuit_id=f"{vm_id}_resource_monitor",
        circuit_type=CircuitType.RESOURCE_MONITOR,
        elements=elements,
        description=f"Multi-resource monitoring circuit for VM {vm_id}: {', '.join(resources)}"
    )


# Legacy functions (keeping for backward compatibility)
def get_atp_monitor_circuit() -> GeneticCircuit:
    """Get the ATP monitoring circuit"""
    return GeneticCircuit(
        circuit_id="atp_monitor",
        circuit_type=CircuitType.RESOURCE_MONITOR,
        elements=[
            GeneticElement(
                element_id="atp_sensor_promoter",
                sequence="TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGAGC",
                element_type=ElementType.PROMOTER,
                regulation_target="atp_reporter"
            ),
            GeneticElement(
                element_id="atp_reporter",
                sequence="ATGAAAGCAATTTTCGTACTGAAAGGTTGGTGGCGCACTTCCTGAA",
                element_type=ElementType.GENE,
                regulation_target=None
            )
        ],
        description="ATP-sensitive promoter driving fluorescent reporter"
    )


def get_ribosome_monitor_circuit() -> GeneticCircuit:
    """Get the ribosome usage monitoring circuit"""
    return GeneticCircuit(
        circuit_id="ribosome_monitor",
        circuit_type=CircuitType.RESOURCE_MONITOR,
        elements=[
            GeneticElement(
                element_id="ribosome_sensor_promoter",
                sequence="TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGACC",
                element_type=ElementType.PROMOTER,
                regulation_target="ribosome_reporter"
            ),
            GeneticElement(
                element_id="ribosome_reporter",
                sequence="ATGAAAGCAATTTTCGTACTGAAAGGTTGGTGGCGCACTTCCTGCC",
                element_type=ElementType.GENE
            ),
            GeneticElement(
                element_id="ribosome_sensor_rna",
                sequence="GCAAGCUGGUCGGCAUCGGCAUC",
                element_type=ElementType.SRNA,
                regulation_target="ribosome_reporter"
            )
        ],
        description="Ribosome occupancy sensor with regulatory RNA"
    )


def get_metabolic_monitor_circuit() -> GeneticCircuit:
    """Get the metabolic activity monitoring circuit"""
    return GeneticCircuit(
        circuit_id="metabolic_monitor", 
        circuit_type=CircuitType.RESOURCE_MONITOR,
        elements=[
            GeneticElement(
                element_id="metabolic_sensor_promoter",
                sequence="TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGGCC",
                element_type=ElementType.PROMOTER,
                regulation_target="metabolic_reporter"
            ),
            GeneticElement(
                element_id="metabolic_reporter",
                sequence="ATGAAAGCAATTTTCGTACTGAAAGGTTGGTGGCGCACTTCCTGGG",
                element_type=ElementType.GENE
            ),
            GeneticElement(
                element_id="metabolic_terminator",
                sequence="AAAAAAGCCCGCTCACGGCCCCTTTTTCTATATAGT",
                element_type=ElementType.TERMINATOR
            )
        ],
        description="Metabolic activity sensor with transcriptional terminator"
    )


def get_resource_stress_circuit() -> GeneticCircuit:
    """Get the resource stress detection circuit"""
    return GeneticCircuit(
        circuit_id="resource_stress",
        circuit_type=CircuitType.RESOURCE_MONITOR,
        elements=[
            GeneticElement(
                element_id="stress_sensor_promoter",
                sequence="TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGAAA",
                element_type=ElementType.PROMOTER,
                regulation_target="stress_reporter"
            ),
            GeneticElement(
                element_id="stress_response_gene",
                sequence="ATGAAAGCAATTTTCGTACTGAAAGGTTGGTGGCGCACTTCCTGTT",
                element_type=ElementType.GENE
            ),
            GeneticElement(
                element_id="stress_reporter",
                sequence="ATGGTGAGCAAGGGCGAGGAGCTGTTCACCGGGGTGGTGCCCATC",
                element_type=ElementType.GENE
            )
        ],
        description="Resource stress detection and response circuit"
    )


def create_custom_monitor(monitor_name: str, target_molecule: str, 
                         promoter_seq: str, reporter_seq: str) -> GeneticCircuit:
    """Create a custom monitoring circuit for a specific molecule"""
    return GeneticCircuit(
        circuit_id=f"{monitor_name}_monitor",
        circuit_type=CircuitType.RESOURCE_MONITOR,
        elements=[
            GeneticElement(
                name=f"{monitor_name}_promoter",
                sequence=promoter_seq,
                element_type=ElementType.PROMOTER,
                regulation_target=f"{monitor_name}_reporter"
            ),
            GeneticElement(
                name=f"{monitor_name}_reporter",
                sequence=reporter_seq,
                element_type=ElementType.GENE
            )
        ],
        description=f"Custom monitoring circuit for {target_molecule}"
    )


# Circuit library for easy access
MONITOR_CIRCUITS = {
    "atp_monitor": get_atp_monitor_circuit,
    "ribosome_monitor": get_ribosome_monitor_circuit, 
    "metabolic_monitor": get_metabolic_monitor_circuit,
    "resource_stress": get_resource_stress_circuit,
}
