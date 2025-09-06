"""
Genetic algorithm optimization for circuit design.

This module provides evolutionary optimization algorithms for improving
genetic circuit efficiency, resource usage, and biological compatibility.
"""

import random
import copy
from typing import List, Dict, Tuple, Callable, Optional
from dataclasses import dataclass
from ..core.elements import GeneticCircuit, GeneticElement


@dataclass
class OptimizationResult:
    """Result of circuit optimization"""
    original_circuit: GeneticCircuit
    optimized_circuit: GeneticCircuit
    fitness_improvement: float
    generations: int
    optimization_log: List[str]


class CircuitFitnessEvaluator:
    """Evaluates fitness of genetic circuits"""
    
    def __init__(self):
        self.weights = {
            "length_efficiency": 0.3,    # Shorter is better
            "gc_content": 0.2,           # 40-60% GC is optimal
            "restriction_sites": 0.2,    # Fewer restriction sites is better
            "regulatory_conflicts": 0.2,  # No conflicts is better
            "resource_usage": 0.1        # Lower resource usage is better
        }
    
    def evaluate_fitness(self, circuit: GeneticCircuit) -> float:
        """Evaluate the overall fitness of a circuit"""
        fitness_scores = {}
        
        # Length efficiency (shorter circuits are generally better)
        total_length = sum(len(e.sequence) for e in circuit.elements)
        fitness_scores["length_efficiency"] = self._evaluate_length(total_length)
        
        # GC content (40-60% is optimal for most organisms)
        gc_content = self._calculate_gc_content(circuit)
        fitness_scores["gc_content"] = self._evaluate_gc_content(gc_content)
        
        # Restriction sites (fewer is better for cloning)
        restriction_count = self._count_restriction_sites(circuit)
        fitness_scores["restriction_sites"] = self._evaluate_restriction_sites(restriction_count)
        
        # Regulatory conflicts (none is better)
        conflict_count = self._count_regulatory_conflicts(circuit)
        fitness_scores["regulatory_conflicts"] = self._evaluate_conflicts(conflict_count)
        
        # Resource usage estimation
        resource_score = self._estimate_resource_usage(circuit)
        fitness_scores["resource_usage"] = resource_score
        
        # Calculate weighted fitness
        total_fitness = sum(
            score * self.weights[metric] 
            for metric, score in fitness_scores.items()
        )
        
        return total_fitness
    
    def _calculate_gc_content(self, circuit: GeneticCircuit) -> float:
        """Calculate GC content of entire circuit"""
        all_sequence = "".join(e.sequence for e in circuit.elements).upper()
        if not all_sequence:
            return 0.0
        
        gc_count = all_sequence.count('G') + all_sequence.count('C')
        return gc_count / len(all_sequence)
    
    def _evaluate_length(self, length: int) -> float:
        """Evaluate length efficiency (0-1 scale)"""
        # Optimal length around 1000-5000 bp
        if 1000 <= length <= 5000:
            return 1.0
        elif length < 1000:
            return 0.5 + (length / 2000)  # Shorter gets some penalty
        else:
            return max(0.1, 1.0 - (length - 5000) / 10000)  # Longer gets more penalty
    
    def _evaluate_gc_content(self, gc_content: float) -> float:
        """Evaluate GC content (0-1 scale, optimal 40-60%)"""
        if 0.4 <= gc_content <= 0.6:
            return 1.0
        elif 0.3 <= gc_content <= 0.7:
            return 0.8
        elif 0.2 <= gc_content <= 0.8:
            return 0.6
        else:
            return 0.2
    
    def _count_restriction_sites(self, circuit: GeneticCircuit) -> int:
        """Count restriction enzyme sites in circuit"""
        restriction_sites = [
            "GAATTC", "GGATCC", "AAGCTT", "CTCGAG", "GTCGAC", "GCGGCCGC"
        ]
        
        all_sequence = "".join(e.sequence for e in circuit.elements).upper()
        count = 0
        for site in restriction_sites:
            count += all_sequence.count(site)
        
        return count
    
    def _evaluate_restriction_sites(self, count: int) -> float:
        """Evaluate restriction site count (fewer is better)"""
        if count == 0:
            return 1.0
        elif count <= 2:
            return 0.8
        elif count <= 5:
            return 0.6
        else:
            return max(0.1, 0.6 - (count - 5) * 0.1)
    
    def _count_regulatory_conflicts(self, circuit: GeneticCircuit) -> int:
        """Count regulatory conflicts in circuit"""
        targets = {}
        for element in circuit.elements:
            if element.regulation_target:
                if element.regulation_target not in targets:
                    targets[element.regulation_target] = 0
                targets[element.regulation_target] += 1
        
        # Count targets with multiple regulators
        conflicts = sum(1 for count in targets.values() if count > 1)
        return conflicts
    
    def _evaluate_conflicts(self, conflict_count: int) -> float:
        """Evaluate regulatory conflicts (none is better)"""
        if conflict_count == 0:
            return 1.0
        else:
            return max(0.1, 1.0 - conflict_count * 0.3)
    
    def _estimate_resource_usage(self, circuit: GeneticCircuit) -> float:
        """Estimate resource usage of circuit"""
        # Simple estimation based on number of genes and their lengths
        gene_count = len([e for e in circuit.elements if e.element_type.value == "gene"])
        avg_gene_length = sum(len(e.sequence) for e in circuit.elements 
                             if e.element_type.value == "gene")
        
        if gene_count > 0:
            avg_gene_length /= gene_count
        
        # Normalize resource usage (lower is better)
        resource_score = max(0.1, 1.0 - (gene_count * avg_gene_length) / 10000)
        return resource_score


class GeneticAlgorithmOptimizer:
    """Genetic algorithm optimizer for circuit design"""
    
    def __init__(self, population_size: int = 50, mutation_rate: float = 0.1,
                 crossover_rate: float = 0.7, elitism_rate: float = 0.1):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elitism_rate = elitism_rate
        self.fitness_evaluator = CircuitFitnessEvaluator()
        
        # DNA bases for mutations
        self.dna_bases = ['A', 'T', 'G', 'C']
    
    def optimize_circuit(self, circuit: GeneticCircuit, generations: int = 100,
                        target_fitness: float = 0.9) -> OptimizationResult:
        """Optimize a genetic circuit using genetic algorithms"""
        
        optimization_log = []
        optimization_log.append(f"Starting optimization of circuit: {circuit.circuit_id}")
        
        # Create initial population
        population = self._create_initial_population(circuit)
        
        original_fitness = self.fitness_evaluator.evaluate_fitness(circuit)
        optimization_log.append(f"Original fitness: {original_fitness:.3f}")
        
        best_circuit = circuit
        best_fitness = original_fitness
        
        for generation in range(generations):
            # Evaluate fitness for all individuals
            fitness_scores = [
                self.fitness_evaluator.evaluate_fitness(individual)
                for individual in population
            ]
            
            # Find best individual in this generation
            max_fitness_idx = fitness_scores.index(max(fitness_scores))
            generation_best = population[max_fitness_idx]
            generation_best_fitness = fitness_scores[max_fitness_idx]
            
            # Update global best
            if generation_best_fitness > best_fitness:
                best_circuit = copy.deepcopy(generation_best)
                best_fitness = generation_best_fitness
                optimization_log.append(
                    f"Generation {generation}: New best fitness {best_fitness:.3f}"
                )
            
            # Check if target fitness reached
            if best_fitness >= target_fitness:
                optimization_log.append(
                    f"Target fitness {target_fitness} reached at generation {generation}"
                )
                break
            
            # Create next generation
            population = self._create_next_generation(population, fitness_scores)
        
        fitness_improvement = best_fitness - original_fitness
        optimization_log.append(
            f"Optimization complete. Fitness improved by {fitness_improvement:.3f}"
        )
        
        return OptimizationResult(
            original_circuit=circuit,
            optimized_circuit=best_circuit,
            fitness_improvement=fitness_improvement,
            generations=generation + 1,
            optimization_log=optimization_log
        )
    
    def _create_initial_population(self, base_circuit: GeneticCircuit) -> List[GeneticCircuit]:
        """Create initial population with variations of the base circuit"""
        population = [copy.deepcopy(base_circuit)]  # Include original
        
        for _ in range(self.population_size - 1):
            variant = copy.deepcopy(base_circuit)
            # Apply random mutations to create variants
            for element in variant.elements:
                if random.random() < 0.3:  # 30% chance to mutate each element
                    element.sequence = self._mutate_sequence(element.sequence, 0.05)
            population.append(variant)
        
        return population
    
    def _create_next_generation(self, population: List[GeneticCircuit],
                               fitness_scores: List[float]) -> List[GeneticCircuit]:
        """Create the next generation using selection, crossover, and mutation"""
        next_generation = []
        
        # Elitism: keep best individuals
        elite_count = int(self.population_size * self.elitism_rate)
        if elite_count > 0:
            # Sort by fitness and take the best
            sorted_indices = sorted(range(len(fitness_scores)), 
                                  key=lambda i: fitness_scores[i], reverse=True)
            for i in range(elite_count):
                next_generation.append(copy.deepcopy(population[sorted_indices[i]]))
        
        # Generate rest of population through crossover and mutation
        while len(next_generation) < self.population_size:
            # Selection
            parent1 = self._tournament_selection(population, fitness_scores)
            parent2 = self._tournament_selection(population, fitness_scores)
            
            # Crossover
            if random.random() < self.crossover_rate:
                offspring = self._crossover(parent1, parent2)
            else:
                offspring = copy.deepcopy(parent1)
            
            # Mutation
            offspring = self._mutate_circuit(offspring)
            
            next_generation.append(offspring)
        
        return next_generation[:self.population_size]
    
    def _tournament_selection(self, population: List[GeneticCircuit],
                            fitness_scores: List[float], tournament_size: int = 3) -> GeneticCircuit:
        """Select individual using tournament selection"""
        tournament_indices = random.sample(range(len(population)), 
                                          min(tournament_size, len(population)))
        tournament_fitness = [fitness_scores[i] for i in tournament_indices]
        winner_idx = tournament_indices[tournament_fitness.index(max(tournament_fitness))]
        return population[winner_idx]
    
    def _crossover(self, parent1: GeneticCircuit, parent2: GeneticCircuit) -> GeneticCircuit:
        """Perform crossover between two circuits"""
        offspring = copy.deepcopy(parent1)
        
        # Simple crossover: swap some elements between parents
        min_elements = min(len(parent1.elements), len(parent2.elements))
        
        for i in range(min_elements):
            if random.random() < 0.5:  # 50% chance to take from parent2
                if i < len(parent2.elements):
                    offspring.elements[i] = copy.deepcopy(parent2.elements[i])
        
        return offspring
    
    def _mutate_circuit(self, circuit: GeneticCircuit) -> GeneticCircuit:
        """Apply mutations to a circuit"""
        mutated = copy.deepcopy(circuit)
        
        for element in mutated.elements:
            if random.random() < self.mutation_rate:
                element.sequence = self._mutate_sequence(element.sequence, 0.01)
        
        return mutated
    
    def _mutate_sequence(self, sequence: str, mutation_rate: float) -> str:
        """Apply point mutations to a DNA sequence"""
        sequence_list = list(sequence.upper())
        
        for i in range(len(sequence_list)):
            if random.random() < mutation_rate:
                # Point mutation: change to random base
                current_base = sequence_list[i]
                available_bases = [b for b in self.dna_bases if b != current_base]
                sequence_list[i] = random.choice(available_bases)
        
        return "".join(sequence_list)


def optimize_multiple_circuits(circuits: List[GeneticCircuit], 
                             generations: int = 100) -> List[OptimizationResult]:
    """Optimize multiple circuits simultaneously"""
    optimizer = GeneticAlgorithmOptimizer()
    results = []
    
    for circuit in circuits:
        result = optimizer.optimize_circuit(circuit, generations)
        results.append(result)
    
    return results


def optimize_for_chassis(circuit: GeneticCircuit, chassis: str = "ecoli") -> OptimizationResult:
    """Optimize circuit for specific chassis organism"""
    optimizer = GeneticAlgorithmOptimizer()
    
    # Adjust fitness weights based on chassis
    if chassis == "ecoli":
        optimizer.fitness_evaluator.weights.update({
            "gc_content": 0.3,  # E. coli prefers ~50% GC
            "length_efficiency": 0.3,
            "restriction_sites": 0.2,
            "regulatory_conflicts": 0.2,
        })
    elif chassis == "yeast":
        optimizer.fitness_evaluator.weights.update({
            "gc_content": 0.2,  # Yeast is more tolerant of GC variation
            "length_efficiency": 0.4,  # Length is more important
            "restriction_sites": 0.2,
            "regulatory_conflicts": 0.2,
        })
    
    return optimizer.optimize_circuit(circuit)
