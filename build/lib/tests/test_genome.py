"""
Unit tests for Syn3A genome and VM image builder
"""

import unittest
import tempfile
import os
import sys

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.genome.syn3a import Syn3ATemplate, VMImageBuilder, Gene, Syn3AGenome

class TestSyn3AGenome(unittest.TestCase):
    """Test Syn3A genome functionality"""
    
    def test_gene_creation(self):
        """Test creating a gene"""
        gene = Gene(
            gene_id="TEST_001",
            name="test_gene",
            sequence="ATGAAAGCAATTTTCGTACTGAAAGGTTGGTGGCGCACTTCCTGAA",
            function="Test function",
            essential=True,
            category="test"
        )
        
        self.assertEqual(gene.gene_id, "TEST_001")
        self.assertEqual(gene.name, "test_gene")
        self.assertTrue(gene.essential)
        self.assertEqual(gene.category, "test")
    
    def test_syn3a_genome_creation(self):
        """Test creating Syn3A genome"""
        genes = [
            Gene("G1", "gene1", "ATGAAATAA", "Function 1", True, "category1"),
            Gene("G2", "gene2", "ATGGGGTAA", "Function 2", False, "category2")
        ]
        
        genome = Syn3AGenome(
            genome_id="test_genome",
            genes=genes,
            total_size=1000,
            gc_content=0.35
        )
        
        self.assertEqual(genome.genome_id, "test_genome")
        self.assertEqual(len(genome.genes), 2)
        self.assertEqual(genome.total_size, 1000)
        self.assertEqual(genome.gc_content, 0.35)
    
    def test_get_essential_genes(self):
        """Test getting essential genes"""
        genes = [
            Gene("G1", "gene1", "ATG", "Function 1", True, "cat1"),
            Gene("G2", "gene2", "ATG", "Function 2", False, "cat2"),
            Gene("G3", "gene3", "ATG", "Function 3", True, "cat1")
        ]
        
        genome = Syn3AGenome("test", genes, 1000, 0.35)
        essential = genome.get_essential_genes()
        
        self.assertEqual(len(essential), 2)
        self.assertEqual(essential[0].gene_id, "G1")
        self.assertEqual(essential[1].gene_id, "G3")
    
    def test_get_genes_by_category(self):
        """Test getting genes by category"""
        genes = [
            Gene("G1", "gene1", "ATG", "Function 1", True, "cat1"),
            Gene("G2", "gene2", "ATG", "Function 2", False, "cat2"),
            Gene("G3", "gene3", "ATG", "Function 3", True, "cat1")
        ]
        
        genome = Syn3AGenome("test", genes, 1000, 0.35)
        cat1_genes = genome.get_genes_by_category("cat1")
        
        self.assertEqual(len(cat1_genes), 2)
        self.assertEqual(cat1_genes[0].gene_id, "G1")
        self.assertEqual(cat1_genes[1].gene_id, "G3")

class TestSyn3ATemplate(unittest.TestCase):
    """Test Syn3A template functionality"""
    
    def setUp(self):
        """Set up template"""
        self.template = Syn3ATemplate()
    
    def test_template_creation(self):
        """Test template initialization"""
        genome = self.template.get_genome()
        
        self.assertIsInstance(genome, Syn3AGenome)
        self.assertEqual(genome.genome_id, "syn3a_minimal_v1.0")
        self.assertGreater(len(genome.genes), 0)
        self.assertGreater(genome.total_size, 0)
    
    def test_essential_genes_present(self):
        """Test that essential genes are present"""
        genome = self.template.get_genome()
        essential_genes = genome.get_essential_genes()
        
        self.assertGreater(len(essential_genes), 5)  # Should have multiple essential genes
        
        # Check for key essential gene categories
        categories = set(gene.category for gene in essential_genes)
        expected_categories = {"replication", "transcription", "translation", "metabolism"}
        self.assertTrue(expected_categories.issubset(categories))

class TestVMImageBuilder(unittest.TestCase):
    """Test VM image builder functionality"""
    
    def setUp(self):
        """Set up image builder"""
        self.builder = VMImageBuilder()
    
    def test_build_vm_image(self):
        """Test building a VM image"""
        config = {
            "resource_limits": {
                "max_ribosomes": 25
            },
            "isolation_level": "high"
        }
        
        vm_image = self.builder.build_vm_image("test-vm", config)
        
        self.assertEqual(vm_image["vm_id"], "test-vm")
        self.assertEqual(vm_image["config"], config)
        self.assertEqual(vm_image["hypervisor_version"], "bioxen-1.0")
        self.assertIn("genome", vm_image)
        self.assertIn("resource_requirements", vm_image)
        
        # Check that genome was modified
        genome = vm_image["genome"]
        self.assertNotEqual(genome.genome_id, "syn3a_minimal_v1.0")  # Should be modified
        self.assertIn("test-vm", genome.genome_id)
    
    def test_resource_requirements_calculation(self):
        """Test resource requirements calculation"""
        vm_image = self.builder.build_vm_image("test-vm", {})
        requirements = vm_image["resource_requirements"]
        
        self.assertIn("min_ribosomes", requirements)
        self.assertIn("min_atp_percentage", requirements)
        self.assertIn("min_memory_kb", requirements)
        self.assertIn("min_rna_polymerase", requirements)
        
        self.assertGreater(requirements["min_ribosomes"], 0)
        self.assertGreater(requirements["min_atp_percentage"], 0)
        self.assertGreater(requirements["min_memory_kb"], 0)
    
    def test_save_load_vm_image(self):
        """Test saving and loading VM images"""
        vm_image = self.builder.build_vm_image("test-vm", {"test": "config"})
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            # Save image
            self.builder.save_vm_image(vm_image, temp_file)
            self.assertTrue(os.path.exists(temp_file))
            
            # Load image
            loaded_image = self.builder.load_vm_image(temp_file)
            
            self.assertEqual(loaded_image["vm_id"], "test-vm")
            self.assertEqual(loaded_image["config"]["test"], "config")
            self.assertEqual(loaded_image["hypervisor_version"], "bioxen-1.0")
            
            # Check genome was reconstructed
            self.assertIsInstance(loaded_image["genome"], Syn3AGenome)
            self.assertEqual(len(loaded_image["genome"].genes), len(vm_image["genome"].genes))
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_protein_to_dna_conversion(self):
        """Test protein to DNA conversion"""
        protein_seq = "MHGS"  # Met-His-Gly-Ser
        dna_seq = self.builder._protein_to_dna(protein_seq)
        
        # Should be 12 nucleotides (4 codons × 3 nucleotides)
        self.assertEqual(len(dna_seq), 12)
        self.assertTrue(dna_seq.startswith("ATG"))  # Should start with Met codon
    
    def test_vm_tagging(self):
        """Test that VM-specific tags are added"""
        vm_image = self.builder.build_vm_image("tagged-vm", {})
        genome = vm_image["genome"]
        
        # Should have added VM marker gene
        marker_genes = [g for g in genome.genes if "marker" in g.gene_id]
        self.assertGreater(len(marker_genes), 0)
        
        # Should have added monitoring genes
        monitoring_genes = [g for g in genome.genes if g.category == "hypervisor"]
        self.assertGreater(len(monitoring_genes), 0)

if __name__ == '__main__':
    unittest.main()
