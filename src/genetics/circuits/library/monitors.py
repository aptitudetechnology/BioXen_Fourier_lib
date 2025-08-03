"""
Monitoring circuit implementations for resource tracking.

This module contains genetic circuits for monitoring cellular resources
like ATP levels, ribosome usage, and metabolic activity.
"""

from ..core.elements import GeneticCircuit, GeneticElement, CircuitType, ElementType


def get_atp_monitor_circuit() -> GeneticCircuit:
    """Get the ATP monitoring circuit"""
    return GeneticCircuit(
        circuit_id="atp_monitor",
        circuit_type=CircuitType.RESOURCE_MONITOR,
        elements=[
            GeneticElement(
                name="atp_sensor_promoter",
                sequence="TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGAGC",
                element_type=ElementType.PROMOTER,
                regulation_target="atp_reporter"
            ),
            GeneticElement(
                name="atp_reporter",
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
                name="ribosome_sensor_promoter",
                sequence="TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGACC",
                element_type=ElementType.PROMOTER,
                regulation_target="ribosome_reporter"
            ),
            GeneticElement(
                name="ribosome_reporter",
                sequence="ATGAAAGCAATTTTCGTACTGAAAGGTTGGTGGCGCACTTCCTGCC",
                element_type=ElementType.GENE
            ),
            GeneticElement(
                name="ribosome_sensor_rna",
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
                name="metabolic_sensor_promoter",
                sequence="TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGGCC",
                element_type=ElementType.PROMOTER,
                regulation_target="metabolic_reporter"
            ),
            GeneticElement(
                name="metabolic_reporter",
                sequence="ATGAAAGCAATTTTCGTACTGAAAGGTTGGTGGCGCACTTCCTGGG",
                element_type=ElementType.GENE
            ),
            GeneticElement(
                name="metabolic_terminator",
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
                name="stress_sensor_promoter",
                sequence="TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGAAA",
                element_type=ElementType.PROMOTER,
                regulation_target="stress_reporter"
            ),
            GeneticElement(
                name="stress_response_gene",
                sequence="ATGAAAGCAATTTTCGTACTGAAAGGTTGGTGGCGCACTTCCTGTT",
                element_type=ElementType.GENE
            ),
            GeneticElement(
                name="stress_reporter",
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
