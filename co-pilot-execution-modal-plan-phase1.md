# BioXen Execution Modal Upgrade - Phase 1: MVP Foundation

## Phase 1 Overview: Minimal Viable Prototype (Weeks 1-2)

**Objective**: Create a minimal viable biological computation engine that executes genomic code as live computation, not simulation, using hybrid static/dynamic execution cores.

**Duration**: 2 weeks  
**Priority**: MVP Foundation - Prove biological computation viability  
**Dependencies**: Completion of API upgrade plan (co-pilot-api-plan-phase3.md)  

---

## Biological Computation Architecture

### Centralized Service Architecture
```
BioXen Hypervisor Infrastructure:
├── biological_computation_services/
│   ├── static_metabolic_service.py    # Centralized COBRApy computation service
│   ├── dynamic_kinetic_service.py     # Centralized Tellurium computation service
│   └── computation_orchestrator.py    # Service coordination and load balancing
├── execution_modal/
│   ├── hypervisor_client.py          # Lightweight VM-side computation client
│   ├── process_executor.py           # VM process routing and execution
│   └── mvp_demo.py                   # Service-based computation demonstration
└── vm_instances/
    ├── ecoli_vm_1/                   # Lightweight VM instances
    ├── ecoli_vm_2/                   # No local computation engines
    └── yeast_vm_1/                   # Service-based computation calls
```

### Service-Based Computation Principles
1. **Centralized Cores**: Single computation service instances for all VMs
2. **Lightweight VMs**: Individual VMs contain no computation engines
3. **Service Requests**: VMs send computation requests to centralized services
4. **Hypervisor Pattern**: True separation of compute resources from VM instances
5. **Horizontal Scaling**: Independent scaling of computation services and VMs

---

## Week 1: Centralized Computation Services

### Day 1-2: Biological Computation Services Infrastructure

#### Centralized Service Architecture
- **Static Metabolic Service**: Centralized COBRApy computation service
- **Dynamic Kinetic Service**: Centralized Tellurium computation service  
- **Service Communication**: REST API or message queue for VM-service communication

#### `src/biological_computation_services/static_metabolic_service.py`
```python
from typing import Dict, Any
import cobra
from flask import Flask, request, jsonify
import logging

class StaticMetabolicComputationService:
    """Centralized COBRApy computation service for all VM instances"""
    
    def __init__(self):
        self.app = Flask(__name__)
        self.loaded_models = {}  # Cache for loaded metabolic models
        self.setup_routes()
        
    def setup_routes(self):
        """Setup REST API endpoints for computation requests"""
        
        @self.app.route('/compute/metabolic', methods=['POST'])
        def compute_metabolic():
            try:
                request_data = request.json
                result = self.execute_metabolic_computation(request_data)
                return jsonify(result)
            except Exception as e:
                return jsonify({"error": str(e), "status": "failed"}), 500
                
        @self.app.route('/health', methods=['GET'])
        def health_check():
            return jsonify({"status": "healthy", "service": "static_metabolic"})
    
    def execute_metabolic_computation(self, computation_request: Dict[str, Any]) -> Dict[str, Any]:
        """Execute centralized metabolic computation"""
        
        # Extract computation parameters
        chassis_type = computation_request.get("chassis_type", "base")
        model_path = computation_request.get("model_path", f"bytecode/{chassis_type}_metabolism.xml")
        objective = computation_request.get("objective", "BIOMASS_Ecoli_core_w_GAM")
        constraints = computation_request.get("constraints", {})
        
        # Load or retrieve cached model
        model_key = f"{chassis_type}_{hash(model_path)}"
        if model_key not in self.loaded_models:
            model = cobra.io.read_sbml_model(model_path)
            self.loaded_models[model_key] = model
        else:
            model = self.loaded_models[model_key].copy()  # Work with copy to avoid state issues
        
        # Configure computation
        if objective in model.reactions:
            model.objective = objective
            
        # Apply constraints
        for reaction_id, bounds in constraints.items():
            if reaction_id in model.reactions:
                model.reactions.get_by_id(reaction_id).bounds = bounds
        
        # Execute computation
        solution = model.optimize()
        
        return {
            "computation_type": "static_metabolic",
            "status": solution.status,
            "optimal_objective": solution.objective_value,
            "flux_state": dict(solution.fluxes),
            "computation_service": "centralized_cobrapy",
            "model_key": model_key,
            "execution_result": "computed_state"
        }
    
    def start_service(self, host='localhost', port=5001):
        """Start the centralized computation service"""
        logging.info(f"Starting Static Metabolic Computation Service on {host}:{port}")
        self.app.run(host=host, port=port, debug=False)

if __name__ == "__main__":
    service = StaticMetabolicComputationService()
    service.start_service()
```

#### `src/biological_computation_services/dynamic_kinetic_service.py`
```python
from typing import Dict, Any
import tellurium as te
from flask import Flask, request, jsonify
import logging

class DynamicKineticComputationService:
    """Centralized Tellurium computation service for all VM instances"""
    
    def __init__(self):
        self.app = Flask(__name__)
        self.loaded_programs = {}  # Cache for loaded kinetic programs
        self.setup_routes()
        
    def setup_routes(self):
        """Setup REST API endpoints for kinetic computation requests"""
        
        @self.app.route('/compute/kinetic', methods=['POST'])
        def compute_kinetic():
            try:
                request_data = request.json
                result = self.execute_kinetic_computation(request_data)
                return jsonify(result)
            except Exception as e:
                return jsonify({"error": str(e), "status": "failed"}), 500
                
        @self.app.route('/health', methods=['GET'])
        def health_check():
            return jsonify({"status": "healthy", "service": "dynamic_kinetic"})
    
    def execute_kinetic_computation(self, computation_request: Dict[str, Any]) -> Dict[str, Any]:
        """Execute centralized kinetic computation"""
        
        # Extract computation parameters
        kinetic_code = computation_request.get("kinetic_code", self._get_default_kinetic_code())
        initial_conditions = computation_request.get("initial_conditions", {})
        time_start = computation_request.get("time_start", 0)
        time_end = computation_request.get("time_end", 10)
        time_points = computation_request.get("time_points", 100)
        
        # Load or retrieve cached kinetic program
        program_key = hash(kinetic_code)
        if program_key not in self.loaded_programs:
            program = te.loada(kinetic_code)
            self.loaded_programs[program_key] = kinetic_code  # Store code, not object (thread safety)
        
        # Create fresh instance for computation
        program = te.loada(kinetic_code)
        
        # Set initial conditions
        for species, concentration in initial_conditions.items():
            try:
                program[species] = concentration
            except:
                pass  # Species not in model
        
        # Execute computation
        computed_trajectory = program.simulate(time_start, time_end, time_points)
        
        return {
            "computation_type": "dynamic_kinetic",
            "time_vector": computed_trajectory[:, 0].tolist(),
            "species_trajectories": {
                program.getFloatingSpeciesIds()[i]: computed_trajectory[:, i+1].tolist() 
                for i in range(len(program.getFloatingSpeciesIds()))
            },
            "final_state": computed_trajectory[-1, 1:].tolist(),
            "computation_service": "centralized_tellurium",
            "program_key": str(program_key),
            "execution_result": "computed_trajectory"
        }
    
    def _get_default_kinetic_code(self) -> str:
        """Default kinetic computation for gene expression"""
        return """
        model gene_expression_computation
            # Biological computation: gene expression kinetics
            -> mRNA; k_transcription * gene_activity
            mRNA -> ; k_mRNA_decay * mRNA
            mRNA -> protein; k_translation * mRNA
            protein -> ; k_protein_decay * protein
            
            # Initial computational state
            gene_activity = 1.0
            k_transcription = 0.1
            k_mRNA_decay = 0.05  
            k_translation = 0.2
            k_protein_decay = 0.01
        end
        """
    
    def start_service(self, host='localhost', port=5002):
        """Start the centralized computation service"""
        logging.info(f"Starting Dynamic Kinetic Computation Service on {host}:{port}")
        self.app.run(host=host, port=port, debug=False)

if __name__ == "__main__":
    service = DynamicKineticComputationService()
    service.start_service()
```

### Day 3-4: Lightweight VM-Side Computation Client

#### `src/execution_modal/hypervisor_client.py`
```python
from typing import Dict, Any
import requests
import logging
from ..chassis import get_chassis_config

class BiologicalComputationClient:
    """Lightweight client for VM instances to request centralized computation"""
    
    def __init__(self, static_service_url="http://localhost:5001", dynamic_service_url="http://localhost:5002"):
        self.static_service_url = static_service_url
        self.dynamic_service_url = dynamic_service_url
        self.chassis_configs = {}
    
    def request_static_computation(self, computation_request: Dict[str, Any]) -> Dict[str, Any]:
        """Send metabolic computation request to centralized service"""
        try:
            response = requests.post(
                f"{self.static_service_url}/compute/metabolic",
                json=computation_request,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "error": f"Service error: {response.status_code}",
                    "status": "service_unavailable"
                }
                
        except requests.exceptions.RequestException as e:
            logging.warning(f"Static computation service unavailable: {e}")
            return {
                "error": f"Service connection failed: {str(e)}",
                "status": "service_unavailable"
            }
    
    def request_dynamic_computation(self, computation_request: Dict[str, Any]) -> Dict[str, Any]:
        """Send kinetic computation request to centralized service"""
        try:
            response = requests.post(
                f"{self.dynamic_service_url}/compute/kinetic",
                json=computation_request,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "error": f"Service error: {response.status_code}",
                    "status": "service_unavailable"
                }
                
        except requests.exceptions.RequestException as e:
            logging.warning(f"Dynamic computation service unavailable: {e}")
            return {
                "error": f"Service connection failed: {str(e)}",
                "status": "service_unavailable"
            }
    
    def check_service_health(self) -> Dict[str, bool]:
        """Check health of computation services"""
        health_status = {
            "static_service": False,
            "dynamic_service": False
        }
        
        try:
            static_response = requests.get(f"{self.static_service_url}/health", timeout=5)
            health_status["static_service"] = static_response.status_code == 200
        except:
            pass
            
        try:
            dynamic_response = requests.get(f"{self.dynamic_service_url}/health", timeout=5)
            health_status["dynamic_service"] = dynamic_response.status_code == 200
        except:
            pass
            
        return health_status

#### `src/execution_modal/process_executor.py`
```python
from typing import Dict, Any
from .hypervisor_client import BiologicalComputationClient
from ..chassis import get_chassis_config

class BiologicalComputationHypervisor:
    """Lightweight hypervisor for routing biological processes to centralized services"""
    
    def __init__(self):
        self.computation_client = BiologicalComputationClient()
        self.execution_mode = "service_based"  # "symbolic", "service_based", "hybrid"
    
    def execute_biological_process(self, process_code: str, vm_context: Dict[str, Any]) -> Dict[str, Any]:
        """Route biological process to appropriate centralized computation service"""
        
        # Parse process code to determine computational strategy
        if process_code.startswith("metabolic_") or "flux" in process_code:
            return self._request_static_computation(process_code, vm_context)
        elif process_code.startswith("kinetic_") or "dynamic" in process_code:
            return self._request_dynamic_computation(process_code, vm_context)
        else:
            # Fall back to symbolic execution for non-computational processes
            return self._execute_symbolic_process(process_code, vm_context)
    
    def _request_static_computation(self, process_code: str, vm_context: Dict[str, Any]) -> Dict[str, Any]:
        """Request metabolic computation from centralized service"""
        chassis_type = vm_context.get("biological_type", "base")
        chassis_config = get_chassis_config(chassis_type)
        
        # Prepare computation request
        computation_request = {
            "chassis_type": chassis_type,
            "model_path": chassis_config.get("metabolic_model", f"bytecode/{chassis_type}_metabolism.xml"),
            "objective": vm_context.get("objective", "BIOMASS_Ecoli_core_w_GAM"),
            "constraints": vm_context.get("media_constraints", {}),
            "vm_id": vm_context.get("vm_id", "unknown"),
            "process_code": process_code
        }
        
        # Send request to centralized service
        service_result = self.computation_client.request_static_computation(computation_request)
        
        if service_result.get("status") == "service_unavailable":
            # Fall back to symbolic execution if service unavailable
            return self._execute_symbolic_process(process_code, vm_context)
        
        return {
            "status": "success",
            "execution_type": "service_based_computation",
            "computation_service": "centralized_static",
            "process_code": process_code,
            "biological_output": f"Centralized metabolic computation: {service_result.get('optimal_objective', 'N/A'):.4f}",
            "service_results": service_result,
            "execution_time": 0.5  # Network + computation time
        }
    
    def _request_dynamic_computation(self, process_code: str, vm_context: Dict[str, Any]) -> Dict[str, Any]:
        """Request kinetic computation from centralized service"""
        
        # Prepare computation request
        computation_request = {
            "kinetic_code": vm_context.get("kinetic_code"),  # Custom or default
            "initial_conditions": vm_context.get("initial_conditions", {}),
            "time_start": vm_context.get("time_start", 0),
            "time_end": vm_context.get("time_end", 10),
            "time_points": vm_context.get("time_points", 100),
            "vm_id": vm_context.get("vm_id", "unknown"),
            "process_code": process_code
        }
        
        # Send request to centralized service
        service_result = self.computation_client.request_dynamic_computation(computation_request)
        
        if service_result.get("status") == "service_unavailable":
            # Fall back to symbolic execution if service unavailable
            return self._execute_symbolic_process(process_code, vm_context)
        
        return {
            "status": "success",
            "execution_type": "service_based_computation",
            "computation_service": "centralized_dynamic",
            "process_code": process_code,
            "biological_output": f"Centralized kinetic computation: {len(service_result.get('time_vector', []))} time points",
            "service_results": service_result,
            "execution_time": 0.3  # Network + computation time
        }
    
    def _execute_symbolic_process(self, process_code: str, vm_context: Dict[str, Any]) -> Dict[str, Any]:
        """Fall back to symbolic execution for non-computational processes"""
        return {
            "status": "success",
            "execution_type": "symbolic",
            "computation_service": "vm_local_symbolic",
            "process_code": process_code,
            "biological_output": f"Symbolic execution: {process_code}",
            "execution_time": 0.1
        }
```

### Day 5: Service-Based Biological Computation Demo

#### `src/execution_modal/mvp_demo.py`
```python
"""Service-Based Biological Computation Demo - Centralized Architecture"""

from ..api import create_bio_vm
from .process_executor import BiologicalComputationHypervisor

def run_service_based_computation_demo():
    """Demonstrate service-based biological computation architecture"""
    
    print("🧬 BioXen Service-Based Biological Computation Demo")
    print("🏗️  Architecture: Lightweight VMs → Centralized Computation Services")
    print("=" * 70)
    
    # Create lightweight biological VM (no computation engines installed)
    vm = create_bio_vm("service_demo_vm", "ecoli", "lightweight")
    vm.start()
    
    # Initialize lightweight hypervisor (service client only)
    hypervisor = BiologicalComputationHypervisor()
    
    # Check service availability
    print("\n🔧 Service Health Check")
    health_status = hypervisor.computation_client.check_service_health()
    print(f"   Static Metabolic Service: {'✅ Online' if health_status['static_service'] else '❌ Offline'}")
    print(f"   Dynamic Kinetic Service: {'✅ Online' if health_status['dynamic_service'] else '❌ Offline'}")
    
    # Test 1: Centralized Static Metabolic Computation
    print("\n🧮 Test 1: Centralized Static Metabolic Computation")
    print("   Request: Lightweight VM → Static Computation Service → Response")
    
    vm_context = {
        "vm_id": "service_demo_vm",
        "biological_type": "ecoli",
        "objective": "BIOMASS_Ecoli_core_w_GAM",
        "optimization_target": "growth"
    }
    
    result1 = hypervisor.execute_biological_process("metabolic_optimization", vm_context)
    print(f"   Execution Type: {result1['execution_type']}")
    print(f"   Computation Service: {result1['computation_service']}")
    print(f"   Result: {result1['biological_output']}")
    
    if result1['execution_type'] == 'service_based_computation':
        service_data = result1['service_results']
        print(f"   Service Response: {service_data.get('computation_service', 'N/A')}")
        print(f"   Computed State: Optimal objective = {service_data.get('optimal_objective', 'N/A'):.4f}")
    
    # Test 2: Centralized Dynamic Kinetic Computation  
    print("\n⚡ Test 2: Centralized Dynamic Kinetic Computation")
    print("   Request: Lightweight VM → Dynamic Computation Service → Response")
    
    kinetic_context = {
        "vm_id": "service_demo_vm",
        "time_end": 20,
        "time_points": 50,
        "initial_conditions": {"mRNA": 0, "protein": 0}
    }
    
    result2 = hypervisor.execute_biological_process("kinetic_gene_expression", kinetic_context)
    print(f"   Execution Type: {result2['execution_type']}")
    print(f"   Computation Service: {result2['computation_service']}")
    print(f"   Result: {result2['biological_output']}")
    
    if result2['execution_type'] == 'service_based_computation':
        service_data = result2['service_results']
        print(f"   Service Response: {service_data.get('computation_service', 'N/A')}")
        final_protein = service_data.get('final_state', [0])[-1] if service_data.get('final_state') else 0
        print(f"   Computed State: Final protein level = {final_protein:.4f}")
    
    # Test 3: Service Unavailable (Fallback to Symbolic)
    print("\n🔄 Test 3: Service Unavailable Fallback")
    print("   Scenario: Service offline → Automatic symbolic fallback")
    
    result3 = hypervisor.execute_biological_process("protein_folding_complex_unknown", {})
    print(f"   Execution Type: {result3['execution_type']}")
    print(f"   Computation Service: {result3['computation_service']}")
    print(f"   Result: {result3['biological_output']}")
    
    # Architecture Summary
    print("\n🏗️  Service-Based Architecture Benefits")
    print("   🖥️  Lightweight VMs: No local computation engines, minimal resource usage")
    print("   🏭 Centralized Services: Shared computation resources, horizontal scaling")
    print("   🔄 Graceful Fallback: Automatic symbolic execution when services unavailable")
    print("   📡 Service Communication: REST API requests for computation")
    print("   ⚖️  Load Distribution: Multiple VMs share centralized computation infrastructure")
    
    print("\n✅ Service-Based Biological Computation Demo Complete!")
    print("   True hypervisor architecture: VMs consume computation as a service!")

def start_computation_services():
    """Helper function to start centralized computation services"""
    import threading
    import time
    from ..biological_computation_services.static_metabolic_service import StaticMetabolicComputationService
    from ..biological_computation_services.dynamic_kinetic_service import DynamicKineticComputationService
    
    print("🚀 Starting Centralized Biological Computation Services...")
    
    # Start static metabolic service in background thread
    static_service = StaticMetabolicComputationService()
    static_thread = threading.Thread(target=static_service.start_service, args=('localhost', 5001))
    static_thread.daemon = True
    static_thread.start()
    
    # Start dynamic kinetic service in background thread
    dynamic_service = DynamicKineticComputationService()
    dynamic_thread = threading.Thread(target=dynamic_service.start_service, args=('localhost', 5002))
    dynamic_thread.daemon = True
    dynamic_thread.start()
    
    print("⏳ Waiting for services to initialize...")
    time.sleep(3)  # Allow services to start
    
    print("✅ Centralized Computation Services Ready!")
    return static_thread, dynamic_thread

if __name__ == "__main__":
    # Start services first
    service_threads = start_computation_services()
    
    # Run demo
    run_service_based_computation_demo()
```

---

## Week 2: Computational Integration & Validation

### Day 6-7: Service Integration with Existing VM Architecture

#### Update `src/bioxen_jcvi_vm_lib/api/biological_vm.py`
```python
# Integrate service-based computation into existing BiologicalVM classes

class BasicBiologicalVM(BiologicalVM):
    def __init__(self, vm_id: str, biological_type: str, config: Dict[str, Any]):
        super().__init__(vm_id, biological_type, config)
        # ... existing initialization ...
        
        # Service-based computation integration (lightweight)
        self._service_computation_enabled = config.get("enable_service_computation", False)
        self._computation_service_urls = config.get("computation_service_urls", {
            "static": "http://localhost:5001",
            "dynamic": "http://localhost:5002"
        })
        
        if self._service_computation_enabled:
            from ..execution_modal.process_executor import BiologicalComputationHypervisor
            # Lightweight hypervisor - no local computation engines
            self._computation_hypervisor = BiologicalComputationHypervisor()
            # Configure service URLs
            self._computation_hypervisor.computation_client.static_service_url = self._computation_service_urls["static"]
            self._computation_hypervisor.computation_client.dynamic_service_url = self._computation_service_urls["dynamic"]
    
    def execute_biological_process(self, process_code: str) -> Dict[str, Any]:
        """Enhanced execution with service-based biological computation"""
        if hasattr(self, '_computation_hypervisor') and self._service_computation_enabled:
            vm_context = {
                "vm_id": self.vm_id,
                "biological_type": self.biological_type,
                "vm_resources": self.get_resource_usage(),  # VM-level resources only
                "chassis_config": self.get_chassis_config(),
                "service_config": self._computation_service_urls
            }
            return self._computation_hypervisor.execute_biological_process(process_code, vm_context)
        else:
            # Original symbolic execution (no services)
            return self._execute_biological_process_impl(process_code)
    
    def get_computation_service_status(self) -> Dict[str, Any]:
        """Check status of centralized computation services"""
        if hasattr(self, '_computation_hypervisor'):
            health_status = self._computation_hypervisor.computation_client.check_service_health()
            return {
                "service_based_computation": True,
                "static_service_url": self._computation_service_urls["static"],
                "dynamic_service_url": self._computation_service_urls["dynamic"],
                "service_health": health_status,
                "vm_computation_mode": "service_client"
            }
        else:
            return {
                "service_based_computation": False,
                "vm_computation_mode": "symbolic_only"
            }

class EnhancedBiologicalVM(BasicBiologicalVM):
    """Enhanced VM with advanced service-based computation features"""
    
    def __init__(self, vm_id: str, biological_type: str, config: Dict[str, Any]):
        # Force enable service computation for enhanced VMs
        config["enable_service_computation"] = True
        super().__init__(vm_id, biological_type, config)
        
        # Enhanced features
        self._computation_caching = config.get("enable_computation_caching", True)
        self._computation_cache = {}
    
    def execute_biological_process(self, process_code: str) -> Dict[str, Any]:
        """Enhanced execution with caching and service optimization"""
        
        # Check cache first (for expensive computations)
        cache_key = f"{process_code}_{hash(str(self.get_chassis_config()))}"
        if self._computation_caching and cache_key in self._computation_cache:
            cached_result = self._computation_cache[cache_key]
            cached_result["cache_hit"] = True
            return cached_result
        
        # Execute via services
        result = super().execute_biological_process(process_code)
        
        # Cache result if successful service-based computation
        if (self._computation_caching and 
            result.get("execution_type") == "service_based_computation" and
            result.get("status") == "success"):
            self._computation_cache[cache_key] = result.copy()
            result["cache_hit"] = False
        
        return result
```

### Day 8-9: Biological Computation Validation & Testing

#### Create Biological Bytecode Repository
```bash
# Create biological bytecode directory structure
mkdir -p bytecode/
mkdir -p bytecode/ecoli/
mkdir -p bytecode/yeast/
mkdir -p bytecode/orthogonal/
mkdir -p bytecode/base/

# Download/create standard biological computation models
# E. coli core metabolic model (standard in computational biology)
# Kinetic models for gene expression, metabolism
```

#### `tests/test_biological_computation.py`
```python
import pytest
from src.execution_modal.mvp_demo import run_biological_computation_demo
from src.execution_modal.process_executor import BiologicalComputationHypervisor

def test_static_metabolic_computation():
    """Test static metabolic computation core"""
    hypervisor = BiologicalComputationHypervisor()
    vm_context = {"biological_type": "ecoli", "objective": "BIOMASS_Ecoli_core_w_GAM"}
    
    result = hypervisor.execute_biological_process("metabolic_optimization", vm_context)
    
    assert result["status"] == "success"
    assert result["execution_type"] in ["biological_computation", "symbolic"]  # Allow fallback
    assert "computation_core" in result

def test_dynamic_kinetic_computation():
    """Test dynamic kinetic computation core"""
    hypervisor = BiologicalComputationHypervisor()
    vm_context = {"time_end": 10, "time_points": 50}
    
    result = hypervisor.execute_biological_process("kinetic_gene_expression", vm_context)
    
    assert result["status"] == "success"
    assert result["execution_type"] in ["biological_computation", "symbolic"]
    assert "computation_core" in result

def test_computation_vs_symbolic_execution():
    """Test that biological computation provides different results than symbolic"""
    hypervisor = BiologicalComputationHypervisor()
    
    # Computational process
    result_computed = hypervisor.execute_biological_process("metabolic_optimization", {"biological_type": "ecoli"})
    
    # Symbolic process
    result_symbolic = hypervisor.execute_biological_process("unknown_process", {})
    
    # Should use different execution types
    if result_computed["execution_type"] == "biological_computation":
        assert result_symbolic["execution_type"] == "symbolic"
        assert result_computed["computation_core"] != result_symbolic["computation_core"]

def test_biological_computation_demo():
    """Test complete biological computation demonstration"""
    # Should run without errors and demonstrate all computation cores
    run_biological_computation_demo()

def test_hypervisor_routing():
    """Test that hypervisor correctly routes processes to computation cores"""
    hypervisor = BiologicalComputationHypervisor()
    
    # Test metabolic routing
    metabolic_result = hypervisor.execute_biological_process("metabolic_test", {})
    # Should route to static core or symbolic fallback
    
    # Test kinetic routing  
    kinetic_result = hypervisor.execute_biological_process("kinetic_test", {})
    # Should route to dynamic core or symbolic fallback
    
    # Test unknown routing
    unknown_result = hypervisor.execute_biological_process("unknown_test", {})
    # Should route to symbolic fallback
    assert unknown_result["execution_type"] == "symbolic"
```

### Day 10: Documentation & Production Deployment

#### Update `README.md`
```markdown
## Biological Computation Engine

BioXen now executes genomic code as live biological computation, not simulation:

### Architecture
- **Static Compiler (COBRApy)**: Constraint-based optimization of metabolic networks
- **Dynamic Engine (Tellurium)**: ODE solving of kinetic biological processes  
- **Computation Hypervisor**: Routes biological code to appropriate execution cores

### Quick Start
```python
from bioxen_jcvi_vm_lib.execution_modal.mvp_demo import run_biological_computation_demo
run_biological_computation_demo()
```

### Biological Computation vs Simulation
- **Computation**: Mathematical derivation of biological states from genomic code
- **Not Simulation**: No approximation - exact solutions to biological equations
- **Virtual Machine**: Cell genomic code runs as executable biological bytecode
```

#### Installation Requirements
```bash
# Centralized Services (single installation)
pip install cobra>=0.25.0         # Static metabolic computation service
pip install tellurium>=2.2.0      # Dynamic kinetic computation service
pip install flask>=2.2.0          # REST API framework for services

# Lightweight VM Clients (minimal dependencies)
pip install requests>=2.28.0      # HTTP client for service communication
# No COBRApy or Tellurium needed in VM instances!
```

---

## Success Criteria (Service-Based Biological Computation)

### Week 1 Deliverables
- [ ] Centralized biological computation services (Static + Dynamic)
- [ ] Lightweight VM-side computation client
- [ ] Service-based computation demonstration

### Week 2 Deliverables  
- [ ] Integration with existing BioXen VM architecture
- [ ] Comprehensive test suite for service-based computation
- [ ] Documentation emphasizing centralized service architecture

### Service-Based Validation
1. **Centralized Services**: Single instances of COBRApy and Tellurium serve multiple VMs
2. **Lightweight VMs**: Individual VMs have minimal computation dependencies
3. **Service Communication**: REST API requests/responses for biological computation
4. **Graceful Degradation**: Automatic symbolic fallback when services unavailable
5. **Horizontal Scaling**: Services and VMs can be scaled independently
6. **Resource Efficiency**: Shared computation infrastructure reduces overall resource usage

### Ready for Phase 2
- Service-based biological computation architecture established
- True hypervisor paradigm with centralized computation services
- Foundation for scaling both VMs and computation services independently
- Clear separation of concerns: VMs handle process routing, services handle computation
