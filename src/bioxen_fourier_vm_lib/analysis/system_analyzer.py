"""
BioXen System Analyzer - MVP Implementation
Four-lens analysis for biological VM time series

Version 2.1: Corrected for actual BioXen codebase structure

This module implements sophisticated signal analysis using four complementary
mathematical "lenses" that each reveal different aspects of biological systems:

1. Fourier Lens (Lomb-Scargle): Detects periodic rhythms (circadian, ultradian)
2. Wavelet Lens: Localizes transient events in time-frequency domain
3. Laplace Lens: Assesses system stability and dynamics
4. Z-Transform Lens: Filters noise from discrete-time signals

Scientific Rationale:
    - Lomb-Scargle handles irregular biological sampling (mandatory for real data)
    - Wavelets essential for non-stationary signals (cell cycle, stress response)
    - Laplace reveals system stability (homeostasis vs chaos)
    - Z-Transform provides noise-robust measurements

Philosophy: "Stand on Giants' Shoulders"
    - Leverage mature libraries (scipy, astropy, PyWavelets)
    - Write minimal integration code (~450 lines vs 500,000+ in libraries)
    - Focus on biological interpretation, not reimplementation
"""

from scipy import signal
from scipy.fft import fft, fftfreq
from astropy.timeseries import LombScargle
import pywt
import numpy as np
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass


@dataclass
class FourierResult:
    """
    Frequency domain analysis results using Lomb-Scargle periodogram.
    
    Attributes:
        frequencies: Array of analyzed frequencies (Hz)
        power_spectrum: Power spectral density at each frequency
        dominant_frequency: Frequency with highest power (Hz)
        dominant_period: Period of dominant frequency (hours)
        significance: Statistical significance (1 - false alarm probability)
        harmonics: List of detected harmonic components (Phase 1)
        harmonic_power: Total power in all harmonics (Phase 1)
    
    Example:
        >>> result = analyzer.fourier_lens(atp_data, timestamps)
        >>> if 20 < result.dominant_period < 28:
        ...     print("Circadian rhythm detected!")
        >>> # Phase 1: Multi-harmonic detection
        >>> for h in result.harmonics:
        ...     print(f"Period: {h['period']:.1f}h, Power: {h['power']:.3f}")
    """
    frequencies: np.ndarray
    power_spectrum: np.ndarray
    dominant_frequency: float
    dominant_period: float
    significance: Optional[float] = None  # False alarm probability
    # Phase 1: Multi-harmonic detection
    harmonics: Optional[List[Dict[str, float]]] = None
    harmonic_power: Optional[float] = None


@dataclass
class WaveletResult:
    """
    Time-frequency analysis results using continuous wavelet transform.
    
    Attributes:
        scales: Wavelet scales used in analysis
        coefficients: Complex wavelet coefficients [scales x time]
        transient_events: List of detected transient events
        time_frequency_map: Absolute values of coefficients (power map)
        wavelet_used: Name of mother wavelet used (Phase 1)
        selection_score: Quality score for wavelet selection (Phase 1)
        alternative_wavelets: Other good wavelet options (Phase 1)
    
    Example:
        >>> result = analyzer.wavelet_lens(atp_data)
        >>> print(f"Detected {len(result.transient_events)} stress responses")
        >>> # Phase 1: Automatic wavelet selection
        >>> print(f"Optimal wavelet: {result.wavelet_used}")
        >>> print(f"Selection score: {result.selection_score:.3f}")
    """
    scales: np.ndarray
    coefficients: np.ndarray
    transient_events: List[Dict[str, Any]]
    time_frequency_map: np.ndarray
    # Phase 1: Automatic wavelet selection
    wavelet_used: Optional[str] = None
    selection_score: Optional[Dict[str, float]] = None
    alternative_wavelets: Optional[List[Tuple[str, Dict[str, float]]]] = None


@dataclass
class LaplaceResult:
    """
    System stability analysis results based on pole locations.
    
    Attributes:
        poles: Complex pole locations in s-plane
        stability: Classification ('stable', 'oscillatory', 'unstable')
        natural_frequency: System's natural oscillation frequency (Hz)
        damping_ratio: Damping coefficient (0=undamped, >1=overdamped)
    
    Example:
        >>> result = analyzer.laplace_lens(atp_data)
        >>> if result.stability == 'unstable':
        ...     print("WARNING: System homeostasis compromised!")
    """
    poles: np.ndarray
    stability: str  # 'stable', 'oscillatory', 'unstable'
    natural_frequency: float
    damping_ratio: float


@dataclass
class ZTransformResult:
    """
    Digital filtering results using Butterworth filter.
    
    Attributes:
        filtered_signal: Noise-reduced signal
        noise_reduction_percent: Percentage of noise removed
        cutoff_frequency: Filter cutoff frequency (Hz)
    
    Example:
        >>> result = analyzer.z_transform_lens(noisy_signal)
        >>> print(f"Noise reduced by {result.noise_reduction_percent:.1f}%")
    """
    filtered_signal: np.ndarray
    noise_reduction_percent: float
    cutoff_frequency: float


class SystemAnalyzer:
    """
    MVP Four-Lens System Analyzer for biological time series.
    
    This analyzer applies four complementary mathematical transforms to reveal
    different aspects of biological system dynamics:
    
    Lenses:
        1. Fourier (Lomb-Scargle): Detect rhythms and periodicity
        2. Wavelet: Localize transient events in time-frequency
        3. Laplace: Assess system stability and transfer functions
        4. Z-Transform: Filter noise from discrete-time signals
    
    Typical Workflow:
        1. Initialize with sampling rate matching your data collection
        2. Validate signal quality with validate_signal()
        3. Apply individual lenses or all at once
        4. Interpret results in biological context
    
    Example:
        >>> # Initialize for PerformanceProfiler (5-second intervals)
        >>> analyzer = SystemAnalyzer(sampling_rate=0.2)
        >>> 
        >>> # Validate data quality
        >>> validation = analyzer.validate_signal(atp_data)
        >>> if not validation['all_passed']:
        ...     print("Signal quality issues:", validation)
        >>> 
        >>> # Analyze ATP levels
        >>> fourier = analyzer.fourier_lens(atp_data, timestamps)
        >>> print(f"Circadian period: {fourier.dominant_period:.1f} hours")
        >>> 
        >>> # Detect stress response transients
        >>> wavelet = analyzer.wavelet_lens(atp_data)
        >>> print(f"Transient events: {len(wavelet.transient_events)}")
        >>> 
        >>> # Check system stability
        >>> laplace = analyzer.laplace_lens(atp_data)
        >>> print(f"System stability: {laplace.stability}")
        >>> 
        >>> # Get noise-reduced signal
        >>> ztransform = analyzer.z_transform_lens(atp_data)
        >>> print(f"Noise reduced by: {ztransform.noise_reduction_percent:.1f}%")
    
    Args:
        sampling_rate: Samples per second (default: 0.2 = 5-second intervals)
                      For PerformanceProfiler: 0.2 Hz (monitoring_interval=5.0)
    """
    
    def __init__(self, sampling_rate: float = 0.2):
        """
        Initialize analyzer.
        
        Args:
            sampling_rate: Samples per second (default: 0.2 = 5-second intervals)
                          For PerformanceProfiler: 0.2 Hz (monitoring_interval=5.0)
                          For hourly data: 1/3600 Hz
                          For daily data: 1/86400 Hz
        """
        self.sampling_rate = sampling_rate
        self.nyquist_freq = sampling_rate / 2.0
        
    # ========== LENS 1: FOURIER (LOMB-SCARGLE) ==========
    
    def fourier_lens(
        self, 
        time_series: np.ndarray, 
        timestamps: Optional[np.ndarray] = None
    ) -> FourierResult:
        """
        Lens 1: Frequency-domain analysis with Lomb-Scargle periodogram.
        
        Uses Lomb-Scargle (biology gold standard) for irregular sampling,
        handles both uniform and irregular data without interpolation bias.
        
        Scientific Note:
            Lomb-Scargle is MANDATORY for real biological data due to:
            - Irregular sampling (missed measurements, system downtime)
            - Missing data points (sensor failures, maintenance windows)
            - No interpolation bias (preserves signal integrity)
            - Robust to outliers and gaps
        
        Biological Applications:
            - Circadian rhythm detection (~24h periods)
            - Ultradian rhythms (<24h: metabolism, secretion)
            - Cell cycle periodicity (varies by organism)
            - Seasonal variations in metabolic state
        
        Args:
            time_series: Signal values (e.g., ATP levels from profiler)
            timestamps: Time points (seconds). If None, assumes uniform sampling
        
        Returns:
            FourierResult with frequency spectrum and dominant period
        
        Example:
            >>> # Detect circadian rhythm in ATP levels
            >>> result = analyzer.fourier_lens(atp_levels, timestamps)
            >>> if 20 < result.dominant_period < 28:
            ...     print(f"Circadian rhythm: {result.dominant_period:.1f}h")
            ...     print(f"Confidence: {result.significance*100:.1f}%")
        """
        # Ensure time_series is numpy array
        time_series = np.asarray(time_series)
        
        # MVP: Use Lomb-Scargle for all cases (handles both uniform and irregular)
        if timestamps is None:
            timestamps = np.arange(len(time_series)) / self.sampling_rate
        else:
            timestamps = np.asarray(timestamps)
        
        # Lomb-Scargle periodogram (handles irregular sampling)
        ls = LombScargle(timestamps, time_series, fit_mean=True)
        
        # Auto-detect frequency range suitable for biological data
        # For biological data: look for periods from 10 seconds to ~100 hours
        # Minimum frequency = 1/(100 hours) = 2.78e-6 Hz
        # Maximum frequency = Nyquist frequency
        frequency, power = ls.autopower(
            minimum_frequency=1.0/(100*3600),  # Max period: 100 hours
            maximum_frequency=self.nyquist_freq,
            samples_per_peak=10  # Good frequency resolution
        )
        
        # Find dominant frequency
        peak_idx = np.argmax(power)
        dominant_freq = frequency[peak_idx]
        dominant_period = 1.0 / dominant_freq if dominant_freq > 0 else float('inf')
        
        # Statistical significance (False Alarm Probability)
        # Values close to 1.0 indicate high confidence in periodicity
        false_alarm_prob = ls.false_alarm_probability(power.max())
        significance = 1.0 - false_alarm_prob
        
        return FourierResult(
            frequencies=frequency,
            power_spectrum=power,
            dominant_frequency=dominant_freq,
            dominant_period=dominant_period / 3600.0,  # Convert seconds to hours
            significance=significance
        )
    
    # ========== LENS 2: WAVELET ==========
    
    def wavelet_lens(
        self,
        time_series: np.ndarray,
        wavelet_name: str = 'morl'
    ) -> WaveletResult:
        """
        Lens 2: Time-frequency analysis for non-stationary signals.
        
        ESSENTIAL for biological signals because:
            - Cell cycle transitions (G1→S→G2→M) are non-stationary
            - Transient stress responses (heat shock, oxidative stress)
            - Phase-specific metabolic changes
            - Resource allocation shifts during VM operations
        
        Unlike Fourier (assumes stationarity), wavelets localize events in BOTH
        time and frequency, making them ideal for detecting:
            - When did the stress response occur?
            - How long did the metabolic shift last?
            - Which frequency components changed during phase transition?
        
        Biological Applications:
            - Detect ATP spikes during resource reallocation
            - Identify ribosome utilization surges
            - Localize cell cycle phase boundaries
            - Find transient metabolic adaptations
        
        Args:
            time_series: Signal values
            wavelet_name: Mother wavelet ('morl', 'db4', 'mexh', 'cgau5')
                         'morl' (Morlet) is good default for biological signals
        
        Returns:
            WaveletResult with time-frequency map and detected transients
        
        Example:
            >>> # Detect stress responses in ATP levels
            >>> result = analyzer.wavelet_lens(atp_levels)
            >>> for event in result.transient_events:
            ...     time_point = event['time_index'] * 5  # 5-second intervals
            ...     print(f"Stress event at {time_point}s")
        """
        # Ensure time_series is numpy array
        time_series = np.asarray(time_series)
        
        # Continuous Wavelet Transform (CWT)
        # Scales: smaller scales detect high-frequency (short-duration) events
        #         larger scales detect low-frequency (long-duration) events
        max_scale = min(128, len(time_series)//4)
        scales = np.arange(1, max_scale)
        
        # Use PyWavelets cwt for MVP
        # Returns coefficients matrix [scales x time]
        coefficients, frequencies = pywt.cwt(
            time_series, 
            scales, 
            wavelet_name,
            sampling_period=1.0/self.sampling_rate
        )
        
        # Detect transient events (simple threshold for MVP)
        transients = self._detect_transients_mvp(coefficients)
        
        return WaveletResult(
            scales=scales,
            coefficients=coefficients,
            transient_events=transients,
            time_frequency_map=np.abs(coefficients)  # Power map
        )
    
    def _detect_transients_mvp(self, cwt_matrix: np.ndarray) -> List[Dict[str, Any]]:
        """
        MVP: Simple transient detection via threshold.
        
        Production version would use:
            - Ridge detection algorithms
            - Scale-dependent thresholds
            - Multi-scale integration
            - Statistical significance testing
        
        Args:
            cwt_matrix: Wavelet coefficients [scales x time]
        
        Returns:
            List of transient event dictionaries
        """
        # Calculate total wavelet power across scales at each time point
        power = np.sum(np.abs(cwt_matrix)**2, axis=0)
        
        # Threshold: mean + 2 standard deviations
        # This catches events that are significantly different from baseline
        threshold = np.mean(power) + 2 * np.std(power)
        
        # Find time points exceeding threshold
        transient_indices = np.where(power > threshold)[0]
        
        # Group nearby transients (within 5 samples)
        events = []
        if len(transient_indices) > 0:
            # Split into groups when gap > 5 samples
            groups = np.split(
                transient_indices, 
                np.where(np.diff(transient_indices) > 5)[0] + 1
            )
            
            for group in groups:
                if len(group) > 0:
                    events.append({
                        'time_index': int(np.mean(group)),  # Center of event
                        'intensity': float(power[group].max()),  # Peak intensity
                        'duration_samples': len(group)  # Event duration
                    })
        
        return events
    
    # ========== LENS 3: LAPLACE (STABILITY) ==========
    
    def laplace_lens(self, time_series: np.ndarray) -> LaplaceResult:
        """
        Lens 3: System stability and transfer function analysis.
        
        Answers the critical question: "Is this biological system stable?"
        
        Pole Locations and Biological Meaning:
            - Stable: Poles in left half-plane (damped oscillations)
                     → System returns to equilibrium after perturbation
                     → Homeostasis is maintained
                     
            - Oscillatory: Poles on imaginary axis (sustained rhythms)
                          → System exhibits limit cycles
                          → Natural biological rhythms (circadian, ultradian)
                          
            - Unstable: Poles in right half-plane (exponential growth)
                       → System diverges from equilibrium
                       → Resource exhaustion, runaway processes
        
        Biological Applications:
            - ATP homeostasis stability assessment
            - Ribosome allocation feedback loop characterization
            - Early warning for system instability
            - Metabolic pathway regulation analysis
        
        Args:
            time_series: Signal values
        
        Returns:
            LaplaceResult with poles and stability classification
        
        Example:
            >>> result = analyzer.laplace_lens(atp_levels)
            >>> if result.stability == 'unstable':
            ...     print("WARNING: ATP homeostasis compromised!")
            >>> elif result.stability == 'oscillatory':
            ...     print(f"Natural rhythm: {1/result.natural_frequency:.1f}s period")
        """
        # Ensure time_series is numpy array
        time_series = np.asarray(time_series)
        
        # Estimate frequency response using Welch's method
        # This gives us the power spectral density (PSD)
        nperseg = min(256, len(time_series)//4)
        if nperseg < 4:
            nperseg = len(time_series)
            
        freqs, psd = signal.welch(
            time_series, 
            fs=self.sampling_rate,
            nperseg=nperseg
        )
        
        # MVP: Fit 2nd-order system to frequency response
        # 2nd-order systems are common in biology (feedback loops, oscillators)
        # Transfer function: H(s) = ωn² / (s² + 2ζωn·s + ωn²)
        
        # Find dominant frequency (skip DC component)
        if len(psd) > 1:
            peak_idx = np.argmax(psd[1:]) + 1  # Skip DC
        else:
            peak_idx = 0
            
        omega_n = 2 * np.pi * freqs[peak_idx]  # Natural frequency (rad/s)
        
        # Estimate damping ratio from peak sharpness
        # Q-factor = peak_power / noise_floor ≈ 1/(2ζ)
        peak_power = psd[peak_idx]
        noise_floor = np.median(psd)
        
        if noise_floor > 0:
            q_factor = peak_power / noise_floor
            zeta = 1.0 / (2.0 * q_factor) if q_factor > 0 else 0.5
        else:
            zeta = 0.5  # Default moderate damping
        
        # Clamp damping ratio to reasonable range
        zeta = np.clip(zeta, 0.01, 2.0)
        
        # Calculate poles for 2nd-order system
        # Poles: -ζωn ± jωn√(1-ζ²)  for underdamped (ζ < 1)
        # Poles: -ζωn ± ωn√(ζ²-1)   for overdamped (ζ > 1)
        
        if zeta < 1.0:
            # Underdamped: complex conjugate poles
            real_part = -zeta * omega_n
            imag_part = omega_n * np.sqrt(1 - zeta**2)
            poles = np.array([
                complex(real_part, imag_part),
                complex(real_part, -imag_part)
            ])
            
            # Classify stability based on pole locations
            if real_part < -0.01:  # Tolerance for numerical stability
                stability = 'stable'
            elif abs(real_part) <= 0.01:
                stability = 'oscillatory'
            else:
                stability = 'unstable'
        else:
            # Overdamped: real poles
            poles = np.array([
                -zeta * omega_n + omega_n * np.sqrt(zeta**2 - 1),
                -zeta * omega_n - omega_n * np.sqrt(zeta**2 - 1)
            ])
            stability = 'stable'
        
        return LaplaceResult(
            poles=poles,
            stability=stability,
            natural_frequency=omega_n / (2 * np.pi),  # Convert rad/s to Hz
            damping_ratio=zeta
        )
    
    # ========== LENS 4: Z-TRANSFORM (FILTERING) ==========
    
    def z_transform_lens(
        self,
        time_series: np.ndarray,
        cutoff_freq: Optional[float] = None,
        filter_order: int = 4
    ) -> ZTransformResult:
        """
        Lens 4: Digital filtering for noise reduction.
        
        Uses discrete-time Z-transform based Butterworth filter to remove
        measurement noise while preserving biological signal features.
        
        Why Digital Filtering for Biological Data?
            - Biosensors are inherently noisy (molecular fluctuations)
            - Sampling process introduces quantization noise
            - Thermal noise from electronic measurement systems
            - Environmental perturbations (temperature, vibration)
        
        Butterworth Filter Properties:
            - Maximally flat passband (no ripples in signal of interest)
            - Smooth frequency response
            - Good phase characteristics (minimal distortion)
            - Stable digital implementation using SOS format
        
        Biological Applications:
            - Clean noisy ATP measurements
            - Smooth ribosome utilization curves
            - Remove high-frequency measurement artifacts
            - Prepare data for downstream analysis
        
        Args:
            time_series: Signal values
            cutoff_freq: Filter cutoff (Hz). If None, auto-select as Nyquist/4
            filter_order: Filter order (default: 4, higher = steeper rolloff)
        
        Returns:
            ZTransformResult with filtered signal and noise reduction metrics
        
        Example:
            >>> # Remove noise from ATP measurements
            >>> result = analyzer.z_transform_lens(noisy_atp)
            >>> clean_atp = result.filtered_signal
            >>> print(f"Noise reduced by {result.noise_reduction_percent:.1f}%")
        """
        # Ensure time_series is numpy array
        time_series = np.asarray(time_series)
        
        # Auto-select cutoff frequency if not provided
        if cutoff_freq is None:
            # Default: 1/4 of Nyquist frequency
            # This removes high-frequency noise while preserving biological signals
            cutoff_freq = self.nyquist_freq / 4.0
        
        # Ensure cutoff is below Nyquist
        cutoff_freq = min(cutoff_freq, self.nyquist_freq * 0.99)
        
        # Design Butterworth lowpass filter
        # Use SOS (Second-Order Sections) format for numerical stability
        sos = signal.butter(
            filter_order, 
            cutoff_freq, 
            btype='low',
            fs=self.sampling_rate, 
            output='sos'
        )
        
        # Apply filter using forward-backward filtering (zero phase distortion)
        # sosfiltfilt applies filter twice (forward + backward) = zero phase shift
        filtered = signal.sosfiltfilt(sos, time_series)
        
        # Calculate noise reduction
        # Use median filter to estimate noise floor
        # Compare variance of high-frequency components before/after filtering
        noise_power_original = np.var(time_series - signal.medfilt(time_series, kernel_size=3))
        noise_power_filtered = np.var(filtered - signal.medfilt(filtered, kernel_size=3))
        
        if noise_power_original > 0:
            noise_reduction = (1.0 - noise_power_filtered/noise_power_original) * 100
        else:
            noise_reduction = 0.0
            
        # Clamp to [0, 100] range
        noise_reduction = max(0, min(100, noise_reduction))
        
        return ZTransformResult(
            filtered_signal=filtered,
            noise_reduction_percent=noise_reduction,
            cutoff_frequency=cutoff_freq
        )
    
    # ========== VALIDATION LAYER ==========
    
    def validate_signal(self, time_series: np.ndarray) -> Dict[str, Any]:
        """
        Pre-flight validation checks (MANDATORY for scientific rigor).
        
        Ensures signal quality before applying analysis lenses. Poor quality
        signals lead to spurious results and incorrect biological interpretations.
        
        Validation Checks:
            - Sufficient length: At least 50 samples for meaningful statistics
            - Not constant: Signal has variation (std > 1e-10)
            - No NaNs: All values are finite numbers
            - No infinities: All values in valid range
            - Sufficient variance: Signal is not near-constant noise
        
        Args:
            time_series: Signal values to validate
        
        Returns:
            Dictionary of validation results with 'all_passed' boolean
        
        Example:
            >>> validation = analyzer.validate_signal(atp_data)
            >>> if not validation['all_passed']:
            ...     print("Signal quality issues:")
            ...     for check, passed in validation.items():
            ...         if not passed:
            ...             print(f"  - {check}")
            ...     return
        """
        time_series = np.asarray(time_series)
        
        checks = {
            'sufficient_length': len(time_series) >= 50,
            'not_constant': np.std(time_series) > 1e-10,
            'no_nans': not np.any(np.isnan(time_series)),
            'no_infs': not np.any(np.isinf(time_series)),
            'sufficient_variance': np.var(time_series) > 1e-8,
        }
        
        # Overall pass/fail
        checks['all_passed'] = all(checks.values())
        
        return checks
