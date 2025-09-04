"""
JCVI Manager - Unified API access to JCVI functionality

This module provides a clean API wrapper around the existing JCVI integration
infrastructure, making JCVI capabilities accessible through the factory pattern
while maintaining graceful fallback mechanisms.
"""

import sys
import os
from typing import Dict, Any, Optional, List
from pathlib import Path

# Add root directory to path for imports
root_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_dir))

try:
    from bioxen_jcvi_integration import BioXenJCVIIntegration
    from phase4_jcvi_cli_integration import JCVICLIIntegrator
    from bioxen_to_jcvi_converter import BioXenToJCVIConverter
except ImportError as e:
    print(f"Warning: Could not import JCVI integration modules: {e}")
    BioXenJCVIIntegration = None
    JCVICLIIntegrator = None
    BioXenToJCVIConverter = None


class JCVIManager:
    """
    Unified JCVI functionality manager for the API layer.
    
    This class wraps the existing JCVI integration infrastructure to provide
    clean API access while maintaining all existing capabilities including
    graceful fallback, format conversion, and hardware optimization.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize JCVI Manager with configuration.
        
        Args:
            config: Configuration dictionary with JCVI settings
        """
        self.config = config
        self._integration = None
        self._cli_integrator = None
        self._converter = None
        self._available = False
        
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize JCVI integration components if available."""
        try:
            # Initialize core integration
            if BioXenJCVIIntegration:
                self._integration = BioXenJCVIIntegration()
                self._available = self._integration.jcvi_available
            
            # Initialize CLI integrator if enabled and available
            if (JCVICLIIntegrator and 
                self.config.get('jcvi_cli_enabled', True) and 
                self._available):
                try:
                    self._cli_integrator = JCVICLIIntegrator()
                except Exception as e:
                    print(f"Warning: CLI integrator initialization failed: {e}")
                    self._cli_integrator = None
            
            # Initialize converter if available
            if BioXenToJCVIConverter:
                self._converter = BioXenToJCVIConverter()
                
        except Exception as e:
            print(f"Warning: JCVI component initialization failed: {e}")
            self._available = False
    
    @property
    def available(self) -> bool:
        """Check if JCVI functionality is available."""
        return self._available and self._integration is not None
    
    @property
    def cli_available(self) -> bool:
        """Check if JCVI CLI integration is available."""
        return self.available and self._cli_integrator is not None
    
    @property
    def converter_available(self) -> bool:
        """Check if format converter is available."""
        return self._converter is not None
    
    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive JCVI integration status."""
        return {
            'jcvi_available': self.available,
            'cli_integration_available': self.cli_available,
            'converter_available': self.converter_available,
            'config': {
                'jcvi_cli_enabled': self.config.get('jcvi_cli_enabled', True),
                'hardware_optimization': self.config.get('hardware_optimization', False),
                'fallback_mode': self.config.get('fallback_mode', True)
            }
        }
    
    def get_genome_statistics(self, genome_path: str) -> Dict[str, Any]:
        """
        Get enhanced genome statistics using JCVI integration.
        
        Args:
            genome_path: Path to genome file
            
        Returns:
            Dictionary with genome statistics, enhanced if JCVI available
        """
        if not self.available:
            return {
                'error': 'JCVI integration not available',
                'fallback': 'Use basic genome analysis instead'
            }
        
        try:
            return self._integration.get_genome_statistics(genome_path)
        except Exception as e:
            return {
                'error': f'JCVI analysis failed: {str(e)}',
                'fallback': 'Basic analysis recommended'
            }
    
    def run_synteny_analysis(self, genome1: str, genome2: str, **kwargs) -> Dict[str, Any]:
        """
        Run synteny analysis using JCVI CLI tools.
        
        Args:
            genome1: Path to first genome file
            genome2: Path to second genome file
            **kwargs: Additional parameters for synteny analysis
            
        Returns:
            Dictionary with synteny analysis results
        """
        if not self.cli_available:
            return {
                'error': 'JCVI CLI integration not available',
                'available': self.available,
                'cli_enabled': self.config.get('jcvi_cli_enabled', True)
            }
        
        try:
            # Ensure genomes are in FASTA format
            fasta1 = self.ensure_fasta_format(genome1)
            fasta2 = self.ensure_fasta_format(genome2)
            
            if not fasta1 or not fasta2:
                return {
                    'error': 'Could not convert genomes to FASTA format',
                    'genome1_fasta': fasta1,
                    'genome2_fasta': fasta2
                }
            
            # Run synteny analysis
            return self._cli_integrator.run_synteny_analysis(fasta1, fasta2, **kwargs)
            
        except Exception as e:
            return {
                'error': f'Synteny analysis failed: {str(e)}',
                'fallback': 'Basic comparative analysis recommended'
            }
    
    def ensure_fasta_format(self, genome_path: str) -> Optional[str]:
        """
        Ensure genome file is in FASTA format for JCVI compatibility.
        
        Args:
            genome_path: Path to genome file (.genome or .fasta)
            
        Returns:
            Path to FASTA file, or None if conversion failed
        """
        if not self.available:
            return None
            
        try:
            return self._integration.ensure_fasta_format(genome_path)
        except Exception as e:
            print(f"Warning: FASTA format conversion failed: {e}")
            return None
    
    def convert_format(self, input_path: str, output_path: str) -> bool:
        """
        Convert between BioXen and JCVI formats.
        
        Args:
            input_path: Path to input file
            output_path: Path to output file
            
        Returns:
            True if conversion successful, False otherwise
        """
        if not self.converter_available:
            print("Warning: Format converter not available")
            return False
        
        try:
            return self._converter.convert_genome(input_path, output_path)
        except Exception as e:
            print(f"Warning: Format conversion failed: {e}")
            return False
    
    def run_comparative_genomics(self, genomes: List[str], **kwargs) -> Dict[str, Any]:
        """
        Run comprehensive comparative genomics analysis.
        
        Args:
            genomes: List of genome file paths
            **kwargs: Additional parameters for analysis
            
        Returns:
            Dictionary with comparative analysis results
        """
        if not self.cli_available:
            return {
                'error': 'JCVI CLI integration required for comparative genomics',
                'available_methods': ['basic_comparison'] if self.available else []
            }
        
        if len(genomes) < 2:
            return {'error': 'At least 2 genomes required for comparative analysis'}
        
        try:
            # Ensure all genomes are in FASTA format
            fasta_genomes = []
            for genome in genomes:
                fasta_path = self.ensure_fasta_format(genome)
                if fasta_path:
                    fasta_genomes.append(fasta_path)
                else:
                    return {
                        'error': f'Could not convert genome to FASTA: {genome}',
                        'converted': fasta_genomes
                    }
            
            # Run comprehensive analysis using CLI integrator
            if hasattr(self._cli_integrator, 'run_comparative_genomics'):
                return self._cli_integrator.run_comparative_genomics(fasta_genomes, **kwargs)
            else:
                # Fallback to pairwise synteny analysis
                results = {}
                for i in range(len(fasta_genomes)):
                    for j in range(i + 1, len(fasta_genomes)):
                        pair_key = f"{Path(fasta_genomes[i]).name}_vs_{Path(fasta_genomes[j]).name}"
                        results[pair_key] = self.run_synteny_analysis(
                            fasta_genomes[i], fasta_genomes[j], **kwargs
                        )
                return {
                    'method': 'pairwise_synteny',
                    'results': results,
                    'genome_count': len(fasta_genomes)
                }
        
        except Exception as e:
            return {
                'error': f'Comparative genomics analysis failed: {str(e)}',
                'genomes_processed': len(fasta_genomes) if 'fasta_genomes' in locals() else 0
            }
    
    def get_hardware_info(self) -> Dict[str, Any]:
        """Get hardware information and optimization status."""
        if not self.cli_available:
            return {'error': 'CLI integration not available'}
        
        try:
            if hasattr(self._cli_integrator, 'hardware_info'):
                return self._cli_integrator.hardware_info
            elif hasattr(self._cli_integrator, '_detect_hardware'):
                return self._cli_integrator._detect_hardware()
            else:
                return {'info': 'Hardware detection not available in CLI integrator'}
        except Exception as e:
            return {'error': f'Hardware detection failed: {str(e)}'}
    
    def cleanup(self):
        """Cleanup JCVI resources and temporary files."""
        try:
            if self._cli_integrator and hasattr(self._cli_integrator, 'cleanup'):
                self._cli_integrator.cleanup()
            
            if self._integration and hasattr(self._integration, 'cleanup'):
                self._integration.cleanup()
                
        except Exception as e:
            print(f"Warning: JCVI cleanup failed: {e}")


def create_jcvi_manager(config: Optional[Dict[str, Any]] = None) -> JCVIManager:
    """
    Factory function to create a JCVI Manager instance.
    
    Args:
        config: Optional configuration dictionary
        
    Returns:
        Configured JCVIManager instance
    """
    if config is None:
        config = {
            'jcvi_cli_enabled': True,
            'hardware_optimization': False,
            'fallback_mode': True
        }
    
    return JCVIManager(config)
