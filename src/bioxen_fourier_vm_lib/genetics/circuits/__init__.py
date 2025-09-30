"""
Modular genetic circuits system for BioXen hypervisor.

This module provides the core genetic circuit functionality including
element definitions, circuit compilation, specialized circuit libraries,
optimization algorithms, and export capabilities.
"""

# Core circuit functionality
from .core.elements import (
    ElementType,
    GeneticElement,
    GeneticCircuit
)

from .core.compiler import (
    BioCompiler,
    CompilationConfig,
    CompilationResult
)

from .core.factory import (
    CircuitFactory,
    create_gene_expression_circuit,
    create_regulatory_circuit,
    create_metabolic_circuit
)

from .core.validator import (
    CircuitValidator,
    ValidationIssue,
    IssueSeverity,
    validate_circuit_basic,
    validate_circuit_advanced
)

# Circuit library
from .library.monitors import (
    create_atp_monitor,
    create_ph_monitor,
    create_temperature_monitor,
    create_resource_monitor
)

from .library.schedulers import (
    create_round_robin_scheduler,
    create_priority_scheduler,
    create_resource_aware_scheduler
)

from .library.isolation import (
    create_vm_isolation_circuit,
    create_namespace_circuit,
    create_security_circuit
)

from .library.memory import (
    create_memory_allocator,
    create_garbage_collector,
    create_heap_manager
)

# Optimization
from .optimization import (
    GeneticAlgorithmOptimizer,
    CircuitFitnessEvaluator,
    OptimizationResult,
    BiologicalConstraintsValidator,
    ConstraintViolation,
    ConstraintSeverity,
    ValidationResult,
    optimize_and_validate_circuit,
    get_optimization_recommendations
)

# Exports
from .exports import (
    JCVIFormatExporter,
    JCVIFeature,
    JCVIAnnotation,
    JCVIGenomeRecord,
    export_multiple_circuits_to_jcvi,
    create_jcvi_assembly_script,
    export_circuit_complete,
    get_export_formats,
    validate_export_requirements,
    HAS_VISUALIZATION
)

# Visualization (if available)
from .exports import (
    CircuitVisualizer,
    VisualizationStyle,
    create_circuit_gallery,
    export_circuit_visualization_report
)

__all__ = [
    # Core Elements
    "ElementType",
    "GeneticElement", 
    "GeneticCircuit",
    
    # Compilation
    "BioCompiler",
    "CompilationConfig",
    "CompilationResult",
    
    # Factory
    "CircuitFactory",
    "create_gene_expression_circuit",
    "create_regulatory_circuit", 
    "create_metabolic_circuit",
    
    # Validation
    "CircuitValidator",
    "ValidationIssue",
    "IssueSeverity",
    "validate_circuit_basic",
    "validate_circuit_advanced",
    
    # Library - Monitors
    "create_atp_monitor",
    "create_ph_monitor",
    "create_temperature_monitor", 
    "create_resource_monitor",
    
    # Library - Schedulers
    "create_round_robin_scheduler",
    "create_priority_scheduler",
    "create_resource_aware_scheduler",
    
    # Library - Isolation
    "create_vm_isolation_circuit",
    "create_namespace_circuit",
    "create_security_circuit",
    
    # Library - Memory
    "create_memory_allocator",
    "create_garbage_collector",
    "create_heap_manager",
    
    # Optimization
    "GeneticAlgorithmOptimizer",
    "CircuitFitnessEvaluator",
    "OptimizationResult",
    "BiologicalConstraintsValidator",
    "ConstraintViolation",
    "ConstraintSeverity",
    "ValidationResult",
    "optimize_and_validate_circuit",
    "get_optimization_recommendations",
    
    # Exports
    "JCVIFormatExporter",
    "JCVIFeature",
    "JCVIAnnotation", 
    "JCVIGenomeRecord",
    "export_multiple_circuits_to_jcvi",
    "create_jcvi_assembly_script",
    "export_circuit_complete",
    "get_export_formats",
    "validate_export_requirements",
    "HAS_VISUALIZATION",
    
    # Visualization
    "CircuitVisualizer",
    "VisualizationStyle",
    "create_circuit_gallery",
    "export_circuit_visualization_report"
]


def get_modular_circuits_info():
    """Get information about the modular circuits system"""
    return {
        "version": "1.0.0",
        "modules": {
            "core": "Base genetic elements, compilation, factory, validation",
            "library": "Specialized circuits for monitors, schedulers, isolation, memory",
            "optimization": "Genetic algorithms and biological constraints validation", 
            "exports": "JCVI-compatible format export and visualization tools"
        },
        "features": {
            "genetic_elements": "Type-safe genetic element definitions",
            "biocompiler": "Advanced DNA sequence compilation with optimization",
            "circuit_factory": "Dynamic circuit generation with templates",
            "validation": "Comprehensive biological constraints checking",
            "optimization": "Evolutionary algorithm optimization",
            "jcvi_export": "Full JCVI toolkit compatibility",
            "visualization": f"Circuit visualization {'available' if HAS_VISUALIZATION else 'requires matplotlib'}"
        },
        "compatibility": {
            "jcvi_formats": ["GenBank", "GFF3", "FASTA", "AGP", "Feature Table", "JSON"],
            "assembly_tools": ["JCVI assembly pipeline", "Custom assembly scripts"],
            "visualization": HAS_VISUALIZATION
        }
    }


def create_demo_circuit():
    """Create a demonstration circuit showing modular capabilities"""
    from .core.elements import GeneticElement, ElementType, GeneticCircuit
    
    # Create elements using the modular system
    elements = [
        GeneticElement(
            element_id="demo_promoter",
            element_type=ElementType.PROMOTER,
            sequence="TTGACAGCTAGCTCAGTCCTAGGTATAATGCTAGC"
        ),
        GeneticElement(
            element_id="demo_rbs",
            element_type=ElementType.RBS,
            sequence="AAGGAGGTGATCCATG"
        ),
        GeneticElement(
            element_id="demo_gene",
            element_type=ElementType.GENE,
            sequence="ATGAAAGCCATTTTGGCAGTAGCGGCGATCGGCACAGGCATTTATGCGTGA"
        ),
        GeneticElement(
            element_id="demo_terminator",
            element_type=ElementType.TERMINATOR,
            sequence="GCCTCTTCGCTATTACGCCAGCTGGCGAAAGGGGGATGTGCTGCAAGGCG"
        )
    ]
    
    circuit = GeneticCircuit(
        circuit_id="modular_demo_circuit",
        elements=elements
    )
    
    return circuit
