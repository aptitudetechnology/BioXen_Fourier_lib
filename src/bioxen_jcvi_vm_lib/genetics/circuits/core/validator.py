"""
Biological constraint validation engine for genetic circuits.

This module provides validation of genetic circuits against biological
constraints and compatibility rules.
"""

from typing import List, Dict, Set, Tuple
import re
from .elements import GeneticCircuit, GeneticElement, ElementType


class ValidationResult:
    """Result of circuit validation"""
    
    def __init__(self):
        self.is_valid = True
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.suggestions: List[str] = []
    
    def add_error(self, message: str):
        """Add a validation error"""
        self.errors.append(message)
        self.is_valid = False
    
    def add_warning(self, message: str):
        """Add a validation warning"""
        self.warnings.append(message)
    
    def add_suggestion(self, message: str):
        """Add a validation suggestion"""
        self.suggestions.append(message)
    
    def __str__(self):
        result = f"Validation Result: {'PASS' if self.is_valid else 'FAIL'}\n"
        
        if self.errors:
            result += f"Errors ({len(self.errors)}):\n"
            for error in self.errors:
                result += f"  - {error}\n"
        
        if self.warnings:
            result += f"Warnings ({len(self.warnings)}):\n"
            for warning in self.warnings:
                result += f"  - {warning}\n"
        
        if self.suggestions:
            result += f"Suggestions ({len(self.suggestions)}):\n"
            for suggestion in self.suggestions:
                result += f"  - {suggestion}\n"
        
        return result


class BioValidator:
    """Validates genetic circuits against biological constraints"""
    
    def __init__(self):
        # Common restriction enzyme sites that should be avoided
        self.restriction_sites = {
            "EcoRI": "GAATTC",
            "BamHI": "GGATCC", 
            "HindIII": "AAGCTT",
            "XhoI": "CTCGAG",
            "SalI": "GTCGAC",
            "NotI": "GCGGCCGC",
            "XbaI": "TCTAGA"
        }
        
        # Problematic sequence motifs
        self.problematic_motifs = {
            "polyA": r"A{8,}",  # Long poly-A tracts
            "polyT": r"T{8,}",  # Long poly-T tracts
            "high_gc": r"[GC]{15,}",  # High GC content regions
            "direct_repeats": r"(.{6,})\1",  # Direct repeats
        }
        
        # Standard genetic code
        self.start_codons = ["ATG", "GTG", "TTG"]
        self.stop_codons = ["TAA", "TAG", "TGA"]
    
    def validate_circuit(self, circuit: GeneticCircuit) -> ValidationResult:
        """Validate a complete genetic circuit"""
        result = ValidationResult()
        
        # Basic circuit validation
        self._validate_circuit_structure(circuit, result)
        
        # Validate individual elements
        for element in circuit.elements:
            self._validate_element(element, result)
        
        # Check for conflicts between elements
        self._validate_element_interactions(circuit, result)
        
        # Check sequence-level issues
        self._validate_circuit_sequence(circuit, result)
        
        return result
    
    def validate_multiple_circuits(self, circuits: List[GeneticCircuit]) -> ValidationResult:
        """Validate multiple circuits for compatibility"""
        result = ValidationResult()
        
        # Validate each circuit individually
        for circuit in circuits:
            circuit_result = self.validate_circuit(circuit)
            result.errors.extend(circuit_result.errors)
            result.warnings.extend(circuit_result.warnings)
            result.suggestions.extend(circuit_result.suggestions)
            
            if not circuit_result.is_valid:
                result.is_valid = False
        
        # Check for cross-circuit conflicts
        self._validate_circuit_compatibility(circuits, result)
        
        return result
    
    def _validate_circuit_structure(self, circuit: GeneticCircuit, result: ValidationResult):
        """Validate the basic structure of a circuit"""
        if not circuit.circuit_id:
            result.add_error("Circuit must have a valid ID")
        
        if not circuit.elements:
            result.add_error("Circuit must contain at least one genetic element")
        
        if not circuit.description:
            result.add_warning("Circuit should have a description")
        
        # Check for required element types based on circuit type
        element_types = {e.element_type for e in circuit.elements}
        
        if circuit.circuit_type.value == "resource_monitor":
            if ElementType.PROMOTER not in element_types:
                result.add_error("Resource monitor circuits must include a promoter")
            if ElementType.GENE not in element_types:
                result.add_error("Resource monitor circuits must include a reporter gene")
        
        elif circuit.circuit_type.value == "scheduler":
            if ElementType.RBS not in element_types:
                result.add_warning("Scheduler circuits typically include RBS elements")
        
        elif circuit.circuit_type.value == "isolation":
            if ElementType.PROMOTER not in element_types or ElementType.GENE not in element_types:
                result.add_warning("Isolation circuits typically include promoters and genes")
    
    def _validate_element(self, element: GeneticElement, result: ValidationResult):
        """Validate an individual genetic element"""
        # Check sequence validity
        if not element.sequence:
            result.add_error(f"Element '{element.element_id}' has empty sequence")
            return
        
        # Check for valid DNA sequence
        if not self._is_valid_dna_sequence(element.sequence):
            result.add_error(f"Element '{element.element_id}' contains invalid DNA characters")
        
        # Element-specific validation
        if element.element_type == ElementType.GENE:
            self._validate_gene_element(element, result)
        elif element.element_type == ElementType.PROMOTER:
            self._validate_promoter_element(element, result)
        elif element.element_type == ElementType.RBS:
            self._validate_rbs_element(element, result)
        
        # Check for restriction sites
        self._check_restriction_sites(element, result)
        
        # Check for problematic motifs
        self._check_problematic_motifs(element, result)
    
    def _validate_gene_element(self, element: GeneticElement, result: ValidationResult):
        """Validate a gene element"""
        sequence = element.sequence.upper()
        
        # Check length is multiple of 3
        if len(sequence) % 3 != 0:
            result.add_warning(f"Gene '{element.element_id}' length is not a multiple of 3")
        
        # Check for start codon
        if len(sequence) >= 3:
            start_codon = sequence[:3]
            if start_codon not in self.start_codons:
                result.add_warning(f"Gene '{element.element_id}' does not start with a start codon")
        
        # Check for premature stop codons
        if len(sequence) >= 6:  # At least 2 codons
            for i in range(3, len(sequence) - 3, 3):
                codon = sequence[i:i+3]
                if codon in self.stop_codons:
                    result.add_warning(f"Gene '{element.element_id}' contains premature stop codon at position {i}")
                    break
        
        # Check for proper stop codon at end
        if len(sequence) >= 3:
            end_codon = sequence[-3:]
            if end_codon not in self.stop_codons:
                result.add_warning(f"Gene '{element.element_id}' does not end with a stop codon")
    
    def _validate_promoter_element(self, element: GeneticElement, result: ValidationResult):
        """Validate a promoter element"""
        sequence = element.sequence.upper()
        
        # Check reasonable length
        if len(sequence) < 10:
            result.add_warning(f"Promoter '{element.element_id}' is very short ({len(sequence)} bp)")
        elif len(sequence) > 200:
            result.add_warning(f"Promoter '{element.element_id}' is very long ({len(sequence)} bp)")
        
        # Check for common promoter motifs (simplified)
        if "TATA" not in sequence and "TTGACA" not in sequence:
            result.add_suggestion(f"Promoter '{element.element_id}' may lack common recognition motifs")
    
    def _validate_rbs_element(self, element: GeneticElement, result: ValidationResult):
        """Validate a ribosome binding site element"""
        sequence = element.sequence.upper()
        
        # Check reasonable length
        if len(sequence) < 8:
            result.add_warning(f"RBS '{element.element_id}' is very short ({len(sequence)} bp)")
        elif len(sequence) > 30:
            result.add_warning(f"RBS '{element.element_id}' is very long ({len(sequence)} bp)")
        
        # Check for Shine-Dalgarno sequence
        if "AGGAGG" not in sequence and "GGAGG" not in sequence:
            result.add_warning(f"RBS '{element.element_id}' may lack Shine-Dalgarno sequence")
    
    def _validate_element_interactions(self, circuit: GeneticCircuit, result: ValidationResult):
        """Validate interactions between elements in a circuit"""
        # Check for regulatory conflicts
        regulatory_targets = {}
        for element in circuit.elements:
            if element.regulation_target:
                if element.regulation_target not in regulatory_targets:
                    regulatory_targets[element.regulation_target] = []
                regulatory_targets[element.regulation_target].append(element)
        
        # Warn about multiple regulators for same target
        for target, regulators in regulatory_targets.items():
            if len(regulators) > 1:
                regulator_names = [r.name for r in regulators]
                result.add_warning(f"Target '{target}' has multiple regulators: {regulator_names}")
        
        # Check for orphaned regulatory elements
        target_names = {e.name for e in circuit.elements}
        for element in circuit.elements:
            if element.regulation_target and element.regulation_target not in target_names:
                result.add_warning(f"Element '{element.element_id}' targets '{element.regulation_target}' which is not in the circuit")
    
    def _validate_circuit_sequence(self, circuit: GeneticCircuit, result: ValidationResult):
        """Validate the complete assembled circuit sequence"""
        # This would validate the complete assembled sequence
        total_length = sum(len(e.sequence) for e in circuit.elements)
        
        if total_length > 50000:  # 50kb limit
            result.add_warning(f"Circuit is very large ({total_length} bp)")
        
        # Check GC content
        all_sequences = "".join(e.sequence for e in circuit.elements)
        gc_content = self._calculate_gc_content(all_sequences)
        
        if gc_content < 0.3 or gc_content > 0.7:
            result.add_warning(f"Circuit GC content is {gc_content:.2%} (outside optimal 30-70% range)")
    
    def _validate_circuit_compatibility(self, circuits: List[GeneticCircuit], result: ValidationResult):
        """Validate compatibility between multiple circuits"""
        # Check for naming conflicts
        all_element_names = []
        for circuit in circuits:
            for element in circuit.elements:
                all_element_names.append((element.element_id, circuit.circuit_id))
        
        name_counts = {}
        for name, circuit_id in all_element_names:
            if name not in name_counts:
                name_counts[name] = []
            name_counts[name].append(circuit_id)
        
        for name, circuit_ids in name_counts.items():
            if len(circuit_ids) > 1:
                result.add_warning(f"Element name '{name}' is used in multiple circuits: {circuit_ids}")
    
    def _is_valid_dna_sequence(self, sequence: str) -> bool:
        """Check if sequence contains only valid DNA characters"""
        return bool(re.match(r'^[ATGCatgc]*$', sequence))
    
    def _calculate_gc_content(self, sequence: str) -> float:
        """Calculate GC content of a sequence"""
        if not sequence:
            return 0.0
        
        sequence = sequence.upper()
        gc_count = sequence.count('G') + sequence.count('C')
        return gc_count / len(sequence)
    
    def _check_restriction_sites(self, element: GeneticElement, result: ValidationResult):
        """Check for unwanted restriction sites"""
        sequence = element.sequence.upper()
        
        for enzyme, site in self.restriction_sites.items():
            if site in sequence:
                result.add_warning(f"Element '{element.element_id}' contains {enzyme} site ({site})")
    
    def _check_problematic_motifs(self, element: GeneticElement, result: ValidationResult):
        """Check for problematic sequence motifs"""
        sequence = element.sequence.upper()
        
        for motif_name, pattern in self.problematic_motifs.items():
            if re.search(pattern, sequence):
                result.add_warning(f"Element '{element.element_id}' contains {motif_name} motif")


# Additional classes and enums required by the modular system
from enum import Enum
from dataclasses import dataclass


class IssueSeverity(Enum):
    """Severity levels for validation issues"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class ValidationIssue:
    """Represents a validation issue"""
    severity: IssueSeverity
    message: str
    element_id: str = None
    suggestion: str = None


class CircuitValidator:
    """Main circuit validator class with enhanced functionality"""
    
    def __init__(self):
        self.bio_validator = BioValidator()
        self.issues: List[ValidationIssue] = []
    
    def validate_circuit(self, circuit: GeneticCircuit) -> ValidationResult:
        """Validate a circuit using comprehensive rules"""
        self.issues = []
        
        # Use the existing bio validator
        result = self.bio_validator.validate_circuit(circuit)
        
        # Convert warnings and errors to ValidationIssue format
        for warning in result.warnings:
            self.issues.append(ValidationIssue(
                severity=IssueSeverity.WARNING,
                message=warning
            ))
        
        for error in result.errors:
            self.issues.append(ValidationIssue(
                severity=IssueSeverity.ERROR,
                message=error
            ))
        
        # Add additional modular system validations
        self._validate_modular_compatibility(circuit, result)
        
        return result
    
    def _validate_modular_compatibility(self, circuit: GeneticCircuit, result: ValidationResult):
        """Validate compatibility with modular system requirements"""
        
        # Check that all elements have proper IDs
        for element in circuit.elements:
            if not element.element_id or element.element_id.strip() == "":
                result.add_error(f"Element missing valid element_id")
                self.issues.append(ValidationIssue(
                    severity=IssueSeverity.ERROR,
                    message="Element missing valid element_id",
                    element_id=str(element)
                ))
        
        # Check for duplicate element IDs
        element_ids = [e.element_id for e in circuit.elements if e.element_id]
        duplicate_ids = set([x for x in element_ids if element_ids.count(x) > 1])
        
        for dup_id in duplicate_ids:
            result.add_error(f"Duplicate element ID: {dup_id}")
            self.issues.append(ValidationIssue(
                severity=IssueSeverity.ERROR,
                message=f"Duplicate element ID: {dup_id}",
                element_id=dup_id
            ))
    
    def get_issues_by_severity(self, severity: IssueSeverity) -> List[ValidationIssue]:
        """Get issues filtered by severity"""
        return [issue for issue in self.issues if issue.severity == severity]


# Standalone validation functions for convenience
def validate_circuit_basic(circuit: GeneticCircuit) -> ValidationResult:
    """Perform basic circuit validation"""
    validator = BioValidator()
    return validator.validate_circuit(circuit)


def validate_circuit_advanced(circuit: GeneticCircuit) -> ValidationResult:
    """Perform advanced circuit validation with modular system compatibility"""
    validator = CircuitValidator()
    return validator.validate_circuit(circuit)
