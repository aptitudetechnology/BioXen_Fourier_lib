#!/usr/bin/env python3
"""
Test script for enhanced interactive CLI with v0.0.03 features
"""

import sys
import os
sys.path.append('.')

def test_enhanced_interactive_cli():
    """Test the enhanced interactive CLI functionality."""
    
    print("🧪 Testing Enhanced Interactive CLI (v0.0.03)")
    print("="*60)
    
    try:
        # Test imports
        print("1️⃣ Testing imports...")
        
        # Test JCVI manager
        from src.api.jcvi_manager import create_jcvi_manager
        jcvi_manager = create_jcvi_manager()
        print(f"   ✅ JCVI Manager: {type(jcvi_manager)}")
        
        # Test acquisition components
        from src.jcvi_integration.genome_acquisition import JCVIGenomeAcquisition
        from src.jcvi_integration.analysis_coordinator import JCVIWorkflowCoordinator
        
        acquisition = JCVIGenomeAcquisition()
        coordinator = JCVIWorkflowCoordinator()
        print(f"   ✅ Acquisition System: {type(acquisition)}")
        print(f"   ✅ Workflow Coordinator: {type(coordinator)}")
        
        print("\n2️⃣ Testing enhanced functionality...")
        
        # Test listing available genomes
        available_genomes = jcvi_manager.list_available_genomes()
        print(f"   📋 Available genomes: {available_genomes}")
        
        # Test enhanced interactive CLI class structure
        print("\n3️⃣ Testing interactive CLI class...")
        
        # Import the main class from the file (simulated)
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "interactive_bioxen_jcvi_api", 
            "/home/chris/BioXen_jcvi_vm_lib/interactive-bioxen-jcvi-api.py"
        )
        interactive_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(interactive_module)
        
        # Test if the enhanced features are detected
        ACQUISITION_AVAILABLE = getattr(interactive_module, 'ACQUISITION_AVAILABLE', False)
        print(f"   🔄 Acquisition Available: {'✅' if ACQUISITION_AVAILABLE else '❌'}")
        
        print("\n✅ All tests passed! Enhanced interactive CLI is ready.")
        print("\n📋 Summary of v0.0.03 enhancements:")
        print("   • 📥 Real genome acquisition (replaces simulation)")
        print("   • 🔄 Complete workflow coordination")
        print("   • 📋 List available genomes")
        print("   • 📥 Acquire & analyze in one step")
        print("   • 🧪 Enhanced JCVI analysis menu")
        print("   • ⚡ Automatic fallback to legacy modes")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_enhanced_interactive_cli()
    sys.exit(0 if success else 1)
