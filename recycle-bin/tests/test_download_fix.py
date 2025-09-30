#!/usr/bin/env python3
"""
Quick test script to verify ncbi-genome-download command works correctly.
"""

import subprocess
import sys
from pathlib import Path

def test_ncbi_download_command():
    """Test the corrected ncbi-genome-download command."""
    
    print("🧪 Testing NCBI Download Command")
    print("="*40)
    
    # Test accession (E. coli K-12 MG1655)
    accession = "NC_000913.3"
    
    # Create test download directory
    test_dir = Path("test_downloads")
    test_dir.mkdir(exist_ok=True)
    
    # Corrected command
    cmd = [
        'ncbi-genome-download',
        'bacteria',
        '--formats', 'fasta',
        '--output-folder', str(test_dir),
        '--parallel', '1',
        '--retries', '2',
        '--assembly-accessions', accession,
        '--dry-run'  # Only test, don't actually download
    ]
    
    print(f"🔄 Testing command: {' '.join(cmd)}")
    print("💡 Using --dry-run to test without downloading")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Command syntax is correct!")
            print("📊 Output:")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print("❌ Command failed:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Command timed out")
        return False
    except FileNotFoundError:
        print("❌ ncbi-genome-download not found")
        print("💡 Install with: pip install ncbi-genome-download")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        # Clean up test directory
        if test_dir.exists():
            import shutil
            shutil.rmtree(test_dir, ignore_errors=True)

def show_alternative_approaches():
    """Show alternative download approaches if ncbi-genome-download fails."""
    
    print("\n🔄 Alternative Download Approaches")
    print("="*40)
    
    print("1. 📥 Direct NCBI FTP Download:")
    print("   wget ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/005/825/GCF_000005825.2_ASM582v2/")
    
    print("\n2. 🧬 Using BioPython (if available):")
    print("   from Bio import Entrez")
    print("   # Set your email and download via Entrez")
    
    print("\n3. 🌐 Manual Download:")
    print("   Visit: https://www.ncbi.nlm.nih.gov/assembly/")
    print("   Search for accession: NC_000913.3")
    print("   Download FASTA files manually")
    
    print("\n4. 🔧 Using JCVI Entrez tools:")
    print("   from jcvi.apps.entrez import download_genbank")
    print("   # Use JCVI's built-in download capabilities")

if __name__ == "__main__":
    success = test_ncbi_download_command()
    
    if not success:
        show_alternative_approaches()
        
    print(f"\n📋 Test Result: {'PASSED' if success else 'NEEDS ATTENTION'}")
