"""
BioXen Four-Lens Analysis System

This module provides sophisticated time-series analysis for biological VM signals
using four complementary mathematical "lenses":

1. Fourier (Lomb-Scargle) - Frequency domain analysis for rhythm detection
2. Wavelet - Time-frequency analysis for transient event detection
3. Laplace - System stability and transfer function analysis
4. Z-Transform - Digital filtering for noise reduction

Example:
    >>> from bioxen_fourier_vm_lib.analysis import SystemAnalyzer
    >>> analyzer = SystemAnalyzer(sampling_rate=0.2)  # 5-second intervals
    >>> fourier_result = analyzer.fourier_lens(signal_data, timestamps)
    >>> print(f"Dominant period: {fourier_result.dominant_period:.1f} hours")
"""

from .system_analyzer import (
    SystemAnalyzer,
    FourierResult,
    WaveletResult,
    LaplaceResult,
    ZTransformResult
)

__all__ = [
    'SystemAnalyzer',
    'FourierResult',
    'WaveletResult',
    'LaplaceResult',
    'ZTransformResult'
]

__version__ = '0.1.0-mvp'
