"""
Isolation circuit implementations for VM separation.

This module contains genetic circuits for maintaining isolation between
virtual machines using orthogonal genetic systems.
"""

from ..core.elements import GeneticCircuit, GeneticElement, CircuitType, ElementType


def get_memory_isolation_circuit() -> GeneticCircuit:
    """Get the memory isolation circuit"""
    return GeneticCircuit(
        circuit_id="memory_isolation",
        circuit_type=CircuitType.ISOLATION,
        elements=[
            GeneticElement(
                element_id="vm1_rnap",
                sequence="ATGCGTCGTCTGACCCTGAAACAGGCAATCACC",  # RNA polymerase variant 1
                element_type=ElementType.GENE,
                vm_specific=True
            ),
            GeneticElement(
                element_id="vm2_rnap",
                sequence="ATGCGTCGTCTGACCCTGAAGCAGGCAATCACC",  # RNA polymerase variant 2  
                element_type=ElementType.GENE,
                vm_specific=True
            ),
            GeneticElement(
                element_id="vm1_promoter",
                sequence="TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGAGC",
                element_type=ElementType.PROMOTER,
                vm_specific=True,
                regulation_target="vm1_genes"
            ),
            GeneticElement(
                element_id="vm2_promoter", 
                sequence="TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGACC",
                element_type=ElementType.PROMOTER,
                vm_specific=True,
                regulation_target="vm2_genes"
            )
        ],
        description="VM-specific RNA polymerases and promoters for memory isolation"
    )


def get_namespace_isolation_circuit() -> GeneticCircuit:
    """Get the namespace isolation circuit using orthogonal genetic codes"""
    return GeneticCircuit(
        circuit_id="namespace_isolation",
        circuit_type=CircuitType.ISOLATION,
        elements=[
            # Orthogonal tRNA/synthetase pairs
            GeneticElement(
                element_id="orthogonal_trna_1",
                sequence="GGGGCCCGCCAGATGATGGATGTTAGGTGGCCTTCTAAACCCCACC",
                element_type=ElementType.GENE,
                vm_specific=True
            ),
            GeneticElement(
                element_id="orthogonal_synthetase_1",
                sequence="ATGGTGACCCTGAAACAGGCAATCACCAAGATCATC",
                element_type=ElementType.GENE,
                vm_specific=True
            ),
            GeneticElement(
                element_id="orthogonal_trna_2",
                sequence="GGGGCCCGCCAGATGATGGATGTTAGGTGGCCTTCTAAACCGCACC",
                element_type=ElementType.GENE,
                vm_specific=True
            ),
            GeneticElement(
                element_id="orthogonal_synthetase_2",
                sequence="ATGGTGACCCTGAAACAGGCAATCACCAAGATCGTC",
                element_type=ElementType.GENE,
                vm_specific=True
            ),
            # Stop codon suppression elements
            GeneticElement(
                element_id="amber_suppressor_trna",
                sequence="GGGCCCGCCAGATGATGGATGTTAGGTGGCCTTCTAAACCGCACC",
                element_type=ElementType.GENE,
                vm_specific=True
            )
        ],
        description="Orthogonal genetic code elements for namespace isolation"
    )


def get_membrane_isolation_circuit() -> GeneticCircuit:
    """Get the membrane-based isolation circuit"""
    return GeneticCircuit(
        circuit_id="membrane_isolation",
        circuit_type=CircuitType.ISOLATION,
        elements=[
            # Membrane protein targeting sequences
            GeneticElement(
                element_id="vm1_membrane_target",
                sequence="ATGAAACGCATCGGCTACGTGCAGGCAATCACCAAGATCATCACC",
                element_type=ElementType.GENE,
                vm_specific=True
            ),
            GeneticElement(
                element_id="vm2_membrane_target",
                sequence="ATGAAACGCATCGGCTACGTGCAGGCAATCGCCAAGATCGTCACC",
                element_type=ElementType.GENE,
                vm_specific=True
            ),
            # Membrane channel proteins
            GeneticElement(
                element_id="vm1_channel",
                sequence="ATGCTGACCCTGAAACAGGCAATCACCAAGATCATCACCGGCTACGTG",
                element_type=ElementType.GENE,
                vm_specific=True
            ),
            GeneticElement(
                element_id="vm2_channel",
                sequence="ATGCTGACCCTGAAACAGGCAATCGCCAAGATCGTCACCGGCTACGTG",
                element_type=ElementType.GENE,
                vm_specific=True
            ),
            # Compartment-specific promoters
            GeneticElement(
                element_id="compartment1_promoter",
                sequence="TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGAGC",
                element_type=ElementType.PROMOTER,
                vm_specific=True,
                regulation_target="vm1_compartment"
            ),
            GeneticElement(
                element_id="compartment2_promoter",
                sequence="TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGACC",
                element_type=ElementType.PROMOTER,
                vm_specific=True,
                regulation_target="vm2_compartment"
            )
        ],
        description="Membrane-based compartmentalization for VM isolation"
    )


def get_transcriptional_isolation_circuit() -> GeneticCircuit:
    """Get the transcriptional isolation circuit"""
    return GeneticCircuit(
        circuit_id="transcriptional_isolation",
        circuit_type=CircuitType.ISOLATION,
        elements=[
            # Sigma factor variants for each VM
            GeneticElement(
                element_id="vm1_sigma_factor",
                sequence="ATGACCCTGAAACAGGCAATCACCAAGATCATCACCGGCTACGTGCAG",
                element_type=ElementType.GENE,
                vm_specific=True
            ),
            GeneticElement(
                element_id="vm2_sigma_factor",
                sequence="ATGACCCTGAAACAGGCAATCGCCAAGATCGTCACCGGCTACGTGCAG",
                element_type=ElementType.GENE,
                vm_specific=True
            ),
            GeneticElement(
                element_id="vm3_sigma_factor",
                sequence="ATGACCCTGAAACAGGCAATCTCCAAGATCTTCACCGGCTACGTGCAG",
                element_type=ElementType.GENE,
                vm_specific=True
            ),
            # Corresponding promoters that only respond to specific sigma factors
            GeneticElement(
                element_id="vm1_specific_promoter",
                sequence="TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGAGC",
                element_type=ElementType.PROMOTER,
                vm_specific=True,
                regulation_target="vm1_genes"
            ),
            GeneticElement(
                element_id="vm2_specific_promoter",
                sequence="TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGACC",
                element_type=ElementType.PROMOTER,
                vm_specific=True,
                regulation_target="vm2_genes"
            ),
            GeneticElement(
                element_id="vm3_specific_promoter",
                sequence="TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGGCC",
                element_type=ElementType.PROMOTER,
                vm_specific=True,
                regulation_target="vm3_genes"
            )
        ],
        description="Transcriptional isolation using VM-specific sigma factors"
    )


def get_protein_isolation_circuit() -> GeneticCircuit:
    """Get the protein-level isolation circuit"""
    return GeneticCircuit(
        circuit_id="protein_isolation",
        circuit_type=CircuitType.ISOLATION,
        elements=[
            # Protein tags for isolation
            GeneticElement(
                element_id="vm1_protein_tag",
                sequence="ATGCACCACCACCACCACCAC",  # His6 tag DNA
                element_type=ElementType.TAG,
                vm_specific=True
            ),
            GeneticElement(
                element_id="vm2_protein_tag",
                sequence="ATGTACCCATACGATGTTCCAGATTACGCT",  # FLAG tag DNA
                element_type=ElementType.TAG,
                vm_specific=True
            ),
            GeneticElement(
                element_id="vm3_protein_tag",
                sequence="ATGGGCTCCAGCCACCACCACCACCACCACAGCCTGGGCCTCGAG",  # Extended tag
                element_type=ElementType.TAG,
                vm_specific=True
            ),
            # Chaperones for proper protein folding
            GeneticElement(
                element_id="vm1_chaperone",
                sequence="ATGAAGAAGATCATTACCGACAAGGACGACGACAAGACCACCACC",
                element_type=ElementType.GENE,
                vm_specific=True
            ),
            GeneticElement(
                element_id="vm2_chaperone",
                sequence="ATGAAGAAGATCATTACCGACAAGGACGACGACAAGACCACCGCC",
                element_type=ElementType.GENE,
                vm_specific=True
            ),
            # Protein localization signals
            GeneticElement(
                element_id="vm1_localization_signal",
                sequence="AAGAAGGCCACCACCACC",
                element_type=ElementType.TAG,
                vm_specific=True
            ),
            GeneticElement(
                element_id="vm2_localization_signal",
                sequence="AAGAAGGCCACCACCGCC",
                element_type=ElementType.TAG,
                vm_specific=True
            )
        ],
        description="Protein-level isolation using tags, chaperones, and localization"
    )


def create_vm_isolation_circuit(vm_id: str, isolation_level: str = "standard") -> GeneticCircuit:
    """Create a VM-specific isolation circuit"""
    elements = []
    
    # Base RNA polymerase variant
    base_rnap = "ATGCGTCGTCTGACCCTGAAACAGGCAATCACC"
    # Modify sequence based on VM ID
    vm_num = vm_id.replace("vm", "")
    modified_rnap = base_rnap[:-3] + f"G{chr(67 + int(vm_num) % 3)}C"
    
    elements.append(
        GeneticElement(
            name=f"{vm_id}_rnap",
            sequence=modified_rnap,
            element_type=ElementType.GENE,
            vm_specific=True
        )
    )
    
    # Corresponding promoter
    base_promoter = "TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGAGC"
    modified_promoter = base_promoter[:-3] + f"G{chr(67 + int(vm_num) % 3)}C"
    
    elements.append(
        GeneticElement(
            name=f"{vm_id}_promoter",
            sequence=modified_promoter,
            element_type=ElementType.PROMOTER,
            vm_specific=True,
            regulation_target=f"{vm_id}_genes"
        )
    )
    
    # Add additional isolation elements based on level
    if isolation_level == "high":
        # Add orthogonal tRNA
        elements.append(
            GeneticElement(
                name=f"{vm_id}_orthogonal_trna",
                sequence=f"GGGGCCCGCCAGATGATGGATGTTAGGTGGCCTTCTAAACCG{chr(67 + int(vm_num) % 3)}ACC",
                element_type=ElementType.GENE,
                vm_specific=True
            )
        )
        
        # Add protein tag
        elements.append(
            GeneticElement(
                name=f"{vm_id}_protein_tag",
                sequence=f"ATGCACCACCACCACCACCAC{chr(67 + int(vm_num) % 3) * 3}",
                element_type=ElementType.TAG,
                vm_specific=True
            )
        )
    
    return GeneticCircuit(
        circuit_id=f"{vm_id}_isolation",
        circuit_type=CircuitType.ISOLATION,
        elements=elements,
        description=f"Isolation circuit for {vm_id} with {isolation_level} level isolation"
    )


# Circuit library for easy access
ISOLATION_CIRCUITS = {
    "memory_isolation": get_memory_isolation_circuit,
    "namespace_isolation": get_namespace_isolation_circuit,
    "membrane_isolation": get_membrane_isolation_circuit,
    "transcriptional_isolation": get_transcriptional_isolation_circuit,
    "protein_isolation": get_protein_isolation_circuit,
}
