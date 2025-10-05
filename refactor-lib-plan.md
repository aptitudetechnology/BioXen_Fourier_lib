# 🔄 BioXen Library Refactor Plan
**Unifying the 4 Lenses Architecture with PyCWT-mod Server**

---

**Date Created:** 5 October 2025  
**Current Status:** Server running at wavelet.local:8000 (86.5% tests passing)  
**Goal:** Refactor library to use 4-Lens architecture with PyCWT-mod as the foundation  

---

## ⚠️ IMPORTANT: Prerequisites

> **DO NOT EXECUTE THIS REFACTOR PLAN YET!**
>
> This refactor assumes certain features exist and are integrated. Before proceeding,
> complete **Phase 1-4** of the Development Roadmap to build and validate the core system.

### Required Prerequisites

**Before starting this refactor, you MUST have:**

- [ ] **Phase 1 Complete:** Profiler with automatic real-time analysis
- [ ] **Phase 2 Complete:** VMs generating continuous time-series data
- [ ] **Phase 3 Complete:** VM-Analysis integration working (self-regulation)
- [ ] **Phase 4 Complete:** Performance validation showing need for optimization

**See:** `docs/DEVELOPMENT_ROADMAP.md` for implementation order  
**See:** `docs/IMPLEMENTATION_STATUS.md` for current state assessment

### When to Execute This Refactor

Execute this plan **ONLY IF:**

1. ✅ The integrated system works (VMs + Analysis + Profiler all functional)
2. ✅ Phase 4 performance profiling completed
3. ✅ Bottlenecks identified that justify remote computation
4. ✅ One or more of these conditions met:
   - Analysis overhead > 20% of VM execution time
   - Analysis latency > 500ms
   - Memory usage unsustainable for long simulations
   - Hardware acceleration available and justified

### Why Wait?

**Premature optimization risks:**
- Building infrastructure before validating need
- Architectural complexity without clear benefits
- Wasted effort if local computation is sufficient
- Harder to iterate on tightly coupled systems

**Build first, optimize later:**
- Get VMs working with integrated analysis (Phases 1-3)
- Measure actual performance (Phase 4)
- Refactor only if measurements show need (Phase 5)

---

## 🎯 Vision

Transform BioXen from a monolithic library into a **modular 4-Lens architecture** where each lens is:
1. **Self-contained** - Independent analysis capabilities
2. **REST API enabled** - Remote computation via PyCWT-mod server
3. **Hardware accelerated** - FPGA/GPU support through server backends
4. **Consistently designed** - Unified interface across all lenses

**Key Insight:** The PyCWT-mod REST API server at `wavelet.local:8000` provides the blueprint for how ALL lenses should work!

---

## 📊 Current State Assessment

### ✅ What We Have Now

**PyCWT-mod Server (Operational)**
- **Location:** `wavelet.local:8000`
- **API Spec:** `api-specification-document.md` (1169 lines, v1.0.0)
- **Test Suite:** `client-tests/` (90/104 tests passing - 86.5%)
- **Hardware Support:** Tang Nano 9K (FPGA), ELM11 (embedded), CPU (sequential/joblib)
- **Endpoints Working:**
  - ✅ Health & docs (100%)
  - ✅ Hardware detection (100%)
  - ✅ Benchmark system (100%)
  - ✅ Backend management (93.8%)
  - 🟡 Wavelet analysis (65.4% - CWT/WCT/XWT)
  - 🟡 Integration workflows (61.5%)

**BioXen Library (Current)**
- **Location:** `src/bioxen_fourier_vm_lib/`
- **Architecture:** Monolithic with SystemAnalyzer class
- **4 Lenses Implemented:**
  1. Fourier Lens (Lomb-Scargle)
  2. Wavelet Lens (CWT/DWT with auto-select, MRA)
  3. Laplace Lens (Transfer functions)
  4. Z-Transform Lens (Discrete filtering)
- **Status:** MVP complete, Phase 1.5 MRA complete
- **Issue:** All lenses tightly coupled in single class

---

## 🏗️ Refactor Architecture

### Server Architecture Options

**We have 3 viable approaches - let's choose the best one:**

#### Option 1: Unified Multi-Lens Server (RECOMMENDED ⭐)
**Single server handling all 4 lenses with shared infrastructure**

```
BioXen Unified Server (bioxen.local:8000)
├── /api/v1/wavelet/*    ← PyCWT-mod endpoints
├── /api/v1/fourier/*    ← SciPy FFT, Lomb-Scargle
├── /api/v1/laplace/*    ← Python-Control, SciPy signal
├── /api/v1/ztransform/* ← SciPy signal, custom filters
├── /api/v1/hardware/detect
├── /api/v1/backends/
└── /api/v1/benchmark/all

Backend Libraries (All Python-based):
├── PyWavelets (pywt)         ← Already integrated
├── SciPy (signal, fft)       ← Standard library
├── Astropy (timeseries)      ← Lomb-Scargle
├── Python-Control            ← Control systems
└── NumPy                     ← Foundation

Hardware Acceleration:
├── PyCWT-mod backends        ← Tang Nano 9K, ELM11 (working!)
├── CuPy (GPU)               ← GPU acceleration for FFT, matrix ops
├── FFTW                     ← Optimized CPU FFT
└── Custom FPGA cores        ← Extend current FPGA for all lenses
```

**Advantages:**
- ✅ **Single deployment** - One server to manage
- ✅ **Shared hardware** - Tang Nano 9K can accelerate ALL lenses
- ✅ **Code reuse** - Common infrastructure, logging, monitoring
- ✅ **Easier maintenance** - One codebase, one API spec
- ✅ **Lower latency** - No inter-service communication
- ✅ **Simpler architecture** - One client library talks to one server

#### Option 2: Specialized Lens Servers
**Separate servers for each lens (microservices approach)**

```
Wavelet Server (wavelet.local:8000)
├── PyCWT-mod (operational!)
└── Tang Nano 9K FPGA

Fourier Server (fourier.local:8001)
├── SciPy FFT, Astropy
└── GPU (cuFFT) or FFTW

Laplace Server (laplace.local:8002)
├── Python-Control
└── Symbolic math (SymPy)

Z-Transform Server (ztransform.local:8003)
├── SciPy signal
└── DSP-specific hardware
```

**Advantages:**
- ✅ **Specialized optimization** - Each server tuned for one task
- ✅ **Independent scaling** - Scale popular lenses separately
- ✅ **Fault isolation** - One server down doesn't affect others
- ✅ **Technology diversity** - Could use different languages/frameworks

**Disadvantages:**
- ❌ **Complex deployment** - 4 servers to manage
- ❌ **Hardware duplication** - Need FPGA/GPU for each server
- ❌ **Network overhead** - Cross-lens operations require inter-service calls
- ❌ **More maintenance** - 4 codebases, 4 API specs

#### Option 3: Hybrid Approach
**Unified server with optional specialized accelerators**

```
BioXen Main Server (bioxen.local:8000)
├── All 4 lenses (software)
└── Basic hardware acceleration

Optional Accelerator Services:
├── fpga-accel.local:9000    ← Dedicated FPGA for all lenses
├── gpu-accel.local:9001     ← GPU cluster for parallel processing
└── dsp-accel.local:9002     ← Real-time DSP hardware
```

### The 4-Lens Modular Design (Recommended: Option 1)

```
BioXen Library (Client-Side)
├── lenses/
│   ├── fourier_lens.py      ← Lens 1: Steady-state periodic
│   ├── wavelet_lens.py      ← Lens 2: Non-stationary, transients
│   ├── laplace_lens.py      ← Lens 3: System stability
│   └── ztransform_lens.py   ← Lens 4: Discrete-time filtering
├── clients/
│   └── bioxen_client.py     ← Single unified REST API client
├── backends/
│   ├── local_backend.py     ← Local computation (current default)
│   └── remote_backend.py    ← Remote server computation
└── system_analyzer.py       ← Unified interface (facade pattern)

BioXen Unified Server (Optional, Hardware-Accelerated)
└── bioxen.local:8000        ← All 4 lenses in one FastAPI server
    ├── /api/v1/wavelet/*
    ├── /api/v1/fourier/*
    ├── /api/v1/laplace/*
    └── /api/v1/ztransform/*
```

### Why Option 1 (Unified Server) is Best

**1. All Libraries are Python-Based**
```python
# No need for different languages/frameworks!
import pywt              # Wavelets
import scipy.signal      # FFT, filtering, Z-transform
import scipy.fft         # Fast Fourier Transform
from astropy.timeseries import LombScargle  # Irregular sampling
import control           # Laplace, control theory
import numpy as np       # Everything
```

**2. Shared Hardware Acceleration**
- Tang Nano 9K FPGA can be programmed for multiple operations
- GPU (CuPy) works for all matrix/FFT operations
- No need to duplicate expensive hardware

**3. Cross-Lens Optimization**
```python
# Example: Wavelet + Fourier hybrid analysis
@app.post("/api/v1/hybrid/wavelet-fourier")
def hybrid_analysis(signal):
    # Wavelet for transient detection
    transients = pycwt.detect_transients(signal)
    
    # Fourier for stable regions
    stable_regions = signal[~transients]
    spectrum = scipy.fft.fft(stable_regions)
    
    return {"transients": transients, "spectrum": spectrum}
```

**4. Simpler Deployment**
```bash
# One server to start
docker run -p 8000:8000 bioxen/unified-server

# vs 4 separate services
docker-compose up wavelet fourier laplace ztransform
```

### Key Design Principles

1. **Each Lens = Standalone Module**
   - Can run independently
   - Shares unified client for remote computation
   - Provides consistent API

2. **Dual-Mode Operation**
   - **Local Mode:** Computation on local machine (default)
   - **Remote Mode:** Offload to unified hardware-accelerated server

3. **Unified Interface**
   - `SystemAnalyzer` becomes a facade/orchestrator
   - Each lens accessible via: `analyzer.fourier_lens()`, `analyzer.wavelet_lens()`, etc.
   - Automatic backend selection (local vs remote)

4. **Server-First Design**
   - REST API defines the canonical interface
   - Client library wraps API for Pythonic usage
   - Server handles hardware acceleration transparently

5. **Single Server, Multiple Lenses**
   - One FastAPI server with multiple routers (one per lens)
   - Shared backend infrastructure (Tang Nano 9K, GPU, CPU)
   - All using Python scientific stack (no language barriers)

### Library Stack Consolidation

**All 4 Lenses Use Python Libraries:**

| Lens | Primary Libraries | Hardware Acceleration |
|------|------------------|---------------------|
| **Wavelet** | PyWavelets, SciPy | PyCWT-mod (FPGA), CuPy (GPU) |
| **Fourier** | SciPy FFT, Astropy | FFTW, cuFFT (GPU), FPGA |
| **Laplace** | Python-Control, SciPy | CuPy (matrix ops), SymPy |
| **Z-Transform** | SciPy signal, NumPy | FPGA (real-time), CuPy (batch) |

**Shared Infrastructure:**
```python
# Single FastAPI app with multiple routers
from fastapi import FastAPI
from .routers import wavelet, fourier, laplace, ztransform
from .backends import FPGABackend, GPUBackend, CPUBackend

app = FastAPI(title="BioXen Unified Analysis Server")

# Register all lens routers
app.include_router(wavelet.router, prefix="/api/v1/wavelet")
app.include_router(fourier.router, prefix="/api/v1/fourier")
app.include_router(laplace.router, prefix="/api/v1/laplace")
app.include_router(ztransform.router, prefix="/api/v1/ztransform")

# Shared backend management
@app.get("/api/v1/backends/")
def list_all_backends():
    return {
        "wavelet": wavelet.get_backends(),
        "fourier": fourier.get_backends(),
        "laplace": laplace.get_backends(),
        "ztransform": ztransform.get_backends()
    }

# Unified hardware detection
@app.get("/api/v1/hardware/detect")
def detect_hardware():
    return {
        "fpga": FPGABackend.detect(),  # Tang Nano 9K
        "gpu": GPUBackend.detect(),    # CUDA/CuPy
        "cpu": CPUBackend.detect()     # Multi-core
    }
```

---

## 🤔 Decision: Why Unified Server (Not Separate Servers)?

### Technical Reasons

**1. All Libraries Are Python-Compatible**
```python
# Everything runs in the same Python environment!
import pywt              # PyWavelets for CWT/DWT
import scipy.signal      # Filtering, Z-transform, Laplace
import scipy.fft         # FFT
from astropy.timeseries import LombScargle
import control           # Control systems
import numpy as np       # Universal foundation
import cupy as cp        # GPU acceleration (if available)
```
No need for:
- ❌ Different programming languages (C++, Rust, Julia)
- ❌ Inter-process communication (gRPC, message queues)
- ❌ Data serialization overhead
- ❌ Multiple deployment pipelines

**2. Hardware Can Be Shared**
```
Tang Nano 9K FPGA:
├── Wavelet cores (already implemented!)
├── FFT cores (can add)
├── Matrix multiply (for Laplace)
└── IIR/FIR filter cores (for Z-transform)

GPU (CuPy/CUDA):
├── Batch FFT (all lenses need this)
├── Matrix operations (Laplace state-space)
├── Parallel filtering (Z-transform)
└── Wavelet transforms (speed boost)
```
One piece of hardware, multiple acceleration targets!

**3. Cross-Lens Operations**
Many biological analyses need MULTIPLE lenses:
```python
# Example: Stress response analysis
def analyze_stress_response(signal):
    # 1. Wavelet: Detect transient stress event
    transients = wavelet_analysis(signal)
    
    # 2. Fourier: Normal circadian rhythm (non-transient regions)
    normal_signal = signal[~transients]
    circadian = lomb_scargle(normal_signal)
    
    # 3. Laplace: Recovery dynamics (transfer function)
    recovery_tf = identify_system(stress_input, response_output)
    
    # 4. Z-Transform: Real-time monitoring filter
    monitoring_filter = design_filter(cutoff=circadian_freq)
    
    return {
        "transients": transients,
        "circadian_rhythm": circadian,
        "recovery_dynamics": recovery_tf,
        "monitoring_filter": monitoring_filter
    }
```
**Single server = no network latency between lenses!**

**4. Deployment Simplicity**
```bash
# Unified approach (SIMPLE)
docker run -p 8000:8000 bioxen/server
# One server, one port, one process

# vs Microservices approach (COMPLEX)
docker-compose up
# - 4 separate containers
# - 4 different ports (8000-8003)
# - 4x configuration files
# - Service mesh/API gateway needed
# - Load balancer needed
# - 4x monitoring/logging setup
```

**5. Cost and Resource Efficiency**
```
Unified Server:
- One machine with Tang Nano 9K FPGA
- One GPU (shared by all lenses)
- One set of Python dependencies
- Estimated cost: $500-2000

vs Microservices:
- Need 4 separate machines OR
- Need orchestration (Kubernetes)
- Possibly 4 FPGAs or complex routing
- 4x memory footprint (Python runtime)
- Estimated cost: $2000-8000+
```

### Practical Reasons

**6. Development Velocity**
- ✅ One codebase to understand
- ✅ Shared utilities and helpers
- ✅ Single test suite
- ✅ One API specification document
- ✅ Faster iteration

**7. User Experience**
```python
# User perspective (unified):
from bioxen import BioXenClient
client = BioXenClient("http://bioxen.local:8000")
result = client.wavelet.analyze(signal)
result = client.fourier.lomb_scargle(signal)

# vs (microservices):
from bioxen import WaveletClient, FourierClient, LaplaceClient, ZTransformClient
wavelet = WaveletClient("http://wavelet.local:8000")
fourier = FourierClient("http://fourier.local:8001")
laplace = LaplaceClient("http://laplace.local:8002")
ztransform = ZTransformClient("http://ztransform.local:8003")
# Users need to manage 4 connections!
```

**8. Research/Academic Environment**
- Most biology labs have ONE computational server
- Easy to deploy: clone repo, run one command
- Low maintenance: one thing to update
- Easy to share: give collaborators one URL

### 📚 Software Separation Analysis: Are There Lens-Specific Library Ecosystems?

**The real question: Do the lenses have incompatible dependencies that would benefit from isolation?**

Let me analyze each lens's library ecosystem:

#### 🌊 Fourier Lens Library Stack
```python
# Core Python Libraries
import scipy.fft              # Modern FFT implementation
import numpy.fft              # Classic FFT
from astropy.timeseries import LombScargle  # Irregular sampling

# Specialized Options (same language, different performance)
import pyfftw                 # FFTW3 wrapper (faster)
import mkl_fft                # Intel MKL (fastest on Intel CPUs)
import cupy.fft               # GPU-accelerated FFT
```

**Alternative Ecosystems:**
- MATLAB Signal Processing Toolbox (proprietary, $$$)
- Julia `FFTW.jl` (different language)
- C++ FFTW directly (different language)

**Verdict:** ✅ **Python ecosystem is mature and complete**
- All options are Python-compatible
- Can swap backends without API changes
- No need for language barriers

---

#### 📈 Wavelet Lens Library Stack
```python
# Core Python Libraries
import pywt                   # PyWavelets (gold standard)
import scipy.signal           # cwt, morlet, ricker

# Specialized Options
import kymatio               # GPU-accelerated wavelets (PyTorch backend)
import mlpy.wavelet          # Machine learning focus
# wavelets-ext (C extensions)
```

**Alternative Ecosystems:**
- MATLAB Wavelet Toolbox (proprietary, $$$)
- R `wavelets` package (different language)
- WaveLab (MATLAB, academic)

**Verdict:** ✅ **Python ecosystem is best-in-class**
- PyWavelets is THE reference implementation
- kymatio adds GPU without changing language
- Actually better than MATLAB for research

---

#### ⚙️ Laplace Lens Library Stack
```python
# Core Python Libraries (OPEN SOURCE!)
import control               # python-control (Richard Murray, Caltech)
                            # Full control systems: TF, state-space, bode, nyquist
import scipy.signal          # lti, TransferFunction, StateSpace (built-in!)

# Specialized Options (OPEN SOURCE!)
import harold                # Modern control library (pure Python)
import slycot                # Python wrapper for SLICOT (FORTRAN, fast)
                            # NOTE: slycot wraps SLICOT which IS open source!
```

**Open Source Alternatives:**
- **python-control** (Python, recommended) ✅
- **GNU Octave + control package** (MATLAB-compatible, free)
- **Julia ControlSystems.jl** (fast, modern)
- **SLICOT** (FORTRAN/C, industry-grade, open source!)

**Proprietary (NOT USED):**
- ❌ MATLAB Control System Toolbox ($$$, not open source)
- ❌ Scilab (different ecosystem, less maintained)

**Verdict:** ✅ **Python ecosystem is excellent AND fully open source!**
- `python-control` is Caltech-developed, industry-grade
- Used in aerospace, robotics, AND biology research
- SLICOT backend (via slycot) provides FORTRAN speed
- `scipy.signal` provides fallback for basic operations
- **NO proprietary software needed!** 🎉

---

#### 📊 Z-Transform Lens Library Stack
```python
# Core Python Libraries
import scipy.signal          # zpk, filter design, freqz
import numpy                 # polynomial operations

# Specialized Options
import filterpy              # Kalman filters (excellent!)
import pykalman              # Alternative Kalman
import simdkalman            # SIMD-optimized Kalman
```

**Alternative Ecosystems:**
- MATLAB DSP Toolbox (industry standard, $$$)
- GNU Radio (C++/Python hybrid, real-time focus)
- C++ libraries (Eigen + custom code)

**Verdict:** ✅ **Python ecosystem is excellent**
- SciPy signal processing is comprehensive
- filterpy is better than MATLAB for Kalman
- No need for C++ unless doing embedded hardware

---

### 🌟 ALL Libraries Are Open Source!

**BioXen uses 100% open-source software. Here's the complete stack:**

```bash
# Install ALL lens libraries (one command!)
pip install numpy scipy pywt astropy control filterpy

# Optional: Performance boosters
pip install cupy-cuda12x    # GPU acceleration (NVIDIA)
pip install pyfftw          # FFTW3 wrapper (faster FFT)
pip install kymatio         # GPU wavelets (requires PyTorch)
pip install slycot          # FORTRAN SLICOT wrapper (faster control)
```

**License Summary:**

| Library | License | Purpose | Required? |
|---------|---------|---------|-----------|
| **NumPy** | BSD-3 | Foundation for all | ✅ Yes |
| **SciPy** | BSD-3 | FFT, filters, signal processing | ✅ Yes |
| **PyWavelets** | MIT | Wavelet transforms | ✅ Yes |
| **Astropy** | BSD-3 | Lomb-Scargle periodogram | ✅ Yes |
| **python-control** | BSD-3 | Control systems, Laplace | ✅ Yes |
| **filterpy** | MIT | Kalman filters | ✅ Yes |
| **CuPy** | MIT | GPU acceleration | ⭐ Optional |
| **PyFFTW** | BSD-3 | Fast FFT | ⭐ Optional |
| **kymatio** | BSD-3 | GPU wavelets | ⭐ Optional |
| **slycot** | BSD-3 | Fast control systems | ⭐ Optional |

**Key Points:**
- ✅ All BSD/MIT licenses (permissive, commercial-friendly)
- ✅ No proprietary dependencies (no MATLAB, no fees)
- ✅ No GPL/AGPL (no viral licensing)
- ✅ Can deploy in academic OR commercial settings
- ✅ Can modify and redistribute freely

**About python-control:**
```python
# python-control is THE open-source control systems library
# Developed at Caltech by Richard Murray
# Used by: NASA JPL, SpaceX, robotics labs, biology research
# Features: Transfer functions, state-space, stability analysis,
#           root locus, Bode plots, Nyquist plots, LQR, pole placement

import control

# Create transfer function: H(s) = 1 / (s^2 + 2s + 1)
sys = control.TransferFunction([1], [1, 2, 1])

# Analyze stability
poles = control.pole(sys)
print(f"Poles: {poles}")  # Both negative = stable!

# Plot Bode diagram
control.bode_plot(sys)

# Design controller (LQR, pole placement, etc.)
K = control.lqr(A, B, Q, R)
```

**About SLICOT (optional speedup):**
```bash
# SLICOT = Subroutine Library In COntrol Theory
# Written in FORTRAN (fast!), open source (BSD)
# Industry standard for numerical control algorithms
# Used in aerospace, automotive, robotics

# Install Python wrapper:
pip install slycot

# python-control automatically uses slycot if available
# No code changes needed - just faster execution!
```

**Comparison with MATLAB:**

| Feature | MATLAB Control Toolbox | python-control + SciPy |
|---------|------------------------|------------------------|
| **Cost** | $1000+/year | FREE ✅ |
| **License** | Proprietary | Open Source (BSD) ✅ |
| **Transfer Functions** | ✅ | ✅ |
| **State-Space** | ✅ | ✅ |
| **Bode/Nyquist Plots** | ✅ | ✅ |
| **Root Locus** | ✅ | ✅ |
| **LQR/LQG** | ✅ | ✅ |
| **Pole Placement** | ✅ | ✅ |
| **Script Automation** | ⚠️ Needs MATLAB | ✅ Pure Python |
| **Integration with Biology Tools** | ❌ Difficult | ✅ Easy (same ecosystem) |
| **Deployment** | ❌ License server | ✅ Docker/pip |

**For BioXen: python-control is better than MATLAB because:**
1. ✅ Free and open source
2. ✅ Integrates with NumPy/SciPy biology tools
3. ✅ Easy deployment (no license servers)
4. ✅ Scriptable and automatable
5. ✅ Active development (updates regularly)

---

### 🤔 Should We Keep Software Separate?

**Arguments FOR separation:**

1. **Dependency Isolation**
   ```bash
   # If libraries conflict:
   Fourier server: scipy==1.10, numpy==1.24
   Wavelet server: kymatio==0.3 (requires PyTorch 2.0)
   Laplace server: slycot==0.5 (requires old FORTRAN)
   ```
   → BUT: We're using core libraries (scipy, numpy, pywt) that play nicely together!

2. **Performance Optimization**
   ```python
   # Different backends per lens:
   Fourier: mkl_fft (Intel optimized)
   Wavelet: kymatio (PyTorch GPU)
   Laplace: slycot (FORTRAN)
   Z-Transform: simdkalman (SIMD)
   ```
   → BUT: These are **backend swaps**, not architecture changes!
   → Single server can import all and choose backend dynamically

3. **Development Independence**
   ```
   Team A: Fourier expert, updates Lomb-Scargle daily
   Team B: Wavelet expert, updates CWT monthly
   Team C: Control theorist, updates Laplace rarely
   ```
   → BUT: BioXen is single-team, coordinated development!

**Arguments AGAINST separation:**

1. **No Dependency Conflicts**
   ```bash
   pip install scipy numpy pywt astropy python-control filterpy
   # These all work together! No version conflicts!
   ```

2. **Shared Core**
   ```python
   # ALL lenses share:
   import numpy as np
   # Fourier uses: np.fft, np.correlate
   # Wavelet uses: np arrays for scales
   # Laplace uses: np.linalg for state-space
   # Z-Transform uses: np.roots for poles/zeros
   ```
   → **70% of the code is NumPy operations!**

3. **Cross-Lens Operations Are Common**
   ```python
   # Real biology workflow:
   def analyze_gene_expression(data):
       # 1. Wavelet: Remove transients
       cleaned = wavelet_denoise(data)
       
       # 2. Fourier: Find circadian frequency
       freq = lomb_scargle(cleaned)
       
       # 3. Z-Transform: Design bandpass filter
       b, a = butter_bandpass(freq - 0.1, freq + 0.1)
       
       # 4. Laplace: Model feedback control
       tf = system_identification(filtered, stimulus)
   ```
   → **Separate servers = 4x network calls + serialization overhead!**

4. **Library Updates Affect Multiple Lenses**
   ```bash
   # NumPy 2.0 breaking change affects ALL lenses
   # Better to update once than 4 times
   ```

### 📊 Decision Matrix: Software Separation?

| Criterion | Unified | Separate | Winner |
|-----------|---------|----------|--------|
| Dependency conflicts? | None found | Potential isolation benefit | **Unified** ✅ |
| Performance optimization? | Backend swapping works | Slightly easier per-service tuning | **Unified** ✅ |
| Development velocity? | Single codebase | 4x repositories | **Unified** ✅ |
| Cross-lens operations? | Zero latency | Network overhead | **Unified** ✅ |
| Team structure? | Single team | Would need 4 teams | **Unified** ✅ |
| Library updates? | Update once | Update 4x | **Unified** ✅ |
| Code reuse? | Shared utilities | Duplicate code | **Unified** ✅ |

**Score: Unified 7, Separate 0**

### 🎯 Final Recommendation: UNIFIED SOFTWARE

**Why?**
1. ✅ No dependency conflicts (scipy, numpy, pywt, control all compatible)
2. ✅ Shared NumPy core (70% of operations)
3. ✅ Cross-lens workflows need tight integration
4. ✅ Backend optimization doesn't require separation
5. ✅ Single team, coordinated development

**But keep modularity!**
```python
# Server structure (unified but organized):
bioxen_server/
├── routers/
│   ├── fourier_router.py      # Independent module
│   ├── wavelet_router.py      # Independent module
│   ├── laplace_router.py      # Independent module
│   └── ztransform_router.py   # Independent module
├── lenses/
│   ├── fourier_lens.py        # Can extract later if needed
│   ├── wavelet_lens.py        # Can extract later if needed
│   ├── laplace_lens.py        # Can extract later if needed
│   └── ztransform_lens.py     # Can extract later if needed
└── main.py                     # Ties it together
```

**We get the best of both worlds:**
- ✅ Tight integration (shared memory, no network)
- ✅ Modular code (can extract modules later)
- ✅ Independent testing (each lens has own tests)
- ✅ Clear ownership (each file has clear purpose)

---

### When Would We Split?

**Microservices make sense IF:**
1. **Massive scale** - Processing thousands of requests/second per lens
2. **Different languages required** - e.g., need Rust for ultra-low latency Z-transform
3. **Separate teams** - Different groups owning different lenses
4. **Different deployment cycles** - Need to update one lens independently
5. **Hardware constraints** - Different lenses on different machines
6. **Dependency hell** - Libraries genuinely conflict (NOT the case here)

**For BioXen:**
- ❌ Scale: Biology labs typically <100 concurrent users
- ❌ Languages: All Python libraries available
- ❌ Teams: Single project, integrated development
- ❌ Deployment: Coordinated releases make sense
- ❌ Hardware: Can share Tang Nano 9K + GPU
- ❌ Dependencies: No conflicts found

### Migration Path (If Needed Later)

**The architecture supports future splitting:**
```python
# Current: All lenses in one server
app.include_router(wavelet.router, prefix="/api/v1/wavelet")
app.include_router(fourier.router, prefix="/api/v1/fourier")

# Future: Split if needed
# 1. Keep router code identical
# 2. Deploy each router as separate service
# 3. Add API gateway in front
# 4. Client code doesn't change!
```

**We can start unified and split later if requirements change!**

---

## � No Proprietary Software Required!

**BioXen is 100% open source. We do NOT use:**

| ❌ Proprietary | ✅ Open Source Alternative | Status |
|----------------|---------------------------|--------|
| MATLAB Control Toolbox ($$$) | python-control (BSD) | **Better for biology!** |
| MATLAB Signal Processing | scipy.signal (BSD) | **Equal or better** |
| MATLAB Wavelet Toolbox | PyWavelets (MIT) | **Reference implementation** |
| Mathematica | SymPy (BSD) | Not needed |
| LabVIEW | Python + libraries | Better for automation |
| Simulink | Python-control + SciPy | Better for scripting |

### Why python-control Is Better Than MATLAB for BioXen:

**Technical Reasons:**
```python
# 1. Same ecosystem (no data export/import)
import numpy as np
from scipy import signal
import control as ct

data = np.load('gene_expression.npy')        # NumPy
filtered = signal.butter(data)                # SciPy
sys = ct.StateSpace(A, B, C, D)              # control
# All in one environment!

# vs MATLAB:
# - Load data in Python
# - Export to .mat file
# - Process in MATLAB
# - Import back to Python
# Pain!
```

**Practical Reasons:**
1. **Cost**: Free vs $1000+/year per seat
2. **Deployment**: `pip install` vs license server setup
3. **Automation**: Pure Python scripts vs MATLAB engine API
4. **Integration**: Direct with biology tools (BioPython, scanpy, etc.)
5. **Collaboration**: Students can run on any machine (no license needed)

**What python-control Provides:**
- ✅ Transfer functions: `ct.TransferFunction(num, den)`
- ✅ State-space models: `ct.StateSpace(A, B, C, D)`
- ✅ Bode plots: `ct.bode_plot(sys)`
- ✅ Nyquist plots: `ct.nyquist_plot(sys)`
- ✅ Root locus: `ct.root_locus(sys)`
- ✅ LQR control: `ct.lqr(A, B, Q, R)`
- ✅ Pole placement: `ct.place(A, B, poles)`
- ✅ System interconnections: `ct.feedback()`, `ct.series()`
- ✅ Time responses: `ct.step_response()`, `ct.impulse_response()`
- ✅ Stability analysis: `ct.pole()`, `ct.damp()`

**Developed by:**
- Richard Murray (Caltech)
- Active open-source community
- Used by: NASA JPL, robotics labs, academia

**Performance:**
- Standard: Pure Python (fast enough for biology)
- Optimized: Uses slycot (FORTRAN SLICOT wrapper) if installed
- SLICOT = industry-standard numerical library (open source!)

### Installation for All Lenses:

```bash
# Core libraries (required)
pip install numpy scipy pywt astropy control filterpy matplotlib

# Optional performance boosters
pip install slycot          # Faster control systems (FORTRAN)
pip install pyfftw          # Faster FFT (FFTW3 wrapper)
pip install cupy-cuda12x    # GPU acceleration (NVIDIA)
pip install kymatio         # GPU wavelets (PyTorch backend)

# That's it! No license keys, no activation, no fees.
```

### License Compliance:

**All libraries are BSD or MIT licensed:**
- ✅ Can use commercially
- ✅ Can modify and redistribute
- ✅ Can bundle with proprietary software
- ✅ No viral licensing (not GPL/AGPL)
- ✅ No attribution requirements in binary distributions

**Perfect for:**
- Academic research (free for students!)
- Commercial biology tools (no royalties!)
- Open-source projects (compatible licenses!)

---

## �📋 Phase 1: Wavelet Lens Refactor (Starting Point)

**Why Start Here?**
- ✅ Server already running and tested
- ✅ API specification complete
- ✅ Client tests validate server behavior
- ✅ Hardware acceleration proven working
- ✅ Most complex lens - if this works, others will be easier

### Step 0: Migrate PyCWT-mod to Unified BioXen Server

**Current State:** Standalone PyCWT-mod server at `wavelet.local:8000`

**Migration Strategy:**
1. Keep existing PyCWT-mod endpoints working (backward compatibility)
2. Add new lens routers to same FastAPI app
3. Gradually migrate to unified endpoint structure
4. Update API specification to include all lenses

**New Server Structure:**
```
server/
├── main.py                      ← Unified FastAPI app
├── routers/
│   ├── wavelet.py              ← Existing PyCWT-mod endpoints
│   ├── fourier.py              ← New Fourier lens
│   ├── laplace.py              ← New Laplace lens
│   └── ztransform.py           ← New Z-Transform lens
├── backends/
│   ├── fpga_backend.py         ← Tang Nano 9K (shared by all lenses)
│   ├── gpu_backend.py          ← CuPy acceleration
│   ├── cpu_sequential.py       ← Single-core
│   └── cpu_parallel.py         ← Joblib multi-core
└── core/
    ├── wavelet_ops.py          ← PyWavelets wrapper
    ├── fourier_ops.py          ← SciPy FFT, Astropy
    ├── laplace_ops.py          ← Python-Control
    └── ztransform_ops.py       ← SciPy signal
```

**Timeline:** 1-2 weeks (in parallel with client development)

### Step 1: Create Unified BioXen Client Library

**File:** `src/bioxen_fourier_vm_lib/clients/bioxen_client.py`

**Purpose:** Single Python client that wraps ALL lens endpoints

**Why Unified Client:**
- ✅ One connection pool for all requests
- ✅ Consistent error handling across lenses
- ✅ Automatic server discovery
- ✅ Simpler user experience

**Features:**
```python
from bioxen_fourier_vm_lib.clients import BioXenClient

# Connect to unified server
client = BioXenClient(base_url="http://bioxen.local:8000")

# Or for backward compatibility with existing PyCWT-mod server
client = BioXenClient(base_url="http://wavelet.local:8000")

# Check server health
health = client.health_check()

# List available backends
backends = client.list_backends()

# Detect hardware
hardware = client.detect_hardware()

# Continuous Wavelet Transform
result = client.cwt(
    signal=my_signal,
    dt=1.0,
    wavelet='morlet',
    backend='elm11',  # Use FPGA acceleration
    scales=np.arange(1, 128)
)

# Wavelet Coherence Transform
coherence = client.wct(
    signal1=glucose,
    signal2=insulin,
    dt=0.25,
    backend='joblib',
    significance_test=True,
    mc_count=300
)

# Cross Wavelet Transform
cross = client.xwt(
    signal1=input_signal,
    signal2=output_signal,
    dt=1.0,
    backend='sequential'
)

# Benchmark backends
benchmark = client.benchmark(
    signal_length=1000,
    mc_count=100,
    backends=['sequential', 'joblib', 'elm11']
)

# NEW: Access other lenses from same client
# Fourier analysis
fourier_result = client.fourier.lomb_scargle(
    signal=my_signal,
    times=time_points,
    frequency_range=(0.01, 0.5)
)

# Laplace analysis
tf = client.laplace.identify_system(
    input_signal=glucose,
    output_signal=insulin,
    dt=5.0
)

# Z-Transform filtering
filtered = client.ztransform.apply_filter(
    signal=noisy_signal,
    filter_design=my_filter
)
```

**Implementation:**
- Uses `httpx` for HTTP requests (already in client-tests)
- Wraps ALL endpoints from unified API specification
- Lens-specific methods organized under submodules: `client.wavelet.*`, `client.fourier.*`, etc.
- Proper error handling and retry logic
- Automatic result parsing to NumPy arrays
- Connection pooling for performance
- Automatic fallback to local if server unavailable

### Step 2: Extract Wavelet Lens to Standalone Module

**File:** `src/bioxen_fourier_vm_lib/lenses/wavelet_lens.py`

**Purpose:** Independent wavelet analysis module with dual-mode support

**Architecture:**
```python
from bioxen_fourier_vm_lib.lenses.wavelet_lens import WaveletLens

# Create lens with local computation (default)
lens = WaveletLens(mode='local')

# Or with remote server
lens = WaveletLens(
    mode='remote',
    server_url='http://wavelet.local:8000',
    default_backend='elm11'  # Use FPGA by default
)

# Unified API - same whether local or remote
result = lens.analyze(
    signal=my_signal,
    dt=1.0,
    method='cwt',
    auto_select=True,
    enable_mra=True,
    mra_levels=5
)

# Access results (same format for local/remote)
print(f"Wavelet: {result.wavelet_used}")
print(f"Score: {result.selection_score}")
print(f"MRA components: {result.mra_components.keys()}")
```

**Implementation:**
- Extract current wavelet code from `SystemAnalyzer`
- Add `LocalBackend` and `RemoteBackend` support
- Use `PyCWTClient` for remote mode
- Keep all existing features (auto-select, MRA, transient detection)
- Transparent backend switching

### Step 3: Update SystemAnalyzer to Use New Architecture

**File:** `src/bioxen_fourier_vm_lib/analysis/system_analyzer.py`

**Changes:**
```python
from bioxen_fourier_vm_lib.lenses import (
    FourierLens,
    WaveletLens,
    LaplaceLens,
    ZTransformLens
)

class SystemAnalyzer:
    """
    Unified interface for multi-lens biological signal analysis.
    
    Each lens can operate in local or remote mode.
    """
    
    def __init__(self, wavelet_server=None, fourier_server=None,
                 laplace_server=None, ztransform_server=None):
        """
        Initialize analyzer with optional remote servers.
        
        Args:
            wavelet_server: URL for PyCWT-mod server (e.g., 'http://wavelet.local:8000')
            fourier_server: URL for Fourier server (future)
            laplace_server: URL for Laplace server (future)
            ztransform_server: URL for Z-transform server (future)
        """
        # Initialize lenses
        self.fourier_lens = FourierLens(
            mode='remote' if fourier_server else 'local',
            server_url=fourier_server
        )
        
        self.wavelet_lens = WaveletLens(
            mode='remote' if wavelet_server else 'local',
            server_url=wavelet_server
        )
        
        self.laplace_lens = LaplaceLens(
            mode='remote' if laplace_server else 'local',
            server_url=laplace_server
        )
        
        self.ztransform_lens = ZTransformLens(
            mode='remote' if ztransform_server else 'local',
            server_url=ztransform_server
        )
    
    # Keep existing lens methods but delegate to lens objects
    def fourier_lens_analyze(self, *args, **kwargs):
        """Fourier analysis (delegates to FourierLens)."""
        return self.fourier_lens.analyze(*args, **kwargs)
    
    def wavelet_lens_analyze(self, *args, **kwargs):
        """Wavelet analysis (delegates to WaveletLens)."""
        return self.wavelet_lens.analyze(*args, **kwargs)
    
    def laplace_lens_analyze(self, *args, **kwargs):
        """Laplace analysis (delegates to LaplaceLens)."""
        return self.laplace_lens.analyze(*args, **kwargs)
    
    def ztransform_lens_analyze(self, *args, **kwargs):
        """Z-transform analysis (delegates to ZTransformLens)."""
        return self.ztransform_lens.analyze(*args, **kwargs)
```

**Benefits:**
- Backward compatible with existing code
- Each lens independently testable
- Easy to add new lenses
- Flexible deployment (local, remote, or hybrid)

### Step 4: Update Tests for New Architecture

**Changes:**
- Update existing tests in `tests/` to use new lens modules
- Keep all existing functionality tests passing
- Add tests for remote mode (using mock server)
- Add integration tests with actual server
- Ensure backward compatibility

### Step 5: Documentation and Migration Guide

**Create:**
1. Migration guide for existing users
2. Updated API documentation
3. Examples for local vs remote usage
4. Performance benchmarks (local vs FPGA)
5. Deployment guide for self-hosted servers

---

## 📋 Phase 2: Fourier Lens Refactor

**Goal:** Apply lessons learned from wavelet lens to Fourier lens

### Components to Create

1. **Fourier Server** (Future)
   - REST API similar to PyCWT-mod
   - Hardware-accelerated FFT (GPU/FPGA)
   - Lomb-Scargle periodogram optimization for biological data
   
   **Proposed Endpoints:**
   
   **Core Fourier Analysis:**
   - `POST /api/v1/fourier/lomb-scargle` - Lomb-Scargle periodogram (irregular sampling)
     ```json
     {
       "signal": [1.2, 1.5, ...],
       "times": [0.0, 1.3, 2.7, ...],  // Irregular time points
       "frequency_range": [0.01, 0.5],
       "backend": "gpu"
     }
     ```
   
   - `POST /api/v1/fourier/fft` - Fast Fourier Transform (regular sampling)
     ```json
     {
       "signal": [1.2, 1.5, ...],
       "dt": 0.25,
       "window": "hann",
       "backend": "fftw"  // FFTW, cuFFT, or custom FPGA
     }
     ```
   
   - `POST /api/v1/fourier/stft` - Short-Time Fourier Transform
     ```json
     {
       "signal": [1.2, 1.5, ...],
       "dt": 0.25,
       "window_size": 256,
       "overlap": 128,
       "window_type": "hann"
     }
     ```
   
   **Spectral Analysis:**
   - `POST /api/v1/fourier/power-spectrum` - Power spectral density
   - `POST /api/v1/fourier/cross-spectrum` - Cross-spectral density
   - `POST /api/v1/fourier/coherence` - Spectral coherence between signals
   - `POST /api/v1/fourier/phase-spectrum` - Phase relationships
   
   **Biological Applications:**
   - `POST /api/v1/fourier/circadian` - Circadian rhythm detection (optimized for 24h)
     ```json
     {
       "signal": [1.2, 1.5, ...],
       "times": [0.0, 1.3, ...],
       "period_range": [20, 28],  // Hours
       "organism": "human",  // Species-specific optimization
       "confidence_interval": 0.95
     }
     ```
   
   - `POST /api/v1/fourier/ultradian` - Ultradian rhythm detection (<24h)
   - `POST /api/v1/fourier/infradian` - Infradian rhythm detection (>24h)
   
   **Hardware-Specific:**
   - `GET /api/v1/fourier/backends` - List FFT backends (FFTW, cuFFT, FPGA)
   - `POST /api/v1/fourier/benchmark` - Benchmark FFT implementations

2. **Fourier Client Library**
   - `src/bioxen_fourier_vm_lib/clients/fourier_client.py`
   - Wraps Fourier server API
   - Similar interface to PyCWT client
   
   **Example Usage:**
   ```python
   from bioxen_fourier_vm_lib.clients import FourierClient
   
   client = FourierClient(base_url="http://fourier.local:8001")
   
   # Lomb-Scargle for irregular sampling
   result = client.lomb_scargle(
       signal=atp_levels,
       times=measurement_times,
       frequency_range=(0.01, 0.5),
       backend='gpu'
   )
   
   # Circadian analysis
   circadian = client.circadian_analysis(
       signal=gene_expression,
       times=time_points,
       organism='human',
       confidence_interval=0.95
   )
   ```

3. **Standalone Fourier Lens**
   - `src/bioxen_fourier_vm_lib/lenses/fourier_lens.py`
   - Extract from SystemAnalyzer
   - Dual-mode support (local/remote)

**Timeline:** After Wavelet Lens refactor complete

**Hardware Acceleration Strategy:**
- **GPU (cuFFT):** 10-100x speedup for large signals (>10,000 points)
- **FFTW:** Optimized CPU implementation (2-5x speedup)
- **FPGA:** Custom FFT cores for real-time analysis

---

## 📋 Phase 3: Laplace Lens Refactor

**Goal:** System stability and transfer function analysis as a service

### Components to Create

1. **Laplace Server** (Future)
   - Transfer function computation
   - State-space model analysis
   - Stability analysis
   - Control system design
   
   **Proposed Endpoints:**
   
   **Transfer Function Analysis:**
   - `POST /api/v1/laplace/identify` - System identification from I/O data
     ```json
     {
       "input_signal": [1.0, 1.2, ...],
       "output_signal": [0.5, 0.8, ...],
       "dt": 0.25,
       "model_order": "auto",  // Or specify [num_order, den_order]
       "method": "arx"  // ARX, ARMAX, subspace, etc.
     }
     ```
   
   - `POST /api/v1/laplace/transfer-function` - Analyze transfer function
     ```json
     {
       "numerator": [1.0, 2.0],
       "denominator": [1.0, 3.0, 2.0],
       "analysis": ["bode", "nyquist", "step_response", "impulse_response"]
     }
     ```
   
   - `POST /api/v1/laplace/frequency-response` - Frequency response analysis
     ```json
     {
       "transfer_function": {...},
       "frequency_range": [0.001, 100],
       "num_points": 1000
     }
     ```
   
   **Stability Analysis:**
   - `POST /api/v1/laplace/stability` - Check system stability
     ```json
     {
       "transfer_function": {...},
       "margin_type": "both",  // gain, phase, or both
       "return_poles": true
     }
     ```
   
   - `POST /api/v1/laplace/pole-zero` - Pole-zero analysis
   - `POST /api/v1/laplace/root-locus` - Root locus plot data
   
   **State-Space Analysis:**
   - `POST /api/v1/laplace/state-space/convert` - TF ↔ State-space conversion
     ```json
     {
       "transfer_function": {...},
       "form": "controllable"  // controllable, observable, modal
     }
     ```
   
   - `POST /api/v1/laplace/state-space/analyze` - State-space system analysis
     ```json
     {
       "A": [[...]],  // State matrix
       "B": [[...]],  // Input matrix
       "C": [[...]],  // Output matrix
       "D": [[...]],  // Feedthrough matrix
       "analysis": ["controllability", "observability", "stability"]
     }
     ```
   
   - `POST /api/v1/laplace/state-space/simulate` - Time-domain simulation
   
   **Biological System Identification:**
   - `POST /api/v1/laplace/bio/homeostasis` - Homeostatic feedback analysis
     ```json
     {
       "sensor_signal": [36.5, 36.7, ...],  // e.g., body temperature
       "actuator_signal": [0.2, 0.5, ...],   // e.g., metabolic rate
       "disturbance_signal": [20, 22, ...],  // e.g., ambient temp
       "dt": 60.0,  // 1 minute sampling
       "model_type": "feedback"
     }
     ```
   
   - `POST /api/v1/laplace/bio/drug-response` - Pharmacokinetics/dynamics
     ```json
     {
       "dose_signal": [100, 0, 0, ...],      // Drug dosing
       "concentration_signal": [0, 50, ...],  // Blood concentration
       "response_signal": [0, 0.8, ...],      // Biological response
       "compartment_model": "two_compartment"
     }
     ```
   
   - `POST /api/v1/laplace/bio/metabolic-control` - Metabolic pathway control
   
   **Control Design:**
   - `POST /api/v1/laplace/controller/pid` - PID controller design
     ```json
     {
       "plant_tf": {...},
       "requirements": {
         "settling_time": 10.0,
         "overshoot": 0.1,
         "steady_state_error": 0.01
       },
       "tuning_method": "ziegler-nichols"
     }
     ```
   
   - `POST /api/v1/laplace/controller/lqr` - Linear Quadratic Regulator
   - `POST /api/v1/laplace/controller/observer` - State observer design
   
   **Benchmarking:**
   - `POST /api/v1/laplace/benchmark` - Performance comparison
   - `GET /api/v1/laplace/backends` - List available backends

2. **Laplace Client Library**
   - `src/bioxen_fourier_vm_lib/clients/laplace_client.py`
   
   **Example Usage:**
   ```python
   from bioxen_fourier_vm_lib.clients import LaplaceClient
   
   client = LaplaceClient(base_url="http://laplace.local:8002")
   
   # System identification
   tf = client.identify_system(
       input_signal=glucose_input,
       output_signal=insulin_output,
       dt=5.0,  # 5 minute sampling
       model_order='auto'
   )
   
   # Stability analysis
   stability = client.analyze_stability(
       transfer_function=tf,
       margin_type='both'
   )
   
   # Homeostatic feedback
   feedback = client.analyze_homeostasis(
       sensor_signal=temperature,
       actuator_signal=metabolic_rate,
       disturbance_signal=ambient_temp
   )
   ```

3. **Standalone Laplace Lens**
   - `src/bioxen_fourier_vm_lib/lenses/laplace_lens.py`
   - Extract control theory code
   - Dual-mode support

**Timeline:** After Fourier Lens refactor complete

**Hardware Acceleration Strategy:**
- **GPU:** Matrix operations for large state-space systems
- **Symbolic Math Libraries:** CAS systems for analytical solutions
- **Numerical Solvers:** High-performance ODE/DAE solvers

---

## 📋 Phase 4: Z-Transform Lens Refactor

**Goal:** Discrete-time filtering and digital signal processing

### Components to Create

1. **Z-Transform Server** (Future)
   - Digital filter design and implementation
   - Kalman filtering and state estimation
   - Discrete-time system analysis
   - Real-time signal processing
   
   **Proposed Endpoints:**
   
   **Digital Filter Design:**
   - `POST /api/v1/ztransform/filter/design` - Design digital filter
     ```json
     {
       "filter_type": "lowpass",  // lowpass, highpass, bandpass, bandstop
       "method": "butterworth",   // butterworth, chebyshev, elliptic, bessel
       "order": 4,
       "critical_freq": 0.1,  // Normalized frequency (0-1)
       "sample_rate": 4.0,    // Hz
       "requirements": {
         "passband_ripple": 0.5,  // dB
         "stopband_attenuation": 40  // dB
       }
     }
     ```
   
   - `POST /api/v1/ztransform/filter/fir` - FIR filter design
     ```json
     {
       "method": "window",  // window, frequency_sampling, least_squares
       "window_type": "hamming",
       "num_taps": 64,
       "cutoff_freq": 0.2,
       "filter_type": "lowpass"
     }
     ```
   
   - `POST /api/v1/ztransform/filter/iir` - IIR filter design
   - `POST /api/v1/ztransform/filter/adaptive` - Adaptive filter (LMS, RLS)
   
   **Signal Filtering:**
   - `POST /api/v1/ztransform/filter/apply` - Apply designed filter
     ```json
     {
       "signal": [1.2, 1.5, ...],
       "filter": {
         "b": [0.1, 0.2, ...],  // Numerator coefficients
         "a": [1.0, -0.5, ...]  // Denominator coefficients
       },
       "initial_conditions": "zero",  // zero, lfilter_zi, custom
       "backend": "scipy"  // scipy, fpga, custom
     }
     ```
   
   - `POST /api/v1/ztransform/filter/filtfilt` - Zero-phase filtering
   - `POST /api/v1/ztransform/filter/cascade` - Cascade multiple filters
   
   **Kalman Filtering:**
   - `POST /api/v1/ztransform/kalman/design` - Design Kalman filter
     ```json
     {
       "system_model": {
         "F": [[...]],  // State transition matrix
         "H": [[...]],  // Observation matrix
         "Q": [[...]],  // Process noise covariance
         "R": [[...]]   // Measurement noise covariance
       },
       "initial_state": [0, 0],
       "initial_covariance": [[1, 0], [0, 1]]
     }
     ```
   
   - `POST /api/v1/ztransform/kalman/filter` - Run Kalman filter
     ```json
     {
       "measurements": [1.2, 1.5, ...],
       "kalman_model": {...},
       "return_estimates": true,
       "return_covariances": true
     }
     ```
   
   - `POST /api/v1/ztransform/kalman/smooth` - Kalman smoother (RTS)
   - `POST /api/v1/ztransform/kalman/extended` - Extended Kalman Filter (EKF)
   - `POST /api/v1/ztransform/kalman/unscented` - Unscented Kalman Filter (UKF)
   
   **Discrete System Analysis:**
   - `POST /api/v1/ztransform/system/analyze` - Analyze discrete system
     ```json
     {
       "numerator": [1.0, 0.5],
       "denominator": [1.0, -0.8, 0.15],
       "sample_time": 0.25,
       "analysis": ["stability", "frequency_response", "step_response"]
     }
     ```
   
   - `POST /api/v1/ztransform/system/discretize` - Continuous to discrete
     ```json
     {
       "continuous_system": {...},
       "sample_time": 0.25,
       "method": "tustin"  // tustin, zoh, foh, euler
     }
     ```
   
   - `POST /api/v1/ztransform/system/poles-zeros` - Pole-zero analysis
   
   **Biological Signal Processing:**
   - `POST /api/v1/ztransform/bio/denoise` - Biological signal denoising
     ```json
     {
       "signal": [36.5, 36.7, ...],
       "signal_type": "temperature",  // temperature, ecg, eeg, etc.
       "noise_model": "gaussian",
       "method": "kalman"  // kalman, wavelet, adaptive
     }
     ```
   
   - `POST /api/v1/ztransform/bio/baseline-correction` - Baseline wander removal
     ```json
     {
       "signal": [...],
       "baseline_type": "polynomial",  // polynomial, median, morphological
       "order": 3
     }
     ```
   
   - `POST /api/v1/ztransform/bio/spike-detection` - Action potential detection
     ```json
     {
       "signal": [...],
       "method": "threshold",  // threshold, template_matching, wavelet
       "threshold": 3.0,  // Standard deviations
       "refractory_period": 5  // Samples
     }
     ```
   
   - `POST /api/v1/ztransform/bio/artifact-removal` - Remove measurement artifacts
   
   **Real-Time Processing:**
   - `POST /api/v1/ztransform/realtime/init` - Initialize real-time filter
     ```json
     {
       "filter_config": {...},
       "buffer_size": 1024,
       "latency_target": 10  // milliseconds
     }
     ```
   
   - `POST /api/v1/ztransform/realtime/process` - Process incoming samples
     ```json
     {
       "session_id": "rt_12345",
       "samples": [1.2, 1.3, 1.4],
       "timestamps": [0.0, 0.25, 0.5]
     }
     ```
   
   - `DELETE /api/v1/ztransform/realtime/{session_id}` - Close session
   
   **Filter Analysis:**
   - `POST /api/v1/ztransform/analysis/frequency-response` - Filter freq response
   - `POST /api/v1/ztransform/analysis/group-delay` - Group delay analysis
   - `POST /api/v1/ztransform/analysis/impulse-response` - Impulse response
   - `POST /api/v1/ztransform/analysis/stability` - Stability check
   
   **Benchmarking:**
   - `POST /api/v1/ztransform/benchmark` - Performance testing
   - `GET /api/v1/ztransform/backends` - List available backends

2. **Z-Transform Client Library**
   - `src/bioxen_fourier_vm_lib/clients/ztransform_client.py`
   
   **Example Usage:**
   ```python
   from bioxen_fourier_vm_lib.clients import ZTransformClient
   
   client = ZTransformClient(base_url="http://ztransform.local:8003")
   
   # Design digital filter
   filter_design = client.design_filter(
       filter_type='lowpass',
       method='butterworth',
       order=4,
       critical_freq=0.1,
       sample_rate=4.0
   )
   
   # Apply filter to signal
   filtered = client.apply_filter(
       signal=noisy_ecg,
       filter=filter_design,
       method='filtfilt'  # Zero-phase
   )
   
   # Kalman filtering
   kalman = client.design_kalman_filter(
       system_model={
           'F': [[1, 0.25], [0, 1]],  # Position and velocity
           'H': [[1, 0]],
           'Q': [[0.01, 0], [0, 0.01]],
           'R': [[1.0]]
       }
   )
   
   estimates = client.run_kalman_filter(
       measurements=position_measurements,
       kalman_model=kalman
   )
   
   # Real-time processing
   session = client.init_realtime_filter(
       filter_config=filter_design,
       buffer_size=1024,
       latency_target=10
   )
   
   for sample_batch in data_stream:
       filtered_batch = client.process_realtime(
           session_id=session['id'],
           samples=sample_batch
       )
   ```

3. **Standalone Z-Transform Lens**
   - `src/bioxen_fourier_vm_lib/lenses/ztransform_lens.py`
   - Extract filtering code
   - Dual-mode support (local/remote)
   - Real-time streaming support

**Timeline:** After Laplace Lens refactor complete

**Hardware Acceleration Strategy:**
- **FPGA:** Ultra-low latency filtering (<1ms) for real-time applications
- **DSP Chips:** Dedicated hardware for signal processing
- **GPU:** Batch processing for large datasets
- **Custom ASICs:** Future consideration for production deployments

**Real-Time Considerations:**
- **Latency Targets:** 
  - ICU monitoring: <10ms
  - Neural recording: <1ms
  - Cell culture: <100ms
- **Throughput:** Support 1000+ channels simultaneously
- **Reliability:** Graceful degradation, no data loss

---

## 🎯 Implementation Roadmap

### Week 1-2: PyCWT Client Library (Highest Priority)

**Deliverables:**
- [ ] `pycwt_client.py` - Complete REST API client
- [ ] Unit tests using mock server
- [ ] Integration tests with wavelet.local:8000
- [ ] Documentation and examples
- [ ] Performance benchmarks

**Success Criteria:**
- All endpoints wrapped in Pythonic API
- Tests pass at >95% rate
- Client handles network errors gracefully
- Response parsing validates against API spec

### Week 3: Wavelet Lens Extraction

**Deliverables:**
- [ ] `wavelet_lens.py` - Standalone wavelet module
- [ ] `LocalBackend` - Current implementation
- [ ] `RemoteBackend` - Uses PyCWT client
- [ ] Automatic backend selection
- [ ] All existing tests passing

**Success Criteria:**
- No functionality lost from current implementation
- Local and remote modes produce identical results (within numerical precision)
- Performance on par with current implementation
- Clean, documented API

### Week 4: SystemAnalyzer Refactor

**Deliverables:**
- [ ] Updated `system_analyzer.py` using lens objects
- [ ] Backward compatibility layer
- [ ] Migration guide for users
- [ ] Updated examples and tutorials
- [ ] Performance regression tests

**Success Criteria:**
- All existing tests pass without modification
- New architecture fully tested
- Documentation complete
- No breaking changes for users

### Week 5-6: Fourier Lens Refactor

**Deliverables:**
- [ ] `fourier_lens.py` - Standalone module
- [ ] Local backend working
- [ ] Integration with SystemAnalyzer
- [ ] Tests and documentation

**Note:** Server implementation deferred to later phase

### Week 7-8: Laplace & Z-Transform Lenses

**Deliverables:**
- [ ] `laplace_lens.py` - Standalone module
- [ ] `ztransform_lens.py` - Standalone module
- [ ] Both integrated with SystemAnalyzer
- [ ] Complete test coverage
- [ ] Updated documentation

### Week 9-10: Polish & Optimization

**Deliverables:**
- [ ] Performance optimization
- [ ] Code cleanup and refactoring
- [ ] Comprehensive documentation
- [ ] Example notebooks
- [ ] Tutorial videos

---

## 🔧 Technical Considerations

### API Design Principles

**1. Consistency Across Lenses**
```python
# All lenses should have similar interface
result = lens.analyze(
    signal,
    dt=1.0,
    method='specific_method',
    backend='auto',  # 'local', 'remote', or specific backend
    **method_specific_params
)
```

**2. Progressive Enhancement**
```python
# Start simple (local computation)
analyzer = SystemAnalyzer()

# Upgrade to hardware acceleration when available
analyzer = SystemAnalyzer(
    wavelet_server='http://wavelet.local:8000'
)

# Full hardware acceleration (future)
analyzer = SystemAnalyzer(
    wavelet_server='http://wavelet.local:8000',
    fourier_server='http://fourier.local:8001',
    laplace_server='http://laplace.local:8002',
    ztransform_server='http://ztransform.local:8003'
)
```

**3. Transparent Fallback**
```python
# If remote server unavailable, automatically fall back to local
lens = WaveletLens(mode='remote', server_url='http://down.server:8000')
result = lens.analyze(signal)  # Automatically uses local backend
# Logs warning: "Remote server unavailable, using local backend"
```

### Performance Considerations

**Benchmark Requirements:**
- Local computation should remain fast for small signals
- Remote computation should show speedup for large signals (>1000 points)
- Network overhead should be minimized (batch requests when possible)
- Hardware acceleration should provide 2-100x speedup (depending on hardware)

**Optimization Strategies:**
- Connection pooling for remote backends
- Request batching for multiple analyses
- Async support for concurrent requests
- Caching for repeated computations
- Smart backend selection based on signal size

### Error Handling

**Network Errors:**
```python
try:
    result = lens.analyze(signal, backend='remote')
except NetworkError:
    # Automatic fallback to local
    result = lens.analyze(signal, backend='local')
    logger.warning("Remote server unavailable, used local fallback")
```

**Validation Errors:**
```python
try:
    result = client.cwt(signal=[])  # Empty signal
except ValidationError as e:
    print(f"Invalid input: {e}")
    # Returns user-friendly error message
```

**Server Errors:**
```python
try:
    result = lens.analyze(signal, backend='remote')
except ServerError as e:
    print(f"Server error: {e.status_code} - {e.message}")
    # Server returns detailed error information
```

---

## 📊 Testing Strategy

### 1. Unit Tests (Per Lens)
- Test each lens in isolation
- Mock remote backends
- Test error handling
- Test edge cases

### 2. Integration Tests
- Test lens integration with SystemAnalyzer
- Test local/remote backend switching
- Test actual server communication
- Test fallback mechanisms

### 3. End-to-End Tests
- Test complete workflows
- Test multi-lens analyses
- Test performance benchmarks
- Test hardware acceleration

### 4. Client-Server Tests
- Use existing `client-tests/` suite
- Validate API contract
- Test all endpoints
- Performance testing

### 5. Regression Tests
- Ensure backward compatibility
- Compare results with previous version
- Test all examples still work
- Test migration path

---

## 📚 Documentation Plan

### 1. User Documentation

**Migration Guide:**
- How to update existing code
- What's changed, what's new
- Troubleshooting common issues

**Quick Start:**
- Installation
- Basic usage (local mode)
- Advanced usage (remote mode)
- Hardware acceleration setup

**Tutorials:**
- Each lens with biological examples
- Local vs remote comparison
- Performance optimization
- Custom server deployment

### 2. API Documentation

**Each Lens:**
- Full method documentation
- Parameter descriptions
- Return value specifications
- Usage examples

**Client Libraries:**
- REST API reference
- Python client reference
- Error codes and handling
- Performance guidelines

### 3. Developer Documentation

**Architecture:**
- System design overview
- Module relationships
- Extension points
- Contribution guidelines

**Server Development:**
- How to create new lens servers
- API specification guidelines
- Testing requirements
- Deployment best practices

---

## 🎯 Success Metrics

### Functionality
- [ ] All existing features preserved
- [ ] New remote mode working
- [ ] Hardware acceleration functional
- [ ] 100% backward compatibility

### Performance
- [ ] Local mode: Same speed as current
- [ ] Remote mode: 2-100x speedup (hardware dependent)
- [ ] Network overhead: <10% for signals >1000 points
- [ ] Memory efficiency: No increase for local mode

### Code Quality
- [ ] Test coverage: >95%
- [ ] Documentation: 100% of public APIs
- [ ] Code style: Consistent and clean
- [ ] Dependencies: Minimal additions

### User Experience
- [ ] Easy migration path
- [ ] Clear documentation
- [ ] Helpful error messages
- [ ] Progressive enhancement

---

## 🚀 Future Enhancements

### Phase 5: Multi-Server Orchestration
- Intelligent work distribution across servers
- Load balancing for multiple users
- Automatic server discovery
- Cloud deployment support

### Phase 6: Advanced Hardware Support
- CUDA GPU acceleration
- Custom FPGA designs for each lens
- Distributed computing (Dask, Ray)
- Quantum computing integration (future)

### Phase 7: Web Interface
- Browser-based analysis dashboard
- Real-time visualization
- Collaborative analysis
- Dataset management

### Phase 8: AI Integration
- Automatic lens selection
- Intelligent parameter tuning
- Anomaly detection
- Predictive modeling

---

## 💡 Key Benefits of This Refactor

### For Users
1. **Easy Start:** Works out of the box with local computation
2. **Easy Scale:** Add hardware acceleration when needed
3. **Consistent API:** Same interface for all lenses
4. **Future-Proof:** Easy to add new capabilities

### For Developers
1. **Modular Design:** Each lens independently developable
2. **Easy Testing:** Mock servers for unit tests
3. **Clear Separation:** Client/server boundaries well-defined
4. **Extensible:** Easy to add new lenses or backends

### For Researchers
1. **Hardware Access:** FPGA/GPU acceleration available
2. **Reproducible:** Server versions can be pinned
3. **Scalable:** Cloud deployment possible
4. **Collaborative:** Share servers with team

### For Deployment
1. **Flexible:** Local, remote, or hybrid
2. **Scalable:** Add servers as needed
3. **Resilient:** Automatic fallbacks
4. **Monitorable:** Server metrics available

---

## ✅ Next Immediate Actions

### This Week
1. **Review this plan** - Get feedback and alignment
2. **Start PyCWT client** - Begin with simplest endpoints (health, backends)
3. **Set up dev environment** - Ensure wavelet.local:8000 accessible
4. **Create project structure** - Set up new directories

### Next Week
1. **Complete PyCWT client** - All endpoints wrapped
2. **Write client tests** - Against actual server
3. **Begin wavelet lens extraction** - Start with local backend
4. **Document progress** - Keep this plan updated

---

## 🎉 Conclusion

This refactor transforms BioXen from a monolithic library into a **modern, scalable, hardware-accelerated biological signal analysis platform**. 

By starting with the **PyCWT-mod server** (which is already operational at wavelet.local:8000), we:
1. ✅ Build on proven technology
2. ✅ Validate the architecture with real hardware
3. ✅ Create a template for other lenses
4. ✅ Deliver immediate value (hardware acceleration)

The **4-Lens architecture** provides:
- 🔬 Scientific rigor (each lens has distinct purpose)
- 🧩 Modularity (independent development and testing)
- ⚡ Performance (hardware acceleration where needed)
- 📈 Scalability (add servers as needed)

**Let's transform biological signal analysis, one lens at a time!** 🌊🔬🚀

---

**Document Status:** Living document - update as implementation progresses  
**Last Updated:** 5 October 2025  
**Next Review:** After PyCWT client completion
