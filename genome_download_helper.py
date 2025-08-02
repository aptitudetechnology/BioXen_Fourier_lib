#!/usr/bin/env python3
"""
BioXen Genome Download Helper
============================
Provides robust genome downloading with multiple fallback strategies.
Maps RefSeq accessions to assembly accessions and handles various download methods.
"""

import subprocess
import urllib.request
import urllib.error
import json
from pathlib import Path
from typing import Dict, Optional, Tuple, List
import tempfile
import shutil

class GenomeDownloadHelper:
    """Helper class for downloading genomes with multiple strategies."""
    
    # Mapping of RefSeq accessions to assembly accessions
    REFSEQ_TO_ASSEMBLY = {
        "NC_000913.3": "GCF_000005825.2",  # E. coli K-12 MG1655
        "NC_000908.2": "GCF_000008605.1",  # Mycoplasma genitalium G37
        "NC_001133.9": "GCF_000146045.2",  # S. cerevisiae S288C chromosome I
        "NC_009840.1": "GCF_000015645.1",  # Prochlorococcus marinus MED4
        "NC_009495.1": "GCF_000009685.1",  # Clostridium botulinum A str. ATCC 3502
    }
    
    # Direct NCBI FTP URLs for common genomes
    DIRECT_FTP_URLS = {
        "NC_000913.3": "ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/005/825/GCF_000005825.2_ASM582v2/GCF_000005825.2_ASM582v2_genomic.fna.gz",
        "NC_000908.2": "ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/008/605/GCF_000008605.1_ASM860v1/GCF_000008605.1_ASM860v1_genomic.fna.gz",
        "NC_001133.9": "ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/146/045/GCF_000146045.2_R64/GCF_000146045.2_R64_genomic.fna.gz",
        "NC_009840.1": "ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/015/645/GCF_000015645.1_ASM1564v1/GCF_000015645.1_ASM1564v1_genomic.fna.gz",
        "NC_009495.1": "ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/009/685/GCF_000009685.1_ASM968v1/GCF_000009685.1_ASM968v1_genomic.fna.gz",
    }
    
    def __init__(self, output_dir: str = "genomes"):
        """Initialize the download helper.
        
        Args:
            output_dir: Directory to save downloaded genomes
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def download_genome(self, refseq_accession: str, genome_name: str) -> Tuple[bool, str]:
        """Download a genome using multiple fallback strategies.
        
        Args:
            refseq_accession: RefSeq accession number (e.g., NC_000913.3)
            genome_name: Human-readable name for the genome
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        print(f"🔄 Attempting to download {genome_name} ({refseq_accession})")
        
        # Strategy 1: Try ncbi-genome-download with assembly accession
        success, message = self._try_ncbi_genome_download(refseq_accession, genome_name)
        if success:
            return True, message
        
        print(f"⚠️  Strategy 1 failed: {message}")
        
        # Strategy 2: Try direct FTP download
        success, message = self._try_direct_ftp_download(refseq_accession, genome_name)
        if success:
            return True, message
        
        print(f"⚠️  Strategy 2 failed: {message}")
        
        # Strategy 3: Try wget download
        success, message = self._try_wget_download(refseq_accession, genome_name)
        if success:
            return True, message
        
        print(f"⚠️  Strategy 3 failed: {message}")
        
        # All strategies failed
        return False, "All download strategies failed"
    
    def _try_ncbi_genome_download(self, refseq_accession: str, genome_name: str) -> Tuple[bool, str]:
        """Try downloading with ncbi-genome-download tool."""
        assembly_accession = self.REFSEQ_TO_ASSEMBLY.get(refseq_accession)
        if not assembly_accession:
            return False, f"No assembly accession mapping for {refseq_accession}"
        
        print(f"🔧 Strategy 1: Using ncbi-genome-download with {assembly_accession}")
        
        try:
            # Create temporary download directory
            with tempfile.TemporaryDirectory() as temp_dir:
                cmd = [
                    'ncbi-genome-download',
                    'bacteria',
                    '--formats', 'fasta',
                    '--output-folder', temp_dir,
                    '--parallel', '1',
                    '--retries', '2',
                    '--assembly-accessions', assembly_accession
                ]
                
                print(f"🔄 Running: {' '.join(cmd)}")
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                
                if result.returncode == 0:
                    # Find downloaded files
                    temp_path = Path(temp_dir)
                    fasta_files = list(temp_path.rglob("*.fna*"))
                    
                    if fasta_files:
                        # Copy to final location
                        target_file = self.output_dir / f"{genome_name}.genome"
                        
                        # Handle compressed files
                        source_file = fasta_files[0]
                        if source_file.suffix == '.gz':
                            import gzip
                            with gzip.open(source_file, 'rt') as f_in:
                                with open(target_file, 'w') as f_out:
                                    shutil.copyfileobj(f_in, f_out)
                        else:
                            shutil.copy2(source_file, target_file)
                        
                        return True, f"Downloaded via ncbi-genome-download to {target_file}"
                    else:
                        return False, "No FASTA files found in download"
                else:
                    return False, f"Command failed: {result.stderr}"
                    
        except subprocess.TimeoutExpired:
            return False, "Download timed out (5 minutes)"
        except Exception as e:
            return False, f"Error: {e}"
    
    def _try_direct_ftp_download(self, refseq_accession: str, genome_name: str) -> Tuple[bool, str]:
        """Try downloading directly from NCBI FTP."""
        ftp_url = self.DIRECT_FTP_URLS.get(refseq_accession)
        if not ftp_url:
            return False, f"No direct FTP URL for {refseq_accession}"
        
        print(f"🔧 Strategy 2: Direct FTP download from {ftp_url}")
        
        try:
            target_file = self.output_dir / f"{genome_name}.genome"
            
            # Download the file
            with urllib.request.urlopen(ftp_url, timeout=300) as response:
                # Handle compressed content
                content = response.read()
                
                if ftp_url.endswith('.gz'):
                    import gzip
                    content = gzip.decompress(content)
                
                with open(target_file, 'wb') as f:
                    f.write(content)
            
            return True, f"Downloaded via direct FTP to {target_file}"
            
        except urllib.error.URLError as e:
            return False, f"FTP download failed: {e}"
        except Exception as e:
            return False, f"Error: {e}"
    
    def _try_wget_download(self, refseq_accession: str, genome_name: str) -> Tuple[bool, str]:
        """Try downloading using wget command."""
        ftp_url = self.DIRECT_FTP_URLS.get(refseq_accession)
        if not ftp_url:
            return False, f"No wget URL for {refseq_accession}"
        
        print(f"🔧 Strategy 3: Using wget from {ftp_url}")
        
        try:
            target_file = self.output_dir / f"{genome_name}.genome"
            temp_file = target_file.with_suffix('.tmp')
            
            # Download with wget
            cmd = ['wget', '-q', '-O', str(temp_file), ftp_url]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0 and temp_file.exists():
                # Handle decompression if needed
                if ftp_url.endswith('.gz'):
                    import gzip
                    with gzip.open(temp_file, 'rb') as f_in:
                        with open(target_file, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    temp_file.unlink()  # Remove compressed temp file
                else:
                    temp_file.rename(target_file)
                
                return True, f"Downloaded via wget to {target_file}"
            else:
                if temp_file.exists():
                    temp_file.unlink()
                return False, f"wget failed: {result.stderr}"
                
        except subprocess.TimeoutExpired:
            return False, "wget timed out (5 minutes)"
        except Exception as e:
            return False, f"Error: {e}"
    
    def list_available_genomes(self) -> List[Dict[str, str]]:
        """List all genomes available for download."""
        genomes = []
        for refseq, assembly in self.REFSEQ_TO_ASSEMBLY.items():
            genome_info = {
                'refseq_accession': refseq,
                'assembly_accession': assembly,
                'ftp_available': refseq in self.DIRECT_FTP_URLS
            }
            
            # Add organism names
            organism_names = {
                "NC_000913.3": "Escherichia coli K-12 MG1655",
                "NC_000908.2": "Mycoplasma genitalium G37",
                "NC_001133.9": "Saccharomyces cerevisiae S288C",
                "NC_009840.1": "Prochlorococcus marinus MED4",
                "NC_009495.1": "Clostridium botulinum A str. ATCC 3502",
            }
            
            genome_info['organism'] = organism_names.get(refseq, "Unknown organism")
            genomes.append(genome_info)
        
        return genomes

def test_download_single_genome():
    """Test downloading a single genome."""
    print("🧪 Testing Single Genome Download")
    print("=" * 50)
    
    helper = GenomeDownloadHelper()
    
    # Test with E. coli (most reliable)
    success, message = helper.download_genome("NC_000913.3", "E_coli_K12_MG1655")
    
    if success:
        print(f"✅ Success: {message}")
    else:
        print(f"❌ Failed: {message}")
    
    return success

def main():
    """Test the genome download helper."""
    print("🧬 BioXen Genome Download Helper Test")
    print("=" * 50)
    
    helper = GenomeDownloadHelper()
    
    # List available genomes
    print("\n📋 Available Genomes:")
    genomes = helper.list_available_genomes()
    for genome in genomes:
        print(f"  🧬 {genome['organism']}")
        print(f"     RefSeq: {genome['refseq_accession']}")
        print(f"     Assembly: {genome['assembly_accession']}")
        print(f"     FTP: {'✅' if genome['ftp_available'] else '❌'}")
        print()
    
    # Test download
    print("🔄 Testing download with E. coli K-12 MG1655...")
    success, message = helper.download_genome("NC_000913.3", "E_coli_K12_MG1655_test")
    
    if success:
        print(f"✅ Test passed: {message}")
    else:
        print(f"❌ Test failed: {message}")

if __name__ == "__main__":
    main()
