# BioXen Factory Pattern API - Phase 1.1: JCVI Integration

## Overview
Phase 1.1 builds upon the completed Phase 1 API abstraction layer to integrate the extensive JCVI functionality already present in the codebase. This phase creates a unified API wrapper that exposes JCVI capabilities through the factory pattern while maintaining the robust fallback mechanisms already implemented.

## Objectives
- Expose existing JCVI integration through the API layer
- Maintain graceful fallback when JCVI unavailable  
- Integrate JCVI functionality with the biological VM factory pattern
- Preserve existing integration infrastructure and patterns

## Current JCVI Integration Assets
### Root-Level Integration Modules:
- `bioxen_jcvi_integration.py` - Main integration with graceful fallback
- `phase4_jcvi_cli_integration.py` - Advanced CLI integration for bare metal performance
- `bioxen_to_jcvi_converter.py` - Format conversion utilities

### Integration Strengths:
- ✅ Graceful fallback when JCVI unavailable
- ✅ Format conversion (.genome ↔ .fasta)
- ✅ Hardware-optimized CLI integration
- ✅ Comprehensive test coverage
- ✅ Full JCVI toolkit source included

## Phase 1.1 Implementation Plan

### 1. Create JCVI Manager (`src/api/jcvi_manager.py`)
```python
"""
JCVI Manager - Unified API access to JCVI functionality
Wraps existing integration modules for factory pattern compatibility
"""

from typing import Dict, Any, Optional, List
from ..bioxen_jcvi_integration import BioXenJCVIIntegration
from ..phase4_jcvi_cli_integration import JCVICLIIntegrator
from ..bioxen_to_jcvi_converter import BioXenToJCVIConverter

class JCVIManager:
    """Unified JCVI functionality manager for API layer"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.integration = BioXenJCVIIntegration()
        self.cli_integrator = JCVICLIIntegrator() if config.get('jcvi_cli_enabled', True) else None
        self.converter = BioXenToJCVIConverter()
        
    @property
    def available(self) -> bool:
        """Check if JCVI functionality is available"""
        return self.integration.jcvi_available
        
    def get_genome_statistics(self, genome_path: str) -> Dict[str, Any]:
        """Enhanced genome statistics with JCVI integration"""
        return self.integration.get_genome_statistics(genome_path)
        
    def run_synteny_analysis(self, genome1: str, genome2: str) -> Dict[str, Any]:
        """Run synteny analysis using JCVI CLI tools"""
        if self.cli_integrator and self.available:
            return self.cli_integrator.run_synteny_analysis(genome1, genome2)
        return {"error": "JCVI CLI integration not available"}
        
    def convert_format(self, input_path: str, output_path: str) -> bool:
        """Convert between BioXen and JCVI formats"""
        return self.converter.convert_genome(input_path, output_path)
```

### 2. Extend Biological VM with JCVI (`src/api/biological_vm.py`)
```python
# Add JCVI support to BiologicalVM base class
from .jcvi_manager import JCVIManager

class BiologicalVM(ABC):
    def __init__(self, vm_id: str, config: Dict[str, Any]):
        # ... existing initialization ...
        self.jcvi = JCVIManager(config) if config.get('enable_jcvi', True) else None
        
    @property
    def jcvi_available(self) -> bool:
        """Check if JCVI functionality is available for this VM"""
        return self.jcvi is not None and self.jcvi.available

# Extend concrete implementations
class BasicBiologicalVM(BiologicalVM):
    def analyze_genome(self, genome_path: str) -> Dict[str, Any]:
        """Enhanced genome analysis with optional JCVI integration"""
        if self.jcvi_available:
            return self.jcvi.get_genome_statistics(genome_path)
        return self._basic_genome_analysis(genome_path)

class XCPngBiologicalVM(BiologicalVM):
    def run_comparative_analysis(self, genome1: str, genome2: str) -> Dict[str, Any]:
        """Comparative analysis with JCVI synteny tools"""
        if self.jcvi_available:
            return self.jcvi.run_synteny_analysis(genome1, genome2)
        return self._basic_comparative_analysis(genome1, genome2)
```

### 3. Update Factory Function (`src/api/factory.py`)
```python
# Add JCVI configuration to factory
def create_biological_vm(vm_type: str = "basic", config: Optional[Dict[str, Any]] = None) -> BiologicalVM:
    if config is None:
        config = {}
    
    # Enable JCVI by default
    config.setdefault('enable_jcvi', True)
    config.setdefault('jcvi_cli_enabled', True)
    
    if vm_type == "basic":
        return BasicBiologicalVM("basic_vm", config)
    elif vm_type == "xcpng":
        return XCPngBiologicalVM("xcpng_vm", config)
    elif vm_type == "jcvi_optimized":
        # New VM type optimized for JCVI workflows
        config['jcvi_cli_enabled'] = True
        config['hardware_optimization'] = True
        return XCPngBiologicalVM("jcvi_optimized_vm", config)
    else:
        raise ValueError(f"Unknown VM type: {vm_type}")
```

### 4. Integration with Configuration Manager (`src/api/config_manager.py`)
```python
# Add JCVI configuration schema
JCVI_CONFIG_SCHEMA = {
    'enable_jcvi': bool,
    'jcvi_cli_enabled': bool,
    'hardware_optimization': bool,
    'fallback_mode': bool,
    'jcvi_work_dir': str,
    'jcvi_output_dir': str
}

class ConfigManager:
    def validate_jcvi_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate JCVI-specific configuration"""
        jcvi_config = config.get('jcvi', {})
        
        # Apply defaults
        jcvi_config.setdefault('enable_jcvi', True)
        jcvi_config.setdefault('jcvi_cli_enabled', True)
        jcvi_config.setdefault('hardware_optimization', False)
        jcvi_config.setdefault('fallback_mode', True)
        
        return jcvi_config
```

### 5. Resource Manager Integration (`src/api/resource_manager.py`)
```python
# Add JCVI process tracking
class ResourceManager:
    def track_jcvi_process(self, process_id: str, command: str) -> bool:
        """Track JCVI CLI processes for resource management"""
        self.active_processes[process_id] = {
            'type': 'jcvi_cli',
            'command': command,
            'started_at': datetime.now(),
            'resource_intensive': True
        }
        return True
        
    def get_jcvi_resource_usage(self) -> Dict[str, Any]:
        """Get resource usage for JCVI processes"""
        jcvi_processes = {k: v for k, v in self.active_processes.items() 
                         if v.get('type') == 'jcvi_cli'}
        return {
            'active_jcvi_processes': len(jcvi_processes),
            'processes': jcvi_processes
        }
```

## Implementation Tasks

### Task 1: Core JCVI Manager Implementation
- [ ] Create `src/api/jcvi_manager.py`
- [ ] Implement wrapper for `BioXenJCVIIntegration`
- [ ] Add CLI integration wrapper
- [ ] Include format conversion utilities

### Task 2: Biological VM Integration
- [ ] Extend `BiologicalVM` base class with JCVI support
- [ ] Update `BasicBiologicalVM` with JCVI genome analysis
- [ ] Enhance `XCPngBiologicalVM` with comparative analysis
- [ ] Add fallback methods for when JCVI unavailable

### Task 3: Factory Pattern Enhancement
- [ ] Update factory function to include JCVI configuration
- [ ] Add new `jcvi_optimized` VM type
- [ ] Ensure proper configuration passing

### Task 4: Configuration and Resource Management
- [ ] Add JCVI configuration schema to `ConfigManager`
- [ ] Implement JCVI process tracking in `ResourceManager`
- [ ] Add resource usage monitoring for JCVI operations

### Task 5: Testing and Validation
- [ ] Create `test_jcvi_api_integration.py`
- [ ] Test graceful fallback when JCVI unavailable
- [ ] Validate factory pattern with JCVI functionality
- [ ] Performance testing with hardware optimization

## Usage Examples

### Basic JCVI Integration
```python
from src.api import create_biological_vm

# Create VM with JCVI enabled (default)
vm = create_biological_vm(vm_type="basic")

# Check JCVI availability
if vm.jcvi_available:
    stats = vm.analyze_genome("example.genome")
    print(f"Enhanced stats: {stats}")
```

### Advanced JCVI Workflows
```python
# Create JCVI-optimized VM
vm = create_biological_vm(
    vm_type="jcvi_optimized", 
    config={
        'jcvi_cli_enabled': True,
        'hardware_optimization': True
    }
)

# Run comparative genomics
results = vm.run_comparative_analysis("genome1.fasta", "genome2.fasta")
```

### Graceful Fallback Testing
```python
# Create VM with JCVI disabled
vm = create_biological_vm(
    vm_type="basic",
    config={'enable_jcvi': False}
)

# Should fall back to basic analysis
stats = vm.analyze_genome("example.genome")  # Uses basic BioXen analysis
```

## Success Criteria
- [ ] JCVI functionality accessible through factory pattern API
- [ ] Graceful fallback maintained when JCVI unavailable
- [ ] Existing integration infrastructure preserved and enhanced
- [ ] Performance optimization from Phase 4 CLI integration exposed
- [ ] Comprehensive test coverage for new API integration
- [ ] Documentation updated with JCVI API usage patterns

## Dependencies
- Completed Phase 1 API abstraction layer
- Existing JCVI integration modules (`bioxen_jcvi_integration.py`, etc.)
- JCVI toolkit availability (graceful fallback when missing)

## Timeline
- **Week 1**: Core JCVI Manager and Biological VM integration
- **Week 2**: Factory pattern enhancement and configuration management
- **Week 3**: Resource management integration and testing
- **Week 4**: Documentation, validation, and performance optimization

---
*Phase 1.1 Implementation Plan - Generated September 4, 2025*
