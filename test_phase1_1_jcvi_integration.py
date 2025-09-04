#!/usr/bin/env python3
"""
Test script for Phase 1.1 JCVI Integration

This script tests the JCVI integration functionality added to the 
factory pattern API, including graceful fallback mechanisms.
"""

import sys
import os
from pathlib import Path

# Add the src directory to Python path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

def test_jcvi_manager():
    """Test JCVI Manager functionality."""
    print("🧬 Testing JCVI Manager...")
    
    try:
        from src.api.jcvi_manager import JCVIManager, create_jcvi_manager
        
        # Test with default config
        config = {
            'jcvi_cli_enabled': True,
            'hardware_optimization': False,
            'fallback_mode': True
        }
        
        manager = create_jcvi_manager(config)
        print(f"   ✅ JCVI Manager created successfully")
        
        # Test status
        status = manager.get_status()
        print(f"   📊 JCVI Status: {status}")
        
        # Test availability check
        print(f"   🔍 JCVI Available: {manager.available}")
        print(f"   🔍 CLI Available: {manager.cli_available}")
        print(f"   🔍 Converter Available: {manager.converter_available}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ JCVI Manager test failed: {e}")
        return False

def test_basic_vm_with_jcvi():
    """Test Basic Biological VM with JCVI integration."""
    print("\n🔬 Testing Basic VM with JCVI...")
    
    try:
        from src.api import create_biological_vm
        
        # Create basic VM with JCVI enabled
        vm = create_biological_vm(vm_type="basic")
        print(f"   ✅ Basic VM created: {vm.vm_id}")
        print(f"   🧬 Biological Type: {vm.get_biological_type()}")
        print(f"   🏗️ VM Type: {vm.get_vm_type()}")
        
        # Test JCVI availability
        print(f"   🔍 JCVI Available: {vm.jcvi_available}")
        
        if vm.jcvi_available:
            jcvi_status = vm.get_jcvi_status()
            print(f"   📊 JCVI Status: {jcvi_status}")
        
        # Test genome analysis (should fall back gracefully)
        print("   🧪 Testing genome analysis...")
        
        # Create a dummy genome file for testing
        test_genome_path = "test_genome.fasta"
        with open(test_genome_path, 'w') as f:
            f.write(">test_genome\nATGCATGCATGC\n")
        
        try:
            analysis_result = vm.analyze_genome(test_genome_path)
            print(f"   📈 Analysis Result: {analysis_result}")
        finally:
            # Cleanup test file
            if os.path.exists(test_genome_path):
                os.remove(test_genome_path)
        
        return True
        
    except Exception as e:
        print(f"   ❌ Basic VM test failed: {e}")
        return False

def test_jcvi_optimized_vm():
    """Test JCVI-optimized VM creation."""
    print("\n🚀 Testing JCVI-Optimized VM...")
    
    try:
        from src.api import create_biological_vm
        
        # Create JCVI-optimized VM
        config = {
            'biological_type': 'syn3a',
            'vm_id': 'test_jcvi_optimized'
        }
        
        vm = create_biological_vm(vm_type="jcvi_optimized", config=config)
        print(f"   ✅ JCVI-Optimized VM created: {vm.vm_id}")
        print(f"   🧬 Biological Type: {vm.get_biological_type()}")
        print(f"   🏗️ VM Type: {vm.get_vm_type()}")
        
        # Check JCVI configuration
        jcvi_status = vm.get_jcvi_status()
        print(f"   📊 JCVI Status: {jcvi_status}")
        
        # Test hardware optimization status
        if hasattr(vm, 'get_hardware_optimization_status'):
            hw_status = vm.get_hardware_optimization_status()
            print(f"   ⚡ Hardware Status: {hw_status}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ JCVI-Optimized VM test failed: {e}")
        return False

def test_comparative_analysis():
    """Test comparative analysis functionality."""
    print("\n🔬 Testing Comparative Analysis...")
    
    try:
        from src.api import create_biological_vm
        
        # Create XCPng VM for comparative analysis
        vm = create_biological_vm(vm_type="xcpng", config={'xcpng_config': {}})
        print(f"   ✅ XCPng VM created: {vm.vm_id}")
        
        # Create dummy genome files
        genome1_path = "test_genome1.fasta"
        genome2_path = "test_genome2.fasta"
        
        with open(genome1_path, 'w') as f:
            f.write(">genome1\nATGCATGCATGCTTT\n")
            
        with open(genome2_path, 'w') as f:
            f.write(">genome2\nATGCATGCATGCAAA\n")
        
        try:
            # Test comparative analysis
            if hasattr(vm, 'run_comparative_analysis'):
                result = vm.run_comparative_analysis(genome1_path, genome2_path)
                print(f"   📊 Comparative Analysis: {result}")
            else:
                print("   ⚠️ Comparative analysis method not available")
                
        finally:
            # Cleanup test files
            for path in [genome1_path, genome2_path]:
                if os.path.exists(path):
                    os.remove(path)
        
        return True
        
    except Exception as e:
        print(f"   ❌ Comparative analysis test failed: {e}")
        return False

def test_convenience_functions():
    """Test convenience functions."""
    print("\n🎯 Testing Convenience Functions...")
    
    try:
        from src.api import quick_start_jcvi_vm
        
        # Test quick start JCVI VM
        vm = quick_start_jcvi_vm(biological_type="syn3a")
        print(f"   ✅ Quick JCVI VM created: {vm.vm_id}")
        print(f"   🧬 Biological Type: {vm.get_biological_type()}")
        print(f"   🔍 JCVI Available: {vm.jcvi_available}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Convenience functions test failed: {e}")
        return False

def main():
    """Run all Phase 1.1 tests."""
    print("🧬 BioXen Phase 1.1 JCVI Integration Test Suite")
    print("=" * 50)
    
    tests = [
        test_jcvi_manager,
        test_basic_vm_with_jcvi,
        test_jcvi_optimized_vm,
        test_comparative_analysis,
        test_convenience_functions
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All Phase 1.1 JCVI integration tests passed!")
        return True
    else:
        print("⚠️ Some tests failed - check implementation")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
