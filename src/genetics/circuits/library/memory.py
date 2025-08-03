"""
Memory management circuit implementations for garbage collection.

This module contains genetic circuits for managing protein degradation,
RNA cleanup, and cellular memory management in the hypervisor.
"""

from ..core.elements import GeneticCircuit, GeneticElement, CircuitType, ElementType


def get_protein_degradation_circuit() -> GeneticCircuit:
    """Get the protein degradation circuit"""
    return GeneticCircuit(
        circuit_id="protein_degradation",
        circuit_type=CircuitType.MEMORY_MANAGER,
        elements=[
            GeneticElement(
                name="vm1_protease",
                sequence="ATGAAACGCATCGGCTACGTGCAGGCAATCACC",  # VM1-specific protease
                element_type=ElementType.GENE,
                vm_specific=True
            ),
            GeneticElement(
                name="vm1_deg_tag",
                sequence="GGTAAATAA",  # Degradation tag for VM1 proteins
                element_type=ElementType.TAG,
                vm_specific=True
            ),
            GeneticElement(
                name="vm2_protease",
                sequence="ATGAAACGCATCGGCTACGTGCAGGCAATCGCC", # VM2-specific protease
                element_type=ElementType.GENE, 
                vm_specific=True
            ),
            GeneticElement(
                name="vm2_deg_tag",
                sequence="GGTACATAA",  # Degradation tag for VM2 proteins
                element_type=ElementType.TAG,
                vm_specific=True
            )
        ],
        description="VM-specific protein degradation for garbage collection"
    )


def get_rna_cleanup_circuit() -> GeneticCircuit:
    """Get the RNA cleanup and degradation circuit"""
    return GeneticCircuit(
        circuit_id="rna_cleanup",
        circuit_type=CircuitType.MEMORY_MANAGER,
        elements=[
            # RNase variants for different VMs
            GeneticElement(
                name="vm1_rnase",
                sequence="ATGACCCTGAAACAGGCAATCACCAAGATCATCACCGGCTACGTGCAG",
                element_type=ElementType.GENE,
                vm_specific=True
            ),
            GeneticElement(
                name="vm2_rnase",
                sequence="ATGACCCTGAAACAGGCAATCGCCAAGATCGTCACCGGCTACGTGCAG",
                element_type=ElementType.GENE,
                vm_specific=True
            ),
            # RNA degradation signals
            GeneticElement(
                name="vm1_rna_deg_signal",
                sequence="AAUAAAUAAUAA",  # RNA degradation signal
                element_type=ElementType.TAG,
                vm_specific=True
            ),
            GeneticElement(
                name="vm2_rna_deg_signal",
                sequence="AAUACAUAAUAA",  # Modified RNA degradation signal
                element_type=ElementType.TAG,
                vm_specific=True
            ),
            # Termination enhancement
            GeneticElement(
                name="enhanced_terminator",
                sequence="AAAAAAGCCCGCTCACGGCCCCTTTTTCTATATAGT",
                element_type=ElementType.TERMINATOR
            )
        ],
        description="RNA cleanup and degradation system for memory management"
    )


def get_metabolite_recycling_circuit() -> GeneticCircuit:
    """Get the metabolite recycling circuit"""
    return GeneticCircuit(
        circuit_id="metabolite_recycling",
        circuit_type=CircuitType.MEMORY_MANAGER,
        elements=[
            # Metabolite scavenging enzymes
            GeneticElement(
                name="nucleotide_salvage_enzyme",
                sequence="ATGCTGACCCTGAAACAGGCAATCACCAAGATCATCACCGGCTACGTGCAGGCAATC",
                element_type=ElementType.GENE
            ),
            GeneticElement(
                name="amino_acid_recycler",
                sequence="ATGAAACGCATCGGCTACGTGCAGGCAATCACCAAGATCATCACCCTGAAACAGGC",
                element_type=ElementType.GENE
            ),
            # Metabolite sensors
            GeneticElement(
                name="nucleotide_sensor_promoter",
                sequence="TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGAGC",
                element_type=ElementType.PROMOTER,
                regulation_target="nucleotide_salvage_enzyme"
            ),
            GeneticElement(
                name="amino_acid_sensor_promoter",
                sequence="TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGACC",
                element_type=ElementType.PROMOTER,
                regulation_target="amino_acid_recycler"
            ),
            # Recycling regulatory RNA
            GeneticElement(
                name="recycling_control_rna",
                sequence="GCAAGCUGGUCGGCAUCGGCAUCGCAUC",
                element_type=ElementType.SRNA,
                regulation_target="recycling_system"
            )
        ],
        description="Metabolite recycling system for efficient resource utilization"
    )


def get_garbage_collection_circuit() -> GeneticCircuit:
    """Get the comprehensive garbage collection circuit"""
    return GeneticCircuit(
        circuit_id="garbage_collection",
        circuit_type=CircuitType.MEMORY_MANAGER,
        elements=[
            # Main garbage collector protease
            GeneticElement(
                name="gc_protease",
                sequence="ATGAAACGCATCGGCTACGTGCAGGCAATCACCAAGATCATCACCCTGAAACAGGCAATC",
                element_type=ElementType.GENE
            ),
            # Garbage collection trigger
            GeneticElement(
                name="gc_trigger_promoter",
                sequence="TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGGCC",
                element_type=ElementType.PROMOTER,
                regulation_target="gc_protease"
            ),
            # Universal degradation tags
            GeneticElement(
                name="universal_deg_tag",
                sequence="AANDENYALAA",  # SsrA-like tag
                element_type=ElementType.TAG
            ),
            GeneticElement(
                name="urgent_deg_tag", 
                sequence="AANDENYALAAWENYALAA",  # Extended urgent degradation
                element_type=ElementType.TAG
            ),
            # Memory pressure sensor
            GeneticElement(
                name="memory_pressure_sensor",
                sequence="ATGGTGAGCAAGGGCGAGGAGCTGTTCACCGGGGTGGTGCCCATC",
                element_type=ElementType.GENE
            ),
            GeneticElement(
                name="memory_sensor_promoter",
                sequence="TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGAAA",
                element_type=ElementType.PROMOTER,
                regulation_target="memory_pressure_sensor"
            )
        ],
        description="Comprehensive garbage collection system with memory pressure monitoring"
    )


def get_memory_compaction_circuit() -> GeneticCircuit:
    """Get the memory compaction circuit"""
    return GeneticCircuit(
        circuit_id="memory_compaction",
        circuit_type=CircuitType.MEMORY_MANAGER,
        elements=[
            # DNA compaction proteins
            GeneticElement(
                name="dna_compaction_protein",
                sequence="ATGACCAAGAAGATCATTACCGACAAGGACGACGACAAGACCACCACCGGCTACGTG",
                element_type=ElementType.GENE
            ),
            # Chromatin remodeling complex
            GeneticElement(
                name="chromatin_remodeler",
                sequence="ATGCTGACCCTGAAACAGGCAATCACCAAGATCATCACCGGCTACGTGCAGGCAATCACC",
                element_type=ElementType.GENE
            ),
            # Compaction regulatory elements
            GeneticElement(
                name="compaction_promoter",
                sequence="TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGCCC",
                element_type=ElementType.PROMOTER,
                regulation_target="compaction_proteins"
            ),
            GeneticElement(
                name="compaction_control_rna",
                sequence="GCAAGCUGGUCGGCAUCGGCAUCGCAUCGGCAUC",
                element_type=ElementType.SRNA,
                regulation_target="compaction_system"
            )
        ],
        description="Memory compaction system for efficient DNA organization"
    )


def get_memory_allocation_circuit() -> GeneticCircuit:
    """Get the memory allocation management circuit"""
    return GeneticCircuit(
        circuit_id="memory_allocation",
        circuit_type=CircuitType.MEMORY_MANAGER,
        elements=[
            # Memory allocation tracker
            GeneticElement(
                name="allocation_tracker",
                sequence="ATGGTGACCCTGAAACAGGCAATCACCAAGATCATCACCGGCTACGTGCAGGCAATC",
                element_type=ElementType.GENE
            ),
            # Memory boundary markers
            GeneticElement(
                name="vm1_memory_marker",
                sequence="TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGAGC",
                element_type=ElementType.PROMOTER,
                vm_specific=True,
                regulation_target="vm1_memory_space"
            ),
            GeneticElement(
                name="vm2_memory_marker",
                sequence="TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGACC",
                element_type=ElementType.PROMOTER,
                vm_specific=True,
                regulation_target="vm2_memory_space"
            ),
            # Allocation control system
            GeneticElement(
                name="allocation_controller",
                sequence="ATGAAACGCATCGGCTACGTGCAGGCAATCACCAAGATCATCACCCTG",
                element_type=ElementType.GENE
            ),
            GeneticElement(
                name="allocation_control_rna",
                sequence="GCAAGCUGGUCGGCAUCGGCAUC",
                element_type=ElementType.SRNA,
                regulation_target="allocation_system"
            )
        ],
        description="Memory allocation management for VM memory boundaries"
    )


def create_vm_memory_manager(vm_id: str, cleanup_level: str = "standard") -> GeneticCircuit:
    """Create a VM-specific memory management circuit"""
    elements = []
    
    # VM-specific protease
    base_protease = "ATGAAACGCATCGGCTACGTGCAGGCAATCACC"
    vm_num = vm_id.replace("vm", "")
    modified_protease = base_protease[:-3] + f"A{chr(67 + int(vm_num) % 3)}C"
    
    elements.append(
        GeneticElement(
            name=f"{vm_id}_protease",
            sequence=modified_protease,
            element_type=ElementType.GENE,
            vm_specific=True
        )
    )
    
    # VM-specific degradation tag
    base_tag = "GGTAAATAA"
    modified_tag = base_tag[:-2] + f"{chr(65 + int(vm_num) % 3)}A"
    
    elements.append(
        GeneticElement(
            name=f"{vm_id}_deg_tag",
            sequence=modified_tag,
            element_type=ElementType.TAG,
            vm_specific=True
        )
    )
    
    # Add additional cleanup elements based on level
    if cleanup_level == "aggressive":
        # Add RNase
        elements.append(
            GeneticElement(
                name=f"{vm_id}_rnase",
                sequence=f"ATGACCCTGAAACAGGCAATC{chr(65 + int(vm_num) % 3)}CCAAGATC{chr(65 + int(vm_num) % 3)}TCACCGGCTACGTGCAG",
                element_type=ElementType.GENE,
                vm_specific=True
            )
        )
        
        # Add memory pressure sensor
        elements.append(
            GeneticElement(
                name=f"{vm_id}_memory_sensor",
                sequence="ATGGTGAGCAAGGGCGAGGAGCTGTTCACCGGGGTGGTGCCCATC",
                element_type=ElementType.GENE,
                vm_specific=True
            )
        )
    
    return GeneticCircuit(
        circuit_id=f"{vm_id}_memory_manager",
        circuit_type=CircuitType.MEMORY_MANAGER,
        elements=elements,
        description=f"Memory management circuit for {vm_id} with {cleanup_level} cleanup"
    )


# Circuit library for easy access
MEMORY_CIRCUITS = {
    "protein_degradation": get_protein_degradation_circuit,
    "rna_cleanup": get_rna_cleanup_circuit,
    "metabolite_recycling": get_metabolite_recycling_circuit,
    "garbage_collection": get_garbage_collection_circuit,
    "memory_compaction": get_memory_compaction_circuit,
    "memory_allocation": get_memory_allocation_circuit,
}
