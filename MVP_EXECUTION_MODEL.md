# BioXen Fourier VM Library - MVP Execution Model

## Overview

This MVP (Minimum Viable Product) demonstrates the complete BioXen execution model using **real genomic data** from the Syn3A minimal cell (JCVI-syn3A).

## What It Does

The `execution_model_diagram.py` script implements a working biological VM that:

1. **Loads Real Genome Data** - Parses the `syn3A.fasta` file (187 genes, 117,873 base pairs)
2. **Validates Genome Structure** - Verifies all gene records and calculates metrics
3. **Configures Chassis** - Sets up a Syn3A minimal cell chassis
4. **Allocates Resources** - Distributes biological resources (ATP, ribosomes, tRNA, RNA polymerase)
5. **Processes Signals** - Analyzes genome through the 4-Lens framework:
   - **Fourier Lens**: Identifies periodic patterns (27 peaks found)
   - **Wavelet Lens**: Detects transient events (17 events detected)
   - **Laplace Lens**: Analyzes system stability
   - **Z-Transform Lens**: Applies discrete filtering
6. **Visualizes Execution** - Creates real-time visualization of all stages

## How to Run

```bash
# Activate virtual environment (if using one)
source venv/bin/activate

# Run the MVP
python3 execution_model_diagram.py
```

## Output

The script produces:

1. **Console Output**: Detailed execution log showing each stage
2. **Real-time Visualization**: Interactive display of the execution model
3. **PNG Export**: `bioxen_mvp_execution_YYYYMMDD_HHMMSS.png` with final state

## Execution Results (Last Run)

```
VM ID: syn3a_mvp_001
Status: RUNNING
Chassis: syn3a
Genes Loaded: 187
Total Bases: 117,873
Average GC Content: 40.2%

Resources Allocated:
- ATP: 21,137.3 units
- Ribosomes: 37
- tRNA: 1,870
- RNA Polymerase: 18

Signal Processing Results:
- FOURIER: 27 periodic peaks detected
- WAVELET: 17 transient events detected
- LAPLACE: System stability analyzed
- Z-TRANSFORM: Discrete filter applied (window=5)
```

## Architecture

### Core Components

1. **GenomeRecord** - Represents individual genes with sequence, length, GC content
2. **FastaParser** - Parses FASTA genome files
3. **BiologicalResources** - Manages ATP, ribosomes, tRNA, etc.
4. **SignalProcessor** - Implements 4-Lens signal processing framework
5. **BioXenVM** - Main virtual machine implementation
6. **ExecutionVisualizer** - Real-time visualization system

### Visualization Panels

The output shows 4 panels:

1. **Execution Flow** - Sequential stages with current state highlighted
2. **Resource Allocation** - Bar chart of allocated biological resources
3. **4-Lens Signal Processing** - Central hub with 4 analysis lenses
4. **Genome Metrics** - Statistics and sample gene information

## Why This Is an MVP

This implementation demonstrates the **core BioXen concepts**:

- ✅ Real genomic data processing (not mock data)
- ✅ Factory-based VM creation pattern
- ✅ Chassis-specific configuration
- ✅ Resource allocation modeling
- ✅ 4-Lens signal processing framework
- ✅ VM lifecycle management (CREATED → LOADING → ALLOCATING → PROCESSING → RUNNING)
- ✅ Real-time visualization
- ✅ Metrics collection and analysis

## Next Steps

To extend this MVP:

1. **Add More Chassis Types** - E. coli, Yeast, Orthogonal systems
2. **Implement Biological Processes** - Transcription, translation, metabolism
3. **Add VM Orchestration** - Multiple concurrent VMs
4. **Real Signal Analysis** - Use scipy.fft, pywt for actual transforms
5. **Persistent State** - Save/load VM state
6. **Interactive Control** - CLI for VM management

## Technical Details

### Dependencies

- matplotlib - Visualization
- numpy - Numerical operations
- pathlib - File handling
- datetime - Timestamps

### File Structure

```
execution_model_diagram.py (624 lines)
├── Part 1: Biological VM Components (Lines 1-300)
│   ├── GenomeRecord class
│   ├── FastaParser class
│   ├── ChassisType enum
│   ├── BiologicalResources class
│   ├── SignalProcessor class
│   └── BioXenVM class
├── Part 2: Visualization Components (Lines 300-500)
│   └── ExecutionVisualizer class
└── Part 3: Main Execution (Lines 500-624)
    ├── run_bioxen_mvp() function
    └── main() function
```

## Example Output

```
======================================================================
BioXen Fourier VM Library - MVP Execution Model
======================================================================
Timestamp: 2025-10-01 09:39:43
Genome File: /home/chris/BioXen_Fourier_lib/genomes/syn3A.fasta
======================================================================

[Stage 0] Creating BioXen VM...
[BioXenVM] Created VM 'syn3a_mvp_001' with chassis 'syn3a'

[Stage 1] Loading genome from FASTA file...
[FastaParser] Loading genome from: genomes/syn3A.fasta
[FastaParser] Loaded 187 genes
[BioXenVM] Genome metrics: {'gene_count': 187, 'total_bases': 117873...}

[Stage 2] Validating genome structure...
[Validation] ✓ All 187 genes validated
[Validation] ✓ Total genome size: 117,873 bp

[Stage 3] Configuring Syn3A chassis...
[Chassis] ✓ Minimal cell chassis configured
[Chassis] ✓ Prokaryotic memory model initialized

[Stage 4] Allocating biological resources...
[Resources] Allocated: ATP=21137.3, Ribosomes=37, tRNA=1870, RNA Pol=18

[Stage 5] Processing genome through 4-Lens framework...
[SignalProcessor] Processing genome through 4-Lens framework...
  [Fourier] Found 27 periodic peaks
  [Wavelet] Detected 17 transient events
  [Laplace] System stability: unstable
  [Z-Transform] Applied discrete filter (window=5)

[Stage 6] Starting VM execution...
[BioXenVM] VM 'syn3a_mvp_001' is now RUNNING
[Execution] ✓ VM is now running biological processes

✓ MVP Execution Complete!
```

## License

Same as parent project (BioXen_Fourier_lib)

## Author

Generated for the BioXen Fourier VM Library project
Date: October 1, 2025
