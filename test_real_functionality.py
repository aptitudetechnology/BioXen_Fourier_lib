#!/usr/bin/env python3
"""
Test Real Functionality Implementation

This script directly tests the new real synteny and phylogenetic analysis
implementations to verify they work with actual genome data.
"""

import sys
from pathlib import Path

# Import the interactive genomics module
try:
    from interactive_comparative_genomics import InteractiveComparativeGenomics
except ImportError as e:
    print(f"❌ Error importing: {e}")
    sys.exit(1)

def test_real_synteny_analysis():
    """Test the real synteny analysis implementation"""
    
    print("🧬 Testing Real Synteny Analysis")
    print("=" * 40)
    
    # Create instance
    icg = InteractiveComparativeGenomics()
    
    # Discover genomes
    genomes = icg._discover_genomes()
    if len(genomes) < 2:
        print("❌ Need at least 2 genomes for synteny analysis")
        return False
    
    print(f"📊 Found {len(genomes)} genomes for analysis")
    
    # Test synteny analysis
    try:
        print("\n🔄 Running real synteny analysis...")
        results = icg._real_synteny_analysis(genomes[:3])  # Test with first 3 genomes
        
        print("✅ Synteny Analysis Results:")
        print(f"   📊 Conservation percentage: {results['conservation_pct']:.1f}%")
        print(f"   🧬 Synteny blocks found: {results['synteny_blocks']}")
        print(f"   🔗 Conserved genes: {results['conserved_genes']}")
        print(f"   📏 Average block length: {results['avg_block_length']:.1f} genes")
        
        # Verify this is real data, not default values
        if results['conservation_pct'] != 75.0 or results['synteny_blocks'] != 4:
            print("✅ CONFIRMED: Real analysis (not default fallback values)")
            return True
        else:
            print("⚠️  WARNING: May be using fallback values")
            return False
            
    except Exception as e:
        print(f"❌ Synteny analysis failed: {e}")
        return False

def test_real_phylogenetic_analysis():
    """Test the real phylogenetic analysis implementation"""
    
    print("\n🌳 Testing Real Phylogenetic Analysis")
    print("=" * 40)
    
    # Create instance
    icg = InteractiveComparativeGenomics()
    
    # Discover genomes
    genomes = icg._discover_genomes()
    if len(genomes) < 2:
        print("❌ Need at least 2 genomes for phylogenetic analysis")
        return False
    
    # Test phylogenetic analysis
    try:
        print("\n🔄 Running real phylogenetic analysis...")
        results = icg._real_phylogenetic_analysis(genomes[:4])  # Test with first 4 genomes
        
        print("✅ Phylogenetic Analysis Results:")
        print(f"   📊 Method: {results['method']}")
        print(f"   🌿 Bootstrap average: {results['bootstrap_avg']:.1f}%")
        print(f"   📏 Tree depth: {results['tree_depth']:.3f}")
        print(f"   🌳 Total branches: {results['total_branches']}")
        
        if results['closest_pairs']:
            print(f"   🔗 Closest pairs found: {len(results['closest_pairs'])}")
            for pair in results['closest_pairs'][:2]:
                print(f"      • {pair['genome1']} ↔ {pair['genome2']}: {pair['distance']:.3f}")
        
        if results['distant_pairs']:
            print(f"   🔗 Distant pairs found: {len(results['distant_pairs'])}")
            for pair in results['distant_pairs'][:1]:
                print(f"      • {pair['genome1']} ↔ {pair['genome2']}: {pair['distance']:.3f}")
        
        if results['newick_file']:
            print(f"   📁 Newick tree saved: {results['newick_file']}")
            
            # Verify the file was actually created
            if Path(results['newick_file']).exists():
                print("   ✅ Newick file confirmed on disk")
                
                # Show tree content
                with open(results['newick_file'], 'r') as f:
                    tree_content = f.read().strip()
                    print(f"   🌳 Tree content: {tree_content[:100]}...")
            else:
                print("   ⚠️  Newick file not found on disk")
        
        # Verify this is real analysis with actual genome names
        genome_names = [Path(g).stem for g in genomes]
        found_real_names = any(pair['genome1'] in genome_names for pair in results['closest_pairs'])
        
        if found_real_names:
            print("✅ CONFIRMED: Real analysis using actual genome names")
            return True
        else:
            print("⚠️  WARNING: May be using default/mock data")
            return False
            
    except Exception as e:
        print(f"❌ Phylogenetic analysis failed: {e}")
        return False

def test_vm_creation_with_real_data():
    """Test the enhanced VM creation wizard"""
    
    print("\n🖥️  Testing Enhanced VM Creation")
    print("=" * 40)
    
    icg = InteractiveComparativeGenomics()
    genomes = icg._discover_genomes()
    
    if not genomes:
        print("❌ No genomes found for VM creation test")
        return False
    
    try:
        base_genome = genomes[0]
        config = {'memory': '1024', 'cpus': '2'}
        
        print(f"🔄 Testing VM creation with {Path(base_genome).stem}...")
        
        # Test the enhanced VM creation
        icg._create_optimized_vm(base_genome, config)
        
        # Check if config file was created
        genome_name = Path(base_genome).stem
        config_file = f"vm_config_{genome_name}.json"
        
        if Path(config_file).exists():
            print(f"✅ VM configuration file created: {config_file}")
            
            # Read and display config details
            import json
            with open(config_file, 'r') as f:
                vm_config = json.load(f)
            
            print("📊 VM Configuration Details:")
            print(f"   🧬 Base genome: {vm_config['base_genome']['name']}")
            print(f"   📊 Gene count: {vm_config['base_genome']['gene_count']}")
            print(f"   💾 Memory allocation: {vm_config['resources']['memory_mb']} MB")
            print(f"   🖥️  CPU cores: {vm_config['resources']['cpu_cores']}")
            print(f"   ⚡ Compatible genomes: {vm_config['optimization']['compatible_genomes']}")
            
            print("✅ CONFIRMED: Real VM configuration with actual genome data")
            return True
        else:
            print("⚠️  VM configuration file not created")
            return False
            
    except Exception as e:
        print(f"❌ VM creation test failed: {e}")
        return False

def main():
    """Run all functionality tests"""
    
    print("🚀 BioXen-JCVI Real Functionality Test Suite")
    print("=" * 50)
    print("Testing the improved synteny, phylogenetic, and VM creation implementations")
    print()
    
    results = {
        'synteny': test_real_synteny_analysis(),
        'phylogenetic': test_real_phylogenetic_analysis(), 
        'vm_creation': test_vm_creation_with_real_data()
    }
    
    print(f"\n📊 Test Results Summary")
    print("=" * 30)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {test_name.replace('_', ' ').title()}")
    
    print(f"\n🎯 Overall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All functionality tests PASSED!")
        print("The synteny, phylogenetic, and VM creation features are working with real data!")
    else:
        print("⚠️  Some tests failed - check implementations")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
