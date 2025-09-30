"""
Memory management circuit implementations for garbage collection.

This module contains genetic circuits for managing protein degradation,
RNA cleanup, and cellular memory management in the hypervisor.
"""

from ..core.elements import GeneticCircuit, GeneticElement, CircuitType, ElementType


# Factory functions for creating memory management circuits
def create_memory_allocator(vm_id: str, memory_size: int = 1024) -> GeneticCircuit:
    """Create memory allocator circuit for VM"""
    elements = []
    
    # Add allocator controller promoter
    elements.append(GeneticElement(
        element_id=f"{vm_id}_allocator_promoter",
        sequence="TTGACAGCTAGCTCAGTCCTAGGTATAATGCTAGCGGAATTC",
        element_type=ElementType.PROMOTER,
        vm_specific=True,
        regulation_target=f"{vm_id}_allocator"
    ))
    
    # Add memory allocator gene
    elements.append(GeneticElement(
        element_id=f"{vm_id}_allocator",
        sequence="ATGAAAGCAATTTTCGTACTGAAAGGTTGGTGGCGCACTTCCTGAATTC",
        element_type=ElementType.GENE,
        vm_specific=True
    ))
    
    # Add memory tracking genes based on size
    block_count = max(1, memory_size // 256)  # One gene per 256 units
    base_sequence = "ATGAAAGCAATTTTCGTACTGAAAGGTTGGTGGCGCACTTCCTG"
    
    for i in range(min(block_count, 4)):  # Limit to 4 genes
        sequence = base_sequence + ("AA" if i % 2 == 0 else "GG")
        elements.append(GeneticElement(
            element_id=f"{vm_id}_memory_block_{i+1}",
            sequence=sequence,
            element_type=ElementType.GENE,
            vm_specific=True
        ))
    
    # Add allocation monitoring sRNA
    elements.append(GeneticElement(
        element_id=f"{vm_id}_alloc_monitor",
        sequence="GCAAGCUGGUCGGCAUCAAGCC",
        element_type=ElementType.SRNA,
        vm_specific=True,
        regulation_target=f"{vm_id}_memory_genes"
    ))
    
    # Add terminator
    elements.append(GeneticElement(
        element_id=f"{vm_id}_allocator_terminator",
        sequence="GCCTCTTCGCTATTACGCCAGCTGGCGAAAGGGGGATGTGCTGCAAGGCG",
        element_type=ElementType.TERMINATOR,
        vm_specific=True
    ))
    
    return GeneticCircuit(
        circuit_id=f"{vm_id}_memory_allocator",
        circuit_type=CircuitType.MEMORY_MANAGER,
        elements=elements,
        description=f"Memory allocator circuit for {vm_id} ({memory_size} units)"
    )


def create_garbage_collector(vm_id: str, gc_algorithm: str = "mark_sweep") -> GeneticCircuit:
    """Create garbage collection circuit for VM"""
    elements = []
    
    # Add GC controller promoter
    elements.append(GeneticElement(
        element_id=f"{vm_id}_gc_promoter",
        sequence="TTGACAGCTAGCTCAGTCCTAGGTATAATGCTAGCAAGCTT",
        element_type=ElementType.PROMOTER,
        vm_specific=True,
        regulation_target=f"{vm_id}_gc_controller"
    ))
    
    # Add GC controller gene
    elements.append(GeneticElement(
        element_id=f"{vm_id}_gc_controller",
        sequence="ATGAAAGCAATTTTCGTACTGAAAGGTTGGTGGCGCACTTCCTGAAGC",
        element_type=ElementType.GENE,
        vm_specific=True
    ))
    
    # Add algorithm-specific genes
    if gc_algorithm == "mark_sweep":
        # Mark phase gene
        elements.append(GeneticElement(
            element_id=f"{vm_id}_mark_gene",
            sequence="ATGAAAGCAATTTTCGTACTGAAAGGTTGGTGGCGCACTTCCTGAAAA",
            element_type=ElementType.GENE,
            vm_specific=True
        ))
        
        # Sweep phase gene
        elements.append(GeneticElement(
            element_id=f"{vm_id}_sweep_gene",
            sequence="ATGAAAGCAATTTTCGTACTGAAAGGTTGGTGGCGCACTTCCTGCCCC",
            element_type=ElementType.GENE,
            vm_specific=True
        ))
    
    elif gc_algorithm == "reference_counting":
        # Reference counter gene
        elements.append(GeneticElement(
            element_id=f"{vm_id}_refcount_gene",
            sequence="ATGAAAGCAATTTTCGTACTGAAAGGTTGGTGGCGCACTTCCTGGGGG",
            element_type=ElementType.GENE,
            vm_specific=True
        ))
    
    # Add protease for protein cleanup
    elements.append(GeneticElement(
        element_id=f"{vm_id}_gc_protease",
        sequence="ATGAAACGCATCGGCTACGTGCAGGCAATCACCGGC",
        element_type=ElementType.GENE,
        vm_specific=True
    ))
    
    # Add degradation tags
    elements.append(GeneticElement(
        element_id=f"{vm_id}_deg_tag",
        sequence="AACGCCAACGCCGCCTAG",
        element_type=ElementType.TAG,
        vm_specific=True
    ))
    
    # Add terminator
    elements.append(GeneticElement(
        element_id=f"{vm_id}_gc_terminator",
        sequence="GCCTCTTCGCTATTACGCCAGCTGGCGAAAGGGGGATGTGCTGCAAGGCG",
        element_type=ElementType.TERMINATOR,
        vm_specific=True
    ))
    
    return GeneticCircuit(
        circuit_id=f"{vm_id}_garbage_collector",
        circuit_type=CircuitType.MEMORY_MANAGER,
        elements=elements,
        description=f"Garbage collection circuit for {vm_id} ({gc_algorithm} algorithm)"
    )


def create_heap_manager(vm_id: str, heap_type: str = "dynamic") -> GeneticCircuit:
    """Create heap management circuit for VM"""
    elements = []
    
    # Add heap controller promoter
    elements.append(GeneticElement(
        element_id=f"{vm_id}_heap_promoter",
        sequence="TTGACAGCTAGCTCAGTCCTAGGTATAATGCTAGCCCTGGA",
        element_type=ElementType.PROMOTER,
        vm_specific=True,
        regulation_target=f"{vm_id}_heap_manager"
    ))
    
    # Add heap manager gene
    elements.append(GeneticElement(
        element_id=f"{vm_id}_heap_manager",
        sequence="ATGAAAGCAATTTTCGTACTGAAAGGTTGGTGGCGCACTTCCTGCCGG",
        element_type=ElementType.GENE,
        vm_specific=True
    ))
    
    # Add heap-specific components
    if heap_type == "dynamic":
        # Dynamic allocation gene
        elements.append(GeneticElement(
            element_id=f"{vm_id}_dynamic_alloc",
            sequence="ATGAAAGCAATTTTCGTACTGAAAGGTTGGTGGCGCACTTCCTGAAGG",
            element_type=ElementType.GENE,
            vm_specific=True
        ))
        
        # Deallocation gene
        elements.append(GeneticElement(
            element_id=f"{vm_id}_dealloc",
            sequence="ATGAAAGCAATTTTCGTACTGAAAGGTTGGTGGCGCACTTCCTGCCAA",
            element_type=ElementType.GENE,
            vm_specific=True
        ))
    
    elif heap_type == "fixed":
        # Fixed pool manager
        elements.append(GeneticElement(
            element_id=f"{vm_id}_pool_manager",
            sequence="ATGAAAGCAATTTTCGTACTGAAAGGTTGGTGGCGCACTTCCTGTTAA",
            element_type=ElementType.GENE,
            vm_specific=True
        ))
    
    # Add heap monitoring sRNA
    elements.append(GeneticElement(
        element_id=f"{vm_id}_heap_monitor",
        sequence="GCAAGCUGGUCGGCAUCAAGCCUGGAA",
        element_type=ElementType.SRNA,
        vm_specific=True,
        regulation_target=f"{vm_id}_heap_genes"
    ))
    
    # Add terminator
    elements.append(GeneticElement(
        element_id=f"{vm_id}_heap_terminator",
        sequence="GCCTCTTCGCTATTACGCCAGCTGGCGAAAGGGGGATGTGCTGCAAGGCG",
        element_type=ElementType.TERMINATOR,
        vm_specific=True
    ))
    
    return GeneticCircuit(
        circuit_id=f"{vm_id}_heap_manager",
        circuit_type=CircuitType.MEMORY_MANAGER,
        elements=elements,
        description=f"Heap management circuit for {vm_id} ({heap_type} type)"
    )


# Legacy functions (keeping for backward compatibility)
def get_protein_degradation_circuit() -> GeneticCircuit:
    """Get the protein degradation circuit"""
    return GeneticCircuit(
        circuit_id="protein_degradation",
        circuit_type=CircuitType.MEMORY_MANAGER,
        elements=[
            GeneticElement(
                element_id="vm1_protease",
                sequence="ATGAAACGCATCGGCTACGTGCAGGCAATCACC",  # VM1-specific protease
                element_type=ElementType.GENE,
                vm_specific=True
            ),
            GeneticElement(
                element_id="vm1_deg_tag",
                sequence="GGTAAATAA",  # Degradation tag for VM1 proteins
                element_type=ElementType.TAG,
                vm_specific=True
            ),
            GeneticElement(
                element_id="vm2_protease",
                sequence="ATGAAACGCATCGGCTACGTGCAGGCAATCGCC", # VM2-specific protease
                element_type=ElementType.GENE, 
                vm_specific=True
            ),
            GeneticElement(
                element_id="vm2_deg_tag",
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
                element_id="vm1_rnase",
                sequence="ATGACCCTGAAACAGGCAATCACCAAGATCATCACCGGCTACGTGCAG",
                element_type=ElementType.GENE,
                vm_specific=True
            ),
            GeneticElement(
                element_id="vm2_rnase",
                sequence="ATGACCCTGAAACAGGCAATCGCCAAGATCGTCACCGGCTACGTGCAG",
                element_type=ElementType.GENE,
                vm_specific=True
            ),
            # RNA degradation signals
            GeneticElement(
                element_id="vm1_rna_deg_signal",
                sequence="AAUAAAUAAUAA",  # RNA degradation signal
                element_type=ElementType.TAG,
                vm_specific=True
            ),
            GeneticElement(
                element_id="vm2_rna_deg_signal",
                sequence="AAUACAUAAUAA",  # Modified RNA degradation signal
                element_type=ElementType.TAG,
                vm_specific=True
            ),
            # Termination enhancement
            GeneticElement(
                element_id="enhanced_terminator",
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
                element_id="nucleotide_salvage_enzyme",
                sequence="ATGCTGACCCTGAAACAGGCAATCACCAAGATCATCACCGGCTACGTGCAGGCAATC",
                element_type=ElementType.GENE
            ),
            GeneticElement(
                element_id="amino_acid_recycler",
                sequence="ATGAAACGCATCGGCTACGTGCAGGCAATCACCAAGATCATCACCCTGAAACAGGC",
                element_type=ElementType.GENE
            ),
            # Metabolite sensors
            GeneticElement(
                element_id="nucleotide_sensor_promoter",
                sequence="TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGAGC",
                element_type=ElementType.PROMOTER,
                regulation_target="nucleotide_salvage_enzyme"
            ),
            GeneticElement(
                element_id="amino_acid_sensor_promoter",
                sequence="TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGACC",
                element_type=ElementType.PROMOTER,
                regulation_target="amino_acid_recycler"
            ),
            # Recycling regulatory RNA
            GeneticElement(
                element_id="recycling_control_rna",
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
                element_id="gc_protease",
                sequence="ATGAAACGCATCGGCTACGTGCAGGCAATCACCAAGATCATCACCCTGAAACAGGCAATC",
                element_type=ElementType.GENE
            ),
            # Garbage collection trigger
            GeneticElement(
                element_id="gc_trigger_promoter",
                sequence="TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGGCC",
                element_type=ElementType.PROMOTER,
                regulation_target="gc_protease"
            ),
            # Universal degradation tags
            GeneticElement(
                element_id="universal_deg_tag",
                sequence="AANDENYALAA",  # SsrA-like tag
                element_type=ElementType.TAG
            ),
            GeneticElement(
                element_id="urgent_deg_tag", 
                sequence="AANDENYALAAWENYALAA",  # Extended urgent degradation
                element_type=ElementType.TAG
            ),
            # Memory pressure sensor
            GeneticElement(
                element_id="memory_pressure_sensor",
                sequence="ATGGTGAGCAAGGGCGAGGAGCTGTTCACCGGGGTGGTGCCCATC",
                element_type=ElementType.GENE
            ),
            GeneticElement(
                element_id="memory_sensor_promoter",
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
                element_id="dna_compaction_protein",
                sequence="ATGACCAAGAAGATCATTACCGACAAGGACGACGACAAGACCACCACCGGCTACGTG",
                element_type=ElementType.GENE
            ),
            # Chromatin remodeling complex
            GeneticElement(
                element_id="chromatin_remodeler",
                sequence="ATGCTGACCCTGAAACAGGCAATCACCAAGATCATCACCGGCTACGTGCAGGCAATCACC",
                element_type=ElementType.GENE
            ),
            # Compaction regulatory elements
            GeneticElement(
                element_id="compaction_promoter",
                sequence="TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGCCC",
                element_type=ElementType.PROMOTER,
                regulation_target="compaction_proteins"
            ),
            GeneticElement(
                element_id="compaction_control_rna",
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
                element_id="allocation_tracker",
                sequence="ATGGTGACCCTGAAACAGGCAATCACCAAGATCATCACCGGCTACGTGCAGGCAATC",
                element_type=ElementType.GENE
            ),
            # Memory boundary markers
            GeneticElement(
                element_id="vm1_memory_marker",
                sequence="TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGAGC",
                element_type=ElementType.PROMOTER,
                vm_specific=True,
                regulation_target="vm1_memory_space"
            ),
            GeneticElement(
                element_id="vm2_memory_marker",
                sequence="TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGACC",
                element_type=ElementType.PROMOTER,
                vm_specific=True,
                regulation_target="vm2_memory_space"
            ),
            # Allocation control system
            GeneticElement(
                element_id="allocation_controller",
                sequence="ATGAAACGCATCGGCTACGTGCAGGCAATCACCAAGATCATCACCCTG",
                element_type=ElementType.GENE
            ),
            GeneticElement(
                element_id="allocation_control_rna",
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
