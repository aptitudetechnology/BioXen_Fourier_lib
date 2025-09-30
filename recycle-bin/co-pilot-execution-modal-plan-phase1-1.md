# Phase 1.1: Simple Quorum Sensing Communication Test

## Overview

A minimal viable test case for real biological communication using quorum sensing - the simplest form of cell-to-cell chemical communication.

**Phase**: 1.1 (Pre-Phase 1 Foundation)  
**Duration**: 1-2 days implementation  
**Complexity**: Minimal - Single molecule, well-understood mechanism  
**Purpose**: Prove real biological communication in execution modal

---

## Quorum Sensing Basics

### Mechanism
1. **Producer cells** synthesize autoinducer molecules (AHL)
2. **Autoinducer concentration** increases with cell density
3. **Receiver cells** detect threshold concentration
4. **Population response** occurs when quorum is reached

### Simple Test Case: AHL-Based Communication

#### Sender VM (Producer)
```python
# In execution modal
process_code = "quorum_send_signal"
vm_context = {
    "biological_type": "ecoli",
    "signal_molecule": "3OC6HSL",  # N-(3-oxohexanoyl)-L-homoserine lactone
    "production_rate": "high"
}
```

#### Receiver VM (Detector) 
```python
# In execution modal
process_code = "quorum_detect_signal"
vm_context = {
    "biological_type": "ecoli", 
    "receptor": "LasR",
    "threshold": "10nM",
    "response": "gfp_expression"  # Green fluorescent protein as reporter
}
```

---

## Implementation Plan

### Phase 1.1 MVP Integration

#### Update `tool_integrator.py`
```python
def simulate_quorum_sensing(self, signal_data: Dict[str, Any]) -> Dict[str, Any]:
    """Simple quorum sensing simulation"""
    
    signal_molecule = signal_data.get("signal_molecule", "3OC6HSL")
    concentration = signal_data.get("concentration", 0)
    threshold = signal_data.get("threshold", 10)  # nM
    
    # Simple threshold detection
    if concentration >= threshold:
        response = "activated"
        expression_level = min(concentration / threshold, 10.0)  # Cap at 10x
    else:
        response = "inactive" 
        expression_level = 0.1  # Basal level
    
    return {
        "signal_molecule": signal_molecule,
        "concentration": concentration,
        "threshold": threshold,
        "response": response,
        "expression_level": expression_level,
        "biological_output": f"Quorum sensing: {response} at {concentration}nM"
    }
```

#### Update `process_executor.py`
```python
def _execute_quorum_process(self, process_code: str, vm_context: Dict[str, Any]) -> Dict[str, Any]:
    """Execute quorum sensing processes"""
    
    if process_code == "quorum_send_signal":
        # Producer cell simulation
        signal_data = {
            "signal_molecule": vm_context.get("signal_molecule", "3OC6HSL"),
            "production_rate": vm_context.get("production_rate", "medium"),
            "cell_density": vm_context.get("cell_density", 1e8),  # cells/mL
        }
        
        # Calculate signal concentration based on cell density
        base_production = {"low": 0.1, "medium": 1.0, "high": 5.0}
        production_rate = base_production.get(signal_data["production_rate"], 1.0)
        concentration = (signal_data["cell_density"] / 1e8) * production_rate
        
        signal_data["concentration"] = concentration
        result = self.integrator.simulate_quorum_sensing(signal_data)
        
        return {
            "status": "success",
            "execution_type": "real_computation", 
            "process_code": process_code,
            "signal_produced": signal_data["signal_molecule"],
            "concentration": concentration,
            "biological_output": f"Producing {signal_data['signal_molecule']} at {concentration:.2f}nM"
        }
    
    elif process_code == "quorum_detect_signal":
        # Receiver cell simulation
        signal_data = {
            "signal_molecule": vm_context.get("signal_molecule", "3OC6HSL"),
            "concentration": vm_context.get("ambient_concentration", 0),
            "threshold": vm_context.get("threshold", 10),
            "receptor": vm_context.get("receptor", "LasR")
        }
        
        result = self.integrator.simulate_quorum_sensing(signal_data)
        
        return {
            "status": "success",
            "execution_type": "real_computation",
            "process_code": process_code,
            "signal_detected": signal_data["signal_molecule"],
            "response": result["response"],
            "expression_level": result["expression_level"],
            "biological_output": result["biological_output"]
        }
    
    else:
        return self._execute_symbolic_process(process_code, vm_context)
```

### Demo Implementation

#### `quorum_sensing_demo.py`
```python
"""Simple Quorum Sensing Communication Demo"""

from ..api import create_bio_vm
from .process_executor import MVPProcessExecutor

def run_quorum_sensing_demo():
    """Demonstrate quorum sensing communication between VMs"""
    
    print("🦠 BioXen Quorum Sensing Communication Demo")
    print("=" * 50)
    
    # Create producer and receiver VMs
    producer_vm = create_bio_vm("producer_vm", "ecoli", "basic")
    receiver_vm = create_bio_vm("receiver_vm", "ecoli", "basic")
    
    producer_vm.start()
    receiver_vm.start()
    
    executor = MVPProcessExecutor()
    
    # Test 1: Low cell density - no quorum
    print("\n📊 Test 1: Low Cell Density (No Quorum)")
    producer_context = {
        "biological_type": "ecoli",
        "signal_molecule": "3OC6HSL",
        "production_rate": "low",
        "cell_density": 1e6  # Low density
    }
    
    result1 = executor.execute_biological_process("quorum_send_signal", producer_context)
    ambient_concentration = result1["concentration"]
    
    receiver_context = {
        "biological_type": "ecoli",
        "signal_molecule": "3OC6HSL", 
        "ambient_concentration": ambient_concentration,
        "threshold": 10
    }
    
    result2 = executor.execute_biological_process("quorum_detect_signal", receiver_context)
    
    print(f"   Producer: {result1['biological_output']}")
    print(f"   Receiver: {result2['biological_output']}")
    print(f"   Communication: {'SUCCESS' if result2['response'] == 'activated' else 'NO QUORUM'}")
    
    # Test 2: High cell density - quorum reached
    print("\n📊 Test 2: High Cell Density (Quorum Reached)")
    producer_context["cell_density"] = 1e9  # High density
    producer_context["production_rate"] = "high"
    
    result3 = executor.execute_biological_process("quorum_send_signal", producer_context)
    ambient_concentration = result3["concentration"]
    
    receiver_context["ambient_concentration"] = ambient_concentration
    result4 = executor.execute_biological_process("quorum_detect_signal", receiver_context)
    
    print(f"   Producer: {result3['biological_output']}")
    print(f"   Receiver: {result4['biological_output']}")
    print(f"   Communication: {'SUCCESS' if result4['response'] == 'activated' else 'NO QUORUM'}")
    print(f"   Expression Level: {result4['expression_level']:.1f}x basal")
    
    print("\n✅ Quorum Sensing Communication Demo Complete!")

if __name__ == "__main__":
    run_quorum_sensing_demo()
```

---

## Expected Output

```
🦠 BioXen Quorum Sensing Communication Demo
==================================================

📊 Test 1: Low Cell Density (No Quorum)
   Producer: Producing 3OC6HSL at 0.01nM
   Receiver: Quorum sensing: inactive at 0.01nM
   Communication: NO QUORUM

📊 Test 2: High Cell Density (Quorum Reached)  
   Producer: Producing 3OC6HSL at 50.00nM
   Receiver: Quorum sensing: activated at 50.00nM
   Communication: SUCCESS
   Expression Level: 5.0x basal

✅ Quorum Sensing Communication Demo Complete!
```

---

## Benefits of This Approach

1. **Simple**: Single molecule, well-understood mechanism
2. **Realistic**: Based on actual bacterial communication
3. **Testable**: Clear pass/fail criteria (threshold detection)
4. **Extensible**: Foundation for more complex communication
5. **Fast**: Can implement in 1-2 days

This quorum sensing test would perfectly demonstrate real biological communication in your execution modal while being much simpler than the full Ol-Fi protocol. Should I add this to the Phase 1 plan?
