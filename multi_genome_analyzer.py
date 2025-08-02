#!/usr/bin/env python3
"""
BioXen Multi-Genome Compatibility Analyzer

Phase 2 of the BioXen-JCVI integration roadmap.
Implements advanced multi-genome analysis and compatibility assessment
for biological virtualization optimization.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
import statistics

# Import our integration components
from bioxen_jcvi_integration import BioXenJCVIIntegration

@dataclass
class GenomeProfile:
    """Comprehensive genome profile for compatibility analysis"""
    name: str
    file_path: str
    total_genes: int
    total_bases: int
    average_gene_length: float
    min_gene_length: int
    max_gene_length: int
    gc_content: float
    coding_density: float
    essential_genes: int
    protein_genes: int
    rna_genes: int
    complexity_score: float
    vm_suitability: str  # "excellent", "good", "fair", "poor"

@dataclass
class CompatibilityResult:
    """Results of genome-to-genome compatibility analysis"""
    genome1: str
    genome2: str
    similarity_score: float
    resource_compatibility: str
    shared_functions: List[str]
    unique_features: Dict[str, List[str]]
    vm_colocation_recommendation: str
    optimization_suggestions: List[str]

class MultiGenomeAnalyzer:
    """Advanced multi-genome compatibility and optimization analyzer"""
    
    def __init__(self):
        self.integration = BioXenJCVIIntegration()
        self.genome_profiles: Dict[str, GenomeProfile] = {}
        self.compatibility_matrix: Dict[Tuple[str, str], CompatibilityResult] = {}
    
    def analyze_genome_collection(self, genome_dir: str = "genomes") -> Dict[str, Any]:
        """
        Analyze all genomes in a directory for comprehensive compatibility assessment
        """
        print("🧬 Multi-Genome Compatibility Analysis - Phase 2")
        print("=" * 55)
        
        # Find all genome files
        genome_files = self._find_genome_files(genome_dir)
        
        if not genome_files:
            print("❌ No genome files found for analysis")
            return {}
        
        print(f"🔍 Found {len(genome_files)} genomes for analysis")
        
        # Phase 2A: Individual genome profiling
        print(f"\n📊 Phase 2A: Individual Genome Profiling")
        for genome_file in genome_files:
            profile = self._create_genome_profile(genome_file)
            if profile:
                self.genome_profiles[profile.name] = profile
                print(f"   ✅ {profile.name}: {profile.vm_suitability.upper()} VM suitability")
        
        # Phase 2B: Pairwise compatibility analysis
        print(f"\n🔗 Phase 2B: Pairwise Compatibility Analysis")
        genome_names = list(self.genome_profiles.keys())
        
        for i, genome1 in enumerate(genome_names):
            for genome2 in genome_names[i+1:]:
                compatibility = self._analyze_compatibility(genome1, genome2)
                self.compatibility_matrix[(genome1, genome2)] = compatibility
                print(f"   🔄 {genome1} ↔ {genome2}: {compatibility.similarity_score:.1f}% similar")
        
        # Phase 2C: Resource optimization recommendations
        print(f"\n⚡ Phase 2C: Resource Optimization Analysis")
        optimization_plan = self._generate_optimization_plan()
        
        # Phase 2D: VM allocation strategies
        print(f"\n🖥️  Phase 2D: VM Allocation Strategy")
        allocation_strategy = self._generate_allocation_strategy()
        
        # Compile comprehensive report
        analysis_results = {
            'genome_profiles': {name: asdict(profile) for name, profile in self.genome_profiles.items()},
            'compatibility_matrix': {f"{k[0]}_vs_{k[1]}": asdict(v) for k, v in self.compatibility_matrix.items()},
            'optimization_plan': optimization_plan,
            'allocation_strategy': allocation_strategy,
            'analysis_metadata': {
                'total_genomes': len(self.genome_profiles),
                'compatibility_pairs': len(self.compatibility_matrix),
                'jcvi_enhanced': self.integration.is_jcvi_available(),
                'analysis_version': '2.0'
            }
        }
        
        return analysis_results
    
    def _find_genome_files(self, genome_dir: str) -> List[str]:
        """Find all available genome files"""
        genome_files = []
        
        if not os.path.exists(genome_dir):
            return genome_files
        
        # Look for .genome and .fasta files
        for ext in ['*.genome', '*.fasta']:
            genome_files.extend(Path(genome_dir).glob(ext))
        
        return [str(f) for f in genome_files]
    
    def _create_genome_profile(self, genome_file: str) -> Optional[GenomeProfile]:
        """Create comprehensive genome profile"""
        try:
            # Get enhanced statistics
            stats = self.integration.get_genome_statistics(genome_file)
            
            if not stats or 'total_sequences' not in stats:
                return None
            
            # Calculate additional metrics
            gc_content = self._estimate_gc_content(genome_file)
            essential_genes = self._estimate_essential_genes(stats['total_sequences'])
            coding_density = self._calculate_coding_density(stats)
            complexity_score = self._calculate_complexity_score(stats, gc_content, coding_density)
            vm_suitability = self._assess_vm_suitability(complexity_score, stats['total_sequences'])
            
            # Estimate gene types (simplified for now)
            protein_genes = int(stats['total_sequences'] * 0.85)  # ~85% protein coding
            rna_genes = stats['total_sequences'] - protein_genes
            
            return GenomeProfile(
                name=Path(genome_file).stem,
                file_path=genome_file,
                total_genes=stats['total_sequences'],
                total_bases=stats['total_bases'],
                average_gene_length=stats.get('average_length', 0),
                min_gene_length=stats.get('min_length', 0),
                max_gene_length=stats.get('max_length', 0),
                gc_content=gc_content,
                coding_density=coding_density,
                essential_genes=essential_genes,
                protein_genes=protein_genes,
                rna_genes=rna_genes,
                complexity_score=complexity_score,
                vm_suitability=vm_suitability
            )
            
        except Exception as e:
            print(f"⚠️  Error profiling {genome_file}: {e}")
            return None
    
    def _estimate_gc_content(self, genome_file: str) -> float:
        """Estimate GC content (simplified calculation)"""
        # For synthetic sequences, estimate based on genome type
        if 'syn3a' in genome_file.lower():
            return 31.8  # Known GC content for JCVI-Syn3A
        elif 'mycoplasma' in genome_file.lower():
            return 32.0  # Typical for Mycoplasma
        else:
            return 35.0  # Default estimate
    
    def _estimate_essential_genes(self, total_genes: int) -> int:
        """Estimate number of essential genes"""
        # Based on research: minimal genomes have ~30-50% essential genes
        return int(total_genes * 0.4)
    
    def _calculate_coding_density(self, stats: Dict[str, Any]) -> float:
        """Calculate coding density"""
        if stats['total_bases'] == 0:
            return 0.0
        
        # Estimate coding regions (assume average 85% coding in minimal genomes)
        estimated_coding_bases = stats['total_bases'] * 0.85
        return estimated_coding_bases / stats['total_bases']
    
    def _calculate_complexity_score(self, stats: Dict[str, Any], gc_content: float, coding_density: float) -> float:
        """Calculate genome complexity score (0-100)"""
        # Normalized complexity based on multiple factors
        gene_density = stats['total_sequences'] / max(stats['total_bases'] / 1000, 1)  # genes per kb
        length_variance = stats.get('max_length', 1000) - stats.get('min_length', 100)
        
        # Complexity factors (normalized to 0-1)
        complexity_factors = [
            min(gene_density / 2.0, 1.0),  # Gene density factor
            min(length_variance / 2000, 1.0),  # Length variance factor
            abs(gc_content - 50) / 50,  # GC deviation from 50%
            coding_density  # Coding density
        ]
        
        return sum(complexity_factors) * 25  # Scale to 0-100
    
    def _assess_vm_suitability(self, complexity_score: float, gene_count: int) -> str:
        """Assess VM suitability based on complexity and size"""
        if complexity_score < 30 and gene_count < 300:
            return "excellent"
        elif complexity_score < 50 and gene_count < 600:
            return "good"
        elif complexity_score < 70 and gene_count < 1000:
            return "fair"
        else:
            return "poor"
    
    def _analyze_compatibility(self, genome1: str, genome2: str) -> CompatibilityResult:
        """Analyze compatibility between two genomes"""
        profile1 = self.genome_profiles[genome1]
        profile2 = self.genome_profiles[genome2]
        
        # Calculate similarity metrics
        size_similarity = self._calculate_size_similarity(profile1, profile2)
        complexity_similarity = self._calculate_complexity_similarity(profile1, profile2)
        gc_similarity = self._calculate_gc_similarity(profile1, profile2)
        
        # Overall similarity score
        similarity_score = (size_similarity + complexity_similarity + gc_similarity) / 3
        
        # Resource compatibility assessment
        resource_compatibility = self._assess_resource_compatibility(profile1, profile2)
        
        # Generate recommendations
        vm_colocation = self._assess_vm_colocation(similarity_score, profile1, profile2)
        optimization_suggestions = self._generate_optimization_suggestions(profile1, profile2, similarity_score)
        
        # Shared functions (simplified - could be enhanced with JCVI ortholog analysis)
        shared_functions = self._estimate_shared_functions(profile1, profile2)
        
        # Unique features
        unique_features = {
            genome1: [f"High complexity: {profile1.complexity_score:.1f}"] if profile1.complexity_score > profile2.complexity_score + 10 else [],
            genome2: [f"High complexity: {profile2.complexity_score:.1f}"] if profile2.complexity_score > profile1.complexity_score + 10 else []
        }
        
        return CompatibilityResult(
            genome1=genome1,
            genome2=genome2,
            similarity_score=similarity_score,
            resource_compatibility=resource_compatibility,
            shared_functions=shared_functions,
            unique_features=unique_features,
            vm_colocation_recommendation=vm_colocation,
            optimization_suggestions=optimization_suggestions
        )
    
    def _calculate_size_similarity(self, profile1: GenomeProfile, profile2: GenomeProfile) -> float:
        """Calculate size-based similarity"""
        ratio = min(profile1.total_bases, profile2.total_bases) / max(profile1.total_bases, profile2.total_bases)
        return ratio * 100
    
    def _calculate_complexity_similarity(self, profile1: GenomeProfile, profile2: GenomeProfile) -> float:
        """Calculate complexity-based similarity"""
        diff = abs(profile1.complexity_score - profile2.complexity_score)
        return max(0, 100 - diff)
    
    def _calculate_gc_similarity(self, profile1: GenomeProfile, profile2: GenomeProfile) -> float:
        """Calculate GC content similarity"""
        diff = abs(profile1.gc_content - profile2.gc_content)
        return max(0, 100 - (diff * 2))  # Scale GC difference
    
    def _assess_resource_compatibility(self, profile1: GenomeProfile, profile2: GenomeProfile) -> str:
        """Assess resource sharing compatibility"""
        total_resources = profile1.total_genes + profile2.total_genes
        
        if total_resources < 400:
            return "excellent"
        elif total_resources < 800:
            return "good"
        elif total_resources < 1200:
            return "moderate"
        else:
            return "challenging"
    
    def _assess_vm_colocation(self, similarity: float, profile1: GenomeProfile, profile2: GenomeProfile) -> str:
        """Assess VM co-location recommendation"""
        if similarity > 80 and profile1.vm_suitability in ["excellent", "good"] and profile2.vm_suitability in ["excellent", "good"]:
            return "highly_recommended"
        elif similarity > 60:
            return "recommended"
        elif similarity > 40:
            return "possible_with_optimization"
        else:
            return "not_recommended"
    
    def _generate_optimization_suggestions(self, profile1: GenomeProfile, profile2: GenomeProfile, similarity: float) -> List[str]:
        """Generate optimization suggestions"""
        suggestions = []
        
        if similarity < 50:
            suggestions.append("Consider separate VM allocation due to low compatibility")
        
        if profile1.complexity_score > 70 or profile2.complexity_score > 70:
            suggestions.append("High complexity genomes may require dedicated resources")
        
        if profile1.total_genes + profile2.total_genes > 600:
            suggestions.append("Resource contention likely - implement priority scheduling")
        
        if abs(profile1.gc_content - profile2.gc_content) > 10:
            suggestions.append("Different GC contents may indicate distinct metabolic requirements")
        
        return suggestions if suggestions else ["Standard VM allocation suitable"]
    
    def _estimate_shared_functions(self, profile1: GenomeProfile, profile2: GenomeProfile) -> List[str]:
        """Estimate shared biological functions"""
        # Simplified - could be enhanced with actual ortholog analysis
        base_functions = ["DNA replication", "Protein synthesis", "Energy metabolism"]
        
        if profile1.essential_genes > 50 and profile2.essential_genes > 50:
            base_functions.extend(["Cell division", "RNA processing"])
        
        return base_functions
    
    def _generate_optimization_plan(self) -> Dict[str, Any]:
        """Generate overall resource optimization plan"""
        if not self.genome_profiles:
            return {}
        
        # Analyze genome distribution
        excellent_genomes = [name for name, profile in self.genome_profiles.items() if profile.vm_suitability == "excellent"]
        good_genomes = [name for name, profile in self.genome_profiles.items() if profile.vm_suitability == "good"]
        challenging_genomes = [name for name, profile in self.genome_profiles.items() if profile.vm_suitability in ["fair", "poor"]]
        
        # Calculate resource requirements
        total_genes = sum(profile.total_genes for profile in self.genome_profiles.values())
        average_complexity = statistics.mean(profile.complexity_score for profile in self.genome_profiles.values())
        
        return {
            'genome_distribution': {
                'excellent_vm_candidates': excellent_genomes,
                'good_vm_candidates': good_genomes,
                'challenging_vm_candidates': challenging_genomes
            },
            'resource_estimates': {
                'total_genes_to_virtualize': total_genes,
                'average_complexity': round(average_complexity, 1),
                'estimated_vm_count': len(excellent_genomes) + len(good_genomes),
                'recommended_ribosome_allocation': total_genes * 2  # Rough estimate
            },
            'optimization_strategies': [
                "Group similar complexity genomes in same VM cluster",
                "Allocate dedicated resources for high-complexity genomes",
                "Implement dynamic resource scaling based on genome activity",
                "Use compatibility matrix for optimal VM scheduling"
            ]
        }
    
    def _generate_allocation_strategy(self) -> Dict[str, Any]:
        """Generate VM allocation strategy"""
        if not self.genome_profiles:
            return {}
        
        # Create allocation clusters based on compatibility
        clusters = self._create_compatibility_clusters()
        
        return {
            'allocation_clusters': clusters,
            'scheduling_strategy': 'compatibility_based',
            'load_balancing': 'complexity_weighted',
            'scaling_policy': 'adaptive_per_cluster'
        }
    
    def _create_compatibility_clusters(self) -> List[Dict[str, Any]]:
        """Create genome clusters based on compatibility"""
        clusters = []
        genome_names = list(self.genome_profiles.keys())
        assigned = set()
        
        for genome in genome_names:
            if genome in assigned:
                continue
            
            # Start new cluster
            cluster = {
                'cluster_id': len(clusters) + 1,
                'primary_genome': genome,
                'compatible_genomes': [genome],
                'total_complexity': self.genome_profiles[genome].complexity_score,
                'resource_requirements': self.genome_profiles[genome].total_genes
            }
            
            assigned.add(genome)
            
            # Find compatible genomes
            for other_genome in genome_names:
                if other_genome in assigned:
                    continue
                
                # Check compatibility
                pair_key = (min(genome, other_genome), max(genome, other_genome))
                if pair_key in self.compatibility_matrix:
                    compatibility = self.compatibility_matrix[pair_key]
                    if compatibility.similarity_score > 60:  # Compatibility threshold
                        cluster['compatible_genomes'].append(other_genome)
                        cluster['total_complexity'] += self.genome_profiles[other_genome].complexity_score
                        cluster['resource_requirements'] += self.genome_profiles[other_genome].total_genes
                        assigned.add(other_genome)
            
            clusters.append(cluster)
        
        return clusters

def main():
    """Main analysis function"""
    analyzer = MultiGenomeAnalyzer()
    
    # Run comprehensive analysis
    results = analyzer.analyze_genome_collection()
    
    if not results:
        print("❌ Analysis failed - no genomes found")
        return 1
    
    # Save detailed results
    output_file = "multi_genome_analysis_phase2.json"
    try:
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n💾 Detailed analysis saved to: {output_file}")
    except Exception as e:
        print(f"⚠️  Warning: Could not save results: {e}")
    
    # Print summary
    print(f"\n🎉 Phase 2 Multi-Genome Analysis Complete!")
    print(f"   📊 {results['analysis_metadata']['total_genomes']} genomes analyzed")
    print(f"   🔗 {results['analysis_metadata']['compatibility_pairs']} compatibility pairs assessed")
    print(f"   ⚡ {len(results['allocation_strategy']['allocation_clusters'])} allocation clusters created")
    print(f"   🧬 JCVI enhancement: {'✅ Active' if results['analysis_metadata']['jcvi_enhanced'] else '❌ Fallback mode'}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
