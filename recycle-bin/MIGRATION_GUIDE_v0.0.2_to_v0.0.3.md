# BioXen JCVI VM Library - Migration Guide v0.0.2 → v0.0.3

**Date:** September 4, 2025  
**Library Version:** bioxen-jcvi-vm-lib v0.0.3  
**Migration Status:** 🟡 BREAKING CHANGES - Migration Required  

## Overview

Version 0.0.3 introduces significant enhancements to JCVI integration with some breaking changes to improve API consistency and functionality. This guide helps you migrate from v0.0.2 to v0.0.3.

## 🚨 Breaking Changes

### 1. BioResourceManager Constructor Change

**v0.0.2 (Old):**
```python
from bioxen_jcvi_vm_lib.api import BioResourceManager

# This worked in v0.0.2
resource_manager = BioResourceManager()
```

**v0.0.3 (New):**
```python
from bioxen_jcvi_vm_lib.api import BioResourceManager

# Option 1: Provide VM at initialization
resource_manager = BioResourceManager(vm=my_vm)

# Option 2: Create standalone and bind later (NEW)
resource_manager = BioResourceManager()  # Now works again!
resource_manager.bind_vm(my_vm)  # Bind when needed
```

**Migration Action:** ✅ Fixed in v0.0.3 - Both patterns now work

### 2. Enhanced JCVI Integration Module Structure

**v0.0.2 (Old):**
```python
# This import pattern no longer works
from bioxen_jcvi_integration import BioXenJCVIIntegration
```

**v0.0.3 (New):**
```python
# Use the enhanced integration structure
from src.jcvi_integration.genome_acquisition import JCVIGenomeAcquisition
from src.jcvi_integration.analysis_coordinator import JCVIWorkflowCoordinator
from src.api.jcvi_manager import create_jcvi_manager

# Or use the factory function (recommended)
jcvi_manager = create_jcvi_manager()
```

**Migration Action:** Update import statements to use new enhanced modules

## 🆕 New Features in v0.0.3

### 1. Real Genome Acquisition

**New Capability:**
```python
from src.api.jcvi_manager import create_jcvi_manager

jcvi_manager = create_jcvi_manager()

# List available genomes
available = jcvi_manager.list_available_genomes()
print(available)  # Shows 4 minimal genomes

# Acquire real genome data
result = jcvi_manager.acquire_genome('mycoplasma_genitalium')
if result['status'] == 'success':
    print(f"Genome files: {result['jcvi_ready_files']}")
```

### 2. Complete Workflow Coordination

**New Capability:**
```python
# Run complete acquisition + analysis workflow
genome_list = ['mycoplasma_genitalium', 'mycoplasma_pneumoniae']
workflow_result = jcvi_manager.run_complete_workflow(
    genome_keys=genome_list,
    analysis_type='synteny'
)
```

### 3. Enhanced Interactive CLI

**New Capability:**
```python
# Interactive CLI now includes acquisition features
python3 interactive-bioxen-jcvi-api.py

# New menu options:
# - "📥 Acquire Genome (v0.0.03)"
# - "🔄 Complete Workflow (v0.0.03)"
```

## 📋 Step-by-Step Migration

### Step 1: Update Installation

```bash
# Remove old version
pip uninstall bioxen-jcvi-vm-lib

# Install new version
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple bioxen-jcvi-vm-lib==0.0.3
```

### Step 2: Update BioResourceManager Usage

**Before (v0.0.2):**
```python
from bioxen_jcvi_vm_lib.api import BioResourceManager

def old_pattern():
    resource_manager = BioResourceManager()  # Worked in v0.0.2
    # ... use resource_manager
```

**After (v0.0.3):**
```python
from bioxen_jcvi_vm_lib.api import BioResourceManager

def new_pattern_option1(vm):
    # Option 1: Provide VM at initialization
    resource_manager = BioResourceManager(vm=vm)
    # ... use resource_manager

def new_pattern_option2():
    # Option 2: Standalone initialization (restored in v0.0.3)
    resource_manager = BioResourceManager()  # Now works again!
    # Later, when you have a VM:
    resource_manager.bind_vm(my_vm)
    # ... use resource_manager
```

### Step 3: Update JCVI Integration Usage

**Before (v0.0.2):**
```python
# This import pattern is deprecated
try:
    from bioxen_jcvi_integration import BioXenJCVIIntegration
    integration = BioXenJCVIIntegration()
except ImportError:
    print("JCVI integration not available")
```

**After (v0.0.3):**
```python
# Use the enhanced factory pattern
from src.api.jcvi_manager import create_jcvi_manager

try:
    jcvi_manager = create_jcvi_manager()
    if jcvi_manager.available:
        # Enhanced capabilities available
        available_genomes = jcvi_manager.list_available_genomes()
        # ... use enhanced features
    else:
        print("JCVI integration running in fallback mode")
except Exception as e:
    print(f"JCVI integration not available: {e}")
```

### Step 4: Leverage New Acquisition Features

**New in v0.0.3:**
```python
from src.api.jcvi_manager import create_jcvi_manager

def enhanced_workflow():
    jcvi_manager = create_jcvi_manager()
    
    # 1. List available genomes
    genomes = jcvi_manager.list_available_genomes()
    print(f"Available: {list(genomes.keys())}")
    
    # 2. Acquire specific genomes
    for genome_key in ['mycoplasma_genitalium', 'carsonella_ruddii']:
        result = jcvi_manager.acquire_genome(genome_key)
        if result['status'] == 'success':
            print(f"✅ Acquired {genome_key}")
        else:
            print(f"❌ Failed to acquire {genome_key}: {result['error']}")
    
    # 3. Run complete workflow
    workflow_result = jcvi_manager.run_complete_workflow(
        genome_keys=['mycoplasma_genitalium', 'carsonella_ruddii'],
        analysis_type='comprehensive'
    )
    
    if workflow_result['status'] == 'completed':
        print("✅ Complete workflow finished")
        print(f"Analysis results: {workflow_result['analysis_results']}")
    else:
        print(f"❌ Workflow failed: {workflow_result.get('error', 'Unknown error')}")
```

## 🔄 Compatibility Matrix

| Feature | v0.0.1 | v0.0.2 | v0.0.3 | Migration Required |
|---------|--------|--------|--------|--------------------|
| Core Hypervisor | ✅ | ✅ | ✅ | No |
| Factory Pattern API | ✅ | ✅ | ✅ | No |
| BioResourceManager() | ✅ | ✅ | ✅ | No (fixed in v0.0.3) |
| BioResourceManager(vm) | ❌ | ❌ | ✅ | Optional |
| JCVI Integration | ⚠️ | ⚠️ | ✅ | Yes (import changes) |
| Genome Acquisition | ❌ | ❌ | ✅ | New feature |
| Complete Workflows | ❌ | ❌ | ✅ | New feature |

## ⚠️ Known Issues and Workarounds

### Issue 1: Installation Dependencies

**Problem:** Some environments may have dependency conflicts
**Workaround:**
```bash
pip install --no-deps bioxen-jcvi-vm-lib==0.0.3
pip install -r requirements.txt  # Install dependencies separately
```

### Issue 2: JCVI Tool Dependencies

**Problem:** Some JCVI features require external tools
**Solution:**
```bash
# Install required JCVI dependencies
pip install ncbi-genome-download
pip install jcvi  # If needed for advanced analysis
```

## 🧪 Testing Your Migration

### Quick Validation Script

```python
#!/usr/bin/env python3
"""
Quick validation script for v0.0.3 migration
"""

def test_migration():
    print("🧪 Testing v0.0.3 Migration...")
    
    try:
        # Test 1: Core imports
        from src.hypervisor.core import BioXenHypervisor
        from src.api import create_bio_vm
        print("✅ Core imports working")
        
        # Test 2: Resource manager compatibility
        from src.api.resource_manager import BioResourceManager
        resource_manager = BioResourceManager()  # Should work now
        print("✅ BioResourceManager compatibility fixed")
        
        # Test 3: Enhanced JCVI manager
        from src.api.jcvi_manager import create_jcvi_manager
        jcvi_manager = create_jcvi_manager()
        available_genomes = jcvi_manager.list_available_genomes()
        print(f"✅ Enhanced JCVI manager: {len(available_genomes)} genomes available")
        
        # Test 4: New acquisition feature
        if available_genomes:
            first_genome = list(available_genomes.keys())[0]
            result = jcvi_manager.acquire_genome(first_genome)
            print(f"✅ Genome acquisition test: {result['status']}")
        
        print("\n🎉 Migration validation successful!")
        return True
        
    except Exception as e:
        print(f"❌ Migration validation failed: {e}")
        return False

if __name__ == "__main__":
    test_migration()
```

## 📚 Additional Resources

### Documentation Updates
- [Enhanced Specification Document v0.0.3](specification-document-bioxen_jcvi_vm_lib_ver0.0.03.md)
- [Interactive CLI Enhancement Report](interactive-cli-v0.0.03-enhancement-report.md)
- [Complete API Reference](README.md)

### Getting Help
- **Integration Issues:** Check the validation script above
- **Feature Questions:** Refer to the enhanced specification document
- **Bug Reports:** Include version information and error details

## 🎯 Migration Checklist

- [ ] **Update installation** to v0.0.3
- [ ] **Test BioResourceManager** initialization (should work without VM)
- [ ] **Update JCVI imports** to use `create_jcvi_manager()` factory
- [ ] **Test core functionality** with existing code
- [ ] **Explore new acquisition features** for enhanced workflows
- [ ] **Update interactive CLI usage** to leverage new menu options
- [ ] **Run migration validation script** to confirm everything works
- [ ] **Update documentation** and code comments for team members

## 🚀 Recommended Next Steps

1. **Start with basic migration** - Get existing code working with v0.0.3
2. **Gradually adopt new features** - Begin with `list_available_genomes()`
3. **Leverage complete workflows** - Use `run_complete_workflow()` for comprehensive analysis
4. **Explore interactive enhancements** - Try the enhanced CLI features

The v0.0.3 enhancement provides a solid foundation for production-grade JCVI workflows while maintaining compatibility with existing patterns. The migration effort is moderate and the new capabilities significantly enhance the library's value for bioinformatics applications.

---

**Migration Guide Version:** 1.0  
**Last Updated:** September 4, 2025  
**Next Review:** Upon v0.0.4 release
