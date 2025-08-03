#!/usr/bin/env python3
"""
Quick test for the genome builder fix
"""

import sys
import os

# Add src directory to Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(script_dir, 'src')
sys.path.insert(0, src_dir)

def test_genome_builder_fix():
    """Test that the genome builder import issue is fixed"""
    print("🧬 Testing Genome Builder Fix...")
    
    try:
        from genome.syn3a import VMImageBuilder, Syn3ATemplate
        
        # Test Syn3A template
        template = Syn3ATemplate()
        genome = template.get_genome()
        print(f"  ✅ Syn3A genome loaded: {len(genome.genes)} genes")
        
        # Test VM image builder (this was failing before)
        builder = VMImageBuilder()
        config = {"isolation_level": "high"}
        vm_image = builder.build_vm_image("test-vm", config)
        
        print(f"  ✅ VM image built successfully: {len(vm_image['genome'].genes)} genes")
        print(f"      Genome size: {vm_image['genome'].total_size} bp")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_genome_builder_fix()
    if success:
        print("\n🎉 Genome builder fix successful!")
        print("You can now run the full test suite again with: python3 test_bioxen.py")
    else:
        print("\n❌ Fix didn't work, there may be other issues")
