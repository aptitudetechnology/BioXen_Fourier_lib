"""
Circuit factory for dynamic genetic circuit generation.

This module provides a factory pattern for creating genetic circuits
on demand based on VM configuration and requirements.
"""

from typing import Dict, List, Optional
from .elements import GeneticCircuit, GeneticElement, CircuitType, ElementType


class CircuitFactory:
    """Factory for creating genetic circuits dynamically"""
    
    def __init__(self):
        self.circuit_templates = {}
        self._initialize_templates()
    
    def _initialize_templates(self):
        """Initialize circuit templates for dynamic generation"""
        # These templates will be used to generate circuits on demand
        self.circuit_templates = {
            "monitor": {
                "atp_sensor": {
                    "promoter": "TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGAGC",
                    "reporter": "ATGAAAGCAATTTTCGTACTGAAAGGTTGGTGGCGCACTTCCTGAA"
                },
                "ribosome_monitor": {
                    "promoter": "TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGACC",
                    "reporter": "ATGAAAGCAATTTTCGTACTGAAAGGTTGGTGGCGCACTTCCTGCC"
                }
            },
            "scheduler": {
                "rbs_variants": {
                    "strong": "AGGAGGACAACATG",
                    "medium": "AGGAGAAACATG", 
                    "weak": "AGGACATG"
                },
                "regulatory_rna": "GCAAGCUGGUCGGCAUC"
            },
            "isolation": {
                "rnap_variants": {
                    "vm1": "ATGCGTCGTCTGACCCTGAAACAGGCAATCACC",
                    "vm2": "ATGCGTCGTCTGACCCTGAAGCAGGCAATCACC"
                },
                "promoter_variants": {
                    "vm1": "TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGAGC",
                    "vm2": "TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGACC"
                }
            },
            "memory": {
                "protease_variants": {
                    "vm1": "ATGAAACGCATCGGCTACGTGCAGGCAATCACC",
                    "vm2": "ATGAAACGCATCGGCTACGTGCAGGCAATCGCC"
                },
                "degradation_tags": {
                    "vm1": "GGTAAATAA",
                    "vm2": "GGTACATAA"
                }
            }
        }
    
    def create_monitor(self, monitor_type: str = "atp_sensor") -> GeneticCircuit:
        """Create a monitoring circuit"""
        if monitor_type not in self.circuit_templates["monitor"]:
            raise ValueError(f"Unknown monitor type: {monitor_type}")
        
        template = self.circuit_templates["monitor"][monitor_type]
        
        elements = [
            GeneticElement(
                element_id=f"{monitor_type}_promoter",
                sequence=template["promoter"],
                element_type=ElementType.PROMOTER
            ),
            GeneticElement(
                element_id=f"{monitor_type}_reporter",
                sequence=template["reporter"],
                element_type=ElementType.GENE
            )
        ]
        
        return GeneticCircuit(
            circuit_id=f"{monitor_type}_monitor",
            circuit_type=CircuitType.RESOURCE_MONITOR,
            elements=elements,
            description=f"{monitor_type.replace('_', ' ').title()} monitoring circuit"
        )
    
    def create_scheduler(self, vm_count: int = 3) -> GeneticCircuit:
        """Create a scheduling circuit for multiple VMs"""
        rbs_variants = self.circuit_templates["scheduler"]["rbs_variants"]
        regulatory_rna = self.circuit_templates["scheduler"]["regulatory_rna"]
        
        elements = []
        
        # Add RBS variants for each VM
        rbs_types = ["strong", "medium", "weak"]
        for i in range(min(vm_count, len(rbs_types))):
            vm_id = f"vm{i+1}"
            rbs_type = rbs_types[i]
            
            elements.append(
                GeneticElement(
                    element_id=f"{vm_id}_rbs",
                    sequence=rbs_variants[rbs_type],
                    element_type=ElementType.RBS,
                    vm_specific=True
                )
            )
        
        # Add regulatory RNA
        elements.append(
            GeneticElement(
                element_id="scheduler_sRNA",
                sequence=regulatory_rna,
                element_type=ElementType.SRNA,
                regulation_target="vm_rbs"
            )
        )
        
        return GeneticCircuit(
            circuit_id="ribosome_scheduler",
            circuit_type=CircuitType.SCHEDULER,
            elements=elements,
            description="Time-sliced ribosome allocation using RBS variants"
        )
    
    def create_isolation(self, vm_id: str) -> GeneticCircuit:
        """Create an isolation circuit for a specific VM"""
        rnap_variants = self.circuit_templates["isolation"]["rnap_variants"]
        promoter_variants = self.circuit_templates["isolation"]["promoter_variants"]
        
        if vm_id not in rnap_variants:
            # Generate variant for new VM
            base_rnap = rnap_variants["vm1"]
            # Simple mutation: change one nucleotide
            variant_rnap = base_rnap[:-3] + "GCC"
            rnap_variants[vm_id] = variant_rnap
            
            base_promoter = promoter_variants["vm1"] 
            variant_promoter = base_promoter[:-3] + "GCC"
            promoter_variants[vm_id] = variant_promoter
        
        elements = [
            GeneticElement(
                element_id=f"{vm_id}_rnap",
                sequence=rnap_variants[vm_id],
                element_type=ElementType.GENE,
                vm_specific=True
            ),
            GeneticElement(
                element_id=f"{vm_id}_promoter",
                sequence=promoter_variants[vm_id],
                element_type=ElementType.PROMOTER,
                vm_specific=True,
                regulation_target=f"{vm_id}_genes"
            )
        ]
        
        return GeneticCircuit(
            circuit_id=f"{vm_id}_isolation",
            circuit_type=CircuitType.ISOLATION,
            elements=elements,
            description=f"VM-specific RNA polymerase and promoter for {vm_id} isolation"
        )
    
    def create_memory_manager(self, vm_id: str) -> GeneticCircuit:
        """Create a memory management circuit for a specific VM"""
        protease_variants = self.circuit_templates["memory"]["protease_variants"]
        degradation_tags = self.circuit_templates["memory"]["degradation_tags"]
        
        if vm_id not in protease_variants:
            # Generate variant for new VM
            base_protease = protease_variants["vm1"]
            variant_protease = base_protease[:-3] + "TCC"
            protease_variants[vm_id] = variant_protease
            
            base_tag = degradation_tags["vm1"]
            variant_tag = base_tag[:-2] + "CC"
            degradation_tags[vm_id] = variant_tag
        
        elements = [
            GeneticElement(
                element_id=f"{vm_id}_protease",
                sequence=protease_variants[vm_id],
                element_type=ElementType.GENE,
                vm_specific=True
            ),
            GeneticElement(
                element_id=f"{vm_id}_deg_tag",
                sequence=degradation_tags[vm_id],
                element_type=ElementType.TAG,
                vm_specific=True
            )
        ]
        
        return GeneticCircuit(
            circuit_id=f"{vm_id}_memory_manager",
            circuit_type=CircuitType.MEMORY_MANAGER,
            elements=elements,
            description=f"VM-specific protein degradation for {vm_id} garbage collection"
        )
    
    def create_custom_circuit(self, circuit_id: str, circuit_type: CircuitType, 
                            elements: List[GeneticElement], description: str) -> GeneticCircuit:
        """Create a custom circuit from provided elements"""
        return GeneticCircuit(
            circuit_id=circuit_id,
            circuit_type=circuit_type,
            elements=elements,
            description=description
        )
    
    def get_available_templates(self) -> Dict[str, List[str]]:
        """Get a list of available circuit templates"""
        return {
            category: list(templates.keys()) 
            for category, templates in self.circuit_templates.items()
        }


# Standalone factory functions for convenient circuit creation
def create_gene_expression_circuit(circuit_id: str, gene_name: str, 
                                 promoter_strength: str = "medium") -> GeneticCircuit:
    """Create a basic gene expression circuit"""
    
    # Define promoter sequences by strength
    promoters = {
        "weak": "TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGAGC",
        "medium": "TTGACAGCTAGCTCAGTCCTAGGTATAATGCTAGC",
        "strong": "TTGACAGCTAGCTCAGTCCTAGGTATAATGCTAGCTACTAGAG"
    }
    
    elements = [
        GeneticElement(
            element_id=f"{circuit_id}_promoter",
            element_type=ElementType.PROMOTER,
            sequence=promoters.get(promoter_strength, promoters["medium"])
        ),
        GeneticElement(
            element_id=f"{circuit_id}_rbs",
            element_type=ElementType.RBS,
            sequence="AAGGAGGTGATCCATG"
        ),
        GeneticElement(
            element_id=gene_name,
            element_type=ElementType.GENE,
            sequence="ATGAAAGCCATTTTGGCAGTAGCGGCGATCGGCACAGGCATTTATGCGTGA"
        ),
        GeneticElement(
            element_id=f"{circuit_id}_terminator",
            element_type=ElementType.TERMINATOR,
            sequence="GCCTCTTCGCTATTACGCCAGCTGGCGAAAGGGGGATGTGCTGCAAGGCG"
        )
    ]
    
    return GeneticCircuit(
        circuit_id=circuit_id,
        elements=elements,
        circuit_type=CircuitType.GENE_EXPRESSION,
        description=f"Gene expression circuit for {gene_name}"
    )


def create_regulatory_circuit(circuit_id: str, target_gene: str, 
                            regulation_type: str = "activation") -> GeneticCircuit:
    """Create a regulatory circuit that controls gene expression"""
    
    # Define regulatory sequences
    if regulation_type == "activation":
        regulatory_seq = "TTGACAGCTAGCTCAGTCCTAGGTATAATGCTAGC"
        regulator_gene = "ATGAAACGCATTCTGGCAGTGGCAGGATCGGCACAGGCATTTATGCGTGA"
    else:  # repression
        regulatory_seq = "TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGAGC"
        regulator_gene = "ATGAAACGCATTCTGGCAGTGGCAGGATCGGCACAGGCATTTATGCGAAA"
    
    elements = [
        GeneticElement(
            element_id=f"{circuit_id}_reg_promoter",
            element_type=ElementType.PROMOTER,
            sequence=regulatory_seq
        ),
        GeneticElement(
            element_id=f"{circuit_id}_regulator",
            element_type=ElementType.GENE,
            sequence=regulator_gene,
            regulation_target=target_gene
        ),
        GeneticElement(
            element_id=f"{circuit_id}_operator",
            element_type=ElementType.OPERATOR,
            sequence="TGTGAGCGGATAAACAATTTCACACAGG"
        ),
        GeneticElement(
            element_id=f"{circuit_id}_terminator",
            element_type=ElementType.TERMINATOR,
            sequence="GCCTCTTCGCTATTACGCCAGCTGGCGAAAGGGGGATGTGCTGCAAGGCG"
        )
    ]
    
    return GeneticCircuit(
        circuit_id=circuit_id,
        elements=elements,
        circuit_type=CircuitType.REGULATORY,
        description=f"Regulatory circuit for {regulation_type} of {target_gene}"
    )


def create_metabolic_circuit(circuit_id: str, pathway_name: str, 
                           enzyme_count: int = 3) -> GeneticCircuit:
    """Create a metabolic pathway circuit"""
    
    elements = []
    
    # Add promoter
    elements.append(GeneticElement(
        element_id=f"{circuit_id}_promoter",
        element_type=ElementType.PROMOTER,
        sequence="TTGACAGCTAGCTCAGTCCTAGGTATAATGCTAGC"
    ))
    
    # Add RBS
    elements.append(GeneticElement(
        element_id=f"{circuit_id}_rbs",
        element_type=ElementType.RBS,
        sequence="AAGGAGGTGATCCATG"
    ))
    
    # Add enzymes for the pathway
    base_enzyme_seq = "ATGAAAGCCATTTTGGCAGTAGCGGCGATCGGCACAGGCATTTATGCG"
    for i in range(enzyme_count):
        # Vary the enzyme sequence slightly
        enzyme_seq = base_enzyme_seq + ("TGA" if i == enzyme_count - 1 else "AAA")
        
        elements.append(GeneticElement(
            element_id=f"{pathway_name}_enzyme_{i+1}",
            element_type=ElementType.GENE,
            sequence=enzyme_seq
        ))
    
    # Add terminator
    elements.append(GeneticElement(
        element_id=f"{circuit_id}_terminator",
        element_type=ElementType.TERMINATOR,
        sequence="GCCTCTTCGCTATTACGCCAGCTGGCGAAAGGGGGATGTGCTGCAAGGCG"
    ))
    
    return GeneticCircuit(
        circuit_id=circuit_id,
        elements=elements,
        circuit_type=CircuitType.METABOLIC,
        description=f"Metabolic pathway circuit for {pathway_name} with {enzyme_count} enzymes"
    )
