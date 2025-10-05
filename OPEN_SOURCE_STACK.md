# BioXen Open Source Software Stack

## 🌟 100% Open Source, Zero Proprietary Dependencies

BioXen uses only open-source libraries with permissive licenses (BSD/MIT).

## Core Libraries

### Required Dependencies

```bash
pip install numpy scipy pywt astropy control filterpy matplotlib
```

| Library | Version | License | Purpose |
|---------|---------|---------|---------|
| **NumPy** | 1.24+ | BSD-3 | Array operations, foundation |
| **SciPy** | 1.10+ | BSD-3 | FFT, signal processing, filtering |
| **PyWavelets** | 1.4+ | MIT | Wavelet transforms (CWT/DWT) |
| **Astropy** | 5.0+ | BSD-3 | Lomb-Scargle periodogram |
| **python-control** | 0.9+ | BSD-3 | Control systems, Laplace |
| **filterpy** | 1.4+ | MIT | Kalman filters |
| **matplotlib** | 3.5+ | PSF | Plotting |

### Optional Performance Boosters

```bash
pip install slycot pyfftw cupy-cuda12x kymatio
```

| Library | License | Purpose | Speedup |
|---------|---------|---------|---------|
| **slycot** | BSD-3 | FORTRAN SLICOT wrapper | 2-5x for control |
| **PyFFTW** | BSD-3 | FFTW3 wrapper | 2-3x for FFT |
| **CuPy** | MIT | GPU acceleration | 10-100x for large arrays |
| **kymatio** | BSD-3 | GPU wavelets (PyTorch) | 10-50x for wavelets |

## Lens-Specific Libraries

### 🌊 Fourier Lens
```python
import scipy.fft              # Core FFT
import numpy.fft              # Alternative FFT
from astropy.timeseries import LombScargle  # Irregular sampling

# Optional speedup:
import pyfftw                # FFTW3 wrapper
import cupy.fft              # GPU FFT
```

**Why not MATLAB Signal Processing Toolbox?**
- ❌ Costs $1000+/year
- ✅ SciPy is free and equally capable
- ✅ Better Python integration

---

### 📈 Wavelet Lens
```python
import pywt                  # PyWavelets (gold standard)
import scipy.signal          # cwt, morlet, ricker

# Optional speedup:
import kymatio              # GPU wavelets
```

**Why not MATLAB Wavelet Toolbox?**
- ❌ Costs $1000+/year
- ✅ PyWavelets is THE reference implementation
- ✅ More actively developed
- ✅ Better documentation

---

### ⚙️ Laplace Lens (Control Systems)
```python
import control               # python-control (Caltech)
import scipy.signal          # lti, TransferFunction, StateSpace

# Optional speedup:
import slycot               # FORTRAN SLICOT wrapper
```

**Why not MATLAB Control System Toolbox?**
- ❌ Costs $1000+/year (expensive!)
- ✅ python-control is feature-complete
- ✅ Developed by Richard Murray (Caltech)
- ✅ Used by NASA JPL, robotics labs
- ✅ Better for scripting/automation
- ✅ Same ecosystem as biology tools

**python-control provides:**
- Transfer functions, state-space models
- Bode, Nyquist, Nichols plots
- Root locus, pole/zero analysis
- LQR, LQG, pole placement
- System interconnections (feedback, series, parallel)
- Time responses (step, impulse, frequency)

---

### 📊 Z-Transform Lens (Digital Filters)
```python
import scipy.signal          # zpk, filter design, freqz
import filterpy              # Kalman filters
import numpy                 # Polynomial operations
```

**Why not MATLAB DSP Toolbox?**
- ❌ Costs $1000+/year
- ✅ SciPy signal processing is comprehensive
- ✅ filterpy is better for Kalman filters
- ✅ Free and open source

---

## License Summary

**All BSD-3 or MIT (most permissive):**

| License Type | Libraries | Commercial Use? | Modify? | Redistribute? |
|--------------|-----------|-----------------|---------|---------------|
| **BSD-3** | NumPy, SciPy, Astropy, python-control, slycot, PyFFTW, kymatio | ✅ Yes | ✅ Yes | ✅ Yes |
| **MIT** | PyWavelets, filterpy, CuPy | ✅ Yes | ✅ Yes | ✅ Yes |
| **PSF** | matplotlib | ✅ Yes | ✅ Yes | ✅ Yes |

**What this means:**
- ✅ Can use in commercial products (no royalties)
- ✅ Can modify and keep changes private
- ✅ Can bundle with proprietary software
- ✅ No viral licensing (not GPL/AGPL)
- ✅ No attribution required in binaries (but appreciated!)

## Installation

### Basic Setup (All Lenses)
```bash
# Create virtual environment
python3 -m venv bioxen-env
source bioxen-env/bin/activate

# Install core dependencies
pip install numpy scipy pywt astropy control filterpy matplotlib

# Verify installation
python -c "import numpy, scipy, pywt, astropy, control, filterpy; print('✅ All libraries installed!')"
```

### With Performance Optimizations
```bash
# Add optional speedups
pip install slycot      # Faster control systems (FORTRAN)
pip install pyfftw      # Faster FFT
pip install cupy-cuda12x  # GPU acceleration (NVIDIA only)
pip install kymatio     # GPU wavelets (requires PyTorch)
```

### Docker Deployment
```bash
# Dockerfile
FROM python:3.11-slim
RUN pip install numpy scipy pywt astropy control filterpy matplotlib
COPY . /app
WORKDIR /app
CMD ["python", "server.py"]

# Build and run
docker build -t bioxen-server .
docker run -p 8000:8000 bioxen-server
```

## Comparison with MATLAB

| Feature | MATLAB Ecosystem | BioXen Open Source | Winner |
|---------|------------------|-------------------|--------|
| **Cost** | $1000-5000+/year | FREE | ✅ BioXen |
| **License** | Proprietary | BSD/MIT | ✅ BioXen |
| **FFT** | ✅ Signal Processing Toolbox | ✅ scipy.fft | ✅ Tie |
| **Wavelets** | ✅ Wavelet Toolbox | ✅ PyWavelets | ✅ BioXen (better docs) |
| **Control** | ✅ Control Toolbox | ✅ python-control | ✅ BioXen (free + scriptable) |
| **Filtering** | ✅ DSP Toolbox | ✅ scipy.signal + filterpy | ✅ Tie |
| **Deployment** | ❌ License servers | ✅ pip/Docker | ✅ BioXen |
| **Automation** | ⚠️ MATLAB engine | ✅ Native Python | ✅ BioXen |
| **Biology Integration** | ❌ Difficult | ✅ Native (BioPython, etc.) | ✅ BioXen |
| **GPU Support** | ⚠️ Parallel Toolbox ($$$) | ✅ CuPy (free) | ✅ BioXen |
| **Students** | ⚠️ Campus license only | ✅ Always free | ✅ BioXen |

**MATLAB is better for:**
- Legacy code (if you already have MATLAB scripts)
- Simulink (graphical block diagrams)
- Industries with MATLAB standards (aerospace, automotive)

**BioXen/Python is better for:**
- ✅ Biology research (no budget constraints)
- ✅ Automation and scripting
- ✅ Integration with modern ML tools (PyTorch, TensorFlow)
- ✅ Deployment (Docker, cloud, edge devices)
- ✅ Open science (reproducibility)

## Verification

```python
# Test all lenses are working
import numpy as np
import scipy.signal
import pywt
from astropy.timeseries import LombScargle
import control
import filterpy

print("✅ All lens libraries installed successfully!")

# Fourier Lens
fft = scipy.fft.fft([1, 2, 3, 4])
print(f"✅ Fourier: FFT works")

# Wavelet Lens
coeffs = pywt.dwt([1, 2, 3, 4], 'haar')
print(f"✅ Wavelet: DWT works")

# Laplace Lens
sys = control.TransferFunction([1], [1, 2, 1])
print(f"✅ Laplace: Transfer function works")

# Z-Transform Lens
b, a = scipy.signal.butter(4, 0.5)
print(f"✅ Z-Transform: Filter design works")

print("\n🎉 BioXen is ready to use!")
```

## Support and Documentation

- **python-control**: https://python-control.readthedocs.io
- **PyWavelets**: https://pywavelets.readthedocs.io
- **SciPy**: https://docs.scipy.org
- **Astropy**: https://docs.astropy.org
- **filterpy**: https://filterpy.readthedocs.io

## Contributing

All libraries welcome contributions:
- python-control: https://github.com/python-control/python-control
- PyWavelets: https://github.com/PyWavelets/pywt
- SciPy: https://github.com/scipy/scipy

## Summary

**BioXen uses 100% open source software:**
- ✅ No proprietary dependencies
- ✅ No license costs ($0 forever)
- ✅ No restrictions on use, modification, or distribution
- ✅ Permissive licenses (BSD/MIT)
- ✅ Active communities and excellent documentation

**For the Laplace lens specifically:**
- ✅ python-control is a complete MATLAB replacement
- ✅ Developed at Caltech, industry-grade
- ✅ Used by NASA JPL and robotics labs
- ✅ Better for biology research (Python ecosystem)

**Total cost: $0** 💰✅
