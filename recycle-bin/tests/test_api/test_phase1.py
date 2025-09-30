import pytest
from src.api import create_bio_vm, BasicBiologicalVM, XCPngBiologicalVM
from src.api import get_supported_biological_types, get_supported_vm_types
from src.api import validate_biological_type, validate_vm_type
from src.api import BioResourceManager, ConfigManager

class TestPhase1Foundation:
    """Test Phase 1 foundation implementation"""
    
    def test_create_basic_syn3a_vm(self):
        """Test creating basic Syn3A VM"""
        vm = create_bio_vm("test_syn3a", "syn3a", "basic")
        assert isinstance(vm, BasicBiologicalVM)
        assert vm.vm_id == "test_syn3a"
        assert vm.get_vm_type() == "basic"
        assert vm.get_biological_type() == "syn3a"
    
    def test_create_basic_ecoli_vm(self):
        """Test creating basic E.coli VM"""
        vm = create_bio_vm("test_ecoli", "ecoli", "basic")
        assert isinstance(vm, BasicBiologicalVM)
        assert vm.get_vm_type() == "basic" 
        assert vm.get_biological_type() == "ecoli"
    
    def test_create_basic_minimal_cell_vm(self):
        """Test creating basic minimal cell VM"""
        vm = create_bio_vm("test_minimal", "minimal_cell", "basic")
        assert isinstance(vm, BasicBiologicalVM)
        assert vm.get_vm_type() == "basic"
        assert vm.get_biological_type() == "minimal_cell"
    
    def test_xcpng_requires_config(self):
        """Test that XCP-ng VM type requires config"""
        with pytest.raises(ValueError, match="XCP-ng VM type requires config"):
            create_bio_vm("test", "syn3a", "xcpng")
    
    def test_xcpng_vm_creation_with_config(self):
        """Test XCP-ng VM creation with proper config"""
        config = {
            "xcpng_config": {
                "xapi_url": "https://test-xcpng:443",
                "username": "root",
                "password": "test",
                "ssh_user": "bioxen"
            }
        }
        vm = create_bio_vm("test_xcpng", "syn3a", "xcpng", config)
        assert isinstance(vm, XCPngBiologicalVM)
        assert vm.get_vm_type() == "xcpng"
        assert vm.get_biological_type() == "syn3a"
    
    def test_unsupported_biological_type(self):
        """Test error handling for unsupported biological types"""
        with pytest.raises(ValueError, match="Unsupported biological type"):
            create_bio_vm("test", "unsupported_bio_type", "basic")
    
    def test_unsupported_vm_type(self):
        """Test error handling for unsupported VM types"""
        with pytest.raises(ValueError, match="Unsupported VM type"):
            create_bio_vm("test", "syn3a", "unsupported_vm_type")
    
    def test_basic_vm_default_config(self):
        """Test basic VM creation with default vm_type"""
        vm = create_bio_vm("test_minimal", "minimal_cell")  # Should default to "basic"
        assert vm.get_vm_type() == "basic"
        assert vm.get_biological_type() == "minimal_cell"
    
    def test_xcpng_placeholder_methods(self):
        """Test XCP-ng VM placeholder methods raise NotImplementedError"""
        config = {
            "xcpng_config": {
                "xapi_url": "test", 
                "username": "test", 
                "password": "test", 
                "ssh_user": "test"
            }
        }
        vm = create_bio_vm("test_xcpng", "syn3a", "xcpng", config)
        assert isinstance(vm, XCPngBiologicalVM)
        assert vm.get_vm_type() == "xcpng"
        
        # XCP-ng methods should raise NotImplementedError in Phase 1
        with pytest.raises(NotImplementedError, match="Phase 2"):
            vm.start()
    
    def test_supported_types_functions(self):
        """Test supported types query functions"""
        bio_types = get_supported_biological_types()
        assert "syn3a" in bio_types
        assert "ecoli" in bio_types
        assert "minimal_cell" in bio_types
        
        vm_types = get_supported_vm_types()
        assert "basic" in vm_types
        assert "xcpng" in vm_types
    
    def test_validation_functions(self):
        """Test validation functions"""
        assert validate_biological_type("syn3a") == True
        assert validate_biological_type("invalid") == False
        
        assert validate_vm_type("basic") == True
        assert validate_vm_type("invalid") == False
    
    def test_resource_manager_creation(self):
        """Test BioResourceManager creation"""
        vm = create_bio_vm("test_rm", "syn3a", "basic")
        rm = BioResourceManager(vm)
        assert rm.vm == vm
        assert rm.hypervisor == vm.hypervisor
    
    def test_config_manager_defaults(self):
        """Test ConfigManager default configurations"""
        syn3a_config = ConfigManager.load_defaults("syn3a")
        assert "resource_limits" in syn3a_config
        assert syn3a_config["minimal_mode"] == True
        
        ecoli_config = ConfigManager.load_defaults("ecoli")
        assert "operon_management" in ecoli_config
        assert ecoli_config["operon_management"] == True
    
    def test_config_validation(self):
        """Test configuration validation"""
        basic_config = {"test": "value"}
        assert ConfigManager.validate_config(basic_config, "basic") == True
        
        # XCP-ng config missing required fields
        xcpng_config_incomplete = {"xcpng_config": {"xapi_url": "test"}}
        assert ConfigManager.validate_config(xcpng_config_incomplete, "xcpng") == False
        
        # XCP-ng config with all required fields
        xcpng_config_complete = {
            "xcpng_config": {
                "xapi_url": "test",
                "username": "test", 
                "password": "test",
                "ssh_user": "test"
            }
        }
        assert ConfigManager.validate_config(xcpng_config_complete, "xcpng") == True

class TestBiologicalSpecificMethods:
    """Test biological-specific methods in VM classes"""
    
    def test_syn3a_specific_methods(self):
        """Test Syn3A-specific methods"""
        vm = create_bio_vm("syn3a_test", "syn3a", "basic")
        
        # Essential genes should work for Syn3A
        genes = vm.get_essential_genes()
        assert isinstance(genes, list)
        
        # Operons should raise error for Syn3A
        with pytest.raises(ValueError, match="Operons not supported"):
            vm.manage_operons(["lac_operon"], "activate")
    
    def test_ecoli_specific_methods(self):
        """Test E.coli-specific methods"""
        vm = create_bio_vm("ecoli_test", "ecoli", "basic")
        
        # Plasmid count should work for E.coli
        plasmid_count = vm.get_plasmid_count()
        assert isinstance(plasmid_count, int)
        
        # Essential genes should return empty for E.coli
        genes = vm.get_essential_genes()
        assert genes == []
