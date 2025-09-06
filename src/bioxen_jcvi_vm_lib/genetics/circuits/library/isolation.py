"""
Isolation circuit implementations for VM separation.

This module contains genetic circuits for maintaining isolation between
virtual machines using orthogonal genetic systems.
"""

from ..core.elements import GeneticCircuit, GeneticElement, CircuitType, ElementType


# Factory functions for creating isolation circuits
def create_vm_isolation_circuit(vm_id: str, isolation_features: list = None) -> GeneticCircuit:
    """Create VM isolation circuit with specified features"""
    if isolation_features is None:
        isolation_features = ["memory", "cpu", "network"]
    
    elements = []
    
    # Add VM-specific RNA polymerase for transcriptional isolation
    elements.append(GeneticElement(
        element_id=f"{vm_id}_rnap",
        sequence="ATGCGTCGTCTGACCCTGAAACAGGCAATCACCGGCATCGTG",
        element_type=ElementType.GENE,
        vm_specific=True
    ))
    
    # Add VM-specific promoter
    elements.append(GeneticElement(
        element_id=f"{vm_id}_isolate_promoter",
        sequence="TTGACAGCTAGCTCAGTCCTAGGTATAATGCTAGCAACCTGGATC",
        element_type=ElementType.PROMOTER,
        vm_specific=True,
        regulation_target=f"{vm_id}_genes"
    ))
    
    # Add isolation genes for each feature
    base_sequence = "ATGAAAGCAATTTTCGTACTGAAAGGTTGGTGGCGCACTTCCTG"
    for i, feature in enumerate(isolation_features):
        # Vary sequence slightly for each feature
        sequence = base_sequence + ("AA" if i % 2 == 0 else "GG")
        
        elements.append(GeneticElement(
            element_id=f"{vm_id}_{feature}_isolator",
            sequence=sequence,
            element_type=ElementType.GENE,
            vm_specific=True
        ))
    
    # Add terminator
    elements.append(GeneticElement(
        element_id=f"{vm_id}_isolate_terminator",
        sequence="GCCTCTTCGCTATTACGCCAGCTGGCGAAAGGGGGATGTGCTGCAAGGCG",
        element_type=ElementType.TERMINATOR,
        vm_specific=True
    ))
    
    return GeneticCircuit(
        circuit_id=f"{vm_id}_isolation",
        circuit_type=CircuitType.ISOLATION,
        elements=elements,
        description=f"VM isolation circuit for {vm_id} with features: {', '.join(isolation_features)}"
    )


def create_namespace_circuit(vm_id: str, namespace_type: str = "genetic") -> GeneticCircuit:
    """Create namespace isolation circuit for VM"""
    elements = []
    
    # Add namespace controller promoter
    elements.append(GeneticElement(
        element_id=f"{vm_id}_namespace_promoter",
        sequence="TTGACAGCTAGCTCAGTCCTAGGTATAATGCTAGCGGAATTC",
        element_type=ElementType.PROMOTER,
        vm_specific=True,
        regulation_target=f"{vm_id}_namespace_controller"
    ))
    
    # Add namespace controller gene
    elements.append(GeneticElement(
        element_id=f"{vm_id}_namespace_controller",
        sequence="ATGAAAGCAATTTTCGTACTGAAAGGTTGGTGGCGCACTTCCTGAATTC",
        element_type=ElementType.GENE,
        vm_specific=True
    ))
    
    # Add namespace-specific RBS
    elements.append(GeneticElement(
        element_id=f"{vm_id}_namespace_rbs",
        sequence="AAGGAGGTGATCCATGCC",
        element_type=ElementType.RBS,
        vm_specific=True
    ))
    
    # Add namespace isolation genes based on type
    if namespace_type == "genetic":
        # Genetic namespace isolation
        elements.append(GeneticElement(
            element_id=f"{vm_id}_genetic_barrier",
            sequence="ATGAAAGCAATTTTCGTACTGAAAGGTTGGTGGCGCACTTCCTGCCAA",
            element_type=ElementType.GENE,
            vm_specific=True
        ))
    elif namespace_type == "metabolic":
        # Metabolic namespace isolation
        elements.append(GeneticElement(
            element_id=f"{vm_id}_metabolic_barrier",
            sequence="ATGAAAGCAATTTTCGTACTGAAAGGTTGGTGGCGCACTTCCTGCCGG",
            element_type=ElementType.GENE,
            vm_specific=True
        ))
    
    # Add terminator
    elements.append(GeneticElement(
        element_id=f"{vm_id}_namespace_terminator",
        sequence="GCCTCTTCGCTATTACGCCAGCTGGCGAAAGGGGGATGTGCTGCAAGGCG",
        element_type=ElementType.TERMINATOR,
        vm_specific=True
    ))
    
    return GeneticCircuit(
        circuit_id=f"{vm_id}_namespace",
        circuit_type=CircuitType.ISOLATION,
        elements=elements,
        description=f"Namespace isolation circuit for {vm_id} ({namespace_type} type)"
    )


def create_security_circuit(vm_id: str, security_features: list = None) -> GeneticCircuit:
    """Create security circuit for VM protection"""
    if security_features is None:
        security_features = ["authentication", "encryption", "access_control"]
    
    elements = []
    
    # Add security controller promoter
    elements.append(GeneticElement(
        element_id=f"{vm_id}_security_promoter",
        sequence="TTGACAGCTAGCTCAGTCCTAGGTATAATGCTAGCAAGCTTCC",
        element_type=ElementType.PROMOTER,
        vm_specific=True,
        regulation_target=f"{vm_id}_security_controller"
    ))
    
    # Add security controller gene
    elements.append(GeneticElement(
        element_id=f"{vm_id}_security_controller",
        sequence="ATGAAAGCAATTTTCGTACTGAAAGGTTGGTGGCGCACTTCCTGAAGC",
        element_type=ElementType.GENE,
        vm_specific=True
    ))
    
    # Add security genes for each feature
    base_sequence = "ATGAAAGCAATTTTCGTACTGAAAGGTTGGTGGCGCACTTCCTG"
    for i, feature in enumerate(security_features):
        # Create unique sequences for each security feature
        if feature == "authentication":
            sequence = base_sequence + "AAGC"
        elif feature == "encryption":
            sequence = base_sequence + "CCGG" 
        elif feature == "access_control":
            sequence = base_sequence + "TTAA"
        else:
            sequence = base_sequence + "GGCC"
        
        elements.append(GeneticElement(
            element_id=f"{vm_id}_{feature}_security",
            sequence=sequence,
            element_type=ElementType.GENE,
            vm_specific=True
        ))
    
    # Add security monitoring sRNA
    elements.append(GeneticElement(
        element_id=f"{vm_id}_security_monitor",
        sequence="GCAAGCUGGUCGGCAUCAAGCCUUAA",
        element_type=ElementType.SRNA,
        vm_specific=True,
        regulation_target=f"{vm_id}_security_genes"
    ))
    
    # Add terminator
    elements.append(GeneticElement(
        element_id=f"{vm_id}_security_terminator",
        sequence="GCCTCTTCGCTATTACGCCAGCTGGCGAAAGGGGGATGTGCTGCAAGGCG",
        element_type=ElementType.TERMINATOR,
        vm_specific=True
    ))
    
    return GeneticCircuit(
        circuit_id=f"{vm_id}_security",
        circuit_type=CircuitType.ISOLATION,
        elements=elements,
        description=f"Security circuit for {vm_id} with features: {', '.join(security_features)}"
    )


# Legacy functions (keeping for backward compatibility)
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
            element_id=f"{vm_id}_rnap",
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
            element_id=f"{vm_id}_promoter",
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
                element_id=f"{vm_id}_orthogonal_trna",
                sequence=f"GGGGCCCGCCAGATGATGGATGTTAGGTGGCCTTCTAAACCG{chr(67 + int(vm_num) % 3)}ACC",
                element_type=ElementType.GENE,
                vm_specific=True
            )
        )
        
        # Add protein tag
        elements.append(
            GeneticElement(
                element_id=f"{vm_id}_protein_tag",
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
