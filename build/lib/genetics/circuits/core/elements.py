"""
Core genetic element definitions for the BioXen circuits system.

This module contains the base classes and types for genetic elements
that make up biological circuits in the hypervisor.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ElementType(Enum):
    """Types of genetic elements"""
    PROMOTER = "promoter"
    RBS = "rbs"
    GENE = "gene"
    TERMINATOR = "terminator"
    SRNA = "sRNA"
    TAG = "tag"
    OPERATOR = "operator"  # Added for modular system compatibility


class CircuitType(Enum):
    """Types of genetic circuits"""
    RESOURCE_MONITOR = "resource_monitor"
    SCHEDULER = "scheduler"
    ISOLATION = "isolation"
    MEMORY_MANAGER = "memory_manager"
    GENE_EXPRESSION = "gene_expression"
    REGULATORY = "regulatory"
    METABOLIC = "metabolic"


@dataclass
class GeneticElement:
    """Represents a genetic element (gene, promoter, RBS, etc.)"""
    element_id: str  # Changed from 'name' to 'element_id' for consistency
    element_type: ElementType
    sequence: str
    vm_specific: bool = False
    regulation_target: Optional[str] = None
    
    # Backward compatibility property
    @property
    def name(self) -> str:
        """Backward compatibility: name property maps to element_id"""
        return self.element_id
    
    @name.setter
    def name(self, value: str):
        """Backward compatibility: setting name updates element_id"""
        self.element_id = value
    
    def __post_init__(self):
        """Validate element after initialization"""
        if isinstance(self.element_type, str):
            # Convert string to ElementType enum for backward compatibility
            self.element_type = ElementType(self.element_type)
    
    def get_length(self) -> int:
        """Get the sequence length of this element"""
        return len(self.sequence)
    
    def is_regulatory(self) -> bool:
        """Check if this element has regulatory function"""
        return self.element_type in [ElementType.PROMOTER, ElementType.SRNA]
    
    def is_coding(self) -> bool:
        """Check if this element codes for a protein"""
        return self.element_type == ElementType.GENE


@dataclass
class GeneticCircuit:
    """A complete genetic circuit"""
    circuit_id: str
    elements: list[GeneticElement]
    circuit_type: Optional[CircuitType] = None
    description: str = ""
    
    def get_total_length(self) -> int:
        """Get the total length of all elements in this circuit"""
        return sum(element.get_length() for element in self.elements)
    
    def get_elements_by_type(self, element_type: ElementType) -> list[GeneticElement]:
        """Get all elements of a specific type from this circuit"""
        return [element for element in self.elements if element.element_type == element_type]
    
    def get_vm_specific_elements(self, vm_id: str) -> list[GeneticElement]:
        """Get all elements specific to a VM"""
        return [element for element in self.elements 
                if element.vm_specific and vm_id in element.element_id]
    
    def has_regulatory_conflicts(self) -> bool:
        """Check for potential regulatory conflicts in the circuit"""
        regulatory_elements = [e for e in self.elements if e.is_regulatory()]
        
        # Simple check: if multiple promoters target the same gene
        targets = {}
        for element in regulatory_elements:
            if element.regulation_target:
                if element.regulation_target not in targets:
                    targets[element.regulation_target] = []
                targets[element.regulation_target].append(element)
        
        # Conflict if same target has multiple promoters
        return any(len(promoters) > 1 for promoters in targets.values())
