"""
Test module: VM Lifecycle

Tests for VM creation, state transitions, resource allocation, and status queries.

Status: 🔮 Wishful - Defines ideal VM management APIs
"""

import pytest


@pytest.mark.wishful
class TestVMCreation:
    """Test VM instantiation and configuration."""
    
    def test_create_ecoli_vm(self, test_client, ecoli_vm_config):
        """POST /api/v1/vms - Create E. coli VM"""
        response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        assert response.status_code == 201
        result = response.json()
        
        assert result["vm_id"] == "test_ecoli_001"
        assert result["biological_type"] == "ecoli"
        assert result["state"] == "created"
        assert "genome_file" in result["config"]
    
    def test_create_syn3a_minimal_cell(self, test_client, syn3a_vm_config):
        """Create Syn3A minimal cell (473 genes)"""
        response = test_client.post("/api/v1/vms", json=syn3a_vm_config)
        assert response.status_code == 201
        result = response.json()
        
        assert result["biological_type"] == "syn3a"
        assert result["config"]["gene_count"] == 473
        assert result["vm_type"] == "minimal"
    
    def test_create_yeast_vm(self, test_client, yeast_circadian_vm_config):
        """Create yeast VM with circadian capability"""
        response = test_client.post("/api/v1/vms", json=yeast_circadian_vm_config)
        assert response.status_code == 201
        result = response.json()
        
        assert result["vm_type"] == "circadian_capable"
        assert "genes" in result
        assert "FRQ" in result["genes"]
    
    def test_create_cyanobacteria_vm(self, test_client, cyanobacteria_vm_config):
        """Create cyanobacteria VM with Kai oscillator"""
        response = test_client.post("/api/v1/vms", json=cyanobacteria_vm_config)
        assert response.status_code == 201
        result = response.json()
        
        assert "kaiA" in result["genes"]
        assert "kaiB" in result["genes"]
        assert "kaiC" in result["genes"]
    
    def test_create_vm_with_custom_config(self, test_client):
        """Create VM with custom configuration"""
        response = test_client.post("/api/v1/vms", json={
            "vm_id": "custom_ecoli",
            "biological_type": "ecoli",
            "vm_type": "basic",
            "config": {
                "genome_file": "ecoli_k12.gbk",
                "enable_metabolism": True,
                "enable_gene_expression": True,
                "timestep_seconds": 1.0,
                "max_simulation_hours": 72
            }
        })
        assert response.status_code == 201
    
    def test_create_vm_duplicate_id_error(self, test_client, ecoli_vm_config):
        """Test error when creating VM with duplicate ID"""
        # Create first VM
        test_client.post("/api/v1/vms", json=ecoli_vm_config)
        
        # Try to create duplicate
        response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        assert response.status_code == 409  # Conflict
        assert "already exists" in response.json()["detail"].lower()
    
    def test_create_vm_invalid_type_error(self, test_client):
        """Test error with invalid biological type"""
        response = test_client.post("/api/v1/vms", json={
            "vm_id": "invalid_001",
            "biological_type": "invalid_organism",
            "vm_type": "basic"
        })
        assert response.status_code == 400  # Bad Request


@pytest.mark.wishful
class TestVMLifecycle:
    """Test VM state transitions."""
    
    def test_start_vm(self, test_client, ecoli_vm_config):
        """POST /api/v1/vms/{vm_id}/start"""
        # Create VM first
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        
        # Start VM
        response = test_client.post(f"/api/v1/vms/{vm_id}/start")
        assert response.status_code == 200
        assert response.json()["state"] == "running"
    
    def test_stop_vm(self, test_client, ecoli_vm_config):
        """POST /api/v1/vms/{vm_id}/stop"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        
        # Start then stop
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        response = test_client.post(f"/api/v1/vms/{vm_id}/stop")
        
        assert response.status_code == 200
        assert response.json()["state"] == "stopped"
    
    def test_pause_vm(self, test_client, ecoli_vm_config):
        """POST /api/v1/vms/{vm_id}/pause"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        response = test_client.post(f"/api/v1/vms/{vm_id}/pause")
        
        assert response.status_code == 200
        assert response.json()["state"] == "paused"
    
    def test_resume_vm(self, test_client, ecoli_vm_config):
        """POST /api/v1/vms/{vm_id}/resume"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        
        test_client.post(f"/api/v1/vms/{vm_id}/start")
        test_client.post(f"/api/v1/vms/{vm_id}/pause")
        response = test_client.post(f"/api/v1/vms/{vm_id}/resume")
        
        assert response.status_code == 200
        assert response.json()["state"] == "running"
    
    def test_destroy_vm(self, test_client, ecoli_vm_config):
        """DELETE /api/v1/vms/{vm_id}"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        
        response = test_client.delete(f"/api/v1/vms/{vm_id}")
        assert response.status_code == 204  # No Content
        
        # Verify VM is gone
        status_response = test_client.get(f"/api/v1/vms/{vm_id}/status")
        assert status_response.status_code == 404
    
    def test_state_transition_invalid(self, test_client, ecoli_vm_config):
        """Test invalid state transitions"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        
        # Try to stop VM that hasn't started
        response = test_client.post(f"/api/v1/vms/{vm_id}/stop")
        assert response.status_code == 400  # Bad Request


@pytest.mark.wishful
class TestResourceAllocation:
    """Test VM resource allocation and management."""
    
    def test_allocate_resources(self, test_client, ecoli_vm_config):
        """POST /api/v1/vms/{vm_id}/resources"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        
        response = test_client.post(f"/api/v1/vms/{vm_id}/resources", json={
            "atp": 100.0,
            "ribosomes": 50,
            "amino_acids": 1000
        })
        assert response.status_code == 200
        result = response.json()
        
        assert result["atp"] == 100.0
        assert result["ribosomes"] == 50
        assert result["amino_acids"] == 1000
    
    def test_get_resource_status(self, test_client, ecoli_vm_config):
        """GET /api/v1/vms/{vm_id}/resources"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        
        # Allocate resources
        test_client.post(f"/api/v1/vms/{vm_id}/resources", json={
            "atp": 100.0,
            "ribosomes": 50
        })
        
        # Get status
        response = test_client.get(f"/api/v1/vms/{vm_id}/resources")
        assert response.status_code == 200
        result = response.json()
        
        assert "atp" in result
        assert "ribosomes" in result
    
    def test_update_resources(self, test_client, ecoli_vm_config):
        """PATCH /api/v1/vms/{vm_id}/resources"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        
        # Initial allocation
        test_client.post(f"/api/v1/vms/{vm_id}/resources", json={"atp": 100.0})
        
        # Update
        response = test_client.patch(f"/api/v1/vms/{vm_id}/resources", json={"atp": 150.0})
        assert response.status_code == 200
        assert response.json()["atp"] == 150.0


@pytest.mark.wishful
class TestVMStatus:
    """Test VM status queries."""
    
    def test_get_vm_status(self, test_client, ecoli_vm_config):
        """GET /api/v1/vms/{vm_id}/status"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        
        response = test_client.get(f"/api/v1/vms/{vm_id}/status")
        assert response.status_code == 200
        result = response.json()
        
        assert "state" in result
        assert "resources" in result
        assert "uptime_seconds" in result
        assert "created_at" in result
    
    def test_list_all_vms(self, test_client, ecoli_vm_config, syn3a_vm_config):
        """GET /api/v1/vms"""
        # Create multiple VMs
        test_client.post("/api/v1/vms", json=ecoli_vm_config)
        test_client.post("/api/v1/vms", json=syn3a_vm_config)
        
        response = test_client.get("/api/v1/vms")
        assert response.status_code == 200
        vms = response.json()
        
        assert isinstance(vms, list)
        assert len(vms) >= 2
        
        # Check structure
        for vm in vms:
            assert "vm_id" in vm
            assert "biological_type" in vm
            assert "state" in vm
    
    def test_list_vms_filtered_by_type(self, test_client):
        """GET /api/v1/vms?biological_type=ecoli"""
        response = test_client.get("/api/v1/vms", params={"biological_type": "ecoli"})
        assert response.status_code == 200
        vms = response.json()
        
        for vm in vms:
            assert vm["biological_type"] == "ecoli"
    
    def test_list_vms_filtered_by_state(self, test_client):
        """GET /api/v1/vms?state=running"""
        response = test_client.get("/api/v1/vms", params={"state": "running"})
        assert response.status_code == 200
        vms = response.json()
        
        for vm in vms:
            assert vm["state"] == "running"
    
    def test_get_vm_not_found(self, test_client):
        """Test 404 for non-existent VM"""
        response = test_client.get("/api/v1/vms/nonexistent_vm/status")
        assert response.status_code == 404


@pytest.mark.wishful
class TestVMConfiguration:
    """Test VM configuration management."""
    
    def test_get_vm_config(self, test_client, ecoli_vm_config):
        """GET /api/v1/vms/{vm_id}/config"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        
        response = test_client.get(f"/api/v1/vms/{vm_id}/config")
        assert response.status_code == 200
        config = response.json()
        
        assert "genome_file" in config
        assert "enable_metabolism" in config
    
    def test_update_vm_config(self, test_client, ecoli_vm_config):
        """PATCH /api/v1/vms/{vm_id}/config"""
        create_response = test_client.post("/api/v1/vms", json=ecoli_vm_config)
        vm_id = create_response.json()["vm_id"]
        
        response = test_client.patch(f"/api/v1/vms/{vm_id}/config", json={
            "timestep_seconds": 0.5,
            "enable_gene_expression": True
        })
        assert response.status_code == 200
        
        # Verify update
        config_response = test_client.get(f"/api/v1/vms/{vm_id}/config")
        config = config_response.json()
        assert config["timestep_seconds"] == 0.5
