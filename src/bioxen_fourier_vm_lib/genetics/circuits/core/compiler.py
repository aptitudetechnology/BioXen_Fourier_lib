"""
Advanced BioCompiler for genetic circuit compilation and DNA sequence generation.

This module contains the main BioCompiler class that handles the conversion
of high-level circuit definitions into actual DNA sequences.
"""

from typing import Dict, List, Optional
import random
import re
from dataclasses import dataclass
from enum import Enum
from .elements import GeneticCircuit, GeneticElement, CircuitType, ElementType


class OptimizationLevel(Enum):
    """Optimization levels for DNA compilation"""
    NONE = "none"
    BASIC = "basic"
    AGGRESSIVE = "aggressive"


@dataclass
class CompilationConfig:
    """Configuration for circuit compilation"""
    optimization_level: OptimizationLevel = OptimizationLevel.BASIC
    target_organism: str = "ecoli"
    codon_optimize: bool = True
    remove_restriction_sites: bool = True
    add_assembly_flanks: bool = False
    flanking_sequence_length: int = 40
    gc_content_target: float = 0.5
    avoid_hairpins: bool = True
    max_homology_length: int = 20


@dataclass 
class CompilationResult:
    """Result of circuit compilation"""
    compiled_sequence: str
    optimization_log: List[str]
    warnings: List[str] 
    assembly_ready: bool
    gc_content: float
    restriction_sites_removed: int
    codon_optimization_applied: bool


class BioCompiler:
    """Compiles high-level hypervisor logic into DNA sequences"""
    
    def __init__(self):
        self.genetic_codes = OrthogonalGeneticCode()
        self.spacer_sequence = "GAATTCGAGCTCGGTACCCGGGGATCC"  # Standard cloning spacer
        self.restriction_sites = [
            "GAATTC",  # EcoRI
            "GGATCC",  # BamHI
            "AAGCTT",  # HindIII
            "CTCGAG",  # XhoI
            "GTCGAC",  # SalI
        ]
    
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
        from ..library.monitors import get_atp_monitor_circuit
        from ..library.schedulers import get_ribosome_scheduler_circuit
        
        sequences = {}
        
        # ATP monitor
        atp_circuit = get_atp_monitor_circuit()
        sequences["atp_monitor"] = self._assemble_circuit(atp_circuit)
        
        # Ribosome scheduler
        sched_circuit = get_ribosome_scheduler_circuit()
        sequences["ribosome_scheduler"] = self._assemble_circuit(sched_circuit)
        
        return sequences
    
    def _compile_vm_circuits(self, vm_config: Dict) -> Dict[str, str]:
        """Compile circuits for a specific VM"""
        from ..library.isolation import get_memory_isolation_circuit
        from ..library.memory import get_protein_degradation_circuit
        
        sequences = {}
        vm_id = vm_config.get("vm_id", "vm1")
        
        # Memory isolation
        isolation_circuit = get_memory_isolation_circuit()
        vm_isolation = self._customize_for_vm(isolation_circuit, vm_id)
        sequences[f"{vm_id}_isolation"] = self._assemble_circuit(vm_isolation)
        
        # Protein degradation
        degradation_circuit = get_protein_degradation_circuit()
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
        
        # Join with spacer sequences
        return self.spacer_sequence.join(sequence_parts)
    
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
    
    def optimize_codons(self, sequence: str, organism: str = "ecoli") -> str:
        """Optimize codon usage for the target organism"""
        # Simplified codon optimization
        codon_tables = {
            "ecoli": {
                "TTT": "TTC",  # Phe: TTT -> TTC (more frequent)
                "TTA": "CTG",  # Leu: TTA -> CTG (more frequent)
                "CTA": "CTG",  # Leu: CTA -> CTG
                # Add more optimizations as needed
            }
        }
        
        if organism not in codon_tables:
            return sequence
        
        optimized = sequence
        for old_codon, new_codon in codon_tables[organism].items():
            optimized = optimized.replace(old_codon, new_codon)
        
        return optimized
    
    def add_spacers(self, sequences: List[str], spacer_type: str = "standard") -> str:
        """Add appropriate spacer sequences between genetic elements"""
        spacers = {
            "standard": self.spacer_sequence,
            "minimal": "GAATTC",
            "biobrick": "GAATTCGCGGCCGCTTCTAG",
        }
        
        spacer = spacers.get(spacer_type, self.spacer_sequence)
        return spacer.join(sequences)
    
    def check_restriction_sites(self, sequence: str) -> List[str]:
        """Check for unwanted restriction sites in the sequence"""
        found_sites = []
        
        for site in self.restriction_sites:
            if site in sequence:
                found_sites.append(site)
        
        return found_sites
    
    def remove_restriction_sites(self, sequence: str) -> str:
        """Remove restriction sites while preserving amino acid sequence"""
        # This is a simplified implementation
        # In practice, this would require careful codon substitution
        for site in self.restriction_sites:
            if site in sequence:
                # Simple substitution (would need more sophisticated logic)
                sequence = sequence.replace(site, site[:-1] + "A")
        
        return sequence


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
