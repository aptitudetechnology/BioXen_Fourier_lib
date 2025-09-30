# BioXen Execution Modal Upgrade - Phase 2: MVP Expansion

## Phase 2 Overview: Tellurium Integration (Weeks 3-4)

**Objective**: Expand the MVP foundation by integrating Tellurium for dynamic system simulation and adding pathway analysis capabilities, demonstrating real biochemical modeling.

**Duration**: 2 weeks  
**Priority**: MVP Expansion - Prove dynamic simulation capability  
**Dependencies**: Phase 1 MVP foundation complete (COBRApy + chassis integration)

---

## MVP Expansion Vision

### Core Integration Strategy
```
src/execution_modal/
├── __init__.py
├── process_executor.py      # Enhanced with Tellurium simulation support
├── tool_integrator.py       # Add Tellurium integration
├── pathway_analyzer.py      # Dynamic pathway analysis
├── mvp_demo.py              # Enhanced demo workflow
└── phase2_demo.py           # Phase 2 specific demo
```

### MVP Phase 2 Principles
1. **Dynamic Simulation**: Integrate Tellurium for time-course biochemical modeling
2. **Pathway Analysis**: Add kinetic analysis to complement COBRApy's static analysis
3. **Incremental**: Build directly on Phase 1, no breaking changes
4. **Real Biology**: Demonstrate dynamic biological processes
5. **SBML Standard**: Use standard SBML models for compatibility

---

## Week 3: Tellurium Integration

### Day 1-2: Tellurium Wrapper
- Implement minimal wrapper for Tellurium simulation engine
- Support SBML model loading and time-course simulation

### Day 3-4: Process Executor Enhancement
- Extend `process_executor.py` to route dynamic simulation requests to Tellurium
- Add integration with existing COBRApy results for comprehensive analysis

---

## Week 4: Pathway Analysis & Demo

### Day 5-6: Pathway Analyzer
- Implement `pathway_analyzer.py` for dynamic pathway analysis
- Combine static (COBRApy) and dynamic (Tellurium) results

### Day 7-8: Demo & Testing
- Create `phase2_demo.py` to demonstrate dynamic biochemical modeling
- Add test cases showing COBRApy + Tellurium integration

---

## Technical Implementation

### Tellurium Integration (`tool_integrator.py`)
```python
def simulate_dynamic_pathway(self, pathway_data: Dict[str, Any]) -> Dict[str, Any]:
    """Dynamic pathway simulation using Tellurium"""
    
    import tellurium as te
    
    # Create simple pathway model
    model_sbml = pathway_data.get("sbml_model", self._create_default_pathway())
    simulation_time = pathway_data.get("time_points", 100)
    
    # Load and simulate
    model = te.loada(model_sbml)
    result = model.simulate(0, 10, simulation_time)
    
    return {
        "simulation_type": "dynamic",
        "time_points": result[:, 0].tolist(),
        "concentrations": {f"species_{i}": result[:, i+1].tolist() 
                          for i in range(result.shape[1]-1)},
        "steady_state": result[-1, 1:].tolist(),
        "biological_output": f"Dynamic simulation complete: {simulation_time} time points"
    }

def _create_default_pathway(self) -> str:
    """Simple glycolysis-like pathway for demonstration"""
    return """
    model simple_pathway()
        // Simple glucose -> pyruvate pathway
        S1 -> S2; k1*S1;
        S2 -> S3; k2*S2;
        S3 -> S4; k3*S3;
        
        // Initial conditions
        S1 = 10; S2 = 0; S3 = 0; S4 = 0;
        
        // Rate constants
        k1 = 0.1; k2 = 0.05; k3 = 0.02;
    end
    """
```

### Enhanced Process Executor
```python
def _execute_dynamic_process(self, process_code: str, vm_context: Dict[str, Any]) -> Dict[str, Any]:
    """Execute dynamic biochemical processes"""
    
    if process_code == "simulate_pathway_dynamics":
        # Get chassis-specific parameters
        chassis_config = self._get_chassis_config(vm_context.get("biological_type", "base"))
        
        pathway_data = {
            "sbml_model": vm_context.get("pathway_model"),
            "time_points": vm_context.get("simulation_time", 100),
            "initial_conditions": chassis_config.get("metabolite_concentrations", {}),
            "chassis_constraints": chassis_config.get("constraints", {})
        }
        
        # Run Tellurium simulation
        tellurium_result = self.integrator.simulate_dynamic_pathway(pathway_data)
        
        # Optionally combine with COBRApy steady-state analysis
        if vm_context.get("include_flux_analysis", False):
            flux_result = self.integrator.simulate_flux_balance(pathway_data)
            tellurium_result["flux_analysis"] = flux_result
        
        return {
            "status": "success",
            "execution_type": "real_computation",
            "process_code": process_code,
            "simulation_results": tellurium_result,
            "biological_output": f"Dynamic pathway simulation: {len(tellurium_result['time_points'])} time points"
        }
    
    else:
        # Fallback to Phase 1 execution
        return self._execute_flux_process(process_code, vm_context)
```

### Demo Implementation (`phase2_demo.py`)
```python
"""Phase 2: Tellurium Integration Demo"""

from ..api import create_bio_vm
from .process_executor import MVPProcessExecutor

def run_phase2_demo():
    """Demonstrate Tellurium integration for dynamic simulation"""
    
    print("🧬 BioXen Phase 2: Dynamic Pathway Simulation")
    print("=" * 50)
    
    # Create VM with E. coli chassis
    vm = create_bio_vm("phase2_vm", "ecoli", "enhanced")
    vm.start()
    
    executor = MVPProcessExecutor()
    
    # Test 1: Simple pathway dynamics
    print("\n⚡ Test 1: Dynamic Pathway Simulation")
    vm_context = {
        "biological_type": "ecoli",
        "pathway_model": None,  # Use default
        "simulation_time": 50,
        "include_flux_analysis": True
    }
    
    result = executor.execute_biological_process("simulate_pathway_dynamics", vm_context)
    
    print(f"   Status: {result['status']}")
    print(f"   Type: {result['execution_type']}")
    print(f"   Output: {result['biological_output']}")
    
    # Show some simulation data
    sim_data = result['simulation_results']
    print(f"   Time points: {len(sim_data['time_points'])}")
    print(f"   Final concentrations: {sim_data['steady_state'][:3]}...")  # First 3 species
    
    # Test 2: Compare with static analysis
    if 'flux_analysis' in sim_data:
        print("\n🔬 Test 2: Static vs Dynamic Comparison")
        flux_data = sim_data['flux_analysis']
        print(f"   Static flux balance: {flux_data.get('objective_value', 'N/A')}")
        print(f"   Dynamic steady state: {sim_data['steady_state'][0]:.3f}")
    
    print("\n✅ Phase 2 Tellurium Integration Demo Complete!")

if __name__ == "__main__":
    run_phase2_demo()
```

---

## Success Criteria (MVP Phase 2)

- [ ] Tellurium integration for dynamic pathway simulation
- [ ] SBML model support and time-course analysis
- [ ] Integration with existing COBRApy functionality
- [ ] Demo script showing dynamic + static analysis
- [ ] All Phase 1 functionality preserved
- [ ] Clear foundation for Phase 3 genomic mapping

---

## Installation Requirements

```txt
# Add to requirements.txt
tellurium>=2.2.0      # Dynamic simulation engine
antimony>=2.12.0      # Model definition language
roadrunner>=2.2.0     # Simulation backend
```

---

## Ready for Phase 3

- MVP proves dynamic simulation capability
- Tellurium and COBRApy successfully integrated
- Foundation for genomic mapping and spatial simulation

---
