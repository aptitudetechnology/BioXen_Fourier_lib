"""
Biological constraints validation for genetic circuits.

This module provides comprehensive validation of genetic circuits against
known biological constraints, regulatory requirements, and compatibility rules.
"""

import re
from typing import List, Dict, Set, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
from ..core.elements import GeneticCircuit, GeneticElement, ElementType


class ConstraintSeverity(Enum):
    """Severity levels for constraint violations"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class ConstraintViolation:
    """Represents a biological constraint violation"""
    constraint_name: str
    severity: ConstraintSeverity
    element_id: Optional[str]
    description: str
    suggestion: Optional[str] = None
    position: Optional[int] = None


@dataclass
class ValidationResult:
    """Result of biological constraints validation"""
    is_valid: bool
    violations: List[ConstraintViolation]
    warnings_count: int
    errors_count: int
    critical_count: int


class BiologicalConstraintsValidator:
    """Validates genetic circuits against biological constraints"""
    
    def __init__(self, chassis: str = "ecoli"):
        self.chassis = chassis
        self._load_chassis_constraints()
        
        # Common restriction enzyme sites to avoid
        self.restriction_sites = {
            "EcoRI": "GAATTC",
            "BamHI": "GGATCC", 
            "HindIII": "AAGCTT",
            "XhoI": "CTCGAG",
            "SalI": "GTCGAC",
            "NotI": "GCGGCCGC",
            "XbaI": "TCTAGA",
            "SpeI": "ACTAGT",
            "PstI": "CTGCAG",
            "KpnI": "GGTACC"
        }
        
        # Regulatory sequences that might cause issues
        self.problematic_sequences = {
            "T7_terminator": "GCCTGCAGGTCGAC",
            "lac_operator": "AATTGTGAGCGGATAA",
            "trp_operator": "ACTGTTGACAAT",
            "ara_operator": "GACAGCTATCGCGATTGC"
        }
    
    def _load_chassis_constraints(self):
        """Load chassis-specific biological constraints"""
        if self.chassis == "ecoli":
            self.gc_content_range = (0.45, 0.55)  # E. coli optimal GC content
            self.max_gene_length = 15000  # bp
            self.min_promoter_strength = 0.1
            self.codon_usage_table = self._get_ecoli_codon_usage()
            self.forbidden_motifs = ["GATC", "CCWGG"]  # Dam and Dcm sites
            
        elif self.chassis == "yeast":
            self.gc_content_range = (0.35, 0.45)  # S. cerevisiae GC content
            self.max_gene_length = 20000  # bp
            self.min_promoter_strength = 0.05
            self.codon_usage_table = self._get_yeast_codon_usage()
            self.forbidden_motifs = ["CGATCG"]  # PvuI site
            
        else:  # Generic constraints
            self.gc_content_range = (0.30, 0.70)
            self.max_gene_length = 25000
            self.min_promoter_strength = 0.01
            self.codon_usage_table = {}
            self.forbidden_motifs = []
    
    def validate_circuit(self, circuit: GeneticCircuit) -> ValidationResult:
        """Perform comprehensive validation of a genetic circuit"""
        violations = []
        
        # Structure validation
        violations.extend(self._validate_circuit_structure(circuit))
        
        # Sequence validation
        violations.extend(self._validate_sequences(circuit))
        
        # Regulatory validation
        violations.extend(self._validate_regulatory_elements(circuit))
        
        # Biological compatibility validation
        violations.extend(self._validate_biological_compatibility(circuit))
        
        # Chassis-specific validation
        violations.extend(self._validate_chassis_compatibility(circuit))
        
        # Count violations by severity
        warnings_count = len([v for v in violations if v.severity == ConstraintSeverity.WARNING])
        errors_count = len([v for v in violations if v.severity == ConstraintSeverity.ERROR])
        critical_count = len([v for v in violations if v.severity == ConstraintSeverity.CRITICAL])
        
        is_valid = critical_count == 0 and errors_count == 0
        
        return ValidationResult(
            is_valid=is_valid,
            violations=violations,
            warnings_count=warnings_count,
            errors_count=errors_count,
            critical_count=critical_count
        )
    
    def _validate_circuit_structure(self, circuit: GeneticCircuit) -> List[ConstraintViolation]:
        """Validate basic circuit structure"""
        violations = []
        
        # Check for empty circuit
        if not circuit.elements:
            violations.append(ConstraintViolation(
                constraint_name="empty_circuit",
                severity=ConstraintSeverity.CRITICAL,
                element_id=None,
                description="Circuit contains no genetic elements",
                suggestion="Add at least one genetic element to the circuit"
            ))
            return violations
        
        # Check for required elements
        element_types = {e.element_type for e in circuit.elements}
        
        # Every circuit should have at least one gene
        if ElementType.GENE not in element_types:
            violations.append(ConstraintViolation(
                constraint_name="no_genes",
                severity=ConstraintSeverity.WARNING,
                element_id=None,
                description="Circuit contains no genes",
                suggestion="Consider adding at least one gene to provide functionality"
            ))
        
        # Check element order and relationships
        violations.extend(self._validate_element_order(circuit))
        
        return violations
    
    def _validate_element_order(self, circuit: GeneticCircuit) -> List[ConstraintViolation]:
        """Validate the order and relationships of elements"""
        violations = []
        
        for i, element in enumerate(circuit.elements):
            # Promoters should precede genes
            if element.element_type == ElementType.GENE and i > 0:
                prev_element = circuit.elements[i-1]
                if prev_element.element_type != ElementType.PROMOTER:
                    violations.append(ConstraintViolation(
                        constraint_name="gene_without_promoter",
                        severity=ConstraintSeverity.WARNING,
                        element_id=element.element_id,
                        description=f"Gene {element.element_id} not preceded by a promoter",
                        suggestion="Add a promoter before this gene for proper expression"
                    ))
            
            # Terminators should follow genes
            if (element.element_type == ElementType.GENE and 
                i < len(circuit.elements) - 1):
                next_element = circuit.elements[i+1]
                if next_element.element_type != ElementType.TERMINATOR:
                    violations.append(ConstraintViolation(
                        constraint_name="gene_without_terminator",
                        severity=ConstraintSeverity.WARNING,
                        element_id=element.element_id,
                        description=f"Gene {element.element_id} not followed by a terminator",
                        suggestion="Add a terminator after this gene to prevent read-through"
                    ))
        
        return violations
    
    def _validate_sequences(self, circuit: GeneticCircuit) -> List[ConstraintViolation]:
        """Validate DNA sequences for common issues"""
        violations = []
        
        for element in circuit.elements:
            # Check sequence validity
            if not element.sequence:
                violations.append(ConstraintViolation(
                    constraint_name="empty_sequence",
                    severity=ConstraintSeverity.CRITICAL,
                    element_id=element.element_id,
                    description=f"Element {element.element_id} has empty sequence"
                ))
                continue
            
            # Check for valid DNA bases
            if not re.match(r'^[ATGCRYSWKMBDHVN]*$', element.sequence.upper()):
                violations.append(ConstraintViolation(
                    constraint_name="invalid_dna_sequence",
                    severity=ConstraintSeverity.ERROR,
                    element_id=element.element_id,
                    description=f"Element {element.element_id} contains invalid DNA characters"
                ))
            
            # Check sequence length
            violations.extend(self._validate_sequence_length(element))
            
            # Check GC content
            violations.extend(self._validate_gc_content(element))
            
            # Check for restriction sites
            violations.extend(self._validate_restriction_sites(element))
            
            # Check for problematic sequences
            violations.extend(self._validate_problematic_sequences(element))
        
        return violations
    
    def _validate_sequence_length(self, element: GeneticElement) -> List[ConstraintViolation]:
        """Validate sequence length for element type"""
        violations = []
        length = len(element.sequence)
        
        if element.element_type == ElementType.GENE:
            if length > self.max_gene_length:
                violations.append(ConstraintViolation(
                    constraint_name="gene_too_long",
                    severity=ConstraintSeverity.WARNING,
                    element_id=element.element_id,
                    description=f"Gene {element.element_id} is {length} bp, "
                               f"exceeds recommended maximum of {self.max_gene_length} bp"
                ))
            
            if length % 3 != 0:
                violations.append(ConstraintViolation(
                    constraint_name="gene_not_multiple_of_3",
                    severity=ConstraintSeverity.ERROR,
                    element_id=element.element_id,
                    description=f"Gene {element.element_id} length ({length} bp) "
                               "is not a multiple of 3",
                    suggestion="Adjust gene length to maintain reading frame"
                ))
        
        elif element.element_type == ElementType.PROMOTER:
            if length < 20:
                violations.append(ConstraintViolation(
                    constraint_name="promoter_too_short",
                    severity=ConstraintSeverity.WARNING,
                    element_id=element.element_id,
                    description=f"Promoter {element.element_id} is only {length} bp, "
                               "may be too short for effective regulation"
                ))
        
        return violations
    
    def _validate_gc_content(self, element: GeneticElement) -> List[ConstraintViolation]:
        """Validate GC content of sequences"""
        violations = []
        sequence = element.sequence.upper()
        
        if len(sequence) == 0:
            return violations
        
        gc_count = sequence.count('G') + sequence.count('C')
        gc_content = gc_count / len(sequence)
        
        min_gc, max_gc = self.gc_content_range
        
        if gc_content < min_gc or gc_content > max_gc:
            severity = ConstraintSeverity.WARNING
            if gc_content < 0.2 or gc_content > 0.8:
                severity = ConstraintSeverity.ERROR
            
            violations.append(ConstraintViolation(
                constraint_name="gc_content_out_of_range",
                severity=severity,
                element_id=element.element_id,
                description=f"Element {element.element_id} has GC content of {gc_content:.1%}, "
                           f"outside optimal range of {min_gc:.1%}-{max_gc:.1%}",
                suggestion="Consider codon optimization or sequence modification"
            ))
        
        return violations
    
    def _validate_restriction_sites(self, element: GeneticElement) -> List[ConstraintViolation]:
        """Check for restriction enzyme sites"""
        violations = []
        sequence = element.sequence.upper()
        
        for enzyme, site in self.restriction_sites.items():
            if site in sequence:
                violations.append(ConstraintViolation(
                    constraint_name="restriction_site_present",
                    severity=ConstraintSeverity.WARNING,
                    element_id=element.element_id,
                    description=f"Element {element.element_id} contains {enzyme} site ({site})",
                    suggestion=f"Consider modifying sequence to remove {enzyme} site for easier cloning"
                ))
        
        return violations
    
    def _validate_problematic_sequences(self, element: GeneticElement) -> List[ConstraintViolation]:
        """Check for known problematic sequences"""
        violations = []
        sequence = element.sequence.upper()
        
        for name, motif in self.problematic_sequences.items():
            if motif.upper() in sequence:
                violations.append(ConstraintViolation(
                    constraint_name="problematic_sequence",
                    severity=ConstraintSeverity.WARNING,
                    element_id=element.element_id,
                    description=f"Element {element.element_id} contains {name} sequence",
                    suggestion="Consider modifying sequence to avoid regulatory interference"
                ))
        
        # Check for forbidden motifs specific to chassis
        for motif in self.forbidden_motifs:
            if motif.upper() in sequence:
                violations.append(ConstraintViolation(
                    constraint_name="forbidden_motif",
                    severity=ConstraintSeverity.ERROR,
                    element_id=element.element_id,
                    description=f"Element {element.element_id} contains forbidden motif {motif}",
                    suggestion="Remove or modify the forbidden sequence motif"
                ))
        
        return violations
    
    def _validate_regulatory_elements(self, circuit: GeneticCircuit) -> List[ConstraintViolation]:
        """Validate regulatory relationships and conflicts"""
        violations = []
        
        # Check for regulatory conflicts
        regulatory_targets = {}
        for element in circuit.elements:
            if element.regulation_target:
                if element.regulation_target not in regulatory_targets:
                    regulatory_targets[element.regulation_target] = []
                regulatory_targets[element.regulation_target].append(element)
        
        for target, regulators in regulatory_targets.items():
            if len(regulators) > 1:
                regulator_ids = [r.element_id for r in regulators]
                violations.append(ConstraintViolation(
                    constraint_name="multiple_regulators",
                    severity=ConstraintSeverity.WARNING,
                    element_id=target,
                    description=f"Target {target} has multiple regulators: {regulator_ids}",
                    suggestion="Consider combining regulatory logic or using different targets"
                ))
        
        return violations
    
    def _validate_biological_compatibility(self, circuit: GeneticCircuit) -> List[ConstraintViolation]:
        """Validate biological compatibility and feasibility"""
        violations = []
        
        # Check for excessive metabolic burden
        gene_count = len([e for e in circuit.elements if e.element_type == ElementType.GENE])
        if gene_count > 10:
            violations.append(ConstraintViolation(
                constraint_name="high_metabolic_burden",
                severity=ConstraintSeverity.WARNING,
                element_id=None,
                description=f"Circuit contains {gene_count} genes, may cause high metabolic burden",
                suggestion="Consider splitting into multiple circuits or optimizing expression levels"
            ))
        
        # Check circuit complexity
        total_length = sum(len(e.sequence) for e in circuit.elements)
        if total_length > 50000:  # 50 kb
            violations.append(ConstraintViolation(
                constraint_name="circuit_too_large",
                severity=ConstraintSeverity.WARNING,
                element_id=None,
                description=f"Circuit is {total_length} bp, may be difficult to construct",
                suggestion="Consider modularizing the circuit or using chromosomal integration"
            ))
        
        return violations
    
    def _validate_chassis_compatibility(self, circuit: GeneticCircuit) -> List[ConstraintViolation]:
        """Validate compatibility with specific chassis organism"""
        violations = []
        
        # Chassis-specific validations would be implemented here
        # For now, implement basic codon usage validation
        if self.codon_usage_table:
            violations.extend(self._validate_codon_usage(circuit))
        
        return violations
    
    def _validate_codon_usage(self, circuit: GeneticCircuit) -> List[ConstraintViolation]:
        """Validate codon usage for chassis optimization"""
        violations = []
        
        for element in circuit.elements:
            if element.element_type == ElementType.GENE:
                # Basic codon usage check (simplified)
                sequence = element.sequence.upper()
                if len(sequence) >= 3:
                    # Count rare codons (simplified check)
                    rare_codon_count = 0
                    for i in range(0, len(sequence) - 2, 3):
                        codon = sequence[i:i+3]
                        if codon in ['CGA', 'CGG', 'AGA', 'AGG']:  # Rare arginine codons in E. coli
                            rare_codon_count += 1
                    
                    if rare_codon_count > len(sequence) // 30:  # More than ~3% rare codons
                        violations.append(ConstraintViolation(
                            constraint_name="rare_codon_usage",
                            severity=ConstraintSeverity.WARNING,
                            element_id=element.element_id,
                            description=f"Gene {element.element_id} uses {rare_codon_count} rare codons",
                            suggestion="Consider codon optimization for better expression"
                        ))
        
        return violations
    
    def _get_ecoli_codon_usage(self) -> Dict[str, float]:
        """Get E. coli codon usage frequencies (simplified)"""
        return {
            'TTT': 0.58, 'TTC': 0.42,  # Phe
            'TTA': 0.14, 'TTG': 0.13, 'CTT': 0.12, 'CTC': 0.10, 'CTA': 0.04, 'CTG': 0.47,  # Leu
            # ... (would include full codon table)
        }
    
    def _get_yeast_codon_usage(self) -> Dict[str, float]:
        """Get S. cerevisiae codon usage frequencies (simplified)"""
        return {
            'TTT': 0.59, 'TTC': 0.41,  # Phe
            'TTA': 0.28, 'TTG': 0.29, 'CTT': 0.13, 'CTC': 0.06, 'CTA': 0.14, 'CTG': 0.11,  # Leu
            # ... (would include full codon table)
        }


def validate_circuit_compatibility(circuit1: GeneticCircuit, 
                                 circuit2: GeneticCircuit) -> List[ConstraintViolation]:
    """Validate compatibility between two circuits"""
    violations = []
    
    # Check for conflicting regulation
    targets1 = {e.regulation_target for e in circuit1.elements if e.regulation_target}
    targets2 = {e.regulation_target for e in circuit2.elements if e.regulation_target}
    
    conflicting_targets = targets1.intersection(targets2)
    for target in conflicting_targets:
        violations.append(ConstraintViolation(
            constraint_name="circuit_regulatory_conflict",
            severity=ConstraintSeverity.WARNING,
            element_id=target,
            description=f"Both circuits regulate target {target}",
            suggestion="Consider using different regulatory targets or combining circuits"
        ))
    
    return violations


def batch_validate_circuits(circuits: List[GeneticCircuit], 
                          chassis: str = "ecoli") -> Dict[str, ValidationResult]:
    """Validate multiple circuits and return results"""
    validator = BiologicalConstraintsValidator(chassis)
    results = {}
    
    for circuit in circuits:
        results[circuit.circuit_id] = validator.validate_circuit(circuit)
    
    return results
