#!/usr/bin/env python3
"""
Quick test of genome scanning and usability detection
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / 'src'))

try:
    import questionary
    from genome.schema import BioXenGenomeValidator
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

def test_genome_scanning():
    """Test the genome scanning logic."""
    print("🧬 Testing BioXen Genome Scanning")
    print("=" * 40)
    
    genomes_dir = Path("genomes")
    if not genomes_dir.exists():
        print("❌ No genomes directory found")
        return
    
    genome_files = list(genomes_dir.glob("*.genome"))
    available_genomes = {}
    
    for genome_file in genome_files:
        print(f"\n🔍 Analyzing: {genome_file.name}")
        
        try:
            # Quick validation
            is_valid, errors = BioXenGenomeValidator.validate_file(genome_file)
            
            # For real genomes, we'll be more permissive
            # Consider a genome "usable" if it has structural validity even with warnings
            has_critical_errors = any('invalid format' in str(error).lower() or 
                                    'missing required' in str(error).lower() or
                                    'cannot parse' in str(error).lower() 
                                    for error in errors)
            
            is_usable = is_valid or not has_critical_errors
            
            # Try to get metadata from corresponding JSON file
            json_file = genomes_dir / f"{genome_file.stem}.json"
            metadata = {}
            if json_file.exists():
                import json
                with open(json_file, 'r') as f:
                    metadata = json.load(f)
            
            print(f"   Valid: {is_valid}")
            print(f"   Usable: {is_usable}")
            print(f"   Errors: {len(errors)}")
            print(f"   Critical errors: {has_critical_errors}")
            print(f"   Has metadata: {bool(metadata)}")
            
            if metadata:
                print(f"   Organism: {metadata.get('organism', 'Unknown')}")
                print(f"   Genes: {metadata.get('total_genes', '?')}")
            
            available_genomes[genome_file.stem] = {
                'file': genome_file,
                'valid': is_valid,
                'usable': is_usable,
                'errors': errors,
                'metadata': metadata
            }
            
        except Exception as e:
            print(f"   ❌ Error scanning: {e}")
    
    print(f"\n📊 Summary:")
    print(f"   Total genomes: {len(available_genomes)}")
    
    valid_count = sum(1 for info in available_genomes.values() if info['valid'])
    usable_count = sum(1 for info in available_genomes.values() if info['usable'])
    
    print(f"   Valid genomes: {valid_count}")
    print(f"   Usable genomes: {usable_count}")
    
    print(f"\n🎯 Usable genomes for BioXen:")
    for name, info in available_genomes.items():
        if info['usable']:
            status = "✅ Valid" if info['valid'] else "⚠️  Usable (warnings)"
            organism = info['metadata'].get('organism', name) if info['metadata'] else name
            print(f"   {status}: {organism}")

if __name__ == "__main__":
    test_genome_scanning()
