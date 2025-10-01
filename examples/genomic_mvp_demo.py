"""
Genomic MVP Demo: Four-Lens Analysis System with Real Syn3A Data

Demonstrates all four lenses analyzing real genomic data from Syn3A minimal cell.

This demo shows:
1. Real FASTA file parsing and signal extraction
2. Multiple biological signals (gene lengths, GC content, codon usage)
3. Signal validation and preprocessing
4. All four lens analyses on real data
5. Biological interpretation of results

Uses real Syn3A genome data - no synthetic signals!
"""

import numpy as np
import sys
from pathlib import Path
import re

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from bioxen_fourier_vm_lib.analysis.system_analyzer import SystemAnalyzer


def parse_fasta(filepath):
    """Parse FASTA file and extract gene information."""
    genes = []
    current_gene = None
    current_seq = []
    
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                # Save previous gene
                if current_gene:
                    sequence = ''.join(current_seq)
                    genes.append({
                        'id': current_gene['id'],
                        'description': current_gene['description'],
                        'sequence': sequence,
                        'length': len(sequence)
                    })
                
                # Parse header: >JCVISYN3A_0002_001 DNApolymeraseIIIsubunitbeta len=563 type=1
                parts = line[1:].split(' ')
                gene_id = parts[0]
                description = ' '.join(parts[1:])
                
                current_gene = {
                    'id': gene_id,
                    'description': description
                }
                current_seq = []
            else:
                current_seq.append(line)
        
        # Don't forget the last gene
        if current_gene:
            sequence = ''.join(current_seq)
            genes.append({
                'id': current_gene['id'],
                'description': current_gene['description'],
                'sequence': sequence,
                'length': len(sequence)
            })
    
    return genes


def calculate_gc_content(sequence):
    """Calculate GC content percentage."""
    if not sequence:
        return 0.0
    gc_count = sequence.upper().count('G') + sequence.upper().count('C')
    return (gc_count / len(sequence)) * 100.0


def calculate_codon_bias(sequence):
    """Calculate simple codon bias metric (leucine codon usage)."""
    # Look for leucine codons: CTT, CTC, CTA, CTG, TTA, TTG
    leucine_codons = ['CTT', 'CTC', 'CTA', 'CTG', 'TTA', 'TTG']
    sequence = sequence.upper()
    
    total_codons = len(sequence) // 3
    if total_codons == 0:
        return 0.0
    
    leucine_count = 0
    for i in range(0, len(sequence) - 2, 3):
        codon = sequence[i:i+3]
        if codon in leucine_codons:
            leucine_count += 1
    
    return (leucine_count / total_codons) * 100.0


def extract_biological_signals(genes):
    """Extract multiple biological signals from gene data."""
    
    # Signal 1: Gene lengths (structural complexity)
    gene_lengths = [gene['length'] for gene in genes]
    
    # Signal 2: GC content (thermodynamic stability)
    gc_contents = [calculate_gc_content(gene['sequence']) for gene in genes]
    
    # Signal 3: Codon bias (translation efficiency)
    codon_biases = [calculate_codon_bias(gene['sequence']) for gene in genes]
    
    # Create time-like index (gene position in genome)
    timestamps = np.arange(len(genes))
    
    return {
        'timestamps': timestamps,
        'gene_lengths': np.array(gene_lengths),
        'gc_contents': np.array(gc_contents),
        'codon_biases': np.array(codon_biases),
        'gene_info': genes
    }


def analyze_signal(analyzer, signal_data, signal_name, signal_description):
    """Analyze one biological signal through all four lenses."""
    
    print(f"\n🔍 Analyzing {signal_name}: {signal_description}")
    print("=" * 70)
    
    signal = signal_data
    timestamps = np.arange(len(signal))
    
    # Validate signal
    validation = analyzer.validate_signal(signal)
    if not validation['all_passed']:
        print(f"   ❌ Signal validation failed for {signal_name}")
        for check, passed in validation.items():
            if check == 'all_passed':
                continue
            if not passed:
                print(f"      ✗ {check.replace('_', ' ').title()}")
        return None
    
    print(f"   ✓ Signal validated ({len(signal)} genes)")
    print(f"   Range: {signal.min():.1f} - {signal.max():.1f}")
    print(f"   Mean: {signal.mean():.1f} ± {signal.std():.1f}")
    
    results = {}
    
    # LENS 1: Fourier Analysis
    print(f"\n🔍 LENS 1: Fourier Analysis")
    print("-" * 40)
    try:
        fourier_result = analyzer.fourier_lens(signal, timestamps)
        if fourier_result and hasattr(fourier_result, 'dominant_period'):
            print(f"   Dominant period: {fourier_result.dominant_period:.1f} genes")
            print(f"   Dominant frequency: {fourier_result.dominant_frequency:.4f} Hz")
            if fourier_result.significance:
                print(f"   Significance: {fourier_result.significance:.3f}")
            print(f"   ✅ Detected periodic pattern in {signal_name}")
            results['fourier'] = fourier_result
        else:
            print(f"   No significant periodic patterns found")
    except Exception as e:
        print(f"   ❌ Fourier analysis failed: {e}")
    
    # LENS 2: Wavelet Analysis
    print(f"\n🔍 LENS 2: Wavelet Analysis")
    print("-" * 40)
    try:
        wavelet_result = analyzer.wavelet_lens(signal)
        if wavelet_result and hasattr(wavelet_result, 'transient_events'):
            events = wavelet_result.transient_events
            print(f"   Transient events detected: {len(events)}")
            if events:
                print(f"   ✅ Found {len(events)} significant transitions in {signal_name}")
                # Show first few events
                for i, event in enumerate(events[:3]):
                    if isinstance(event, dict) and 'time' in event:
                        print(f"      Event {i+1}: Gene {event['time']:.0f}")
                    else:
                        print(f"      Event {i+1}: {event}")
            else:
                print(f"   No significant transient events detected")
            results['wavelet'] = wavelet_result
        else:
            print(f"   No transient events detected")
    except Exception as e:
        print(f"   ❌ Wavelet analysis failed: {e}")
    
    # LENS 3: Laplace Analysis
    print(f"\n🔍 LENS 3: Laplace Analysis (System Stability)")
    print("-" * 40)
    try:
        laplace_result = analyzer.laplace_lens(signal)
        if laplace_result and hasattr(laplace_result, 'stability'):
            stability = laplace_result.stability
            print(f"   System stability: {stability.upper()}")
            if hasattr(laplace_result, 'damping_ratio'):
                print(f"   Damping ratio: {laplace_result.damping_ratio:.3f}")
            if hasattr(laplace_result, 'natural_frequency'):
                print(f"   Natural frequency: {laplace_result.natural_frequency:.4f} Hz")
            print(f"   ✅ {signal_name} system is {stability}")
            results['laplace'] = laplace_result
        else:
            print(f"   Unable to determine system stability")
    except Exception as e:
        print(f"   ❌ Laplace analysis failed: {e}")
    
    # LENS 4: Z-Transform Analysis
    print(f"\n🔍 LENS 4: Z-Transform (Digital Filtering)")
    print("-" * 40)
    try:
        ztransform_result = analyzer.z_transform_lens(signal)
        if ztransform_result and hasattr(ztransform_result, 'noise_reduction_percent'):
            noise_reduction = ztransform_result.noise_reduction_percent
            print(f"   Noise reduction: {noise_reduction:.1f}%")
            if hasattr(ztransform_result, 'filtered_signal'):
                print(f"   Filtered signal length: {len(ztransform_result.filtered_signal)}")
            print(f"   ✅ Successfully filtered {signal_name} signal")
            results['ztransform'] = ztransform_result
        else:
            print(f"   Unable to apply Z-transform filtering")
    except Exception as e:
        print(f"   ❌ Z-Transform analysis failed: {e}")
    
    return results


def main():
    print("=" * 70)
    print("BioXen Four-Lens Analysis System - Genomic MVP Demo")
    print("=" * 70)
    print("\nThis demo analyzes REAL genomic data from Syn3A minimal cell")
    print("through all four mathematical lenses.")
    
    # Load genomic data
    print("\n📊 Loading Syn3A genome data...")
    genome_file = Path(__file__).parent.parent / 'genomes' / 'syn3A.fasta'
    
    if not genome_file.exists():
        print(f"❌ Genome file not found: {genome_file}")
        print("Please ensure syn3A.fasta is in the genomes/ directory")
        return 1
    
    genes = parse_fasta(genome_file)
    print(f"   ✓ Loaded {len(genes)} genes from Syn3A genome")
    
    # Extract biological signals
    print("\n🔬 Extracting biological signals...")
    signals = extract_biological_signals(genes)
    
    print("   ✓ Gene lengths (structural complexity)")
    print("   ✓ GC content (thermodynamic stability)")  
    print("   ✓ Codon bias (translation efficiency)")
    
    # Initialize analyzer
    print("\n🔬 Initializing SystemAnalyzer...")
    # Use sampling rate of 1 gene per unit time
    analyzer = SystemAnalyzer(sampling_rate=1.0)
    print("   ✓ Analyzer ready for genomic data")
    
    # Analyze each signal
    all_results = {}
    
    # Signal 1: Gene Lengths
    results1 = analyze_signal(
        analyzer, 
        signals['gene_lengths'],
        "Gene Lengths",
        "Structural complexity across genome"
    )
    if results1:
        all_results['gene_lengths'] = results1
    
    # Signal 2: GC Content
    results2 = analyze_signal(
        analyzer,
        signals['gc_contents'], 
        "GC Content",
        "Thermodynamic stability patterns"
    )
    if results2:
        all_results['gc_contents'] = results2
    
    # Signal 3: Codon Bias
    results3 = analyze_signal(
        analyzer,
        signals['codon_biases'],
        "Codon Bias", 
        "Translation efficiency indicators"
    )
    if results3:
        all_results['codon_biases'] = results3
    
    # Final summary
    print("\n" + "=" * 70)
    print("GENOMIC ANALYSIS SUMMARY")
    print("=" * 70)
    print(f"Genome: Syn3A minimal cell")
    print(f"Genes analyzed: {len(genes)}")
    print(f"Signals processed: {len(all_results)}")
    print()
    
    # Show interesting findings
    print("🔍 Key Findings:")
    
    if 'gene_lengths' in all_results:
        gene_lengths = signals['gene_lengths']
        print(f"• Gene Length Range: {gene_lengths.min()}-{gene_lengths.max()} bp")
        print(f"• Average Gene Length: {gene_lengths.mean():.0f} bp")
    
    if 'gc_contents' in all_results:
        gc_contents = signals['gc_contents']
        print(f"• GC Content Range: {gc_contents.min():.1f}-{gc_contents.max():.1f}%")
        print(f"• Average GC Content: {gc_contents.mean():.1f}%")
    
    # Show some example genes
    print(f"\n📋 Sample Genes:")
    for i, gene in enumerate(genes[:5]):
        print(f"   {i+1}. {gene['id']}: {gene['length']} bp, GC={calculate_gc_content(gene['sequence']):.1f}%")
    
    print(f"\n✅ Genomic MVP Demo Complete!")
    print("=" * 70)
    
    return 0


if __name__ == "__main__":
    exit(main())