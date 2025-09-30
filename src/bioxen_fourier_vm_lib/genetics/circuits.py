"""
Genetic Circuit implementations for the BioXen hypervisor

This module contains the biological implementations of hypervisor functions
using genetic circuits, regulatory RNAs, and protein networks.
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class CircuitType(Enum):
    """Types of genetic circuits"""
    RESOURCE_MONITOR = "resource_monitor"
    SCHEDULER = "scheduler"
    ISOLATION = "isolation"
    MEMORY_MANAGER = "memory_manager"

@dataclass
class GeneticElement:
    """Represents a genetic element (gene, promoter, RBS, etc.)"""
    name: str
    sequence: str
    element_type: str  # "promoter", "rbs", "gene", "terminator", "sRNA"
    vm_specific: bool = False
    regulation_target: Optional[str] = None

@dataclass
class GeneticCircuit:
    """A complete genetic circuit"""
    circuit_id: str
    circuit_type: CircuitType
    elements: List[GeneticElement]
    description: str

class GeneticCircuitLibrary:
    """Library of genetic circuits for hypervisor functions"""
    
    def __init__(self):
        self.circuits: Dict[str, GeneticCircuit] = {}
        self._initialize_circuits()
    
    def _initialize_circuits(self):
        """Initialize the standard genetic circuits"""
        
        # ATP Monitor Circuit
        atp_monitor = GeneticCircuit(
            circuit_id="atp_monitor",
            circuit_type=CircuitType.RESOURCE_MONITOR,
            elements=[
                GeneticElement(
                    name="atp_sensor_promoter",
                    sequence="TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGAGC",
                    element_type="promoter",
                    regulation_target="atp_reporter"
                ),
                GeneticElement(
                    name="atp_reporter",
                    sequence="ATGAAAGCAATTTTCGTACTGAAAGGTTGGTGGCGCACTTCCTGAA",
                    element_type="gene",
                    regulation_target=None
                )
            ],
            description="ATP-sensitive promoter driving fluorescent reporter"
        )
        self.circuits["atp_monitor"] = atp_monitor
        
        # Ribosome Scheduler Circuit
        ribosome_scheduler = GeneticCircuit(
            circuit_id="ribosome_scheduler",
            circuit_type=CircuitType.SCHEDULER,
            elements=[
                GeneticElement(
                    name="vm1_rbs",
                    sequence="AGGAGGACAACATG",  # Strong RBS
                    element_type="rbs",
                    vm_specific=True
                ),
                GeneticElement(
                    name="vm2_rbs", 
                    sequence="AGGAGAAACATG",    # Medium RBS
                    element_type="rbs",
                    vm_specific=True
                ),
                GeneticElement(
                    name="vm3_rbs",
                    sequence="AGGACATG",        # Weak RBS
                    element_type="rbs", 
                    vm_specific=True
                ),
                GeneticElement(
                    name="scheduler_sRNA",
                    sequence="GCAAGCUGGUCGGCAUC",  # Small regulatory RNA
                    element_type="sRNA",
                    regulation_target="vm_rbs"
                )
            ],
            description="Time-sliced ribosome allocation using RBS variants"
        )
        self.circuits["ribosome_scheduler"] = ribosome_scheduler
        
        # Memory Isolation Circuit
        memory_isolation = GeneticCircuit(
            circuit_id="memory_isolation",
            circuit_type=CircuitType.ISOLATION,
            elements=[
                GeneticElement(
                    name="vm1_rnap",
                    sequence="ATGCGTCGTCTGACCCTGAAACAGGCAATCACC",  # RNA polymerase variant 1
                    element_type="gene",
                    vm_specific=True
                ),
                GeneticElement(
                    name="vm2_rnap",
                    sequence="ATGCGTCGTCTGACCCTGAAGCAGGCAATCACC",  # RNA polymerase variant 2  
                    element_type="gene",
                    vm_specific=True
                ),
                GeneticElement(
                    name="vm1_promoter",
                    sequence="TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGAGC",
                    element_type="promoter",
                    vm_specific=True,
                    regulation_target="vm1_genes"
                ),
                GeneticElement(
                    name="vm2_promoter", 
                    sequence="TTGACAATTAATCATCCGGCTCGTATAATGTGTGGAATTGTGACC",
                    element_type="promoter",
                    vm_specific=True,
                    regulation_target="vm2_genes"
                )
            ],
            description="VM-specific RNA polymerases and promoters for memory isolation"
        )
        self.circuits["memory_isolation"] = memory_isolation
        
        # Protein Degradation System
        protein_degradation = GeneticCircuit(
            circuit_id="protein_degradation",
            circuit_type=CircuitType.MEMORY_MANAGER,
            elements=[
                GeneticElement(
                    name="vm1_protease",
                    sequence="ATGAAACGCATCGGCTACGTGCAGGCAATCACC",  # VM1-specific protease
                    element_type="gene",
                    vm_specific=True
                ),
                GeneticElement(
                    name="vm1_deg_tag",
                    sequence="GGTAAATAA",  # Degradation tag for VM1 proteins
                    element_type="tag",
                    vm_specific=True
                ),
                GeneticElement(
                    name="vm2_protease",
                    sequence="ATGAAACGCATCGGCTACGTGCAGGCAATCGCC", # VM2-specific protease
                    element_type="gene", 
                    vm_specific=True
                ),
                GeneticElement(
                    name="vm2_deg_tag",
                    sequence="GGTACATAA",  # Degradation tag for VM2 proteins
                    element_type="tag",
                    vm_specific=True
                )
            ],
            description="VM-specific protein degradation for garbage collection"
        )
        self.circuits["protein_degradation"] = protein_degradation
    
    def get_circuit(self, circuit_id: str) -> Optional[GeneticCircuit]:
        """Get a genetic circuit by ID"""
        return self.circuits.get(circuit_id)
    
    def get_circuits_by_type(self, circuit_type: CircuitType) -> List[GeneticCircuit]:
        """Get all circuits of a specific type"""
        return [circuit for circuit in self.circuits.values() 
                if circuit.circuit_type == circuit_type]
    
    def get_vm_specific_elements(self, vm_id: str) -> List[GeneticElement]:
        """Get all genetic elements specific to a VM"""
        vm_elements = []
        for circuit in self.circuits.values():
            for element in circuit.elements:
                if element.vm_specific and vm_id in element.name:
                    vm_elements.append(element)
        return vm_elements

class OrthogonalGeneticCode:
    """Manages orthogonal genetic codes for VM isolation"""
    
    def __init__(self):
        self.genetic_codes = {
            "vm1": "standard",  # Standard genetic code
            "vm2": "amber_suppression",  # Amber stop codon suppression
            "vm3": "synthetic_aa"  # Modified code with synthetic amino acids
        }
        
        # Orthogonal tRNA/aminoacyl-tRNA synthetase pairs
        self.orthogonal_pairs = {
            "amber_suppression": {
                "trna": "GGGGCCCGCCAGATGATGGATGTTAGGTGGCCTTCTAAACCCCACC",
                "synthetase": "ATGGTGACCCTGAAACAGGCAATCACCAAGATCATC"
            },
            "synthetic_aa": {
                "trna": "GGGGCCCGCCAGATGATGGATGTTAGGTGGCCTTCTAAACCGCACC", 
                "synthetase": "ATGGTGACCCTGAAACAGGCAATCACCAAGATCGTC"
            }
        }
    
    def get_genetic_code(self, vm_id: str) -> str:
        """Get the genetic code used by a VM"""
        return self.genetic_codes.get(vm_id, "standard")
    
    def get_orthogonal_elements(self, vm_id: str) -> Optional[Dict[str, str]]:
        """Get orthogonal tRNA/synthetase pair for a VM"""
        genetic_code = self.get_genetic_code(vm_id)
        if genetic_code in self.orthogonal_pairs:
            return self.orthogonal_pairs[genetic_code]
        return None

class BioCompiler:
    """Compiles high-level hypervisor logic into DNA sequences"""
    
    def __init__(self):
        self.circuit_library = GeneticCircuitLibrary()
        self.genetic_codes = OrthogonalGeneticCode()
    
    def compile_hypervisor(self, vm_configs: List[Dict]) -> Dict[str, str]:
        """
        Compile complete hypervisor DNA sequence
        
        Args:
            vm_configs: List of VM configuration dictionaries
            
        Returns:
            Dictionary mapping sequence names to DNA sequences
        """
        sequences = {}
        
        # Add core hypervisor circuits
        sequences.update(self._compile_core_circuits())
        
        # Add VM-specific circuits
        for vm_config in vm_configs:
            vm_sequences = self._compile_vm_circuits(vm_config)
            sequences.update(vm_sequences)
        
        return sequences
    
    def _compile_core_circuits(self) -> Dict[str, str]:
        """Compile core hypervisor genetic circuits"""
        sequences = {}
        
        # ATP monitor
        atp_circuit = self.circuit_library.get_circuit("atp_monitor")
        sequences["atp_monitor"] = self._assemble_circuit(atp_circuit)
        
        # Ribosome scheduler  
        sched_circuit = self.circuit_library.get_circuit("ribosome_scheduler")
        sequences["ribosome_scheduler"] = self._assemble_circuit(sched_circuit)
        
        return sequences
    
    def _compile_vm_circuits(self, vm_config: Dict) -> Dict[str, str]:
        """Compile circuits for a specific VM"""
        sequences = {}
        vm_id = vm_config.get("vm_id", "vm1")
        
        # Memory isolation
        isolation_circuit = self.circuit_library.get_circuit("memory_isolation") 
        vm_isolation = self._customize_for_vm(isolation_circuit, vm_id)
        sequences[f"{vm_id}_isolation"] = self._assemble_circuit(vm_isolation)
        
        # Protein degradation
        degradation_circuit = self.circuit_library.get_circuit("protein_degradation")
        vm_degradation = self._customize_for_vm(degradation_circuit, vm_id)
        sequences[f"{vm_id}_degradation"] = self._assemble_circuit(vm_degradation)
        
        # Orthogonal genetic elements
        orthogonal_elements = self.genetic_codes.get_orthogonal_elements(vm_id)
        if orthogonal_elements:
            sequences[f"{vm_id}_orthogonal_trna"] = orthogonal_elements["trna"]
            sequences[f"{vm_id}_orthogonal_synthetase"] = orthogonal_elements["synthetase"]
        
        return sequences
    
    def _assemble_circuit(self, circuit: GeneticCircuit) -> str:
        """Assemble genetic elements into a complete circuit sequence"""
        sequence_parts = []
        
        for element in circuit.elements:
            sequence_parts.append(element.sequence)
        
        # Join with standard spacing sequences
        spacer = "GAATTCGAGCTCGGTACCCGGGGATCC"  # Standard cloning spacer
        return spacer.join(sequence_parts)
    
    def _customize_for_vm(self, circuit: GeneticCircuit, vm_id: str) -> GeneticCircuit:
        """Customize a circuit for a specific VM"""
        customized_elements = []
        
        for element in circuit.elements:
            if element.vm_specific and vm_id in element.name:
                customized_elements.append(element)
        
        return GeneticCircuit(
            circuit_id=f"{circuit.circuit_id}_{vm_id}",
            circuit_type=circuit.circuit_type,
            elements=customized_elements,
            description=f"{circuit.description} (customized for {vm_id})"
        )

class ProteinTagging:
    """Manages protein tagging for VM isolation"""
    
    def __init__(self):
        self.vm_tags = {
            "vm1": "MHHHHHHGS",    # His6 tag for VM1
            "vm2": "MYPYDVPDYAGS", # FLAG tag for VM2  
            "vm3": "MGSSHHHHHHSSGLVPRGSHMGS" # Longer composite tag for VM3
        }
        
        self.degradation_signals = {
            "vm1": "AANDENYALAA",  # SsrA-like tag
            "vm2": "AANDENYALAB", 
            "vm3": "AANDENYALAC"
        }
    
    def get_protein_tag(self, vm_id: str) -> str:
        """Get the protein tag sequence for a VM"""
        return self.vm_tags.get(vm_id, "")
    
    def get_degradation_signal(self, vm_id: str) -> str:
        """Get the degradation signal for VM proteins"""
        return self.degradation_signals.get(vm_id, "")
    
    def tag_protein_sequence(self, protein_seq: str, vm_id: str) -> str:
        """Add VM-specific tags to a protein sequence"""
        tag = self.get_protein_tag(vm_id)
        deg_signal = self.get_degradation_signal(vm_id)
        
        # Add N-terminal tag and C-terminal degradation signal
        return tag + protein_seq + deg_signal
