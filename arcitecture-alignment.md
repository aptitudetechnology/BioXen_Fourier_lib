# Prompt for GitHub Copilot: BioXen Architecture Alignment

## Context
You're working on BioXen, a biological VM simulation library that uses a 4-lens frequency domain analysis system as its computational engine. The documentation is currently misaligned with implementation reality and planned architecture.

## Current State Assessment

**What EXISTS:**
- VM simulation engine (genome loading, chassis selection, resource allocation)
- Discrete biological process execution (transcription, translation)
- VM lifecycle management (create, start, stop, destroy)
- 4-lens conceptual framework (documented in research materials)

**What DOESN'T exist yet:**
- SystemAnalyzer class with working implementations of all 4 lenses
- Integration between VMs and the analysis system
- Continuous time-series generation from VM simulations
- Metabolic state tracking and history buffers in VMs
- PyCWT-mod server for hardware acceleration
- Client/server architecture for remote computation

**What's UNCLEAR:**
- Whether any lens implementations exist at all
- Whether VMs currently generate analyzable time-series data
- The actual relationship between simulation and analysis components

## The Vision

Biological VMs should simulate cellular processes that generate continuous time-series data (metabolic states, gene expression levels, etc.). The VM uses the 4-lens analysis system during simulation to:
- Detect circadian rhythm drift (Fourier lens)
- Identify stress response transients (Wavelet lens)
- Analyze homeostatic control stability (Laplace lens)
- Filter measurement noise (Z-Transform lens)

The analysis system isn't a separate tool - it's the VM's computational engine for self-regulation.

## Required Actions

### 1. Create Implementation Status Document
**File:** `docs/IMPLEMENTATION_STATUS.md`

Document what actually exists today:
```markdown
# BioXen Implementation Status

## Implemented Features
- [ ] VM Engine (genome → VM creation → process execution)
- [ ] SystemAnalyzer class
- [ ] Fourier Lens (Lomb-Scargle implementation)
- [ ] Wavelet Lens (CWT/DWT implementation)
- [ ] Laplace Lens (Transfer function implementation)
- [ ] Z-Transform Lens (Digital filter implementation)
- [ ] VM continuous simulation mode
- [ ] Metabolic state tracking in VMs
- [ ] VM-Analysis integration
- [ ] PyCWT-mod server
- [ ] Hardware acceleration support

## In Progress
[List current work]

## Planned
[List future work]
```

### 2. Update README.md

Align the README with reality:
- If SystemAnalyzer doesn't exist, remove examples showing its usage
- If VM-analysis integration doesn't exist, mark it as "planned feature"
- Clearly separate "Current Features" from "Planned Features"
- Explain the vision: VMs will use 4-lens system for self-regulation (future)
- Show what actually works today with real, runnable examples

**Structure:**
```markdown
# BioXen Fourier VM Library

## What It Does Today
[Only include working features with real examples]

## The Vision
[Explain planned VM + 4-lens integration]

## Roadmap
[Clear phases of development]
```

### 3. Update execution-model.md

Add a new section explaining how analysis integrates with VMs:

```markdown
## Analysis Integration (Planned)

VMs will generate continuous time-series data during simulation and use
the 4-lens analysis system for self-regulation:

### Continuous Simulation Mode
```python
vm = create_bio_vm('cell', 'ecoli', 'basic')
vm.start_continuous_simulation(duration_hours=48)

# VM tracks metabolic states over time
history = vm.get_metabolic_history()
# Returns: {'atp': [100, 98, 95, ...], 'glucose': [...], ...}
```

### Analysis-Driven Behavior
```python
# VM periodically analyzes its own state
analysis = vm.analyze_metabolic_state()
if analysis.circadian_drift_detected:
    vm.adjust_clock_genes()
```
```

### 4. Create Development Roadmap
**File:** `docs/DEVELOPMENT_ROADMAP.md`

```markdown
# BioXen Development Roadmap

## Phase 0: Foundation (Current)
- Complete implementation status audit
- Align all documentation with reality
- Identify gaps between vision and implementation

## Phase 1: Build Core Analysis System (Weeks 1-4)
- Implement SystemAnalyzer class if it doesn't exist
- Implement all 4 lenses with local computation only:
  - Fourier: astropy.timeseries.LombScargle
  - Wavelet: pywt (PyWavelets)
  - Laplace: python-control
  - Z-Transform: scipy.signal
- Create test suite for each lens
- Document API for each lens

## Phase 2: Integrate VMs with Analysis (Weeks 5-8)
- Add continuous simulation mode to VMs
- Add metabolic state tracking and history buffers
- Integrate SystemAnalyzer into VM lifecycle
- Define feedback loops (analysis → VM behavior)
- Test complete workflow: VM generates data → analyzes → adjusts

## Phase 3: Performance Validation (Weeks 9-10)
- Benchmark VM performance with analysis overhead
- Identify computational bottlenecks
- Determine if remote computation is needed
- Profile memory usage and latency

## Phase 4: Architecture Refactor (Weeks 11+)
ONLY proceed if Phase 3 shows need for optimization:
- Extract lenses into modular components
- Implement client library for future REST API
- Add dual-mode support (local/remote)
- Build unified server (if needed)
- Add hardware acceleration (if bottlenecks exist)
```

### 5. Update refactor-plan.md

Add a critical preface:

```markdown
# BioXen Library Refactor Plan

> **IMPORTANT:** This refactor plan assumes certain features exist and are
> integrated. Before proceeding with this refactor, complete Phase 1-3 of
> the Development Roadmap to build and integrate the core system.

## Prerequisites
- [ ] SystemAnalyzer implemented with all 4 lenses
- [ ] VMs generating continuous time-series data
- [ ] VM-Analysis integration working
- [ ] Performance profiling completed
- [ ] Bottlenecks identified

## When to Execute This Refactor
This plan should be executed ONLY if:
1. The integrated system works but has performance issues
2. Profiling shows computational bottlenecks
3. Remote computation would provide measurable benefits
4. Hardware acceleration is available and justified

[Rest of existing refactor plan...]
```

### 6. Create Missing Implementation Files

If SystemAnalyzer doesn't exist, create the skeleton:

**File:** `src/bioxen_fourier_vm_lib/analysis/system_analyzer.py`

```python
"""
Four-Lens Biological Signal Analysis System

Provides comprehensive frequency-domain analysis using four complementary
methods optimized for biological time-series data.
"""

from typing import Optional, Dict, Any
import numpy as np

class SystemAnalyzer:
    """
    Unified interface for multi-lens biological signal analysis.
    
    Each lens addresses a specific challenge in biological data:
    - Fourier: Irregular sampling, dominant frequencies
    - Wavelet: Non-stationary signals, transient detection
    - Laplace: System stability, feedback control
    - Z-Transform: Discrete filtering, noise reduction
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize analyzer with optional configuration."""
        self.config = config or {}
        # TODO: Initialize lens implementations
        
    def fourier_lens_analyze(self, signal, times=None, **kwargs):
        """
        Fourier analysis using Lomb-Scargle periodogram.
        
        Best for: Circadian rhythms, irregular sampling
        Library: astropy.timeseries.LombScargle
        """
        # TODO: Implement using astropy
        raise NotImplementedError("Fourier lens not yet implemented")
        
    def wavelet_lens_analyze(self, signal, dt, **kwargs):
        """
        Wavelet analysis using CWT/DWT.
        
        Best for: Non-stationary signals, transient detection
        Library: pywt (PyWavelets)
        """
        # TODO: Implement using pywt
        raise NotImplementedError("Wavelet lens not yet implemented")
        
    def laplace_lens_analyze(self, input_signal, output_signal, dt, **kwargs):
        """
        Laplace domain analysis using transfer functions.
        
        Best for: System stability, feedback control
        Library: python-control
        """
        # TODO: Implement using python-control
        raise NotImplementedError("Laplace lens not yet implemented")
        
    def ztransform_lens_analyze(self, signal, filter_design, **kwargs):
        """
        Z-transform analysis using digital filters.
        
        Best for: Discrete sampling, noise reduction
        Library: scipy.signal
        """
        # TODO: Implement using scipy.signal
        raise NotImplementedError("Z-Transform lens not yet implemented")
```

## Instructions for Copilot

1. **First, audit the codebase:**
   - Does `src/bioxen_fourier_vm_lib/analysis/system_analyzer.py` exist?
   - Are there any implementations of the 4 lenses?
   - Do VMs currently generate time-series data?
   - Is there any VM-analysis integration?

2. **Create the status document** based on your findings

3. **Update documentation** to match reality - remove aspirational features from current capabilities

4. **Flag inconsistencies** where documents contradict each other or the code

5. **Prioritize honesty** - it's better to show missing features clearly than to imply they exist

6. **Suggest next steps** based on what actually needs to be built

## Success Criteria

After these changes:
- README accurately represents current functionality
- Clear distinction between "works today" and "planned future"
- Development roadmap shows logical progression
- Refactor plan is gated behind prerequisite work
- No documentation claims features that don't exist
- Clear path forward for development