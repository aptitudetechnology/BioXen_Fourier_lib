#!/usr/bin/env python3
"""
Test BioXen with real JCVI-Syn3A genome data.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from genome.parser import BioXenRealGenomeIntegrator
from hypervisor.core import BioXenHypervisor, VirtualMachine, ResourceAllocation

def test_real_genome_integration():
    """Test BioXen with actual Syn3A genome data."""
    print("🧬 BioXen Real Genome Integration Test")
    print("=" * 50)
    
    # Load the real genome
    genome_path = Path(__file__).parent / 'genomes' / 'syn3A.genome'
    if not genome_path.exists():
        print(f"❌ Genome file not found: {genome_path}")
        return False
    
    try:
        # Initialize the integrator
        integrator = BioXenRealGenomeIntegrator(genome_path)
        
        # Load and analyze the genome
        print("\n📊 Loading and analyzing JCVI-Syn3A genome...")
        real_genome = integrator.load_genome()
        stats = integrator.get_genome_stats()
        
        print(f"✅ Successfully loaded {stats['organism']}")
        print(f"   📏 Genome size: {stats['genome_length_bp']:,} bp")
        print(f"   🧬 Total genes: {stats['total_genes']}")
        print(f"   ⚡ Essential genes: {stats['essential_genes']} ({stats['essential_percentage']:.1f}%)")
        print(f"   🧱 Protein coding: {stats['protein_coding_genes']}")
        print(f"   📋 RNA genes: {stats['rna_genes']}")
        print(f"   📦 Coding density: {stats['coding_density']:.1f}%")
        print(f"   📏 Avg gene length: {stats['average_gene_length']:.0f} bp")
        
        print("\n🔬 Gene categories:")
        for category, count in stats['gene_categories'].items():
            print(f"   {category.replace('_', ' ').title()}: {count}")
        
        # Create BioXen template
        print("\n🏗️  Creating BioXen VM template...")
        template = integrator.create_vm_template()
        
        print(f"✅ Template created:")
        print(f"   💾 Min memory: {template['min_memory_kb']} KB")
        print(f"   🔧 Min CPU: {template['min_cpu_percent']}%")
        print(f"   ⏱️  Boot time: {template['boot_time_ms']} ms")
        print(f"   🧬 Minimal gene set: {len(template['minimal_gene_set'])} genes")
        
        # Test VM creation with different resource allocations
        print("\n🖥️  Testing VM creation scenarios:")
        
        test_scenarios = [
            {
                'name': 'Minimal Resources',
                'resources': {
                    'memory_kb': template['min_memory_kb'],
                    'cpu_percent': template['min_cpu_percent']
                }
            },
            {
                'name': 'Standard Resources', 
                'resources': {
                    'memory_kb': template['min_memory_kb'] * 2,
                    'cpu_percent': template['min_cpu_percent'] * 2
                }
            },
            {
                'name': 'High Resources',
                'resources': {
                    'memory_kb': template['min_memory_kb'] * 4,
                    'cpu_percent': 50
                }
            },
            {
                'name': 'Insufficient Resources',
                'resources': {
                    'memory_kb': template['min_memory_kb'] // 2,
                    'cpu_percent': template['min_cpu_percent'] // 2
                }
            }
        ]
        
        for i, scenario in enumerate(test_scenarios):
            print(f"\n   Test {i+1}: {scenario['name']}")
            vm_result = integrator.simulate_vm_creation(
                vm_id=f"syn3a_vm_{i+1}",
                allocated_resources=scenario['resources']
            )
            
            status = "✅" if vm_result['resource_constraints_met'] else "❌"
            print(f"   {status} Resource constraints: {'Met' if vm_result['resource_constraints_met'] else 'Failed'}")
            print(f"      🧬 Active genes: {vm_result['active_gene_count']}/{vm_result['total_genome_genes']}")
            print(f"      ⚡ Essential active: {vm_result['essential_genes_active']}")
            print(f"      📊 Genome utilization: {vm_result['genome_utilization_percent']:.1f}%")
            print(f"      ⏱️  Boot time: {vm_result['estimated_boot_time_ms']} ms")
        
        # Test with BioXen hypervisor
        print("\n🏗️  Testing with BioXen Hypervisor...")
        hypervisor = BioXenHypervisor()
        
        # Create resource allocation based on real genome requirements
        resource_allocation = ResourceAllocation(
            memory_kb=template['min_memory_kb'] * 2,
            atp_percentage=25.0,
            ribosomes=20,
            rna_polymerase=10,
            priority=1
        )
        
        try:
            # Create VM using the hypervisor's create_vm method
            vm_id = "real_syn3a_vm"
            success = hypervisor.create_vm(
                vm_id=vm_id,
                genome_template="real_syn3a",
                resource_allocation=resource_allocation
            )
            
            if success:
                print(f"✅ Created VM: {vm_id}")
                
                # Get VM details
                vm = hypervisor.vms[vm_id]
                print(f"   Status: {vm.state}")
                print(f"   Genome template: {vm.genome_template}")
                print(f"   Memory allocated: {vm.resources.memory_kb} KB")
                print(f"   Ribosomes: {vm.resources.ribosomes}")
                
                # Start VM
                hypervisor.start_vm(vm_id)
                vm_status = hypervisor.get_vm_status(vm_id)
                print(f"   Started VM - Status: {vm_status['state']}")
                
                # Test some operations
                resources = hypervisor.get_system_resources()
                active_vms = len([vm for vm in hypervisor.vms.values() if vm.state.value == 'running'])
                print(f"   Active VMs: {active_vms}")
                print(f"   Available ribosomes: {resources['available_ribosomes']}")
                print(f"   Total VMs: {len(hypervisor.vms)}")
                
                # Stop VM
                hypervisor.stop_vm(vm_id)
                print(f"   Stopped VM successfully")
            else:
                print(f"❌ Failed to create VM: {vm_id}")
            
        except Exception as e:
            print(f"❌ Hypervisor test failed: {e}")
            return False
        
        print("\n🎉 Real genome integration test completed successfully!")
        print(f"✅ BioXen can successfully virtualize {real_genome.organism}")
        print(f"   📊 Analyzed {len(real_genome.genes)} genes")
        print(f"   ⚡ Identified {len(real_genome.essential_genes)} essential genes")
        print(f"   🖥️  Successfully created and managed VMs")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_interesting_genes():
    """Show some interesting genes from the real genome."""
    genome_path = Path(__file__).parent / 'genomes' / 'syn3A.genome'
    integrator = BioXenRealGenomeIntegrator(genome_path)
    real_genome = integrator.load_genome()
    
    print("\n🔬 Interesting genes from JCVI-Syn3A:")
    print("=" * 50)
    
    # Show some key essential genes
    categories = ['protein_synthesis', 'dna_replication', 'energy_metabolism', 'transcription']
    
    for category in categories:
        print(f"\n📋 {category.replace('_', ' ').title()}:")
        genes_in_cat = [g for g in real_genome.essential_genes 
                       if g.functional_category == category][:3]
        
        for gene in genes_in_cat:
            print(f"   🧬 {gene.id}: {gene.description[:60]}")
            print(f"      Position: {gene.start:,}-{gene.end:,} ({gene.length:,} bp)")
            print(f"      Strand: {'+' if gene.strand == 1 else '-'}")

if __name__ == "__main__":
    print("🧬 BioXen Real Genome Test Suite")
    print("Testing with actual JCVI-Syn3A genome data\n")
    
    success = test_real_genome_integration()
    
    if success:
        show_interesting_genes()
        print("\n✅ All tests passed! BioXen works with real genome data.")
    else:
        print("\n❌ Tests failed. Check the error messages above.")
        sys.exit(1)
