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
        mra_components: Multi-resolution decomposition components (Phase 1.5)
        denoised_signal: Signal with noise removed via MRA (Phase 1.5)
        reconstruction_error: Error between original and reconstructed (Phase 1.5)
    
    Example:
        >>> result = analyzer.wavelet_lens(atp_data)
        >>> print(f"Detected {len(result.transient_events)} stress responses")
        >>> # Phase 1: Automatic wavelet selection
        >>> print(f"Optimal wavelet: {result.wavelet_used}")
        >>> print(f"Selection score: {result.selection_score:.3f}")
        >>> # Phase 1.5: Multi-resolution analysis
        >>> if result.mra_components:
        ...     print(f"Denoised signal available: {len(result.denoised_signal)} samples")
        ...     print(f"Reconstruction error: {result.reconstruction_error:.3f}")
    """
    scales: np.ndarray
    coefficients: np.ndarray
    transient_events: List[Dict[str, Any]]
    time_frequency_map: np.ndarray
    # Phase 1: Automatic wavelet selection
    wavelet_used: Optional[str] = None
    selection_score: Optional[Dict[str, float]] = None
    alternative_wavelets: Optional[List[Tuple[str, Dict[str, float]]]] = None
    # Phase 1.5: Multi-resolution analysis
    mra_components: Optional[Dict[str, np.ndarray]] = None
    denoised_signal: Optional[np.ndarray] = None
    reconstruction_error: Optional[float] = None


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
        
        # Phase 1: Storage for harmonic detection
        self._current_signal = None
        self._current_timestamps = None
        
    # ========== LENS 1: FOURIER (LOMB-SCARGLE) ==========
    
    def fourier_lens(
        self, 
        time_series: np.ndarray, 
        timestamps: Optional[np.ndarray] = None,
        detect_harmonics: bool = False,
        max_harmonics: int = 5
    ) -> FourierResult:
        """
        Lens 1: Frequency-domain analysis with Lomb-Scargle periodogram.
        
        Uses Lomb-Scargle (biology gold standard) for irregular sampling,
        handles both uniform and irregular data without interpolation bias.
        
        Phase 1 Enhancement: Multi-harmonic detection to find multiple periodic
        components (e.g., 24h circadian + 12h ultradian + 8h rhythms).
        
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
            detect_harmonics: Enable multi-harmonic detection (Phase 1)
            max_harmonics: Maximum number of harmonics to detect (Phase 1)
        
        Returns:
            FourierResult with frequency spectrum and dominant period
        
        Example:
            >>> # MVP: Detect circadian rhythm in ATP levels
            >>> result = analyzer.fourier_lens(atp_levels, timestamps)
            >>> if 20 < result.dominant_period < 28:
            ...     print(f"Circadian rhythm: {result.dominant_period:.1f}h")
            ...     print(f"Confidence: {result.significance*100:.1f}%")
            >>> 
            >>> # Phase 1: Detect multiple harmonics
            >>> result = analyzer.fourier_lens(atp_levels, timestamps, 
            ...                                detect_harmonics=True)
            >>> for h in result.harmonics:
            ...     print(f"Period: {h['period']:.1f}h, Amplitude: {h['amplitude']:.1f}")
        """
        # Ensure time_series is numpy array
        time_series = np.asarray(time_series)
        
        # MVP: Use Lomb-Scargle for all cases (handles both uniform and irregular)
        if timestamps is None:
            timestamps = np.arange(len(time_series)) / self.sampling_rate
        else:
            timestamps = np.asarray(timestamps)
        
        # Phase 1: Store for harmonic detection
        self._current_signal = time_series.copy()
        self._current_timestamps = timestamps.copy()
        
        # Lomb-Scargle periodogram (handles irregular sampling)
        ls = LombScargle(timestamps, time_series, fit_mean=True)
        
        # Calculate actual Nyquist frequency from timestamps
        # For irregular sampling, use median interval
        intervals = np.diff(timestamps)
        median_interval = np.median(intervals)
        actual_sampling_rate = 1.0 / median_interval
        actual_nyquist = actual_sampling_rate / 2.0
        
        # Auto-detect frequency range suitable for biological data
        # For biological data: look for periods from 10 seconds to ~100 hours
        # Minimum frequency = 1/(100 hours) = 2.78e-6 Hz
        # Maximum frequency = Nyquist frequency
        
        # Adaptive frequency resolution based on data duration
        # Longer signals need higher resolution for accurate period detection
        duration_hours = (timestamps[-1] - timestamps[0]) / 3600.0
        if duration_hours > 720:  # More than 30 days
            samples_per_peak = 50  # High resolution for long-term data
        elif duration_hours > 168:  # More than 7 days
            samples_per_peak = 30  # Medium-high resolution
        else:  # Short-term data (< 7 days)
            samples_per_peak = 10  # Standard resolution
        
        frequency, power = ls.autopower(
            minimum_frequency=1.0/(100*3600),  # Max period: 100 hours
            maximum_frequency=actual_nyquist,   # Use actual Nyquist from data
            samples_per_peak=samples_per_peak
        )
        
        # Find dominant frequency
        peak_idx = np.argmax(power)
        dominant_freq = frequency[peak_idx]
        dominant_period = 1.0 / dominant_freq if dominant_freq > 0 else float('inf')
        
        # Statistical significance (False Alarm Probability)
        # Values close to 1.0 indicate high confidence in periodicity
        false_alarm_prob = ls.false_alarm_probability(power.max())
        significance = 1.0 - false_alarm_prob
        
        # Phase 1: Multi-harmonic detection
        harmonics = None
        harmonic_power = None
        
        if detect_harmonics:
            harmonics = self._detect_harmonics(
                ls, frequency, power, max_harmonics
            )
            harmonic_power = sum(h['power'] for h in harmonics) if harmonics else 0.0
        
        return FourierResult(
            frequencies=frequency,
            power_spectrum=power,
            dominant_frequency=dominant_freq,
            dominant_period=dominant_period / 3600.0,  # Convert seconds to hours
            significance=significance,
            harmonics=harmonics,
            harmonic_power=harmonic_power
        )
    
    def _detect_harmonics(
        self,
        ls: LombScargle,
        frequency: np.ndarray,
        power: np.ndarray,
        max_harmonics: int
    ) -> List[Dict[str, float]]:
        """
        Phase 1: Detect multiple harmonic components by iterative peak detection.
        
        Algorithm:
        1. Find dominant peak → record as harmonic
        2. Fit sinusoid at that frequency
        3. Subtract fitted component from signal
        4. Analyze residual for next harmonic
        5. Repeat until power < threshold or max_harmonics reached
        
        This approach is known as "iterative sine fitting" or "sequential component
        extraction" and is widely used in biological rhythm analysis.
        
        Args:
            ls: LombScargle object
            frequency: Frequency array from periodogram
            power: Power array from periodogram
            max_harmonics: Maximum number of harmonics to detect
        
        Returns:
            List of dictionaries with harmonic information:
            - frequency: Harmonic frequency (Hz)
            - period: Harmonic period (hours)
            - power: Spectral power at this frequency
            - amplitude: Signal amplitude (same units as input)
            - phase: Phase offset (radians, 0 to 2π)
        """
        harmonics = []
        residual = self._current_signal.copy()
        timestamps = self._current_timestamps.copy()
        
        for i in range(max_harmonics):
            # Analyze current residual
            ls_residual = LombScargle(timestamps, residual, fit_mean=True)
            freq, pwr = ls_residual.autopower(
                minimum_frequency=1.0/(100*3600),
                maximum_frequency=self.nyquist_freq,
                samples_per_peak=50  # High frequency resolution
            )
            
            # Find peak
            peak_idx = np.argmax(pwr)
            peak_freq = freq[peak_idx]
            peak_power = pwr[peak_idx]
            
            # Stop if power too low (noise threshold)
            # Typical noise floor is around 0.1 for normalized power
            if peak_power < 0.1:
                break
            
            # Estimate amplitude and phase
            amplitude = self._estimate_amplitude(residual, timestamps, peak_freq)
            phase = self._estimate_phase(residual, timestamps, peak_freq)
            
            # Record harmonic
            harmonics.append({
                'frequency': peak_freq,
                'period': 1.0 / peak_freq / 3600,  # Convert to hours
                'power': peak_power,
                'amplitude': amplitude,
                'phase': phase
            })
            
            # Subtract this component from residual
            model = ls_residual.model(timestamps, peak_freq)
            residual = residual - model
        
        return harmonics
    
    def _estimate_phase(
        self,
        signal: np.ndarray,
        timestamps: np.ndarray,
        frequency: float
    ) -> float:
        """
        Phase 1: Estimate phase of sinusoidal component using least squares.
        
        Fits the model: signal = A*sin(2πft) + B*cos(2πft)
        Then calculates phase as: θ = arctan2(B, A)
        
        Phase Convention:
            0° (0 rad) = peak at t=0
            90° (π/2 rad) = peak at t=period/4
            180° (π rad) = trough at t=0
            270° (3π/2 rad) = trough at t=period/4
        
        Args:
            signal: Signal values
            timestamps: Time points (seconds)
            frequency: Frequency to analyze (Hz)
        
        Returns:
            Phase in radians [0, 2π)
        """
        # Build design matrix [sin(2πft), cos(2πft)]
        t = timestamps
        A_matrix = np.column_stack([
            np.sin(2 * np.pi * frequency * t),
            np.cos(2 * np.pi * frequency * t)
        ])
        
        # Least squares fit: signal = A*sin + B*cos
        coeffs, _, _, _ = np.linalg.lstsq(A_matrix, signal, rcond=None)
        
        # Calculate phase from coefficients
        # Phase is angle of complex number (coeffs[0] + i*coeffs[1])
        phase = np.arctan2(coeffs[1], coeffs[0])
        
        # Normalize to [0, 2π)
        return phase % (2 * np.pi)
    
    def _estimate_amplitude(
        self,
        signal: np.ndarray,
        timestamps: np.ndarray,
        frequency: float
    ) -> float:
        """
        Phase 1: Estimate amplitude of sinusoidal component.
        
        Uses least squares to fit: signal = A*sin(2πft) + B*cos(2πft)
        Then calculates amplitude as: R = √(A² + B²)
        
        This gives the peak-to-peak amplitude divided by 2 (i.e., the radius
        of the oscillation in signal units).
        
        Args:
            signal: Signal values
            timestamps: Time points (seconds)
            frequency: Frequency to analyze (Hz)
        
        Returns:
            Amplitude (same units as signal)
        """
        # Build design matrix
        t = timestamps
        A_matrix = np.column_stack([
            np.sin(2 * np.pi * frequency * t),
            np.cos(2 * np.pi * frequency * t)
        ])
        
        # Least squares fit
        coeffs, _, _, _ = np.linalg.lstsq(A_matrix, signal, rcond=None)
        
        # Amplitude from Pythagorean theorem
        # This is the radius of the circular motion in (A, B) space
        amplitude = np.sqrt(coeffs[0]**2 + coeffs[1]**2)
        
        return amplitude
    
    # ========== LENS 2: WAVELET ==========
    
    # Phase 1 Feature 2: Available wavelets for auto-selection
    # Phase 1 Feature 2: Continuous wavelets for CWT analysis
    # Note: Only continuous wavelets work with pywt.cwt()
    # Discrete wavelets (db*, sym*, coif*) require DWT (future enhancement)
    AVAILABLE_WAVELETS = {
        'morl': 'Morlet - Good for smooth oscillations',
        'mexh': 'Mexican Hat - Good for peak detection',
        'gaus4': 'Gaussian 4 - Sharp features, smooth signal',
        'gaus8': 'Gaussian 8 - Very smooth, good for gradual changes',
        'cgau4': 'Complex Gaussian 4 - Phase information preserved',
        'shan': 'Shannon - Good frequency localization',
        'fbsp': 'Frequency B-Spline - Flexible bandwidth'
    }
    
    def wavelet_lens(
        self,
        time_series: np.ndarray,
        wavelet_name: Optional[str] = None,
        auto_select: bool = False,
        enable_mra: bool = False,
        mra_levels: int = 5
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
            wavelet_name: Mother wavelet or None for auto-selection
                         Options: 'morl', 'mexh', 'gaus4', 'db4', 'db8', 'sym4', 'coif2'
                         Default: 'morl' (Morlet) if auto_select=False
            auto_select: Enable automatic optimal wavelet selection (Phase 1 Feature 2)
                        If True, ignores wavelet_name and picks best wavelet
            enable_mra: Enable Multi-Resolution Analysis (Phase 1.5 Feature)
                       If True, performs wavelet decomposition and denoising
            mra_levels: Number of decomposition levels for MRA (default: 5)
                       Higher levels = more detailed decomposition
        
        Returns:
            WaveletResult with time-frequency map and detected transients
            Phase 1: Also includes wavelet_used, selection_score, alternatives
            Phase 1.5: Also includes mra_components, denoised_signal if enable_mra=True
        
        Example:
            >>> # MVP mode: Manual wavelet selection
            >>> result = analyzer.wavelet_lens(atp_levels, wavelet_name='morl')
            >>> 
            >>> # Phase 1: Automatic wavelet selection
            >>> result = analyzer.wavelet_lens(atp_levels, auto_select=True)
            >>> print(f"Optimal wavelet: {result.wavelet_used}")
            >>> print(f"Score: {result.selection_score['total_score']:.3f}")
            >>> 
            >>> # Phase 1.5: Multi-resolution analysis with denoising
            >>> result = analyzer.wavelet_lens(atp_levels, auto_select=True, enable_mra=True)
            >>> print(f"Original noise level: {atp_levels.std():.2f}")
            >>> print(f"Denoised noise level: {result.denoised_signal.std():.2f}")
            >>> print(f"Reconstruction error: {result.reconstruction_error:.4f}")
            >>> 
            >>> # See decomposition components
            >>> print(f"MRA components: {list(result.mra_components.keys())}")
            >>> # ['approximation', 'detail_1', 'detail_2', 'detail_3', 'detail_4', 'detail_5']
        """
        # Ensure time_series is numpy array
        time_series = np.asarray(time_series)
        
        # Phase 1 Feature 2: Automatic wavelet selection
        selection_score = None
        alternative_wavelets = None
        
        if auto_select:
            # Auto-select optimal wavelet
            wavelet_name, selection_score, alternative_wavelets = \
                self._select_optimal_wavelet(time_series)
        elif wavelet_name is None:
            # Default to Morlet if not specified
            wavelet_name = 'morl'
        
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
        
        # Phase 1.5: Multi-Resolution Analysis (MRA)
        mra_components = None
        denoised_signal = None
        reconstruction_error = None
        
        if enable_mra:
            mra_components, denoised_signal, reconstruction_error = \
                self._perform_multi_resolution_analysis(
                    time_series, wavelet_name, mra_levels
                )
        
        return WaveletResult(
            scales=scales,
            coefficients=coefficients,
            transient_events=transients,
            time_frequency_map=np.abs(coefficients),  # Power map
            # Phase 1 Feature 2: Wavelet selection info
            wavelet_used=wavelet_name,
            selection_score=selection_score,
            alternative_wavelets=alternative_wavelets,
            # Phase 1.5: Multi-resolution analysis
            mra_components=mra_components,
            denoised_signal=denoised_signal,
            reconstruction_error=reconstruction_error
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
    
    def _select_optimal_wavelet(
        self,
        time_series: np.ndarray
    ) -> Tuple[str, Dict[str, float], List[Tuple[str, Dict[str, float]]]]:
        """
        Phase 1 Feature 2: Automatically select optimal mother wavelet for signal.
        
        Selection Strategy:
        Tests all available wavelets and scores each based on 4 criteria:
        1. Energy Concentration (30%): How focused is the signal energy?
        2. Time Localization (25%): Can we pinpoint events precisely?
        3. Frequency Localization (25%): Can we identify specific frequencies?
        4. Edge Quality (20%): How clean are the boundaries?
        
        Higher scores = better wavelet for this signal.
        
        Biological Intuition:
        - Smooth oscillations (circadian) → Morlet, Mexican Hat
        - Sharp spikes (stress) → Daubechies, Haar
        - Complex mixed signals → Symlets, Coiflets
        
        Args:
            time_series: Signal to analyze
        
        Returns:
            Tuple of (best_wavelet_name, selection_scores, alternatives_list)
            - best_wavelet_name: Name of optimal wavelet
            - selection_scores: Dict with all metric scores
            - alternatives_list: List of (name, scores) for other wavelets, sorted
        
        Example:
            >>> name, scores, alts = self._select_optimal_wavelet(atp_signal)
            >>> print(f"Best: {name} (score: {scores['total_score']:.3f})")
            >>> print(f"Energy: {scores['energy_concentration']:.3f}")
        """
        scores_all = {}
        max_scale = min(128, len(time_series)//4)
        scales = np.arange(1, max_scale)
        
        # Test each available wavelet
        for wavelet_name in self.AVAILABLE_WAVELETS.keys():
            try:
                # Perform CWT
                coeffs, _ = pywt.cwt(
                    time_series, scales, wavelet_name,
                    sampling_period=1.0/self.sampling_rate
                )
                
                # Calculate selection metrics
                energy_conc = self._calculate_energy_concentration(coeffs)
                time_loc = self._calculate_time_localization(coeffs)
                freq_loc = self._calculate_frequency_localization(coeffs)
                edge_qual = self._calculate_edge_quality(coeffs)
                
                # Weighted composite score
                total = (0.30 * energy_conc +
                        0.25 * time_loc +
                        0.25 * freq_loc +
                        0.20 * edge_qual)
                
                scores_all[wavelet_name] = {
                    'total_score': total,
                    'energy_concentration': energy_conc,
                    'time_localization': time_loc,
                    'frequency_localization': freq_loc,
                    'edge_quality': edge_qual
                }
                
            except Exception:
                # Some wavelets may fail for certain signals
                # Give them a very low score
                scores_all[wavelet_name] = {
                    'total_score': 0.0,
                    'energy_concentration': 0.0,
                    'time_localization': 0.0,
                    'frequency_localization': 0.0,
                    'edge_quality': 0.0
                }
        
        # Find best wavelet
        best_wavelet = max(scores_all.items(), key=lambda x: x[1]['total_score'])
        best_name = best_wavelet[0]
        best_scores = best_wavelet[1]
        
        # Sort alternatives by score
        alternatives = sorted(
            scores_all.items(),
            key=lambda x: x[1]['total_score'],
            reverse=True
        )
        
        return best_name, best_scores, alternatives
    
    def _calculate_energy_concentration(self, coeffs: np.ndarray) -> float:
        """
        Calculate how concentrated the signal energy is in wavelet domain.
        
        Higher concentration = signal has well-defined features
        Lower concentration = signal is noise-like or diffuse
        
        Uses Gini coefficient: measures inequality in energy distribution.
        Score of 1.0 = perfect concentration, 0.0 = uniform distribution.
        
        Args:
            coeffs: Wavelet coefficients [scales x time]
        
        Returns:
            Energy concentration score [0, 1]
        """
        # Calculate power (energy density)
        power = np.abs(coeffs)**2
        power_flat = power.flatten()
        power_flat = np.sort(power_flat)
        
        # Gini coefficient (adapted for our use)
        n = len(power_flat)
        if n == 0 or power_flat.sum() == 0:
            return 0.0
        
        cumsum = np.cumsum(power_flat)
        gini = (2 * np.sum((np.arange(1, n+1) * power_flat))) / (n * cumsum[-1]) - (n + 1) / n
        
        # Normalize to [0, 1] where 1 is best
        return max(0.0, min(1.0, gini))
    
    def _calculate_time_localization(self, coeffs: np.ndarray) -> float:
        """
        Calculate how well events are localized in time.
        
        Good time localization = sharp, well-defined events
        Poor time localization = smeared, unclear timing
        
        Measures the sharpness of peaks in time domain by looking at
        the concentration of power at specific time points.
        
        Args:
            coeffs: Wavelet coefficients [scales x time]
        
        Returns:
            Time localization score [0, 1]
        """
        # Sum power across scales for each time point
        time_power = np.sum(np.abs(coeffs)**2, axis=0)
        
        if time_power.sum() == 0:
            return 0.0
        
        # Normalize
        time_power = time_power / time_power.sum()
        
        # Calculate entropy (lower entropy = better localization)
        # Remove zeros to avoid log(0)
        time_power = time_power[time_power > 0]
        entropy = -np.sum(time_power * np.log2(time_power))
        
        # Normalize by maximum possible entropy
        max_entropy = np.log2(len(time_power)) if len(time_power) > 1 else 1.0
        normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0.0
        
        # Convert to score (lower entropy = higher score)
        return 1.0 - normalized_entropy
    
    def _calculate_frequency_localization(self, coeffs: np.ndarray) -> float:
        """
        Calculate how well frequency components are separated.
        
        Good frequency localization = distinct frequency bands
        Poor frequency localization = blurred frequency content
        
        Measures the concentration of power at specific scales (frequencies).
        
        Args:
            coeffs: Wavelet coefficients [scales x time]
        
        Returns:
            Frequency localization score [0, 1]
        """
        # Sum power across time for each scale
        scale_power = np.sum(np.abs(coeffs)**2, axis=1)
        
        if scale_power.sum() == 0:
            return 0.0
        
        # Normalize
        scale_power = scale_power / scale_power.sum()
        
        # Calculate entropy (lower entropy = better localization)
        scale_power = scale_power[scale_power > 0]
        entropy = -np.sum(scale_power * np.log2(scale_power))
        
        # Normalize by maximum possible entropy
        max_entropy = np.log2(len(scale_power)) if len(scale_power) > 1 else 1.0
        normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0.0
        
        # Convert to score
        return 1.0 - normalized_entropy
    
    def _calculate_edge_quality(self, coeffs: np.ndarray) -> float:
        """
        Calculate quality of signal at edges (boundary effects).
        
        Wavelet transforms can have artifacts at signal boundaries.
        Good edge quality = minimal boundary distortion
        Poor edge quality = strong edge artifacts
        
        Compares power at edges vs center of signal.
        
        Args:
            coeffs: Wavelet coefficients [scales x time]
        
        Returns:
            Edge quality score [0, 1]
        """
        power = np.abs(coeffs)**2
        
        # Define edge regions (10% on each side) and center (middle 80%)
        n_time = power.shape[1]
        edge_size = max(1, n_time // 10)
        
        left_edge = power[:, :edge_size]
        right_edge = power[:, -edge_size:]
        center = power[:, edge_size:-edge_size] if n_time > 2*edge_size else power
        
        # Calculate mean power in each region
        edge_power = (left_edge.mean() + right_edge.mean()) / 2
        center_power = center.mean()
        
        if center_power == 0:
            return 0.0
        
        # Ratio: lower edge/center ratio = better edge quality
        ratio = edge_power / center_power
        
        # Convert to score (lower ratio = higher score)
        # Use sigmoid-like function to map [0, ∞) → [1, 0]
        score = 1.0 / (1.0 + ratio)
        
        return score
    
    def _perform_multi_resolution_analysis(
        self,
        time_series: np.ndarray,
        wavelet: str,
        levels: int
    ) -> Tuple[Dict[str, np.ndarray], np.ndarray, float]:
        """
        Phase 1.5: Perform Multi-Resolution Analysis (MRA) using discrete wavelet transform.
        
        Decomposes signal into approximation (low-frequency trend) and details
        (high-frequency components) at multiple scales. Useful for:
        - Signal denoising (remove high-frequency noise)
        - Trend extraction (get smooth approximation)
        - Multi-scale feature detection
        - Signal compression
        
        Algorithm:
        1. Decompose signal using discrete wavelet transform (DWT)
        2. Extract approximation and detail coefficients at each level
        3. Reconstruct components separately
        4. Create denoised version by removing high-frequency details
        5. Calculate reconstruction error
        
        Args:
            time_series: Input signal
            wavelet: Wavelet name (must be orthogonal: 'db4', 'db8', 'sym4', 'coif2')
            levels: Number of decomposition levels
        
        Returns:
            Tuple of (components_dict, denoised_signal, reconstruction_error)
            - components_dict: Dict with 'approximation' and 'detail_X' arrays
            - denoised_signal: Signal with high-freq noise removed
            - reconstruction_error: RMS error between original and reconstructed
        
        Biological Applications:
            - Remove measurement noise from ATP readings
            - Separate circadian trend from ultradian oscillations
            - Extract slow metabolic changes from fast fluctuations
            - Identify multi-timescale biological processes
        
        Example:
            >>> components, denoised, error = analyzer._perform_multi_resolution_analysis(
            ...     atp_signal, 'db4', 5
            ... )
            >>> print(f"Components: {list(components.keys())}")
            >>> # ['approximation', 'detail_1', 'detail_2', 'detail_3', 'detail_4', 'detail_5']
            >>> print(f"Noise reduction: {error:.3f}")
        """
        # Ensure we have an orthogonal wavelet for DWT
        # CWT wavelets like 'morl' don't work with DWT
        if wavelet in ['morl', 'mexh', 'gaus4']:
            # Map to appropriate orthogonal wavelet
            wavelet_map = {
                'morl': 'db4',   # Smooth → Daubechies
                'mexh': 'sym4',  # Peak detection → Symlet
                'gaus4': 'coif2' # Smooth → Coiflet
            }
            wavelet = wavelet_map[wavelet]
        
        # Perform discrete wavelet decomposition
        coeffs = pywt.wavedec(time_series, wavelet, level=levels)
        
        # coeffs[0] = approximation (low-freq trend)
        # coeffs[1:] = details (high-freq components, finest to coarsest)
        
        # Reconstruct components at full length
        components = {}
        
        # Approximation (smoothed trend)
        approximation = pywt.upcoef('a', coeffs[0], wavelet, level=levels)
        # Trim to original length (DWT can extend signal slightly)
        approximation = approximation[:len(time_series)]
        components['approximation'] = approximation
        
        # Detail components (from highest to lowest frequency)
        detail_sum = np.zeros(len(time_series))
        for i, detail_coeffs in enumerate(coeffs[1:], 1):
            # Reconstruct this detail level
            detail = pywt.upcoef('d', detail_coeffs, wavelet, level=levels-i+1)
            detail = detail[:len(time_series)]
            components[f'detail_{i}'] = detail
            detail_sum += detail
        
        # Create denoised signal by removing highest frequency details
        # Strategy: Keep approximation + lower frequency details, remove noise
        # Rule of thumb: Remove top 1-2 detail levels (highest frequencies)
        levels_to_keep = max(1, levels - 2)  # Keep at least 1 detail level
        
        denoised = approximation.copy()
        for i in range(levels_to_keep):
            if f'detail_{levels-i}' in components:  # Start from coarsest details
                denoised += components[f'detail_{levels-i}']
        
        # Calculate reconstruction error
        full_reconstruction = approximation + detail_sum
        reconstruction_error = np.sqrt(np.mean((time_series - full_reconstruction)**2))
        
        return components, denoised, reconstruction_error
    
    def get_mra_summary(
        self,
        mra_components: Dict[str, np.ndarray]
    ) -> Dict[str, Dict[str, float]]:
        """
        Phase 1.5: Generate summary statistics for MRA components.
        
        Analyzes each component (approximation, details) to understand
        signal decomposition and identify dominant scales.
        
        Args:
            mra_components: Components from _perform_multi_resolution_analysis
        
        Returns:
            Dictionary with statistics for each component:
            - energy: Relative energy content (% of total)
            - rms: Root mean square amplitude
            - peak_to_peak: Max - min value
            - frequency_estimate: Approximate dominant frequency (Hz)
        
        Example:
            >>> summary = analyzer.get_mra_summary(components)
            >>> for name, stats in summary.items():
            ...     print(f"{name}: {stats['energy']:.1f}% energy, "
            ...           f"RMS={stats['rms']:.2f}")
        """
        summary = {}
        
        # Calculate total energy across all components
        total_energy = sum(np.sum(comp**2) for comp in mra_components.values())
        
        for name, component in mra_components.items():
            # Energy content
            energy = np.sum(component**2)
            energy_percent = (energy / total_energy * 100) if total_energy > 0 else 0.0
            
            # Amplitude statistics
            rms = np.sqrt(np.mean(component**2))
            peak_to_peak = np.max(component) - np.min(component)
            
            # Rough frequency estimate using zero crossings
            zero_crossings = np.where(np.diff(np.sign(component)))[0]
            if len(zero_crossings) > 1:
                # Estimate frequency from zero crossing rate
                avg_half_period = len(component) / len(zero_crossings)
                freq_estimate = self.sampling_rate / (2 * avg_half_period)
            else:
                freq_estimate = 0.0
            
            summary[name] = {
                'energy': energy_percent,
                'rms': rms,
                'peak_to_peak': peak_to_peak,
                'frequency_estimate': freq_estimate
            }
        
        return summary
    
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
