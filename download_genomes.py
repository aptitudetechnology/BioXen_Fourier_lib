#!/usr/bin/env python3
"""
BioXen Genome Downloader and Converter

Downloads minimal bacterial genomes from NCBI and converts them to BioXen format.
Focuses on minimal genomes suitable for biological virtualization.
"""

import subprocess
import sys
from pathlib import Path
import tempfile
import shutil

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / 'src'))

try:
    from genome.converter import convert_ncbi_bacteria_download
    from genome.schema import BioXenGenomeValidator
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running from the BioXen root directory")
    sys.exit(1)

# Known minimal genomes suitable for BioXen
MINIMAL_GENOMES = {
    'mycoplasma_genitalium': {
        'scientific_name': 'Mycoplasma genitalium',
        'taxid': '2097',
        'description': 'One of the smallest known bacterial genomes (~580kb, ~470 genes)',
        'assembly_level': 'complete',
        'refseq_category': 'reference'
    },
    'mycoplasma_pneumoniae': {
        'scientific_name': 'Mycoplasma pneumoniae',
        'taxid': '2104',
        'description': 'Small bacterial pathogen (~816kb, ~689 genes)',
        'assembly_level': 'complete',
        'refseq_category': 'reference'
    },
    'carsonella_ruddii': {
        'scientific_name': 'Carsonella ruddii',
        'taxid': '114186',
        'description': 'Smallest known bacterial genome (~160kb, ~182 genes)',
        'assembly_level': 'complete',
        'refseq_category': 'representative'
    },
    'buchnera_aphidicola': {
        'scientific_name': 'Buchnera aphidicola',
        'taxid': '107806',
        'description': 'Endosymbiotic bacterium with reduced genome (~640kb, ~583 genes)',
        'assembly_level': 'complete',
        'refseq_category': 'representative'
    }
}

def check_dependencies():
    """Check if required tools are available."""
    try:
        result = subprocess.run(['ncbi-genome-download', '--help'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            raise FileNotFoundError
    except FileNotFoundError:
        print("❌ ncbi-genome-download not found!")
        print("Install with: pip install ncbi-genome-download")
        return False
    
    return True

def download_genome(genome_key: str, download_dir: Path) -> bool:
    """Download a genome using ncbi-genome-download."""
    
    if genome_key not in MINIMAL_GENOMES:
        print(f"❌ Unknown genome: {genome_key}")
        print(f"Available genomes: {', '.join(MINIMAL_GENOMES.keys())}")
        return False
    
    info = MINIMAL_GENOMES[genome_key]
    
    print(f"🌐 Downloading {info['scientific_name']}...")
    print(f"   Description: {info['description']}")
    
    # Prepare download command
    cmd = [
        'ncbi-genome-download',
        'bacteria',
        '--taxids', info['taxid'],
        '--assembly-levels', info['assembly_level'],
        '--refseq-categories', info['refseq_category'],
        '--formats', 'fasta,gff',
        '--output-folder', str(download_dir),
        '--parallel', '2',
        '--retries', '3'
    ]
    
    try:
        print(f"📥 Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ Download completed successfully")
            return True
        else:
            print(f"❌ Download failed:")
            print(f"Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Download timed out (>5 minutes)")
        return False
    except Exception as e:
        print(f"❌ Download error: {e}")
        return False

def find_downloaded_genome(download_dir: Path, scientific_name: str) -> Path:
    """Find the downloaded genome directory."""
    
    # ncbi-genome-download creates: download_dir/bacteria/genus_species/...
    bacteria_dir = download_dir / 'bacteria'
    
    if not bacteria_dir.exists():
        raise FileNotFoundError(f"No bacteria directory found in {download_dir}")
    
    # Look for genus_species directory
    genus, species = scientific_name.split(' ', 1)
    expected_dir = f"{genus}_{species}"
    
    for subdir in bacteria_dir.iterdir():
        if subdir.is_dir() and expected_dir.lower() in subdir.name.lower():
            # Find the actual genome directory (contains assembly files)
            for assembly_dir in subdir.iterdir():
                if assembly_dir.is_dir():
                    fasta_files = list(assembly_dir.glob("*.fna.gz")) + list(assembly_dir.glob("*.fna"))
                    gff_files = list(assembly_dir.glob("*.gff.gz")) + list(assembly_dir.glob("*.gff"))
                    
                    if fasta_files and gff_files:
                        return assembly_dir
    
    raise FileNotFoundError(f"Could not find downloaded genome for {scientific_name}")

def convert_downloaded_genome(genome_key: str, download_dir: Path, output_dir: Path) -> bool:
    """Convert a downloaded genome to BioXen format."""
    
    info = MINIMAL_GENOMES[genome_key]
    scientific_name = info['scientific_name']
    
    try:
        # Find the downloaded genome
        genome_dir = find_downloaded_genome(download_dir, scientific_name)
        print(f"📁 Found genome files in: {genome_dir}")
        
        # Convert to BioXen format
        schema = convert_ncbi_bacteria_download(genome_dir, scientific_name, output_dir)
        
        # Validate the converted genome
        safe_name = scientific_name.replace(' ', '_')
        bioxen_file = output_dir / f"{safe_name}.genome"
        
        is_valid, errors = BioXenGenomeValidator.validate_file(bioxen_file)
        
        if is_valid:
            print("✅ Validation passed")
        else:
            print("⚠️  Validation warnings:")
            for error in errors[:5]:  # Show first 5 errors
                print(f"   {error}")
        
        return True
        
    except Exception as e:
        print(f"❌ Conversion failed: {e}")
        return False

def download_and_convert_genome(genome_key: str, output_dir: Path, keep_downloads: bool = False):
    """Download and convert a genome in one step."""
    
    if not check_dependencies():
        return False
    
    # Create temporary download directory
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Download genome
        if not download_genome(genome_key, temp_path):
            return False
        
        # Convert to BioXen format
        if not convert_downloaded_genome(genome_key, temp_path, output_dir):
            return False
        
        # Optionally keep downloads
        if keep_downloads:
            download_backup = output_dir / 'downloads' / genome_key
            download_backup.mkdir(parents=True, exist_ok=True)
            shutil.copytree(temp_path / 'bacteria', download_backup / 'bacteria')
            print(f"📁 Downloads saved to: {download_backup}")
    
    return True

def list_available_genomes():
    """List all available minimal genomes."""
    print("🧬 Available Minimal Genomes for BioXen:")
    print("=" * 60)
    
    for key, info in MINIMAL_GENOMES.items():
        print(f"\n🔑 {key}")
        print(f"   Scientific name: {info['scientific_name']}")
        print(f"   Description: {info['description']}")
        print(f"   Assembly level: {info['assembly_level']}")

def main():
    """Main CLI interface."""
    
    if len(sys.argv) < 2:
        print("🧬 BioXen Genome Downloader")
        print("\nUsage:")
        print("  python download_genomes.py list                    # List available genomes")
        print("  python download_genomes.py <genome_key>            # Download and convert")
        print("  python download_genomes.py <genome_key> --keep     # Keep download files")
        print("  python download_genomes.py all                     # Download all genomes")
        print("\nExamples:")
        print("  python download_genomes.py mycoplasma_genitalium")
        print("  python download_genomes.py carsonella_ruddii --keep")
        sys.exit(1)
    
    command = sys.argv[1]
    keep_downloads = '--keep' in sys.argv
    
    # Create output directory
    output_dir = Path('genomes')
    output_dir.mkdir(exist_ok=True)
    
    if command == 'list':
        list_available_genomes()
        
    elif command == 'all':
        print("🌐 Downloading all minimal genomes...")
        
        success_count = 0
        for genome_key in MINIMAL_GENOMES.keys():
            print(f"\n{'='*60}")
            print(f"Processing: {genome_key}")
            print(f"{'='*60}")
            
            if download_and_convert_genome(genome_key, output_dir, keep_downloads):
                success_count += 1
            else:
                print(f"❌ Failed to process {genome_key}")
        
        print(f"\n🎉 Downloaded and converted {success_count}/{len(MINIMAL_GENOMES)} genomes")
        
    elif command in MINIMAL_GENOMES:
        print(f"🧬 Processing: {command}")
        
        if download_and_convert_genome(command, output_dir, keep_downloads):
            print(f"\n🎉 Successfully downloaded and converted {command}")
            
            # Show what was created
            safe_name = MINIMAL_GENOMES[command]['scientific_name'].replace(' ', '_')
            bioxen_file = output_dir / f"{safe_name}.genome"
            json_file = output_dir / f"{safe_name}.json"
            
            print(f"\n📁 Files created:")
            print(f"   {bioxen_file}")
            print(f"   {json_file}")
            
            print(f"\n🧪 Test with BioXen:")
            print(f"   python3 test_real_genome.py  # (using your existing syn3A.genome)")
            print(f"   # Or modify test to use: {bioxen_file}")
        else:
            print(f"❌ Failed to process {command}")
            sys.exit(1)
    
    else:
        print(f"❌ Unknown genome: {command}")
        print("Run 'python download_genomes.py list' to see available genomes")
        sys.exit(1)

if __name__ == "__main__":
    main()
