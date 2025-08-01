"""
Simple demonstration of BioXen hypervisor capabilities

This script demonstrates the core functionality of the biological hypervisor
by creating VMs, running them, and showing resource management.
"""

import time
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from hypervisor.core import BioXenHypervisor, ResourceAllocation
from monitoring.profiler import PerformanceProfiler, BenchmarkSuite
from genome.syn3a import VMImageBuilder
from genetics.circuits import BioCompiler

def demo_basic_vm_operations():
    """Demonstrate basic VM operations"""
    print("=== BioXen Hypervisor Demo ===\n")
    
    # Initialize hypervisor
    print("1. Initializing BioXen hypervisor...")
    hypervisor = BioXenHypervisor(max_vms=4, total_ribosomes=80)
    print(f"   ✓ Hypervisor initialized with {hypervisor.total_ribosomes} ribosomes")
    print(f"   ✓ Available for VMs: {hypervisor.available_ribosomes} ribosomes\n")
    
    # Show initial resources
    resources = hypervisor.get_system_resources()
    print("2. Initial system resources:")
    print(f"   - Total ribosomes: {resources['total_ribosomes']}")
    print(f"   - Available ribosomes: {resources['available_ribosomes']}")
    print(f"   - Hypervisor overhead: {resources['hypervisor_overhead']:.1%}")
    print(f"   - Active VMs: {resources['active_vms']}\n")
    
    # Create first VM
    print("3. Creating first virtual machine (Syn3A-VM1)...")
    vm1_resources = ResourceAllocation(
        ribosomes=20,
        atp_percentage=30.0,
        memory_kb=120,
        priority=2
    )
    
    success = hypervisor.create_vm("syn3a-vm1", "syn3a_minimal", vm1_resources)
    if success:
        print("   ✓ VM 'syn3a-vm1' created successfully")
        print(f"   - Allocated {vm1_resources.ribosomes} ribosomes")
        print(f"   - Allocated {vm1_resources.atp_percentage}% ATP")
        print(f"   - Allocated {vm1_resources.memory_kb} KB memory\n")
    else:
        print("   ✗ Failed to create VM\n")
        return
    
    # Start the VM
    print("4. Starting VM...")
    if hypervisor.start_vm("syn3a-vm1"):
        print("   ✓ VM 'syn3a-vm1' started successfully")
        print("   - Boot sequence: Initialize core genes")
        print("   - Resource allocation: Ribosomes assigned")
        print("   - Status: Running\n")
    
    # Check VM status
    print("5. Checking VM status...")
    status = hypervisor.get_vm_status("syn3a-vm1")
    if status:
        print(f"   - VM ID: {status['vm_id']}")
        print(f"   - State: {status['state']}")
        print(f"   - Uptime: {status['uptime_seconds']:.1f} seconds")
        print(f"   - Health: {status['health_status']}")
        print(f"   - Priority: {status['priority']}\n")
    
    # Create second VM
    print("6. Creating second virtual machine (Syn3A-VM2)...")
    vm2_resources = ResourceAllocation(
        ribosomes=15,
        atp_percentage=25.0,
        memory_kb=100,
        priority=1
    )
    
    if hypervisor.create_vm("syn3a-vm2", "syn3a_minimal", vm2_resources):
        hypervisor.start_vm("syn3a-vm2")
        print("   ✓ VM 'syn3a-vm2' created and started")
        print(f"   - Lower priority (1 vs 2)")
        print(f"   - Fewer resources allocated\n")
    
    # Show resource allocation
    print("7. Current resource allocation:")
    resources = hypervisor.get_system_resources()
    print(f"   - Allocated ribosomes: {resources['allocated_ribosomes']}")
    print(f"   - Free ribosomes: {resources['free_ribosomes']}")
    print(f"   - Total ATP allocated: {resources['total_atp_allocated']:.1f}%")
    print(f"   - Active VMs: {resources['active_vms']}\n")
    
    # List all VMs
    print("8. All virtual machines:")
    vms = hypervisor.list_vms()
    for vm in vms:
        print(f"   - {vm['vm_id']}: {vm['state']} "
              f"(R:{vm['ribosome_allocation']}, "
              f"ATP:{vm['atp_percentage']:.1f}%, "
              f"Mem:{vm['memory_kb']}KB)")
    print()
    
    # Demonstrate scheduling
    print("9. Demonstrating scheduler (time-sliced execution)...")
    for i in range(5):
        print(f"   Scheduling iteration {i+1}...")
        hypervisor.run_scheduler()
        print(f"   - Active VM: {hypervisor.active_vm}")
        time.sleep(2)
    print()
    
    # Pause and resume demonstration
    print("10. VM lifecycle management...")
    print("    Pausing syn3a-vm2...")
    hypervisor.pause_vm("syn3a-vm2")
    
    status = hypervisor.get_vm_status("syn3a-vm2")
    print(f"    ✓ VM state: {status['state']}")
    
    print("    Resuming syn3a-vm2...")
    hypervisor.resume_vm("syn3a-vm2")
    
    status = hypervisor.get_vm_status("syn3a-vm2")
    print(f"    ✓ VM state: {status['state']}\n")
    
    # Clean up
    print("11. Cleaning up...")
    hypervisor.destroy_vm("syn3a-vm1")
    hypervisor.destroy_vm("syn3a-vm2")
    print("    ✓ All VMs destroyed")
    print("    ✓ Resources freed\n")
    
    print("=== Demo Complete ===")

def demo_vm_image_builder():
    """Demonstrate VM image building"""
    print("\n=== VM Image Builder Demo ===\n")
    
    builder = VMImageBuilder()
    
    print("1. Building VM image for Syn3A minimal genome...")
    
    # Create VM configuration
    config = {
        "resource_limits": {
            "max_ribosomes": 25
        },
        "isolation_level": "high",
        "monitoring": True
    }
    
    # Build VM image
    vm_image = builder.build_vm_image("demo-vm", config)
    
    print(f"   ✓ VM image built successfully")
    print(f"   - Genome ID: {vm_image['genome'].genome_id}")
    print(f"   - Total genes: {len(vm_image['genome'].genes)}")
    print(f"   - Genome size: {vm_image['genome'].total_size} bp")
    print(f"   - GC content: {vm_image['genome'].gc_content:.1%}")
    
    # Show essential genes
    essential_genes = vm_image['genome'].get_essential_genes()
    print(f"   - Essential genes: {len(essential_genes)}")
    
    categories = {}
    for gene in vm_image['genome'].genes:
        categories[gene.category] = categories.get(gene.category, 0) + 1
    
    print("   - Gene categories:")
    for category, count in categories.items():
        print(f"     * {category}: {count}")
    
    # Show resource requirements
    requirements = vm_image['resource_requirements']
    print("   - Minimum resource requirements:")
    print(f"     * Ribosomes: {requirements['min_ribosomes']}")
    print(f"     * ATP: {requirements['min_atp_percentage']}%")
    print(f"     * Memory: {requirements['min_memory_kb']} KB")
    print(f"     * RNA polymerase: {requirements['min_rna_polymerase']}")
    
    print("\n=== VM Image Demo Complete ===")

def demo_genetic_circuits():
    """Demonstrate genetic circuit compilation"""
    print("\n=== Genetic Circuit Demo ===\n")
    
    compiler = BioCompiler()
    
    print("1. Compiling hypervisor genetic circuits...")
    
    # Define VM configurations
    vm_configs = [
        {"vm_id": "vm1", "genetic_code": "standard"},
        {"vm_id": "vm2", "genetic_code": "amber_suppression"},
        {"vm_id": "vm3", "genetic_code": "synthetic_aa"}
    ]
    
    # Compile hypervisor DNA
    sequences = compiler.compile_hypervisor(vm_configs)
    
    print(f"   ✓ Generated {len(sequences)} DNA sequences")
    
    for seq_name, seq_dna in sequences.items():
        print(f"   - {seq_name}: {len(seq_dna)} bp")
        if len(seq_dna) > 60:
            print(f"     {seq_dna[:30]}...{seq_dna[-30:]}")
        else:
            print(f"     {seq_dna}")
    
    # Show genetic code variants
    print("\n2. Genetic code isolation:")
    for config in vm_configs:
        vm_id = config["vm_id"]
        genetic_code = compiler.genetic_codes.get_genetic_code(vm_id)
        print(f"   - {vm_id}: {genetic_code}")
        
        orthogonal = compiler.genetic_codes.get_orthogonal_elements(vm_id)
        if orthogonal:
            print(f"     * tRNA: {len(orthogonal['trna'])} bp")
            print(f"     * Synthetase: {len(orthogonal['synthetase'])} bp")
    
    print("\n=== Genetic Circuit Demo Complete ===")

def demo_performance_monitoring():
    """Demonstrate performance monitoring"""
    print("\n=== Performance Monitoring Demo ===\n")
    
    # Create hypervisor
    hypervisor = BioXenHypervisor()
    
    # Create and start VMs
    print("1. Setting up test VMs...")
    hypervisor.create_vm("perf-vm1", "syn3a_minimal")
    hypervisor.create_vm("perf-vm2", "syn3a_minimal")
    hypervisor.start_vm("perf-vm1")
    hypervisor.start_vm("perf-vm2")
    print("   ✓ Two VMs created and started")
    
    # Start monitoring
    print("\n2. Starting performance monitoring...")
    profiler = PerformanceProfiler(hypervisor, monitoring_interval=2.0)
    profiler.start_monitoring()
    print("   ✓ Profiler started (2-second intervals)")
    
    # Run for a short time
    print("\n3. Running system for 20 seconds...")
    for i in range(10):
        hypervisor.run_scheduler()
        profiler.record_context_switch()
        time.sleep(2)
        if i % 3 == 0:
            print(f"   - Iteration {i+1}/10 complete")
    
    # Stop monitoring and get report
    profiler.stop_monitoring()
    report = profiler.get_performance_report()
    
    print("\n4. Performance Report:")
    print(f"   - Monitoring duration: {report['monitoring_duration']:.1f}s")
    
    sys_perf = report['system_performance']
    print(f"   - Average ribosome utilization: {sys_perf['average_ribosome_utilization']:.1f}%")
    print(f"   - Average ATP level: {sys_perf['average_atp_level']:.1f}%")
    print(f"   - Average memory usage: {sys_perf['average_memory_usage']:.1f}%")
    
    if report['scheduling_performance']:
        sched_perf = report['scheduling_performance']
        print(f"   - Scheduling fairness: {sched_perf['average_fairness_score']:.1f}%")
        print(f"   - Average wait time: {sched_perf['average_wait_time']:.1f}s")
    
    if report['bottlenecks']:
        print("   - Bottlenecks detected:")
        for bottleneck in report['bottlenecks']:
            print(f"     * {bottleneck}")
    else:
        print("   - No bottlenecks detected ✓")
    
    if report['recommendations']:
        print("   - Recommendations:")
        for rec in report['recommendations']:
            print(f"     * {rec}")
    
    # Cleanup
    hypervisor.destroy_vm("perf-vm1")
    hypervisor.destroy_vm("perf-vm2")
    
    print("\n=== Performance Demo Complete ===")

def demo_benchmark_suite():
    """Demonstrate benchmark suite"""
    print("\n=== Benchmark Suite Demo ===\n")
    
    hypervisor = BioXenHypervisor()
    benchmark = BenchmarkSuite(hypervisor)
    
    print("Running BioXen benchmark suite...")
    print("(This will take a few minutes)\n")
    
    # Run benchmarks
    print("Phase 1: Single VM performance test...")
    result1 = benchmark.run_single_vm_benchmark()
    print(f"   ✓ Overhead: {result1['hypervisor_overhead']:.1f}%")
    print(f"   ✓ Success: {result1['success_criteria']}")
    
    print("\nPhase 2: Dual VM fairness test...")
    result2 = benchmark.run_dual_vm_benchmark()
    print(f"   ✓ Fairness: {result2['fairness_score']:.1f}%")
    print(f"   ✓ Success: {result2['success_criteria']}")
    
    print("\nPhase 3: Stress test...")
    result3 = benchmark.run_stress_test()
    print(f"   ✓ Max VMs: {result3['max_vms_created']}")
    print(f"   ✓ Success: {result3['success_criteria']}")
    
    # Generate report
    print("\n" + benchmark.generate_benchmark_report())

def main():
    """Run all demonstrations"""
    try:
        demo_basic_vm_operations()
        demo_vm_image_builder()
        demo_genetic_circuits()
        demo_performance_monitoring()
        
        # Ask if user wants to run full benchmark
        response = input("\nRun full benchmark suite? (y/N): ").strip().lower()
        if response == 'y':
            demo_benchmark_suite()
        
        print("\n🧬 All BioXen demonstrations completed successfully! 🧬")
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\nDemo failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
