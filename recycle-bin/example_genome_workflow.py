#!/usr/bin/env python3
"""
Example: Download and test Mycoplasma genitalium with BioXen

This script demonstrates the complete workflow:
1. Download minimal genome from NCBI
2. Convert to BioXen format
3. Test with BioXen hypervisor
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def example_workflow():
    """Demonstrate the complete BioXen genome workflow."""
    
    print("🧬 BioXen Genome Integration Example")
    print("=" * 50)
    
    print("\n📋 Step 1: Download Mycoplasma genitalium genome")
    print("Command that would be run:")
    print("ncbi-genome-download bacteria --taxids 2097 --assembly-levels complete --formats fasta,gff")
    print("(Download skipped in demo - using simulated data)")
    
    print("\n📋 Step 2: Convert to BioXen format")
    print("This would use the converter to parse GFF3 and FASTA files...")
    
    # Simulate what the converter would produce
    from genome.schema import BioXenGenomeSchema, BioXenGeneRecord
    
    # Create example Mycoplasma genitalium genes (simplified)
    example_genes = [
        BioXenGeneRecord(
            start=1, length=1311, end=1311, strand=1, gene_type=1,
            gene_id="MG_001", description="DNA polymerase III subunit beta",
            essential=True, functional_category="dna_replication"
        ),
        BioXenGeneRecord(
            start=1368, length=3150, end=4517, strand=1, gene_type=1,
            gene_id="MG_002", description="DNA gyrase subunit A",
            essential=True, functional_category="dna_replication"
        ),
        BioXenGeneRecord(
            start=4614, length=2466, end=7079, strand=1, gene_type=1,
            gene_id="MG_003", description="DNA gyrase subunit B",
            essential=True, functional_category="dna_replication"
        ),
        BioXenGeneRecord(
            start=7213, length=315, end=7527, strand=1, gene_type=0,
            gene_id="MG_004", description="tRNA-Met",
            essential=True, functional_category="translation"
        ),
        BioXenGeneRecord(
            start=7585, length=1683, end=9267, strand=1, gene_type=1,
            gene_id="MG_005", description="30S ribosomal protein S1",
            essential=True, functional_category="protein_synthesis"
        ),
        # Add some non-essential genes
        BioXenGeneRecord(
            start=10000, length=900, end=10899, strand=1, gene_type=1,
            gene_id="MG_100", description="hypothetical protein",
            essential=False, functional_category="other"
        ),
        BioXenGeneRecord(
            start=11000, length=1200, end=12199, strand=-1, gene_type=1,
            gene_id="MG_101", description="membrane protein",
            essential=False, functional_category="transport"
        ),
    ]
    
    # Create simulated genome schema
    mg_genome = BioXenGenomeSchema(
        organism="Mycoplasma genitalium G37",
        assembly_accession="GCF_000027345.1",
        genome_size=580074,  # Actual M. genitalium genome size
        gc_content=31.7,
        genes=example_genes
    )
    
    print(f"✅ Created BioXen genome schema:")
    print(f"   Organism: {mg_genome.organism}")
    print(f"   Genome size: {mg_genome.genome_size:,} bp")
    print(f"   Total genes: {mg_genome.total_genes}")
    print(f"   Essential genes: {mg_genome.essential_genes}")
    print(f"   GC content: {mg_genome.gc_content:.1f}%")
    
    print("\n📋 Step 3: Export to BioXen format")
    output_file = Path("genomes/Mycoplasma_genitalium_example.genome")
    output_file.parent.mkdir(exist_ok=True)
    mg_genome.export_bioxen_format(output_file)
    print(f"✅ Exported to: {output_file}")
    
    # Show the file contents
    print("\n📄 Generated .genome file contents:")
    with open(output_file, 'r') as f:
        lines = f.readlines()
        for line in lines[:15]:  # Show first 15 lines
            print(f"   {line.rstrip()}")
        if len(lines) > 15:
            print(f"   ... ({len(lines) - 15} more lines)")
    
    print("\n📋 Step 4: Create VM template")
    template = mg_genome.to_vm_template()
    print(f"✅ VM template created:")
    print(f"   Min memory: {template['min_memory_kb']} KB")
    print(f"   Min CPU: {template['min_cpu_percent']}%")
    print(f"   Boot time: {template['boot_time_ms']} ms")
    print(f"   Essential gene categories: {len(template['essential_by_function'])}")
    
    for category, genes in template['essential_by_function'].items():
        print(f"     {category}: {len(genes)} genes")
    
    print("\n📋 Step 5: Test with BioXen hypervisor")
    try:
        from hypervisor.core import BioXenHypervisor, ResourceAllocation
        
        # Create hypervisor
        hypervisor = BioXenHypervisor()
        
        # Create resource allocation based on M. genitalium requirements
        resources = ResourceAllocation(
            memory_kb=template['min_memory_kb'] * 2,
            atp_percentage=30.0,
            ribosomes=25,
            rna_polymerase=10,
            priority=2
        )
        
        # Create and start VM
        vm_id = "mycoplasma_vm"
        success = hypervisor.create_vm(vm_id, "mycoplasma_genitalium", resources)
        
        if success:
            print(f"✅ Created VM: {vm_id}")
            
            # Start VM
            hypervisor.start_vm(vm_id)
            vm_status = hypervisor.get_vm_status(vm_id)
            print(f"✅ Started VM - Status: {vm_status['state']}")
            print(f"   Memory: {vm_status['memory_kb']} KB")
            print(f"   Ribosomes: {vm_status['ribosome_allocation']}")
            print(f"   ATP: {vm_status['atp_percentage']}%")
            
            # Pause VM
            hypervisor.pause_vm(vm_id)
            print(f"✅ VM paused successfully")
            
        else:
            print(f"❌ Failed to create VM")
    
    except Exception as e:
        print(f"❌ Hypervisor test failed: {e}")
    
    print("\n🎉 Example workflow completed!")
    print("\n📚 To use with real data:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Download genome: python download_genomes.py mycoplasma_genitalium")
    print("3. Test integration: python test_real_genome.py")
    
    print("\n🔬 Real workflow commands:")
    print("# Download Mycoplasma genitalium")
    print("ncbi-genome-download bacteria --taxids 2097 --assembly-levels complete --formats fasta,gff")
    print("")
    print("# Convert to BioXen format")
    print("python -c \"")
    print("from src.genome.converter import convert_ncbi_bacteria_download")
    print("from pathlib import Path")
    print("convert_ncbi_bacteria_download(")
    print("    Path('refseq/bacteria/Mycoplasma_genitalium/...'),")
    print("    'Mycoplasma genitalium',")
    print("    Path('genomes/')")
    print(")\"")
    print("")
    print("# Test with BioXen")
    print("python test_real_genome.py")

if __name__ == "__main__":
    example_workflow()
