"""
Unit tests for BioXen hypervisor core functionality
"""

import unittest
import time
from src.hypervisor.core import BioXenHypervisor, ResourceAllocation, VMState

class TestBioXenHypervisor(unittest.TestCase):
    """Test the main hypervisor functionality"""
    
    def setUp(self):
        """Set up test hypervisor"""
        self.hypervisor = BioXenHypervisor(max_vms=4, total_ribosomes=80)
    
    def tearDown(self):
        """Clean up after tests"""
        # Destroy any remaining VMs
        for vm_id in list(self.hypervisor.vms.keys()):
            self.hypervisor.destroy_vm(vm_id)
    
    def test_hypervisor_initialization(self):
        """Test hypervisor initialization"""
        self.assertEqual(self.hypervisor.max_vms, 4)
        self.assertEqual(self.hypervisor.total_ribosomes, 80)
        self.assertEqual(self.hypervisor.available_ribosomes, 68)  # 80 * 0.85
        self.assertEqual(len(self.hypervisor.vms), 0)
        self.assertIsNone(self.hypervisor.active_vm)
    
    def test_create_vm_success(self):
        """Test successful VM creation"""
        resources = ResourceAllocation(ribosomes=20, atp_percentage=25.0, memory_kb=120)
        success = self.hypervisor.create_vm("test-vm1", "syn3a_minimal", resources)
        
        self.assertTrue(success)
        self.assertIn("test-vm1", self.hypervisor.vms)
        
        vm = self.hypervisor.vms["test-vm1"]
        self.assertEqual(vm.vm_id, "test-vm1")
        self.assertEqual(vm.state, VMState.CREATED)
        self.assertEqual(vm.genome_template, "syn3a_minimal")
        self.assertEqual(vm.resources.ribosomes, 20)
    
    def test_create_vm_max_limit(self):
        """Test VM creation at maximum limit"""
        # Create maximum number of VMs
        for i in range(4):
            success = self.hypervisor.create_vm(f"vm{i}", "syn3a_minimal")
            self.assertTrue(success)
        
        # Try to create one more - should fail
        success = self.hypervisor.create_vm("vm5", "syn3a_minimal")
        self.assertFalse(success)
    
    def test_create_duplicate_vm(self):
        """Test creating VM with duplicate ID"""
        success1 = self.hypervisor.create_vm("duplicate", "syn3a_minimal")
        success2 = self.hypervisor.create_vm("duplicate", "syn3a_minimal")
        
        self.assertTrue(success1)
        self.assertFalse(success2)
    
    def test_start_vm(self):
        """Test starting a VM"""
        self.hypervisor.create_vm("test-vm", "syn3a_minimal")
        success = self.hypervisor.start_vm("test-vm")
        
        self.assertTrue(success)
        vm = self.hypervisor.vms["test-vm"]
        self.assertEqual(vm.state, VMState.RUNNING)
        self.assertIsNotNone(vm.start_time)
    
    def test_start_nonexistent_vm(self):
        """Test starting non-existent VM"""
        success = self.hypervisor.start_vm("nonexistent")
        self.assertFalse(success)
    
    def test_pause_resume_vm(self):
        """Test pausing and resuming a VM"""
        self.hypervisor.create_vm("test-vm", "syn3a_minimal")
        self.hypervisor.start_vm("test-vm")
        
        # Pause
        success = self.hypervisor.pause_vm("test-vm")
        self.assertTrue(success)
        self.assertEqual(self.hypervisor.vms["test-vm"].state, VMState.PAUSED)
        
        # Resume
        success = self.hypervisor.resume_vm("test-vm")
        self.assertTrue(success)
        self.assertEqual(self.hypervisor.vms["test-vm"].state, VMState.RUNNING)
    
    def test_destroy_vm(self):
        """Test destroying a VM"""
        self.hypervisor.create_vm("test-vm", "syn3a_minimal")
        self.hypervisor.start_vm("test-vm")
        
        success = self.hypervisor.destroy_vm("test-vm")
        
        self.assertTrue(success)
        self.assertNotIn("test-vm", self.hypervisor.vms)
    
    def test_get_vm_status(self):
        """Test getting VM status"""
        resources = ResourceAllocation(ribosomes=15, atp_percentage=20.0, memory_kb=100)
        self.hypervisor.create_vm("test-vm", "syn3a_minimal", resources)
        self.hypervisor.start_vm("test-vm")
        
        status = self.hypervisor.get_vm_status("test-vm")
        
        self.assertIsNotNone(status)
        self.assertEqual(status["vm_id"], "test-vm")
        self.assertEqual(status["state"], "running")
        self.assertEqual(status["ribosome_allocation"], 15)
        self.assertEqual(status["atp_percentage"], 20.0)
        self.assertEqual(status["memory_kb"], 100)
        self.assertGreaterEqual(status["uptime_seconds"], 0)
    
    def test_list_vms(self):
        """Test listing VMs"""
        # Empty list initially
        vms = self.hypervisor.list_vms()
        self.assertEqual(len(vms), 0)
        
        # Create some VMs
        self.hypervisor.create_vm("vm1", "syn3a_minimal")
        self.hypervisor.create_vm("vm2", "syn3a_minimal")
        self.hypervisor.start_vm("vm1")
        
        vms = self.hypervisor.list_vms()
        self.assertEqual(len(vms), 2)
        
        vm_ids = [vm["vm_id"] for vm in vms]
        self.assertIn("vm1", vm_ids)
        self.assertIn("vm2", vm_ids)
    
    def test_system_resources(self):
        """Test getting system resources"""
        resources = self.hypervisor.get_system_resources()
        
        self.assertEqual(resources["total_ribosomes"], 80)
        self.assertEqual(resources["available_ribosomes"], 68)
        self.assertEqual(resources["allocated_ribosomes"], 0)
        self.assertEqual(resources["free_ribosomes"], 68)
        self.assertEqual(resources["total_atp_allocated"], 0)
        self.assertEqual(resources["hypervisor_overhead"], 0.15)
        self.assertEqual(resources["active_vms"], 0)
        
        # Create and start VM
        resources_vm = ResourceAllocation(ribosomes=20, atp_percentage=30.0)
        self.hypervisor.create_vm("test-vm", "syn3a_minimal", resources_vm)
        self.hypervisor.start_vm("test-vm")
        
        resources = self.hypervisor.get_system_resources()
        self.assertEqual(resources["allocated_ribosomes"], 20)
        self.assertEqual(resources["free_ribosomes"], 48)
        self.assertEqual(resources["total_atp_allocated"], 30.0)
        self.assertEqual(resources["active_vms"], 1)
    
    def test_scheduler(self):
        """Test basic scheduler functionality"""
        # Create two VMs
        self.hypervisor.create_vm("vm1", "syn3a_minimal")
        self.hypervisor.create_vm("vm2", "syn3a_minimal")
        self.hypervisor.start_vm("vm1")
        self.hypervisor.start_vm("vm2")
        
        # Run scheduler
        self.hypervisor.run_scheduler()
        
        # Should have an active VM
        self.assertIsNotNone(self.hypervisor.active_vm)
        self.assertIn(self.hypervisor.active_vm, ["vm1", "vm2"])

class TestResourceAllocation(unittest.TestCase):
    """Test resource allocation functionality"""
    
    def test_resource_allocation_creation(self):
        """Test creating resource allocation"""
        resources = ResourceAllocation(
            ribosomes=25,
            atp_percentage=30.0,
            rna_polymerase=5,
            memory_kb=150,
            priority=3
        )
        
        self.assertEqual(resources.ribosomes, 25)
        self.assertEqual(resources.atp_percentage, 30.0)
        self.assertEqual(resources.rna_polymerase, 5)
        self.assertEqual(resources.memory_kb, 150)
        self.assertEqual(resources.priority, 3)
    
    def test_resource_allocation_defaults(self):
        """Test default values in resource allocation"""
        resources = ResourceAllocation()
        
        self.assertEqual(resources.ribosomes, 0)
        self.assertEqual(resources.atp_percentage, 0.0)
        self.assertEqual(resources.rna_polymerase, 0)
        self.assertEqual(resources.memory_kb, 0)
        self.assertEqual(resources.priority, 1)

if __name__ == '__main__':
    unittest.main()
