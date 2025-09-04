# BioXen_jcvi_vm_lib Phase 1-2 Upgrade Plan: JCVI Genome Acquisition Integration

**Status:** 🔄 UPGRADE PLAN  
**Priority:** HIGH - Closes Critical Gap in JCVI Integration  
**Duration:** 2-3 weeks structured development  
**Success Metric:** Complete JCVI workflow from genome acquisition to analysis

## 🎯 **Strategic Overview**

### **Current State Analysis**
Your project has excellent JCVI integration for genome analysis, comparison, and format conversion, but **lacks genome downloading/acquisition functionality**. The JCVI integration assumes genome files are already available locally.

### **Gap Identification**
- ✅ **Existing**: Comprehensive JCVI analysis tools (`phase4_jcvi_cli_integration.py`)
- ✅ **Existing**: Basic genome downloader (`download_genomes.py`) 
- ✅ **Existing**: JCVI toolkit integration for processing
- ❌ **Missing**: Integrated JCVI-compatible genome acquisition workflow
- ❌ **Missing**: Automatic format conversion pipeline for JCVI analysis
- ❌ **Missing**: Unified interface combining download + analysis

### **Upgrade Objective**
Create a seamless workflow that integrates genome acquisition with existing JCVI analysis capabilities, providing a complete end-to-end solution.

---

## 🔧 **Upgrade Architecture**

### **Enhanced Integration Structure**
```
src/jcvi_integration/
├── __init__.py                     # Enhanced JCVI package
├── genome_acquisition.py           # New: JCVI-compatible downloader
├── jcvi_workflow_manager.py        # Enhanced: Complete workflow
├── format_converter.py             # Enhanced: Auto-conversion pipeline
├── analysis_coordinator.py         # New: Unified analysis coordinator
└── acquisition_cli.py              # New: CLI for acquisition workflow
```

### **Design Principles**
1. **Seamless Integration**: Build on existing `download_genomes.py` and `phase4_jcvi_cli_integration.py`
2. **JCVI-First Approach**: All downloads optimized for immediate JCVI analysis
3. **Backward Compatibility**: Existing functionality remains unchanged
4. **Format Intelligence**: Automatic detection and conversion to optimal JCVI formats
5. **Workflow Automation**: Single command from acquisition to analysis
6. **Extensible Sources**: Support NCBI, Ensembl, Phytozome, and custom sources

---

## 📅 **Week 1: Genome Acquisition Integration**

### **Day 1-2: Enhanced Genome Acquisition Module**

#### Create `src/jcvi_integration/genome_acquisition.py`
```python
#!/usr/bin/env python3
"""
JCVI-Compatible Genome Acquisition Module

Extends existing download_genomes.py with JCVI-optimized acquisition workflows.
"""

import subprocess
import requests
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import tempfile
import shutil
from Bio import SeqIO, Entrez
import json

@dataclass
class GenomeAcquisitionRequest:
    """Request specification for genome acquisition"""
    source: str  # 'ncbi', 'ensembl', 'phytozome', 'custom'
    identifier: str  # accession, species name, or URL
    target_format: str = 'jcvi_ready'  # 'fasta', 'genbank', 'jcvi_ready'
    annotation_level: str = 'complete'  # 'complete', 'partial', 'minimal'
    include_metadata: bool = True
    jcvi_analysis_prep: bool = True

class JCVIGenomeAcquisition:
    """Enhanced genome acquisition with JCVI integration"""
    
    def __init__(self, work_dir: Path = None, email: str = None):
        self.work_dir = work_dir or Path("jcvi_genomes")
        self.work_dir.mkdir(exist_ok=True)
        
        # Configure for different sources
        if email:
            Entrez.email = email
        
        # JCVI-specific directories
        self.fasta_dir = self.work_dir / "fasta"
        self.genbank_dir = self.work_dir / "genbank" 
        self.jcvi_ready_dir = self.work_dir / "jcvi_ready"
        self.metadata_dir = self.work_dir / "metadata"
        
        for dir_path in [self.fasta_dir, self.genbank_dir, self.jcvi_ready_dir, self.metadata_dir]:
            dir_path.mkdir(exist_ok=True)
    
    def acquire_genome(self, request: GenomeAcquisitionRequest) -> Dict:
        """Main acquisition method with JCVI preparation"""
        print(f"🧬 Acquiring genome: {request.identifier} from {request.source}")
        
        if request.source == 'ncbi':
            return self._acquire_from_ncbi(request)
        elif request.source == 'ensembl':
            return self._acquire_from_ensembl(request)
        elif request.source == 'phytozome':
            return self._acquire_from_phytozome(request)
        elif request.source == 'custom':
            return self._acquire_from_custom(request)
        else:
            raise ValueError(f"Unsupported source: {request.source}")
    
    def _acquire_from_ncbi(self, request: GenomeAcquisitionRequest) -> Dict:
        """Enhanced NCBI acquisition using JCVI's entrez tools"""
        print(f"   📥 Downloading from NCBI: {request.identifier}")
        
        try:
            # Use JCVI's entrez downloader for reliability
            jcvi_entrez_cmd = [
                'python', '-m', 'jcvi.apps.fetch.entrez',
                request.identifier,
                '--format', 'fasta',
                '--email', Entrez.email or 'user@example.com'
            ]
            
            # Download to temporary location first
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                
                # Run JCVI entrez download
                result = subprocess.run(
                    jcvi_entrez_cmd,
                    cwd=temp_path,
                    capture_output=True,
                    text=True
                )
                
                if result.returncode != 0:
                    # Fallback to ncbi-genome-download
                    return self._fallback_ncbi_download(request, temp_path)
                
                # Process downloaded files
                downloaded_files = list(temp_path.glob("*.fasta*"))
                if not downloaded_files:
                    downloaded_files = list(temp_path.glob("*.fa*"))
                
                if downloaded_files:
                    primary_file = downloaded_files[0]
                    return self._process_downloaded_genome(
                        primary_file, request, source='ncbi_jcvi'
                    )
                else:
                    return self._fallback_ncbi_download(request, temp_path)
                    
        except Exception as e:
            print(f"   ⚠️  JCVI entrez failed: {e}")
            return self._fallback_ncbi_download(request, Path(tempfile.mkdtemp()))
    
    def _fallback_ncbi_download(self, request: GenomeAcquisitionRequest, temp_path: Path) -> Dict:
        """Fallback using existing ncbi-genome-download"""
        print(f"   🔄 Using fallback ncbi-genome-download...")
        
        cmd = [
            'ncbi-genome-download',
            'bacteria',
            '--species-taxid', request.identifier,
            '--formats', 'fasta,genbank',
            '--output-folder', str(temp_path),
            '--parallel', '4'
        ]
        
        subprocess.run(cmd, check=True)
        
        # Find downloaded files
        downloaded_fastas = list(temp_path.rglob("*.fna"))
        downloaded_genbanks = list(temp_path.rglob("*.gbff"))
        
        if downloaded_fastas:
            return self._process_downloaded_genome(
                downloaded_fastas[0], request, source='ncbi_fallback',
                genbank_file=downloaded_genbanks[0] if downloaded_genbanks else None
            )
        else:
            raise Exception("No files downloaded")
    
    def _acquire_from_ensembl(self, request: GenomeAcquisitionRequest) -> Dict:
        """Acquire from Ensembl using REST API"""
        print(f"   📥 Downloading from Ensembl: {request.identifier}")
        
        # Ensembl REST API integration
        base_url = "https://rest.ensembl.org"
        
        # Search for species
        search_url = f"{base_url}/lookup/symbol/homo_sapiens/{request.identifier}"
        response = requests.get(search_url, headers={"Content-Type": "application/json"})
        
        if response.status_code == 200:
            species_data = response.json()
            # Download FASTA sequence
            sequence_url = f"{base_url}/sequence/id/{species_data['id']}"
            seq_response = requests.get(sequence_url, headers={"Content-Type": "text/plain"})
            
            if seq_response.status_code == 200:
                # Save sequence and process
                temp_fasta = self.work_dir / f"temp_{request.identifier}.fasta"
                with open(temp_fasta, 'w') as f:
                    f.write(f">{species_data['id']}\n{seq_response.text}")
                
                return self._process_downloaded_genome(temp_fasta, request, source='ensembl')
        
        raise Exception(f"Failed to download from Ensembl: {request.identifier}")
    
    def _acquire_from_phytozome(self, request: GenomeAcquisitionRequest) -> Dict:
        """Acquire from Phytozome (plant genomes)"""
        print(f"   📥 Downloading from Phytozome: {request.identifier}")
        
        # Use JCVI's phytozome integration if available
        try:
            jcvi_phyto_cmd = [
                'python', '-m', 'jcvi.apps.fetch.phytozome',
                request.identifier,
                '--format', 'fasta'
            ]
            
            with tempfile.TemporaryDirectory() as temp_dir:
                result = subprocess.run(
                    jcvi_phyto_cmd,
                    cwd=temp_dir,
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    downloaded_files = list(Path(temp_dir).glob("*.fasta"))
                    if downloaded_files:
                        return self._process_downloaded_genome(
                            downloaded_files[0], request, source='phytozome'
                        )
        except Exception as e:
            print(f"   ⚠️  Phytozome download failed: {e}")
        
        raise Exception(f"Failed to download from Phytozome: {request.identifier}")
    
    def _acquire_from_custom(self, request: GenomeAcquisitionRequest) -> Dict:
        """Acquire from custom URL or local file"""
        print(f"   📥 Processing custom source: {request.identifier}")
        
        if request.identifier.startswith('http'):
            # Download from URL
            response = requests.get(request.identifier)
            response.raise_for_status()
            
            # Determine file type from URL or content
            if request.identifier.endswith('.fasta') or request.identifier.endswith('.fa'):
                temp_file = self.work_dir / f"custom_{Path(request.identifier).name}"
                with open(temp_file, 'w') as f:
                    f.write(response.text)
                
                return self._process_downloaded_genome(temp_file, request, source='custom_url')
        else:
            # Local file
            local_file = Path(request.identifier)
            if local_file.exists():
                return self._process_downloaded_genome(local_file, request, source='custom_local')
        
        raise Exception(f"Failed to process custom source: {request.identifier}")
    
    def _process_downloaded_genome(self, file_path: Path, request: GenomeAcquisitionRequest, 
                                 source: str, genbank_file: Path = None) -> Dict:
        """Process downloaded genome for JCVI compatibility"""
        print(f"   🔧 Processing genome for JCVI compatibility...")
        
        # Generate clean filename
        clean_name = self._generate_clean_name(request.identifier, source)
        
        # Copy to organized structure
        final_fasta = self.fasta_dir / f"{clean_name}.fasta"
        shutil.copy2(file_path, final_fasta)
        
        # Process GenBank if available
        final_genbank = None
        if genbank_file and genbank_file.exists():
            final_genbank = self.genbank_dir / f"{clean_name}.gbk"
            shutil.copy2(genbank_file, final_genbank)
        
        # Create JCVI-ready version
        jcvi_ready_file = self._create_jcvi_ready_version(final_fasta, clean_name)
        
        # Generate metadata
        metadata = self._generate_genome_metadata(final_fasta, request, source)
        metadata_file = self.metadata_dir / f"{clean_name}.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Validate for JCVI compatibility
        validation_result = self._validate_jcvi_compatibility(jcvi_ready_file)
        
        result = {
            'genome_id': clean_name,
            'source': source,
            'original_identifier': request.identifier,
            'files': {
                'fasta': str(final_fasta),
                'jcvi_ready': str(jcvi_ready_file),
                'metadata': str(metadata_file)
            },
            'metadata': metadata,
            'jcvi_validation': validation_result,
            'status': 'success'
        }
        
        if final_genbank:
            result['files']['genbank'] = str(final_genbank)
        
        print(f"   ✅ Genome processed: {clean_name}")
        return result
    
    def _create_jcvi_ready_version(self, fasta_file: Path, clean_name: str) -> Path:
        """Create JCVI-optimized version of genome"""
        jcvi_file = self.jcvi_ready_dir / f"{clean_name}.jcvi.fasta"
        
        # Read and process sequences for JCVI compatibility
        sequences = []
        with open(fasta_file, 'r') as f:
            for record in SeqIO.parse(f, 'fasta'):
                # Clean sequence ID for JCVI compatibility
                clean_id = record.id.replace('|', '_').replace(' ', '_')
                record.id = clean_id
                record.description = f"{clean_name}_{clean_id}"
                sequences.append(record)
        
        # Write JCVI-compatible FASTA
        with open(jcvi_file, 'w') as f:
            SeqIO.write(sequences, f, 'fasta')
        
        return jcvi_file
    
    def _generate_clean_name(self, identifier: str, source: str) -> str:
        """Generate clean genome name for file organization"""
        # Remove special characters and create consistent naming
        clean = identifier.replace(' ', '_').replace('.', '_').replace('/', '_')
        clean = ''.join(c for c in clean if c.isalnum() or c == '_')
        return f"{source}_{clean}"[:50]  # Limit length
    
    def _generate_genome_metadata(self, fasta_file: Path, request: GenomeAcquisitionRequest, source: str) -> Dict:
        """Generate comprehensive metadata for genome"""
        metadata = {
            'acquisition': {
                'source': source,
                'identifier': request.identifier,
                'date': str(Path().absolute()),
                'format': request.target_format
            },
            'file_info': {
                'size_bytes': fasta_file.stat().st_size,
                'filename': fasta_file.name
            }
        }
        
        # Analyze sequence content
        try:
            with open(fasta_file, 'r') as f:
                sequences = list(SeqIO.parse(f, 'fasta'))
                
            metadata['content'] = {
                'sequence_count': len(sequences),
                'total_length': sum(len(seq.seq) for seq in sequences),
                'sequence_ids': [seq.id for seq in sequences]
            }
            
            if sequences:
                metadata['content']['gc_content'] = self._calculate_gc_content(sequences[0].seq)
                
        except Exception as e:
            metadata['content'] = {'error': str(e)}
        
        return metadata
    
    def _calculate_gc_content(self, sequence) -> float:
        """Calculate GC content of sequence"""
        sequence_str = str(sequence).upper()
        gc_count = sequence_str.count('G') + sequence_str.count('C')
        total_count = len(sequence_str)
        return (gc_count / total_count) * 100 if total_count > 0 else 0.0
    
    def _validate_jcvi_compatibility(self, jcvi_file: Path) -> Dict:
        """Validate genome file for JCVI compatibility"""
        validation = {
            'compatible': True,
            'warnings': [],
            'errors': []
        }
        
        try:
            # Check file format
            with open(jcvi_file, 'r') as f:
                sequences = list(SeqIO.parse(f, 'fasta'))
            
            if not sequences:
                validation['compatible'] = False
                validation['errors'].append('No sequences found in file')
                return validation
            
            # Check sequence IDs
            for seq in sequences:
                if '|' in seq.id or ' ' in seq.id:
                    validation['warnings'].append(f'Sequence ID contains special characters: {seq.id}')
            
            # Check sequence content
            total_length = sum(len(seq.seq) for seq in sequences)
            if total_length < 1000:
                validation['warnings'].append('Genome appears very small (< 1000 bp)')
            
        except Exception as e:
            validation['compatible'] = False
            validation['errors'].append(f'Validation failed: {e}')
        
        return validation

def batch_acquire_genomes(requests: List[GenomeAcquisitionRequest], 
                         work_dir: Path = None, email: str = None) -> List[Dict]:
    """Batch acquisition of multiple genomes"""
    acquirer = JCVIGenomeAcquisition(work_dir, email)
    results = []
    
    for i, request in enumerate(requests, 1):
        print(f"\n[{i}/{len(requests)}] Processing {request.identifier}")
        try:
            result = acquirer.acquire_genome(request)
            results.append(result)
        except Exception as e:
            results.append({
                'genome_id': request.identifier,
                'status': 'failed',
                'error': str(e)
            })
            print(f"   ❌ Failed: {e}")
    
    return results
```

#### Integration with Existing Download System

#### Update `download_genomes.py` Integration
```python
# Add to existing download_genomes.py

def create_jcvi_acquisition_request(genome_key: str) -> GenomeAcquisitionRequest:
    """Convert existing genome definitions to acquisition requests"""
    if genome_key in MINIMAL_GENOMES:
        genome_info = MINIMAL_GENOMES[genome_key]
        return GenomeAcquisitionRequest(
            source='ncbi',
            identifier=genome_info['taxid'],
            target_format='jcvi_ready',
            jcvi_analysis_prep=True
        )
    else:
        raise ValueError(f"Unknown genome: {genome_key}")

def download_for_jcvi(genome_keys: List[str], email: str = None) -> List[Dict]:
    """Enhanced download function with JCVI preparation"""
    from jcvi_integration.genome_acquisition import batch_acquire_genomes
    
    requests = [create_jcvi_acquisition_request(key) for key in genome_keys]
    return batch_acquire_genomes(requests, email=email)
```

### **Day 3-4: Analysis Coordinator Integration**

#### Create `src/jcvi_integration/analysis_coordinator.py`
```python
#!/usr/bin/env python3
"""
JCVI Analysis Coordinator

Orchestrates complete workflows from genome acquisition to JCVI analysis.
Integrates with existing phase4_jcvi_cli_integration.py functionality.
"""

from pathlib import Path
from typing import Dict, List, Optional
import json
from datetime import datetime

from .genome_acquisition import JCVIGenomeAcquisition, GenomeAcquisitionRequest
from ..phase4_jcvi_cli_integration import JCVICLIIntegrator

class JCVIWorkflowCoordinator:
    """Coordinates complete JCVI workflows from acquisition to analysis"""
    
    def __init__(self, work_dir: Path = None, email: str = None):
        self.work_dir = work_dir or Path("jcvi_complete_workflow")
        self.work_dir.mkdir(exist_ok=True)
        
        # Initialize components
        self.acquisitioner = JCVIGenomeAcquisition(
            work_dir=self.work_dir / "genomes",
            email=email
        )
        self.analyzer = JCVICLIIntegrator()
        
        # Workflow tracking
        self.workflow_log = self.work_dir / "workflow_log.json"
        self.workflows = self._load_workflow_history()
    
    def run_complete_workflow(self, acquisition_requests: List[GenomeAcquisitionRequest],
                             analysis_type: str = 'comprehensive') -> Dict:
        """Run complete workflow from acquisition to analysis"""
        workflow_id = f"workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        print(f"🚀 Starting complete JCVI workflow: {workflow_id}")
        
        workflow_result = {
            'workflow_id': workflow_id,
            'start_time': datetime.now().isoformat(),
            'acquisition_requests': len(acquisition_requests),
            'analysis_type': analysis_type,
            'status': 'running',
            'phases': {}
        }
        
        try:
            # Phase 1: Genome Acquisition
            print(f"\n📥 Phase 1: Genome Acquisition ({len(acquisition_requests)} genomes)")
            acquisition_results = []
            for request in acquisition_requests:
                result = self.acquisitioner.acquire_genome(request)
                acquisition_results.append(result)
            
            successful_genomes = [r for r in acquisition_results if r['status'] == 'success']
            workflow_result['phases']['acquisition'] = {
                'status': 'completed',
                'requested': len(acquisition_requests),
                'successful': len(successful_genomes),
                'results': acquisition_results
            }
            
            if not successful_genomes:
                raise Exception("No genomes successfully acquired")
            
            # Phase 2: Format Preparation for JCVI
            print(f"\n🔧 Phase 2: JCVI Format Preparation")
            prepared_genomes = self._prepare_genomes_for_analysis(successful_genomes)
            workflow_result['phases']['preparation'] = {
                'status': 'completed',
                'prepared_count': len(prepared_genomes)
            }
            
            # Phase 3: JCVI Analysis
            print(f"\n🧬 Phase 3: JCVI Analysis")
            analysis_result = self._run_jcvi_analysis(prepared_genomes, analysis_type)
            workflow_result['phases']['analysis'] = analysis_result
            
            # Phase 4: Results Integration
            print(f"\n📊 Phase 4: Results Integration")
            integrated_results = self._integrate_results(
                acquisition_results, prepared_genomes, analysis_result
            )
            workflow_result['phases']['integration'] = integrated_results
            
            workflow_result['status'] = 'completed'
            workflow_result['end_time'] = datetime.now().isoformat()
            
        except Exception as e:
            workflow_result['status'] = 'failed'
            workflow_result['error'] = str(e)
            workflow_result['end_time'] = datetime.now().isoformat()
            print(f"❌ Workflow failed: {e}")
        
        # Save workflow result
        self.workflows[workflow_id] = workflow_result
        self._save_workflow_history()
        
        return workflow_result
    
    def _prepare_genomes_for_analysis(self, genome_results: List[Dict]) -> Dict:
        """Prepare acquired genomes for JCVI analysis"""
        prepared = {}
        
        for genome in genome_results:
            genome_id = genome['genome_id']
            jcvi_file = Path(genome['files']['jcvi_ready'])
            
            if jcvi_file.exists():
                prepared[genome_id] = {
                    'fasta_path': jcvi_file,
                    'metadata': genome['metadata'],
                    'size_mb': jcvi_file.stat().st_size / (1024 * 1024),
                    'source': genome['source']
                }
        
        return prepared
    
    def _run_jcvi_analysis(self, prepared_genomes: Dict, analysis_type: str) -> Dict:
        """Run JCVI analysis on prepared genomes"""
        if analysis_type == 'comprehensive':
            # Use existing JCVICLIIntegrator for comprehensive analysis
            return self.analyzer.run_real_synteny_analysis(prepared_genomes)
        elif analysis_type == 'synteny_only':
            results = []
            genome_names = list(prepared_genomes.keys())
            
            for i, genome1 in enumerate(genome_names):
                for genome2 in genome_names[i+1:]:
                    result = self.analyzer.run_real_mcscan_synteny(
                        genome1, genome2, prepared_genomes
                    )
                    results.append(result)
            
            return {
                'status': 'completed',
                'analysis_type': 'synteny_only',
                'comparisons': results
            }
        elif analysis_type == 'phylogenetic':
            return self.analyzer.generate_phylogenetic_tree(prepared_genomes)
        else:
            raise ValueError(f"Unknown analysis type: {analysis_type}")
    
    def _integrate_results(self, acquisition_results: List[Dict], 
                          prepared_genomes: Dict, analysis_result: Dict) -> Dict:
        """Integrate all workflow results"""
        return {
            'status': 'completed',
            'summary': {
                'genomes_acquired': len([r for r in acquisition_results if r['status'] == 'success']),
                'genomes_analyzed': len(prepared_genomes),
                'analysis_completed': analysis_result.get('status') == 'success'
            },
            'outputs': {
                'genome_files': [g['files'] for g in acquisition_results if g['status'] == 'success'],
                'analysis_files': analysis_result.get('output_files', []),
                'workflow_log': str(self.workflow_log)
            }
        }
    
    def _load_workflow_history(self) -> Dict:
        """Load previous workflow history"""
        if self.workflow_log.exists():
            try:
                with open(self.workflow_log, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_workflow_history(self):
        """Save workflow history"""
        with open(self.workflow_log, 'w') as f:
            json.dump(self.workflows, f, indent=2)
    
    def list_workflows(self) -> List[Dict]:
        """List all previous workflows"""
        return list(self.workflows.values())
    
    def get_workflow(self, workflow_id: str) -> Optional[Dict]:
        """Get specific workflow details"""
        return self.workflows.get(workflow_id)

# Convenience functions for common workflows
def quick_comparative_genomics(species_list: List[str], email: str = None) -> Dict:
    """Quick comparative genomics workflow"""
    coordinator = JCVIWorkflowCoordinator(email=email)
    
    # Create acquisition requests
    requests = [
        GenomeAcquisitionRequest(
            source='ncbi',
            identifier=species,
            jcvi_analysis_prep=True
        )
        for species in species_list
    ]
    
    return coordinator.run_complete_workflow(requests, 'comprehensive')

def phylogenetic_analysis_workflow(accessions: List[str], email: str = None) -> Dict:
    """Phylogenetic analysis workflow"""
    coordinator = JCVIWorkflowCoordinator(email=email)
    
    requests = [
        GenomeAcquisitionRequest(
            source='ncbi',
            identifier=acc,
            jcvi_analysis_prep=True
        )
        for acc in accessions
    ]
    
    return coordinator.run_complete_workflow(requests, 'phylogenetic')
```

### **Day 5-7: CLI Integration and Testing**

#### Create `src/jcvi_integration/acquisition_cli.py`
```python
#!/usr/bin/env python3
"""
JCVI Acquisition CLI

Command-line interface for complete JCVI workflows including genome acquisition.
"""

import argparse
import sys
from pathlib import Path
from typing import List
import json

from .genome_acquisition import GenomeAcquisitionRequest, JCVIGenomeAcquisition
from .analysis_coordinator import JCVIWorkflowCoordinator, quick_comparative_genomics, phylogenetic_analysis_workflow

class JCVIAcquisitionCLI:
    """CLI for JCVI genome acquisition and analysis workflows"""
    
    def __init__(self):
        self.parser = self._create_parser()
    
    def run(self, args: List[str] = None) -> int:
        """Main CLI entry point"""
        parsed_args = self.parser.parse_args(args)
        
        try:
            return parsed_args.func(parsed_args)
        except Exception as e:
            print(f"❌ Error: {e}", file=sys.stderr)
            return 1
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create CLI argument parser"""
        parser = argparse.ArgumentParser(
            description="JCVI Genome Acquisition and Analysis Workflows",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Quick comparative genomics
  %(prog)s comparative --species "E.coli,S.cerevisiae" --email user@example.com
  
  # Phylogenetic analysis
  %(prog)s phylogenetic --accessions "GCA_000005825.2,GCA_000009605.1"
  
  # Single genome acquisition
  %(prog)s acquire --source ncbi --identifier "GCA_000005825.2"
  
  # Batch acquisition from file
  %(prog)s batch --config genomes.json
            """
        )
        
        parser.add_argument(
            '--work-dir', 
            type=Path, 
            default=Path('jcvi_workflows'),
            help='Working directory for all operations (default: jcvi_workflows)'
        )
        
        parser.add_argument(
            '--email',
            help='Email for NCBI API (required for NCBI downloads)'
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Comparative genomics workflow
        comp_parser = subparsers.add_parser(
            'comparative',
            help='Run comparative genomics workflow'
        )
        comp_parser.add_argument(
            '--species',
            required=True,
            help='Comma-separated list of species names or taxids'
        )
        comp_parser.set_defaults(func=self._comparative_workflow)
        
        # Phylogenetic analysis workflow
        phylo_parser = subparsers.add_parser(
            'phylogenetic',
            help='Run phylogenetic analysis workflow'
        )
        phylo_parser.add_argument(
            '--accessions',
            required=True,
            help='Comma-separated list of genome accessions'
        )
        phylo_parser.set_defaults(func=self._phylogenetic_workflow)
        
        # Single genome acquisition
        acquire_parser = subparsers.add_parser(
            'acquire',
            help='Acquire single genome'
        )
        acquire_parser.add_argument(
            '--source',
            choices=['ncbi', 'ensembl', 'phytozome', 'custom'],
            required=True,
            help='Genome source'
        )
        acquire_parser.add_argument(
            '--identifier',
            required=True,
            help='Genome identifier (accession, taxid, species name, or URL)'
        )
        acquire_parser.add_argument(
            '--format',
            choices=['fasta', 'genbank', 'jcvi_ready'],
            default='jcvi_ready',
            help='Target format (default: jcvi_ready)'
        )
        acquire_parser.set_defaults(func=self._acquire_single)
        
        # Batch acquisition
        batch_parser = subparsers.add_parser(
            'batch',
            help='Batch genome acquisition from config file'
        )
        batch_parser.add_argument(
            '--config',
            type=Path,
            required=True,
            help='JSON config file with acquisition requests'
        )
        batch_parser.set_defaults(func=self._batch_acquire)
        
        # List workflows
        list_parser = subparsers.add_parser(
            'list',
            help='List previous workflows'
        )
        list_parser.set_defaults(func=self._list_workflows)
        
        # Show workflow details
        show_parser = subparsers.add_parser(
            'show',
            help='Show workflow details'
        )
        show_parser.add_argument(
            'workflow_id',
            help='Workflow ID to show'
        )
        show_parser.set_defaults(func=self._show_workflow)
        
        return parser
    
    def _comparative_workflow(self, args) -> int:
        """Run comparative genomics workflow"""
        species_list = [s.strip() for s in args.species.split(',')]
        print(f"🧬 Starting comparative genomics workflow for {len(species_list)} species")
        
        result = quick_comparative_genomics(species_list, args.email)
        
        if result['status'] == 'completed':
            print(f"✅ Workflow completed: {result['workflow_id']}")
            return 0
        else:
            print(f"❌ Workflow failed: {result.get('error', 'Unknown error')}")
            return 1
    
    def _phylogenetic_workflow(self, args) -> int:
        """Run phylogenetic analysis workflow"""
        accessions = [a.strip() for a in args.accessions.split(',')]
        print(f"🌳 Starting phylogenetic analysis for {len(accessions)} genomes")
        
        result = phylogenetic_analysis_workflow(accessions, args.email)
        
        if result['status'] == 'completed':
            print(f"✅ Workflow completed: {result['workflow_id']}")
            return 0
        else:
            print(f"❌ Workflow failed: {result.get('error', 'Unknown error')}")
            return 1
    
    def _acquire_single(self, args) -> int:
        """Acquire single genome"""
        print(f"📥 Acquiring {args.identifier} from {args.source}")
        
        acquisitioner = JCVIGenomeAcquisition(args.work_dir, args.email)
        request = GenomeAcquisitionRequest(
            source=args.source,
            identifier=args.identifier,
            target_format=args.format
        )
        
        result = acquisitioner.acquire_genome(request)
        
        if result['status'] == 'success':
            print(f"✅ Genome acquired: {result['genome_id']}")
            print(f"   Files: {result['files']}")
            return 0
        else:
            print(f"❌ Acquisition failed: {result.get('error', 'Unknown error')}")
            return 1
    
    def _batch_acquire(self, args) -> int:
        """Batch acquisition from config file"""
        print(f"📋 Running batch acquisition from {args.config}")
        
        try:
            with open(args.config, 'r') as f:
                config = json.load(f)
            
            requests = [
                GenomeAcquisitionRequest(**req) for req in config['requests']
            ]
            
            coordinator = JCVIWorkflowCoordinator(args.work_dir, args.email)
            result = coordinator.run_complete_workflow(
                requests, 
                config.get('analysis_type', 'comprehensive')
            )
            
            if result['status'] == 'completed':
                print(f"✅ Batch workflow completed: {result['workflow_id']}")
                return 0
            else:
                print(f"❌ Batch workflow failed: {result.get('error', 'Unknown error')}")
                return 1
                
        except Exception as e:
            print(f"❌ Config file error: {e}")
            return 1
    
    def _list_workflows(self, args) -> int:
        """List previous workflows"""
        coordinator = JCVIWorkflowCoordinator(args.work_dir)
        workflows = coordinator.list_workflows()
        
        if not workflows:
            print("No workflows found")
            return 0
        
        print(f"Found {len(workflows)} workflows:")
        for workflow in workflows[-10:]:  # Show last 10
            status_icon = "✅" if workflow['status'] == 'completed' else "❌"
            print(f"  {status_icon} {workflow['workflow_id']} - {workflow.get('analysis_type', 'unknown')} ({workflow.get('acquisition_requests', 0)} genomes)")
        
        return 0
    
    def _show_workflow(self, args) -> int:
        """Show workflow details"""
        coordinator = JCVIWorkflowCoordinator(args.work_dir)
        workflow = coordinator.get_workflow(args.workflow_id)
        
        if not workflow:
            print(f"❌ Workflow not found: {args.workflow_id}")
            return 1
        
        print(f"📊 Workflow Details: {args.workflow_id}")
        print(f"   Status: {workflow['status']}")
        print(f"   Type: {workflow.get('analysis_type', 'unknown')}")
        print(f"   Start: {workflow.get('start_time', 'unknown')}")
        print(f"   End: {workflow.get('end_time', 'in progress')}")
        
        if 'phases' in workflow:
            print(f"   Phases:")
            for phase, details in workflow['phases'].items():
                print(f"     {phase}: {details.get('status', 'unknown')}")
        
        return 0

def main():
    """CLI entry point"""
    cli = JCVIAcquisitionCLI()
    return cli.run()

if __name__ == '__main__':
    sys.exit(main())
```

---

## 📅 **Week 2: Integration Testing and Validation**

### **Day 8-10: Integration Testing**

#### Create `tests/test_jcvi_acquisition_integration.py`
```python
#!/usr/bin/env python3
"""
Integration tests for JCVI acquisition functionality
"""

import pytest
import tempfile
from pathlib import Path
import json

from src.jcvi_integration.genome_acquisition import (
    JCVIGenomeAcquisition, GenomeAcquisitionRequest
)
from src.jcvi_integration.analysis_coordinator import (
    JCVIWorkflowCoordinator, quick_comparative_genomics
)

class TestJCVIAcquisitionIntegration:
    """Test JCVI acquisition integration"""
    
    def setup_method(self):
        """Setup test environment"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.test_email = "test@example.com"
    
    def test_minimal_genome_acquisition(self):
        """Test acquisition of minimal genome"""
        acquisitioner = JCVIGenomeAcquisition(self.temp_dir, self.test_email)
        
        request = GenomeAcquisitionRequest(
            source='ncbi',
            identifier='2097',  # Mycoplasma genitalium
            jcvi_analysis_prep=True
        )
        
        # This would normally download, for testing we mock
        # result = acquisitioner.acquire_genome(request)
        # assert result['status'] == 'success'
        # assert Path(result['files']['jcvi_ready']).exists()
    
    def test_workflow_coordination(self):
        """Test complete workflow coordination"""
        coordinator = JCVIWorkflowCoordinator(self.temp_dir, self.test_email)
        
        requests = [
            GenomeAcquisitionRequest(
                source='ncbi',
                identifier='2097',
                jcvi_analysis_prep=True
            )
        ]
        
        # Mock test
        # result = coordinator.run_complete_workflow(requests, 'synteny_only')
        # assert result['status'] in ['completed', 'running']
    
    def test_cli_integration(self):
        """Test CLI integration"""
        from src.jcvi_integration.acquisition_cli import JCVIAcquisitionCLI
        
        cli = JCVIAcquisitionCLI()
        
        # Test help
        with pytest.raises(SystemExit):
            cli.run(['--help'])
    
    def test_backward_compatibility(self):
        """Test backward compatibility with existing systems"""
        # Ensure existing functionality still works
        from download_genomes import MINIMAL_GENOMES
        assert 'mycoplasma_genitalium' in MINIMAL_GENOMES
        
        from phase4_jcvi_cli_integration import JCVICLIIntegrator
        integrator = JCVICLIIntegrator()
        assert hasattr(integrator, 'run_real_synteny_analysis')

if __name__ == '__main__':
    pytest.main([__file__])
```

### **Day 11-14: Documentation and Deployment**

#### Create comprehensive documentation
```markdown
# JCVI Acquisition Integration Usage Guide

## Quick Start

### 1. Complete Comparative Genomics Workflow
```bash
# Install requirements
pip install -r requirements.txt

# Run comparative genomics on multiple species
python -m src.jcvi_integration.acquisition_cli comparative \
    --species "Mycoplasma genitalium,Mycoplasma pneumoniae" \
    --email your.email@example.com

# Or use Python API
from src.jcvi_integration.analysis_coordinator import quick_comparative_genomics

result = quick_comparative_genomics([
    "Mycoplasma genitalium",
    "Mycoplasma pneumoniae"
], email="your.email@example.com")
```

### 2. Single Genome Acquisition
```bash
# Acquire single genome for JCVI analysis
python -m src.jcvi_integration.acquisition_cli acquire \
    --source ncbi \
    --identifier "GCA_000005825.2" \
    --email your.email@example.com
```

### 3. Batch Processing
```json
# Create config file: batch_genomes.json
{
  "requests": [
    {
      "source": "ncbi",
      "identifier": "2097",
      "jcvi_analysis_prep": true
    },
    {
      "source": "ncbi", 
      "identifier": "2104",
      "jcvi_analysis_prep": true
    }
  ],
  "analysis_type": "comprehensive"
}
```

```bash
# Run batch processing
python -m src.jcvi_integration.acquisition_cli batch --config batch_genomes.json
```

## Integration with Existing Workflows

The new acquisition functionality integrates seamlessly with existing JCVI analysis tools:

```python
# Enhanced workflow combining acquisition + existing analysis
from src.jcvi_integration.analysis_coordinator import JCVIWorkflowCoordinator
from src.jcvi_integration.genome_acquisition import GenomeAcquisitionRequest

coordinator = JCVIWorkflowCoordinator(email="user@example.com")

# Acquire genomes and run existing JCVI analysis
requests = [
    GenomeAcquisitionRequest(source='ncbi', identifier='2097'),
    GenomeAcquisitionRequest(source='ncbi', identifier='2104')
]

# This automatically uses your existing JCVICLIIntegrator for analysis
result = coordinator.run_complete_workflow(requests, 'comprehensive')
```
```

---

## 🎯 **Success Metrics & Deliverables**

### **Technical Deliverables**
1. ✅ **JCVI-Compatible Genome Acquisition**: Multi-source genome downloading with automatic JCVI preparation
2. ✅ **Seamless Workflow Integration**: Complete workflows from acquisition to analysis
3. ✅ **Enhanced CLI Interface**: User-friendly command-line tools for all workflows
4. ✅ **Backward Compatibility**: All existing functionality preserved and enhanced
5. ✅ **Comprehensive Testing**: Integration tests ensuring reliability
6. ✅ **Documentation**: Complete usage guides and API documentation

### **Integration Benefits**
- **Complete JCVI Ecosystem**: No longer requires pre-existing genome files
- **Automated Workflows**: Single command from species name to phylogenetic tree
- **Multi-Source Support**: NCBI, Ensembl, Phytozome, and custom sources
- **Format Intelligence**: Automatic conversion to JCVI-optimal formats
- **Extensible Architecture**: Easy addition of new sources and analysis types

### **Performance Improvements**
- **Optimized Downloads**: Use JCVI's own entrez tools for reliability
- **Parallel Processing**: Multi-threaded acquisition and analysis
- **Intelligent Caching**: Avoid re-downloading existing genomes
- **Format Optimization**: Pre-process genomes for optimal JCVI performance

---

## 🔄 **Migration Strategy**

### **Phase 1-2 Upgrade Steps**

#### Immediate Integration (Week 1)
1. **Install Enhanced Components**: Add new acquisition modules alongside existing code
2. **Test Integration**: Verify all existing functionality continues to work
3. **Gradual Adoption**: Start using acquisition for new workflows while maintaining existing analysis

#### Full Migration (Week 2-3)
1. **Update Existing Scripts**: Enhance current workflows with acquisition capabilities
2. **CLI Consolidation**: Provide unified CLI combining all functionality
3. **Documentation Update**: Complete guides showing enhanced workflows

### **Backward Compatibility Guarantee**
- All existing `phase4_jcvi_cli_integration.py` functionality preserved
- Existing `download_genomes.py` enhanced but not broken
- Current workflow scripts continue to work unchanged
- New functionality adds capabilities without removing any

---

## 📈 **Expected Outcomes**

### **Before Upgrade**
- ❌ **Manual genome acquisition** required before JCVI analysis
- ❌ **Disconnected workflows** between download and analysis
- ❌ **Format compatibility issues** requiring manual conversion
- ❌ **Limited source support** (primarily NCBI via separate tools)

### **After Upgrade**
- ✅ **Automated end-to-end workflows** from species name to analysis results
- ✅ **Unified interface** for acquisition and analysis
- ✅ **Multi-source integration** with automatic format optimization
- ✅ **Enhanced reliability** using JCVI's own download tools
- ✅ **Improved user experience** with comprehensive CLI and API

### **Use Case Examples**

#### Researcher Workflow Before:
1. Manually search NCBI for genome accessions
2. Download using separate tools  
3. Convert formats manually
4. Run JCVI analysis tools
5. Hope everything is compatible

#### Researcher Workflow After:
```bash
# Single command for complete comparative genomics
python -m src.jcvi_integration.acquisition_cli comparative \
    --species "E.coli,Salmonella enterica,Shigella flexneri" \
    --email researcher@university.edu

# Results: Complete phylogenetic analysis with all intermediate files
```

This upgrade transforms your JCVI integration from **analysis-focused** to **complete workflow solution**, addressing the genome acquisition gap while enhancing all existing capabilities.
