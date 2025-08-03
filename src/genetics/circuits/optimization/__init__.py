"""
Optimization module for genetic circuits.

This module provides genetic algorithm optimization and biological constraints
validation for improving circuit design and ensuring biological compatibility.
"""

from .genetic_algo import (
    GeneticAlgorithmOptimizer,
    CircuitFitnessEvaluator,
    OptimizationResult,
    optimize_multiple_circuits,
    optimize_for_chassis
)

from .bio_constraints import (
    BiologicalConstraintsValidator,
    ConstraintViolation,
    ConstraintSeverity,
    ValidationResult,
    validate_circuit_compatibility,
    batch_validate_circuits
)

__all__ = [
    # Genetic Algorithm Optimization
    "GeneticAlgorithmOptimizer",
    "CircuitFitnessEvaluator", 
    "OptimizationResult",
    "optimize_multiple_circuits",
    "optimize_for_chassis",
    
    # Biological Constraints Validation
    "BiologicalConstraintsValidator",
    "ConstraintViolation",
    "ConstraintSeverity",
    "ValidationResult",
    "validate_circuit_compatibility",
    "batch_validate_circuits"
]


def optimize_and_validate_circuit(circuit, chassis="ecoli", generations=100):
    """
    Convenience function to optimize a circuit and validate the result.
    
    Args:
        circuit: GeneticCircuit to optimize
        chassis: Target chassis organism
        generations: Number of optimization generations
        
    Returns:
        tuple: (OptimizationResult, ValidationResult)
    """
    from ..core.elements import GeneticCircuit
    
    # Optimize the circuit
    optimizer = GeneticAlgorithmOptimizer()
    optimization_result = optimizer.optimize_circuit(circuit, generations)
    
    # Validate the optimized circuit
    validator = BiologicalConstraintsValidator(chassis)
    validation_result = validator.validate_circuit(optimization_result.optimized_circuit)
    
    return optimization_result, validation_result


def get_optimization_recommendations(circuit, chassis="ecoli"):
    """
    Get optimization recommendations for a circuit.
    
    Args:
        circuit: GeneticCircuit to analyze
        chassis: Target chassis organism
        
    Returns:
        dict: Recommendations for circuit improvement
    """
    validator = BiologicalConstraintsValidator(chassis)
    evaluator = CircuitFitnessEvaluator()
    
    validation_result = validator.validate_circuit(circuit)
    fitness_score = evaluator.evaluate_fitness(circuit)
    
    recommendations = {
        "current_fitness": fitness_score,
        "validation_passed": validation_result.is_valid,
        "critical_issues": validation_result.critical_count,
        "improvement_areas": [],
        "suggested_optimizations": []
    }
    
    # Analyze violations for recommendations
    for violation in validation_result.violations:
        if violation.severity in [ConstraintSeverity.ERROR, ConstraintSeverity.CRITICAL]:
            recommendations["improvement_areas"].append({
                "area": violation.constraint_name,
                "description": violation.description,
                "suggestion": violation.suggestion
            })
    
    # Fitness-based recommendations
    if fitness_score < 0.7:
        recommendations["suggested_optimizations"].extend([
            "Consider genetic algorithm optimization",
            "Review sequence lengths and GC content",
            "Check for regulatory conflicts"
        ])
    
    if fitness_score < 0.5:
        recommendations["suggested_optimizations"].extend([
            "Major circuit redesign may be needed",
            "Consider breaking into smaller modules",
            "Validate biological feasibility"
        ])
    
    return recommendations
