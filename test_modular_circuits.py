#!/usr/bin/env python3
"""
Test script for the modular genetic circuits system.

This script validates all components of the modular circuits implementation
and demonstrates the complete workflow from circuit creation to JCVI export.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_core_modules():
    """Test core circuit functionality"""
    print("Testing core modules...")
    
    # Test basic elements
    from src.genetics.circuits.core.elements import GeneticElement, GeneticCircuit, ElementType, CircuitType
    
    # Create test elements
    promoter = GeneticElement(
        element_id="test_promoter",
        element_type=ElementType.PROMOTER,
        sequence="TTGACAGCTAGCTCAGTCCTAGGTATAATGCTAGC"
    )
    
    gene = GeneticElement(
        element_id="test_gene", 
        element_type=ElementType.GENE,
        sequence="ATGAAAGCCATTTTGGCAGTAGCGGCGATCGGCACAGGCATTTATGCGTGA"
    )
    
    terminator = GeneticElement(
        element_id="test_terminator",
        element_type=ElementType.TERMINATOR,
        sequence="GCCTCTTCGCTATTACGCCAGCTGGCGAAAGGGGGATGTGCTGCAAGGCG"
    )
    
    # Create circuit
    circuit = GeneticCircuit(
        circuit_id="test_circuit",
        circuit_type=CircuitType.GENE_EXPRESSION,
        elements=[promoter, gene, terminator]
    )
    
    print(f"✓ Created circuit with {len(circuit.elements)} elements")
    
    # Test factory
    from src.genetics.circuits.core.factory import CircuitFactory, create_gene_expression_circuit
    
    factory_circuit = create_gene_expression_circuit("factory_test", "test_protein")
    print(f"✓ Factory created circuit with {len(factory_circuit.elements)} elements")
    
    # Test validator
    from src.genetics.circuits.core.validator import validate_circuit_basic
    
    validation_result = validate_circuit_basic(circuit)
    print(f"✓ Basic validation passed: {validation_result.is_valid}")
    
    return circuit


def test_library_modules():
    """Test circuit library functionality"""
    print("\nTesting library modules...")
    
    # Test monitor circuits
    from src.genetics.circuits.library.monitors import create_atp_monitor, create_resource_monitor
    
    atp_monitor = create_atp_monitor("vm1")
    resource_monitor = create_resource_monitor("vm1", ["cpu", "memory"])
    
    print(f"✓ Created ATP monitor with {len(atp_monitor.elements)} elements")
    print(f"✓ Created resource monitor with {len(resource_monitor.elements)} elements")
    
    # Test scheduler circuits
    from src.genetics.circuits.library.schedulers import create_round_robin_scheduler, create_priority_scheduler
    
    rr_scheduler = create_round_robin_scheduler(["vm1", "vm2", "vm3"])
    priority_scheduler = create_priority_scheduler({"vm1": 1, "vm2": 2, "vm3": 3})
    
    print(f"✓ Created round-robin scheduler with {len(rr_scheduler.elements)} elements")
    print(f"✓ Created priority scheduler with {len(priority_scheduler.elements)} elements")
    
    # Test isolation circuits
    from src.genetics.circuits.library.isolation import create_vm_isolation_circuit, create_security_circuit
    
    isolation_circuit = create_vm_isolation_circuit("vm1", ["network", "filesystem"])
    security_circuit = create_security_circuit("vm1", ["authentication", "encryption"])
    
    print(f"✓ Created isolation circuit with {len(isolation_circuit.elements)} elements")
    print(f"✓ Created security circuit with {len(security_circuit.elements)} elements")
    
    # Test memory circuits
    from src.genetics.circuits.library.memory import create_memory_allocator, create_garbage_collector
    
    memory_allocator = create_memory_allocator("vm1", 1024)
    garbage_collector = create_garbage_collector("vm1", "mark_sweep")
    
    print(f"✓ Created memory allocator with {len(memory_allocator.elements)} elements")
    print(f"✓ Created garbage collector with {len(garbage_collector.elements)} elements")
    
    return [atp_monitor, rr_scheduler, isolation_circuit, memory_allocator]


def test_optimization_modules():
    """Test optimization functionality"""
    print("\nTesting optimization modules...")
    
    # Create test circuit
    from src.genetics.circuits.core.elements import GeneticElement, ElementType, GeneticCircuit
    
    elements = [
        GeneticElement("opt_promoter", ElementType.PROMOTER, "TTGACAGCTAGCTCAGTCCTAGGTATAATGCTAGC"),
        GeneticElement("opt_gene", ElementType.GENE, "ATGAAAGCCATTTTGGCAGTAGCGGCGATCGGCACAGGCATTTATGCGTGA"),
        GeneticElement("opt_terminator", ElementType.TERMINATOR, "GCCTCTTCGCTATTACGCCAGCTGGCGAAAGGGGGATGTGCTGCAAGGCG")
    ]
    
    circuit = GeneticCircuit("optimization_test", elements)
    
    # Test fitness evaluation
    from src.genetics.circuits.optimization.genetic_algo import CircuitFitnessEvaluator
    
    evaluator = CircuitFitnessEvaluator()
    fitness = evaluator.evaluate_fitness(circuit)
    print(f"✓ Circuit fitness evaluation: {fitness:.3f}")
    
    # Test biological constraints validation
    from src.genetics.circuits.optimization.bio_constraints import BiologicalConstraintsValidator
    
    validator = BiologicalConstraintsValidator("ecoli")
    validation_result = validator.validate_circuit(circuit)
    print(f"✓ Biological validation - Valid: {validation_result.is_valid}, "
          f"Warnings: {validation_result.warnings_count}, Errors: {validation_result.errors_count}")
    
    # Test optimization
    from src.genetics.circuits.optimization import optimize_and_validate_circuit
    
    opt_result, val_result = optimize_and_validate_circuit(circuit, generations=10)
    print(f"✓ Optimization completed - Fitness improvement: {opt_result.fitness_improvement:.3f}")
    
    return circuit, validation_result


def test_export_modules():
    """Test export functionality"""
    print("\nTesting export modules...")
    
    # Create test circuit
    from src.genetics.circuits.core.elements import GeneticElement, ElementType, GeneticCircuit
    
    elements = [
        GeneticElement("export_promoter", ElementType.PROMOTER, "TTGACAGCTAGCTCAGTCCTAGGTATAATGCTAGC"),
        GeneticElement("export_rbs", ElementType.RBS, "AAGGAGGTGATCCATG"),
        GeneticElement("export_gene", ElementType.GENE, "ATGAAAGCCATTTTGGCAGTAGCGGCGATCGGCACAGGCATTTATGCGTGA"),
        GeneticElement("export_terminator", ElementType.TERMINATOR, "GCCTCTTCGCTATTACGCCAGCTGGCGAAAGGGGGATGTGCTGCAAGGCG")
    ]
    
    circuit = GeneticCircuit("export_test", elements)
    
    # Test JCVI format export
    from src.genetics.circuits.exports.jcvi_format import JCVIFormatExporter
    
    exporter = JCVIFormatExporter()
    
    # Test GenBank export
    genbank_content = exporter.export_circuit_to_genbank(circuit)
    print(f"✓ GenBank export: {len(genbank_content)} characters")
    
    # Test GFF3 export
    gff3_content = exporter.export_circuit_to_gff3(circuit)
    print(f"✓ GFF3 export: {len(gff3_content)} characters")
    
    # Test JSON export
    json_content = exporter.export_circuit_to_jcvi_json(circuit)
    print(f"✓ JCVI JSON export: {len(json_content)} characters")
    
    # Test export validation
    from src.genetics.circuits.exports import validate_export_requirements
    
    export_validation = validate_export_requirements(circuit)
    print(f"✓ Export validation - Ready: {export_validation['is_exportable']}, "
          f"Score: {export_validation['export_readiness']:.2f}")
    
    return circuit


def test_integration():
    """Test full integration workflow"""
    print("\nTesting full integration workflow...")
    
    # Create circuit using factory
    from src.genetics.circuits.library.monitors import create_atp_monitor
    
    circuit = create_atp_monitor("integration_test_vm")
    print(f"✓ Created circuit: {circuit.circuit_id}")
    
    # Validate circuit
    from src.genetics.circuits.optimization import BiologicalConstraintsValidator
    
    validator = BiologicalConstraintsValidator("ecoli")
    validation_result = validator.validate_circuit(circuit)
    print(f"✓ Validation completed - Issues: {len(validation_result.violations)}")
    
    # Optimize if needed
    if not validation_result.is_valid:
        from src.genetics.circuits.optimization import GeneticAlgorithmOptimizer
        
        optimizer = GeneticAlgorithmOptimizer()
        opt_result = optimizer.optimize_circuit(circuit, generations=5)
        circuit = opt_result.optimized_circuit
        print(f"✓ Optimization applied - Improvement: {opt_result.fitness_improvement:.3f}")
    
    # Export to JCVI formats
    from src.genetics.circuits.exports import export_circuit_complete
    
    export_files = export_circuit_complete(circuit, "./test_export", 
                                         include_visualization=False, include_jcvi=True)
    print(f"✓ Export completed - Files: {len(export_files)}")
    
    return circuit


def test_modular_system():
    """Test the complete modular circuits system"""
    print("=" * 60)
    print("BioXen Modular Genetic Circuits System Test")
    print("=" * 60)
    
    try:
        # Test core functionality
        core_circuit = test_core_modules()
        
        # Test library circuits
        library_circuits = test_library_modules()
        
        # Test optimization
        opt_circuit, validation = test_optimization_modules()
        
        # Test exports
        export_circuit = test_export_modules()
        
        # Test full integration
        integration_circuit = test_integration()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED")
        print("=" * 60)
        
        # Print system info
        from src.genetics.circuits import get_modular_circuits_info, HAS_VISUALIZATION
        
        info = get_modular_circuits_info()
        print(f"\nModular Circuits System v{info['version']}")
        print(f"Modules: {len(info['modules'])}")
        print(f"Features: {len(info['features'])}")
        print(f"JCVI Formats: {len(info['compatibility']['jcvi_formats'])}")
        print(f"Visualization: {'Available' if HAS_VISUALIZATION else 'Requires matplotlib'}")
        
        # Create demo circuit
        from src.genetics.circuits import create_demo_circuit
        demo = create_demo_circuit()
        print(f"\nDemo circuit created: {demo.circuit_id} ({len(demo.elements)} elements)")
        
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_modular_system()
    sys.exit(0 if success else 1)
