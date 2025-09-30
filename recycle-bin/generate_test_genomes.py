#!/usr/bin/env python3
"""
BioXen Genome Generator for Phase 2 Testing

Creates additional synthetic genomes based on real bacterial species
to demonstrate multi-genome compatibility analysis capabilities.
"""

import os
import random
from pathlib import Path

class SyntheticGenomeGenerator:
    """Generate synthetic genomes based on real bacterial characteristics"""
    
    def __init__(self):
        self.genome_templates = {
            'mycoplasma_genitalium': {
                'gene_count': 470,
                'average_length': 800,
                'gc_content': 32.0,
                'essential_ratio': 0.35,
                'description_templates': [
                    'ATP synthase subunit',
                    'Ribosomal protein',
                    'DNA polymerase',
                    'RNA polymerase',
                    'tRNA synthetase',
                    'Translation factor',
                    'Cell division protein',
                    'Membrane protein',
                    'Metabolic enzyme',
                    'Hypothetical protein'
                ]
            },
            'mycoplasma_pneumoniae': {
                'gene_count': 689,
                'average_length': 950,
                'gc_content': 40.0,
                'essential_ratio': 0.28,
                'description_templates': [
                    'Adhesin protein',
                    'ATP synthase complex',
                    'Ribosomal protein',
                    'DNA repair enzyme',
                    'RNA polymerase subunit',
                    'Aminoacyl-tRNA synthetase',
                    'Cell wall protein',
                    'Transport protein',
                    'Glycolytic enzyme',
                    'Regulatory protein'
                ]
            },
            'carsonella_ruddii': {
                'gene_count': 182,
                'average_length': 650,
                'gc_content': 16.5,
                'essential_ratio': 0.70,
                'description_templates': [
                    'Essential ATP synthase',
                    'Core ribosomal protein',
                    'DNA replication protein',
                    'RNA polymerase core',
                    'tRNA synthetase',
                    'Translation initiation factor',
                    'Cell division protein',
                    'Essential membrane protein',
                    'Core metabolic enzyme',
                    'Minimal protein'
                ]
            },
            'buchnera_aphidicola': {
                'gene_count': 583,
                'average_length': 780,
                'gc_content': 26.3,
                'essential_ratio': 0.42,
                'description_templates': [
                    'Amino acid biosynthesis',
                    'Vitamin synthesis enzyme',
                    'Ribosomal protein',
                    'DNA polymerase',
                    'RNA polymerase',
                    'tRNA synthetase',
                    'Translation factor',
                    'Symbiosis protein',
                    'Metabolic pathway enzyme',
                    'Host interaction protein'
                ]
            }
        }
    
    def generate_all_genomes(self, output_dir: str = "genomes"):
        """Generate all synthetic genomes"""
        print("🧬 Generating Synthetic Genomes for Phase 2 Testing")
        print("=" * 55)
        
        os.makedirs(output_dir, exist_ok=True)
        
        generated_count = 0
        for species, template in self.genome_templates.items():
            output_path = os.path.join(output_dir, f"{species}.genome")
            
            # Skip if already exists
            if os.path.exists(output_path):
                print(f"   ⏭️  {species}.genome already exists, skipping")
                continue
            
            success = self.generate_genome(species, template, output_path)
            if success:
                generated_count += 1
                print(f"   ✅ Generated {species}.genome ({template['gene_count']} genes)")
        
        print(f"\n🎉 Generated {generated_count} new synthetic genomes")
        return generated_count
    
    def generate_genome(self, species: str, template: dict, output_path: str) -> bool:
        """Generate a single synthetic genome"""
        try:
            genes = []
            current_position = 1000  # Start position
            
            for i in range(template['gene_count']):
                # Generate gene characteristics
                gene_length = self._generate_gene_length(template['average_length'])
                strand = random.choice([1, -1])
                gene_type = self._generate_gene_type()
                gene_id = f"{species.upper().replace('_', '')}_{'%04d' % (i + 1)}"
                description = random.choice(template['description_templates'])
                
                # Calculate positions
                start_pos = current_position
                end_pos = current_position + gene_length - 1
                
                # Create gene entry
                gene_line = f"{start_pos:8d} {gene_length:8d} {end_pos:8d} {strand:2d} {gene_type:2d} {gene_id:25s} {description}"
                genes.append(gene_line)
                
                # Update position (add some intergenic space)
                current_position = end_pos + random.randint(50, 200)
            
            # Write genome file
            with open(output_path, 'w') as f:
                f.write('\n'.join(genes))
                f.write('\n')
            
            return True
            
        except Exception as e:
            print(f"❌ Error generating {species}: {e}")
            return False
    
    def _generate_gene_length(self, average: int) -> int:
        """Generate realistic gene length with variation"""
        # Use normal distribution with some bounds
        length = int(random.normalvariate(average, average * 0.3))
        
        # Ensure reasonable bounds
        return max(100, min(3000, length))
    
    def _generate_gene_type(self) -> int:
        """Generate gene type (weighted toward protein-coding)"""
        # 0=RNA, 1=protein, 2=tRNA, 3=rRNA, 4=ncRNA, 5=pseudogene
        weights = [0.05, 0.85, 0.03, 0.02, 0.03, 0.02]
        return random.choices(range(6), weights=weights)[0]

def main():
    """Main function"""
    generator = SyntheticGenomeGenerator()
    
    # Generate all genomes
    count = generator.generate_all_genomes()
    
    if count > 0:
        print(f"\n🚀 Ready for enhanced Phase 2 analysis with {count} new genomes!")
        print("   Run: python3 multi_genome_analyzer.py")
    else:
        print(f"\n📋 All genomes already exist. Phase 2 analysis ready!")
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
