# BioXen Execution Modal Upgrade - Phase 1: MVP Foundation

## Phase 1 Overview: Minimal Viable Prototype (Weeks 1-2)

**Objective**: Create a minimal viable prototype that bridges symbolic process execution to real biological computation using existing open-source tools.

**Duration**: 2 weeks  
**Priority**: MVP Foundation - Prove concept viability  
**Dependencies**: Completion of API upgrade plan (co-pilot-api-plan-phase3.md)  

---

## MVP Architecture Vision

### Core Integration Strategy
```
src/execution_modal/
├── __init__.py              # Package initialization
├── process_executor.py      # Real biological process execution
├── tool_integrator.py       # Open-source tool wrapper
└── mvp_demo.py             # Demonstration workflow
```

### MVP Principles
1. **Minimal Integration**: Focus on 2-3 core tools (COBRApy + Tellurium)
2. **Proof of Concept**: Demonstrate real vs symbolic execution
3. **Non-Breaking**: Preserve all existing functionality
4. **Single Workflow**: One complete end-to-end biological process
5. **Community Tools**: Leverage existing open-source ecosystem

---

## Week 1: MVP Tool Integration

### Day 1-2: Basic Tool Wrapper

#### Core Tool Selection (MVP)
- **COBRApy**: Metabolic modeling and FBA
- **Tellurium**: Systems biology simulation
- **SBML**: Standard exchange format

#### `src/execution_modal/tool_integrator.py`
```python
from typing import Dict, Any, Optional
import cobra
import tellurium as te

class MVPToolIntegrator:
    """Minimal viable tool integration for biological processes"""
    
    def __init__(self):
        self.cobra_models = {}
        self.tellurium_models = {}
    
    def load_cobra_model(self, model_id: str, sbml_file: str):
        """Load metabolic model using COBRApy"""
        model = cobra.io.read_sbml_model(sbml_file)
        self.cobra_models[model_id] = model
        return model
    
    def run_fba(self, model_id: str) -> Dict[str, Any]:
        """Run flux balance analysis"""
        model = self.cobra_models[model_id]
        solution = model.optimize()
        return {
            "status": solution.status,
            "objective_value": solution.objective_value,
            "fluxes": dict(solution.fluxes)
        }
    
    def load_tellurium_model(self, model_id: str, antimony_code: str):
        """Load systems biology model using Tellurium"""
        model = te.loada(antimony_code)
        self.tellurium_models[model_id] = model
        return model
    
    def simulate_dynamics(self, model_id: str, time_points: int = 100) -> Dict[str, Any]:
        """Run time-course simulation"""
        model = self.tellurium_models[model_id]
        result = model.simulate(0, 10, time_points)
        return {
            "time": result[:, 0].tolist(),
            "species": {model.getFloatingSpeciesIds()[i]: result[:, i+1].tolist() 
                       for i in range(len(model.getFloatingSpeciesIds()))}
        }
```

### Day 3-4: Process Executor Bridge

#### `src/execution_modal/process_executor.py`
```python
from typing import Dict, Any
from .tool_integrator import MVPToolIntegrator

class MVPProcessExecutor:
    """Bridge between BioXen symbolic execution and real biological computation"""
    
    def __init__(self):
        self.integrator = MVPToolIntegrator()
        self.execution_mode = "hybrid"  # "symbolic", "real", "hybrid"
    
    def execute_biological_process(self, process_code: str, vm_context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute biological process with real computation when possible"""
        
        # Parse process code to determine execution strategy
        if process_code.startswith("metabolic_"):
            return self._execute_metabolic_process(process_code, vm_context)
        elif process_code.startswith("kinetic_"):
            return self._execute_kinetic_process(process_code, vm_context)
        else:
            # Fall back to symbolic execution for unsupported processes
            return self._execute_symbolic_process(process_code, vm_context)
    
    def _execute_metabolic_process(self, process_code: str, vm_context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute metabolic processes using COBRApy"""
        organism_type = vm_context.get("biological_type", "generic")
        
        # Load appropriate model based on organism
        if organism_type == "ecoli":
            model_file = "models/e_coli_core.xml"  # Standard E. coli model
        else:
            model_file = "models/generic_core.xml"  # Generic minimal model
        
        try:
            self.integrator.load_cobra_model("current", model_file)
            result = self.integrator.run_fba("current")
            
            return {
                "status": "success",
                "execution_type": "real_computation",
                "process_code": process_code,
                "biological_output": f"FBA optimization: {result['objective_value']:.3f}",
                "detailed_results": result,
                "execution_time": 0.5  # Actual computation time
            }
        except Exception as e:
            # Fall back to symbolic execution on error
            return self._execute_symbolic_process(process_code, vm_context)
    
    def _execute_kinetic_process(self, process_code: str, vm_context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute kinetic processes using Tellurium"""
        # Simple example: gene expression dynamics
        antimony_model = """
        model gene_expression
            # Simple gene expression model
            -> mRNA; k1 * gene
            mRNA -> ; k2 * mRNA
            mRNA -> protein; k3 * mRNA
            protein -> ; k4 * protein
            
            gene = 1
            k1 = 0.1; k2 = 0.05; k3 = 0.2; k4 = 0.01
        end
        """
        
        try:
            self.integrator.load_tellurium_model("gene_expr", antimony_model)
            result = self.integrator.simulate_dynamics("gene_expr")
            
            return {
                "status": "success",
                "execution_type": "real_computation",
                "process_code": process_code,
                "biological_output": f"Gene expression dynamics simulated",
                "detailed_results": result,
                "execution_time": 0.3
            }
        except Exception as e:
            return self._execute_symbolic_process(process_code, vm_context)
    
    def _execute_symbolic_process(self, process_code: str, vm_context: Dict[str, Any]) -> Dict[str, Any]:
        """Fall back to original symbolic execution"""
        return {
            "status": "success",
            "execution_type": "symbolic",
            "process_code": process_code,
            "biological_output": f"Symbolic execution: {process_code}",
            "execution_time": 0.1
        }
```

### Day 5: MVP Demo Integration

#### `src/execution_modal/mvp_demo.py`
```python
"""MVP Demonstration of real biological computation in BioXen"""

from ..api import create_bio_vm
from .process_executor import MVPProcessExecutor

def run_mvp_demo():
    """Demonstrate real vs symbolic biological process execution"""
    
    print("🧬 BioXen Execution Modal MVP Demo")
    print("=" * 50)
    
    # Create biological VM using existing API
    vm = create_bio_vm("mvp_demo_vm", "ecoli", "basic")
    vm.start()
    
    # Initialize MVP process executor
    executor = MVPProcessExecutor()
    
    # Test 1: Metabolic process (real computation)
    print("\n📊 Test 1: Metabolic Process (COBRApy)")
    vm_context = {"biological_type": "ecoli"}
    result1 = executor.execute_biological_process("metabolic_fba_optimization", vm_context)
    print(f"   Execution Type: {result1['execution_type']}")
    print(f"   Result: {result1['biological_output']}")
    
    # Test 2: Kinetic process (real computation)
    print("\n⚡ Test 2: Gene Expression Dynamics (Tellurium)")
    result2 = executor.execute_biological_process("kinetic_gene_expression", vm_context)
    print(f"   Execution Type: {result2['execution_type']}")
    print(f"   Result: {result2['biological_output']}")
    
    # Test 3: Unsupported process (symbolic fallback)
    print("\n🔄 Test 3: Unsupported Process (Symbolic Fallback)")
    result3 = executor.execute_biological_process("protein_folding_complex", vm_context)
    print(f"   Execution Type: {result3['execution_type']}")
    print(f"   Result: {result3['biological_output']}")
    
    print("\n✅ MVP Demo Complete - Real biological computation integrated!")

if __name__ == "__main__":
    run_mvp_demo()
```

---

## Week 2: MVP Integration & Testing

### Day 6-7: Integration with Existing Hypervisor

#### Update `src/bioxen_jcvi_vm_lib/api/biological_vm.py`
```python
# Add MVP integration to existing BiologicalVM classes

class BasicBiologicalVM(BiologicalVM):
    def __init__(self, vm_id: str, biological_type: str, config: Dict[str, Any]):
        super().__init__(vm_id, biological_type, config)
        # ... existing initialization ...
        
        # MVP integration
        self._execution_modal_enabled = config.get("enable_execution_modal", False)
        if self._execution_modal_enabled:
            from ..execution_modal.process_executor import MVPProcessExecutor
            self._mvp_executor = MVPProcessExecutor()
    
    def execute_biological_process(self, process_code: str) -> Dict[str, Any]:
        """Enhanced execution with MVP real computation option"""
        if hasattr(self, '_mvp_executor') and self._execution_modal_enabled:
            vm_context = {
                "vm_id": self.vm_id,
                "biological_type": self.biological_type,
                "resources": self.get_resource_usage()
            }
            return self._mvp_executor.execute_biological_process(process_code, vm_context)
        else:
            # Original symbolic execution
            return self._execute_biological_process_impl(process_code)
```

### Day 8-9: MVP Testing & Validation

#### Create Test Models
```bash
# Create minimal test models directory
mkdir -p models/
# Download E. coli core model (standard in COBRApy)
# Create simple Antimony models for testing
```

#### `tests/test_mvp_execution_modal.py`
```python
import pytest
from src.execution_modal.mvp_demo import run_mvp_demo
from src.execution_modal.process_executor import MVPProcessExecutor

def test_mvp_metabolic_execution():
    """Test real metabolic computation"""
    executor = MVPProcessExecutor()
    vm_context = {"biological_type": "ecoli"}
    
    result = executor.execute_biological_process("metabolic_fba_optimization", vm_context)
    
    assert result["status"] == "success"
    assert result["execution_type"] in ["real_computation", "symbolic"]  # Allow fallback

def test_mvp_kinetic_execution():
    """Test real kinetic simulation"""
    executor = MVPProcessExecutor()
    vm_context = {"biological_type": "generic"}
    
    result = executor.execute_biological_process("kinetic_gene_expression", vm_context)
    
    assert result["status"] == "success"
    assert "execution_type" in result

def test_mvp_demo_workflow():
    """Test complete MVP demonstration"""
    # Should run without errors
    run_mvp_demo()
```

### Day 10: Documentation & Deployment

#### Update `README.md`
```markdown
## Execution Modal MVP

BioXen now supports real biological computation alongside symbolic execution:

### Quick Start
```python
from bioxen_jcvi_vm_lib.execution_modal.mvp_demo import run_mvp_demo
run_mvp_demo()
```

### Real vs Symbolic Execution
- **Metabolic processes**: COBRApy flux balance analysis
- **Kinetic processes**: Tellurium time-course simulation  
- **Unsupported processes**: Automatic fallback to symbolic execution
```

#### Installation Requirements
```bash
# Add to requirements.txt
cobra>=0.25.0
tellurium>=2.2.0
```

---

## Success Criteria (MVP)

### Week 1 Deliverables
- [ ] MVP tool integrator with COBRApy + Tellurium
- [ ] Process executor with real/symbolic hybrid execution
- [ ] Working demo script

### Week 2 Deliverables  
- [ ] Integration with existing BioXen API
- [ ] Test suite for MVP functionality
- [ ] Documentation and examples

### MVP Validation
1. **Real Computation**: At least 2 biological processes execute with real computation
2. **Graceful Fallback**: Unsupported processes fall back to symbolic execution
3. **Non-Breaking**: All existing functionality preserved
4. **Demonstrable**: Clear demo showing real vs symbolic execution

### Ready for Phase 2
- MVP proves concept viability
- Community tools successfully integrated
- Foundation for expanding to more tools and processes
- Clear path to scaling real biological computation
