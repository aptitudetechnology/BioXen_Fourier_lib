# BioXen Four-Lens Analysis System: Phase 1 Implementation Plan

**Version:** 1.0  
**Date:** October 1, 2025  
**Status:** Ready to Implement  
**Branch:** dev  
**Prerequisites:** MVP Complete (89% - proceeding with known Fourier issue)

---

## 🎯 Phase 1 Objectives

**Goal:** Transform MVP into research-grade biological signal analysis system

**Focus Areas:**
1. **Advanced Lomb-Scargle Features** - Multi-harmonic detection, phase analysis
2. **Wavelet Mother Function Optimization** - Automatic wavelet selection
3. **Transfer Function System Identification** - ARMAX models, state-space
4. **Consensus Validation** - MetaCycle-style multi-method validation

**Timeline:** 3-4 weeks (120-160 hours)  
**Expected Outcome:** Publication-ready analysis capabilities

---

## 📋 Phase 1 Success Criteria

- [ ] Detect multiple harmonics in biological signals (fundamental + overtones)
- [ ] Automatic optimal wavelet selection for different signal types
- [ ] System identification with transfer functions (ARMAX, state-space)
- [ ] Consensus validation across multiple period detection methods
- [ ] 95%+ test coverage for all new features
- [ ] Research-grade documentation with biological examples
- [ ] Performance benchmarks (analyze 1000 genes < 60 seconds)
- [ ] Integration with existing MVP components (no breaking changes)

---

## 🔬 Feature 1: Advanced Lomb-Scargle Features

### Motivation
MVP Lomb-Scargle detects single dominant frequency. Real biological systems have:
- **Multiple harmonics** (24h, 12h, 8h circadian components)
- **Phase relationships** (when does peak occur?)
- **Statistical confidence** (beyond single false alarm probability)

### Implementation

#### 1.1 Multi-Harmonic Detection

**Add to SystemAnalyzer.fourier_lens():**

```python
def fourier_lens(
    self, 
    time_series: np.ndarray, 
    timestamps: Optional[np.ndarray] = None,
    detect_harmonics: bool = True,
    max_harmonics: int = 5
) -> FourierResult:
    """
    Enhanced Fourier analysis with multi-harmonic detection.
    
    New Parameters:
        detect_harmonics: Find multiple periodic components
        max_harmonics: Maximum number of harmonics to detect
    """
    # ... existing code ...
    
    # NEW: Multi-harmonic detection
    harmonics = []
    if detect_harmonics:
        harmonics = self._detect_harmonics(
            ls, frequency, power, max_harmonics
        )
    
    return FourierResult(
        # ... existing fields ...
        harmonics=harmonics,  # NEW
        harmonic_power=self._calculate_harmonic_power(harmonics),  # NEW
    )

def _detect_harmonics(
    self,
    ls: LombScargle,
    frequency: np.ndarray,
    power: np.ndarray,
    max_harmonics: int
) -> List[Dict[str, float]]:
    """
    Detect multiple harmonic components.
    
    Algorithm:
    1. Find peak → record as harmonic
    2. Subtract fitted sinusoid from signal
    3. Repeat on residual signal
    4. Stop when power < threshold or max_harmonics reached
    """
    harmonics = []
    residual = self.current_signal.copy()  # Store in fourier_lens
    
    for i in range(max_harmonics):
        # Find peak in current residual
        ls_residual = LombScargle(self.current_timestamps, residual)
        freq, pwr = ls_residual.autopower()
        
        peak_idx = np.argmax(pwr)
        peak_freq = freq[peak_idx]
        peak_power = pwr[peak_idx]
        
        # Stop if power too low
        if peak_power < 0.1:  # Threshold
            break
        
        # Record harmonic
        harmonics.append({
            'frequency': peak_freq,
            'period': 1.0 / peak_freq / 3600,  # hours
            'power': peak_power,
            'amplitude': self._estimate_amplitude(residual, peak_freq),
            'phase': self._estimate_phase(residual, peak_freq)
        })
        
        # Subtract fitted component from residual
        model = ls_residual.model(self.current_timestamps, peak_freq)
        residual = residual - model
    
    return harmonics
```

#### 1.2 Phase Analysis

**Add phase estimation methods:**

```python
def _estimate_phase(
    self,
    signal: np.ndarray,
    frequency: float
) -> float:
    """
    Estimate phase of sinusoidal component.
    
    Returns:
        Phase in radians [0, 2π)
    """
    # Fit sine and cosine components
    t = self.current_timestamps
    A = np.column_stack([
        np.sin(2 * np.pi * frequency * t),
        np.cos(2 * np.pi * frequency * t)
    ])
    
    # Least squares fit
    coeffs, _, _, _ = np.linalg.lstsq(A, signal, rcond=None)
    
    # Phase from coefficients
    phase = np.arctan2(coeffs[1], coeffs[0])
    return phase % (2 * np.pi)

def _estimate_amplitude(
    self,
    signal: np.ndarray,
    frequency: float
) -> float:
    """
    Estimate amplitude of sinusoidal component.
    """
    t = self.current_timestamps
    A = np.column_stack([
        np.sin(2 * np.pi * frequency * t),
        np.cos(2 * np.pi * frequency * t)
    ])
    coeffs, _, _, _ = np.linalg.lstsq(A, signal, rcond=None)
    return np.sqrt(coeffs[0]**2 + coeffs[1]**2)
```

#### 1.3 Bootstrap Confidence Intervals

**Add statistical confidence estimation:**

```python
def _calculate_bootstrap_confidence(
    self,
    signal: np.ndarray,
    timestamps: np.ndarray,
    n_bootstrap: int = 100
) -> Dict[str, tuple]:
    """
    Bootstrap confidence intervals for period detection.
    
    Returns:
        Dictionary with (lower, upper) 95% CI for each metric
    """
    from scipy import stats
    
    periods = []
    amplitudes = []
    
    for _ in range(n_bootstrap):
        # Resample with replacement
        indices = np.random.choice(len(signal), size=len(signal), replace=True)
        boot_signal = signal[indices]
        boot_times = timestamps[indices]
        
        # Re-analyze
        ls = LombScargle(boot_times, boot_signal)
        freq, pwr = ls.autopower()
        peak_freq = freq[np.argmax(pwr)]
        
        periods.append(1.0 / peak_freq / 3600)
        amplitudes.append(self._estimate_amplitude(boot_signal, peak_freq))
    
    return {
        'period_ci': (np.percentile(periods, 2.5), np.percentile(periods, 97.5)),
        'amplitude_ci': (np.percentile(amplitudes, 2.5), np.percentile(amplitudes, 97.5))
    }
```

### Testing

```python
def test_multi_harmonic_detection():
    """Test detection of multiple harmonics"""
    analyzer = SystemAnalyzer(sampling_rate=1.0)
    
    # Signal with 24h + 12h components
    t = np.linspace(0, 72, 300)
    signal = (30*np.sin(2*np.pi*t/24) +  # 24h fundamental
              10*np.sin(2*np.pi*t/12))   # 12h harmonic
    
    result = analyzer.fourier_lens(signal, t, detect_harmonics=True)
    
    assert len(result.harmonics) >= 2
    periods = [h['period'] for h in result.harmonics]
    assert any(20 < p < 28 for p in periods)  # 24h
    assert any(10 < p < 14 for p in periods)  # 12h

def test_phase_estimation():
    """Test phase detection accuracy"""
    analyzer = SystemAnalyzer(sampling_rate=1.0)
    
    # Known phase signal
    t = np.linspace(0, 48, 200)
    phase_true = np.pi / 4  # 45 degrees
    signal = np.sin(2*np.pi*t/24 + phase_true)
    
    result = analyzer.fourier_lens(signal, t)
    phase_detected = result.harmonics[0]['phase']
    
    assert abs(phase_detected - phase_true) < 0.1  # Within 0.1 radians
```

---

## 🌊 Feature 2: Wavelet Mother Function Optimization

### Motivation
MVP uses fixed 'morl' (Morlet) wavelet. Different biological signals need different wavelets:
- **Sharp transitions** → Haar, db4 (high frequency localization)
- **Smooth oscillations** → Morlet, Mexican hat (frequency selectivity)
- **Unknown characteristics** → Auto-select optimal wavelet

### Implementation

#### 2.1 Wavelet Selection Algorithm

**Add to SystemAnalyzer:**

```python
AVAILABLE_WAVELETS = {
    'morl': 'Morlet - Good for smooth oscillations',
    'mexh': 'Mexican Hat - Good for peak detection',
    'haar': 'Haar - Sharp transitions, edges',
    'db4': 'Daubechies 4 - Balanced time-frequency',
    'db8': 'Daubechies 8 - Smoother than db4',
    'sym4': 'Symlet 4 - Nearly symmetric, good for signals',
    'coif2': 'Coiflet 2 - Smooth, orthogonal'
}

def wavelet_lens(
    self,
    time_series: np.ndarray,
    wavelet_name: Optional[str] = None,  # NEW: None = auto-select
    auto_select: bool = True
) -> WaveletResult:
    """
    Enhanced wavelet analysis with automatic mother wavelet selection.
    
    New Parameters:
        wavelet_name: Specific wavelet or None for auto-selection
        auto_select: Enable automatic optimal wavelet selection
    """
    # Auto-select optimal wavelet if not specified
    if wavelet_name is None and auto_select:
        wavelet_name = self._select_optimal_wavelet(time_series)
    elif wavelet_name is None:
        wavelet_name = 'morl'  # Default
    
    # ... existing CWT code ...
    
    return WaveletResult(
        # ... existing fields ...
        wavelet_used=wavelet_name,  # NEW
        selection_score=selection_score,  # NEW
        alternative_wavelets=alternatives  # NEW
    )

def _select_optimal_wavelet(
    self,
    time_series: np.ndarray
) -> tuple:
    """
    Automatically select optimal mother wavelet for signal.
    
    Selection Criteria:
    1. Signal energy concentration
    2. Time-frequency resolution trade-off
    3. Edge effect minimization
    
    Returns:
        (best_wavelet_name, selection_score, alternative_recommendations)
    """
    scores = {}
    
    for wavelet_name in ['morl', 'mexh', 'db4', 'db8']:
        try:
            # Perform CWT
            scales = np.arange(1, min(128, len(time_series)//4))
            coeffs, _ = pywt.cwt(
                time_series, scales, wavelet_name,
                sampling_period=1.0/self.sampling_rate
            )
            
            # Calculate selection metrics
            energy_concentration = self._calculate_energy_concentration(coeffs)
            time_localization = self._calculate_time_localization(coeffs)
            freq_localization = self._calculate_freq_localization(coeffs)
            edge_quality = self._calculate_edge_quality(coeffs)
            
            # Composite score (weighted sum)
            score = (0.3 * energy_concentration +
                    0.25 * time_localization +
                    0.25 * freq_localization +
                    0.2 * edge_quality)
            
            scores[wavelet_name] = {
                'total_score': score,
                'energy_concentration': energy_concentration,
                'time_localization': time_localization,
                'freq_localization': freq_localization,
                'edge_quality': edge_quality
            }
        except Exception:
            scores[wavelet_name] = {'total_score': 0.0}
    
    # Select best
    best_wavelet = max(scores.keys(), key=lambda k: scores[k]['total_score'])
    
    # Sort alternatives
    sorted_wavelets = sorted(scores.items(), 
                            key=lambda x: x[1]['total_score'], 
                            reverse=True)
    
    return best_wavelet, scores[best_wavelet], sorted_wavelets[1:4]

def _calculate_energy_concentration(self, coeffs: np.ndarray) -> float:
    """
    Measure how concentrated energy is in time-frequency plane.
    Higher = better localization.
    """
    power = np.abs(coeffs)**2
    total_energy = np.sum(power)
    
    if total_energy == 0:
        return 0.0
    
    # Shannon entropy (lower = more concentrated)
    power_norm = power / total_energy
    power_norm = power_norm[power_norm > 0]  # Avoid log(0)
    entropy = -np.sum(power_norm * np.log(power_norm))
    
    # Normalize to [0, 1], invert so higher = better
    max_entropy = np.log(power.size)
    return 1.0 - (entropy / max_entropy)

def _calculate_time_localization(self, coeffs: np.ndarray) -> float:
    """
    Measure time localization quality.
    """
    power = np.abs(coeffs)**2
    time_profile = np.sum(power, axis=0)  # Sum over scales
    
    # Calculate standard deviation (lower = better localized)
    if np.sum(time_profile) == 0:
        return 0.0
    
    time_profile_norm = time_profile / np.sum(time_profile)
    time_indices = np.arange(len(time_profile))
    mean_time = np.sum(time_indices * time_profile_norm)
    std_time = np.sqrt(np.sum((time_indices - mean_time)**2 * time_profile_norm))
    
    # Normalize: smaller std = better, map to [0,1]
    return np.exp(-std_time / len(time_profile))

def _calculate_freq_localization(self, coeffs: np.ndarray) -> float:
    """
    Measure frequency localization quality.
    """
    power = np.abs(coeffs)**2
    freq_profile = np.sum(power, axis=1)  # Sum over time
    
    if np.sum(freq_profile) == 0:
        return 0.0
    
    freq_profile_norm = freq_profile / np.sum(freq_profile)
    freq_indices = np.arange(len(freq_profile))
    mean_freq = np.sum(freq_indices * freq_profile_norm)
    std_freq = np.sqrt(np.sum((freq_indices - mean_freq)**2 * freq_profile_norm))
    
    return np.exp(-std_freq / len(freq_profile))

def _calculate_edge_quality(self, coeffs: np.ndarray) -> float:
    """
    Measure edge effect quality (less edge distortion = better).
    """
    # Check power near edges vs center
    edge_width = max(5, coeffs.shape[1] // 20)
    
    left_edge_power = np.mean(np.abs(coeffs[:, :edge_width])**2)
    right_edge_power = np.mean(np.abs(coeffs[:, -edge_width:])**2)
    center_power = np.mean(np.abs(coeffs[:, edge_width:-edge_width])**2)
    
    if center_power == 0:
        return 0.0
    
    # Lower edge power relative to center = better
    edge_ratio = (left_edge_power + right_edge_power) / (2 * center_power)
    return 1.0 / (1.0 + edge_ratio)
```

#### 2.2 Multi-Resolution Analysis

**Add multi-scale decomposition:**

```python
def wavelet_multiresolution_analysis(
    self,
    time_series: np.ndarray,
    wavelet: str = 'db4',
    level: int = 5
) -> Dict[str, np.ndarray]:
    """
    Perform wavelet multi-resolution analysis (MRA).
    
    Decomposes signal into approximation + detail coefficients
    at multiple scales.
    
    Args:
        time_series: Input signal
        wavelet: Wavelet name
        level: Decomposition level
    
    Returns:
        Dictionary with approximation and detail coefficients
    """
    coeffs = pywt.wavedec(time_series, wavelet, level=level)
    
    # Reconstruct components at each level
    reconstructed = {}
    reconstructed['approximation'] = pywt.upcoef('a', coeffs[0], wavelet, level=level)
    
    for i, detail in enumerate(coeffs[1:]):
        reconstructed[f'detail_{i+1}'] = pywt.upcoef('d', detail, wavelet, level=level-i)
    
    return reconstructed
```

### Testing

```python
def test_automatic_wavelet_selection():
    """Test automatic wavelet selection"""
    analyzer = SystemAnalyzer(sampling_rate=1.0)
    
    # Sharp transition signal → should prefer haar or db4
    t = np.linspace(0, 10, 200)
    sharp_signal = np.concatenate([np.zeros(100), np.ones(100)])
    
    result = analyzer.wavelet_lens(sharp_signal, wavelet_name=None)
    assert result.wavelet_used in ['haar', 'db4', 'db8']
    
    # Smooth oscillation → should prefer morl
    smooth_signal = np.sin(2*np.pi*t)
    result = analyzer.wavelet_lens(smooth_signal, wavelet_name=None)
    assert result.wavelet_used in ['morl', 'mexh']
```

---

## 🎛️ Feature 3: Transfer Function System Identification

### Motivation
Understand system dynamics beyond stability:
- **Input-output relationships** (how ATP affects growth rate)
- **System response** (impulse, step response)
- **Model-based prediction** (forecast future behavior)

### Implementation

#### 3.1 ARMAX Model Fitting

**Add new method to SystemAnalyzer:**

```python
from scipy.signal import lfilter
from scipy.optimize import minimize

def identify_transfer_function(
    self,
    input_signal: np.ndarray,
    output_signal: np.ndarray,
    model_order: tuple = (2, 2)
) -> Dict[str, Any]:
    """
    Identify system transfer function using ARMAX model.
    
    Model: A(z)y[n] = B(z)u[n] + e[n]
    where A(z), B(z) are polynomials in z^-1
    
    Args:
        input_signal: System input (e.g., ATP level)
        output_signal: System output (e.g., growth rate)
        model_order: (na, nb) order of A and B polynomials
    
    Returns:
        Dictionary with transfer function coefficients and metrics
    """
    na, nb = model_order
    
    # Estimate ARMAX parameters using least squares
    params = self._estimate_armax_parameters(
        input_signal, output_signal, na, nb
    )
    
    # Extract A and B polynomials
    a_coeffs = np.array([1.0] + list(params[:na]))
    b_coeffs = np.array(params[na:na+nb])
    
    # Calculate transfer function
    tf_zeros, tf_poles, tf_gain = self._armax_to_transfer_function(
        a_coeffs, b_coeffs
    )
    
    # Model validation
    predicted_output = lfilter(b_coeffs, a_coeffs, input_signal)
    fit_quality = self._calculate_fit_quality(output_signal, predicted_output)
    
    return {
        'a_coeffs': a_coeffs,
        'b_coeffs': b_coeffs,
        'zeros': tf_zeros,
        'poles': tf_poles,
        'gain': tf_gain,
        'fit_quality': fit_quality,
        'predicted_output': predicted_output,
        'model_order': model_order
    }

def _estimate_armax_parameters(
    self,
    input_sig: np.ndarray,
    output_sig: np.ndarray,
    na: int,
    nb: int
) -> np.ndarray:
    """
    Estimate ARMAX parameters using least squares.
    """
    n = len(output_sig)
    max_lag = max(na, nb)
    
    # Build regression matrix
    X = []
    y = []
    
    for i in range(max_lag, n):
        row = []
        # Past outputs (AR part)
        for j in range(1, na + 1):
            row.append(-output_sig[i - j])
        # Past inputs (MA part)
        for j in range(nb):
            row.append(input_sig[i - j])
        
        X.append(row)
        y.append(output_sig[i])
    
    X = np.array(X)
    y = np.array(y)
    
    # Least squares solution
    params, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    return params

def _armax_to_transfer_function(
    self,
    a_coeffs: np.ndarray,
    b_coeffs: np.ndarray
) -> tuple:
    """
    Convert ARMAX model to transfer function (zeros, poles, gain).
    """
    # Zeros from numerator (B polynomial)
    if len(b_coeffs) > 1:
        zeros = np.roots(b_coeffs)
    else:
        zeros = np.array([])
    
    # Poles from denominator (A polynomial)
    if len(a_coeffs) > 1:
        poles = np.roots(a_coeffs)
    else:
        poles = np.array([])
    
    # Gain
    gain = b_coeffs[0] / a_coeffs[0] if a_coeffs[0] != 0 else 1.0
    
    return zeros, poles, gain

def _calculate_fit_quality(
    self,
    actual: np.ndarray,
    predicted: np.ndarray
) -> Dict[str, float]:
    """
    Calculate fit quality metrics.
    """
    # Trim to same length
    min_len = min(len(actual), len(predicted))
    actual = actual[:min_len]
    predicted = predicted[:min_len]
    
    # R-squared
    ss_res = np.sum((actual - predicted)**2)
    ss_tot = np.sum((actual - np.mean(actual))**2)
    r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0.0
    
    # RMSE
    rmse = np.sqrt(np.mean((actual - predicted)**2))
    
    # NRMSE (normalized)
    range_actual = np.max(actual) - np.min(actual)
    nrmse = rmse / range_actual if range_actual > 0 else float('inf')
    
    return {
        'r_squared': r_squared,
        'rmse': rmse,
        'nrmse': nrmse
    }
```

#### 3.2 State-Space Representation

**Add state-space conversion:**

```python
def convert_to_state_space(
    self,
    transfer_function: Dict[str, Any]
) -> Dict[str, np.ndarray]:
    """
    Convert transfer function to state-space representation.
    
    State-space form:
        x[k+1] = A*x[k] + B*u[k]
        y[k] = C*x[k] + D*u[k]
    
    Returns:
        Dictionary with A, B, C, D matrices
    """
    from scipy.signal import tf2ss
    
    num = transfer_function['b_coeffs']
    den = transfer_function['a_coeffs']
    
    A, B, C, D = tf2ss(num, den)
    
    return {
        'A': A,  # State transition matrix
        'B': B,  # Input matrix
        'C': C,  # Output matrix
        'D': D,  # Feedthrough matrix
        'state_dimension': A.shape[0]
    }

def simulate_system_response(
    self,
    state_space: Dict[str, np.ndarray],
    input_signal: np.ndarray,
    initial_state: Optional[np.ndarray] = None
) -> np.ndarray:
    """
    Simulate system response to input using state-space model.
    """
    A = state_space['A']
    B = state_space['B']
    C = state_space['C']
    D = state_space['D']
    
    n_states = A.shape[0]
    n_steps = len(input_signal)
    
    # Initialize state
    if initial_state is None:
        x = np.zeros(n_states)
    else:
        x = initial_state.copy()
    
    # Simulate
    output = np.zeros(n_steps)
    
    for k in range(n_steps):
        # Output equation
        output[k] = C @ x + D * input_signal[k]
        
        # State update
        x = A @ x + B * input_signal[k]
    
    return output
```

### Testing

```python
def test_transfer_function_identification():
    """Test system identification"""
    analyzer = SystemAnalyzer(sampling_rate=1.0)
    
    # Create known system: y[n] = 0.8*y[n-1] + 0.5*u[n]
    input_sig = np.random.randn(200)
    output_sig = np.zeros(200)
    
    for i in range(1, 200):
        output_sig[i] = 0.8 * output_sig[i-1] + 0.5 * input_sig[i]
    
    # Identify
    tf = analyzer.identify_transfer_function(input_sig, output_sig, model_order=(1, 1))
    
    # Check coefficient recovery
    assert abs(tf['a_coeffs'][1] + 0.8) < 0.1  # Should recover -0.8
    assert abs(tf['b_coeffs'][0] - 0.5) < 0.1  # Should recover 0.5
    assert tf['fit_quality']['r_squared'] > 0.9
```

---

## ✅ Feature 4: Consensus Validation (MetaCycle-style)

### Motivation
Single method can give false positives. Consensus validation:
- **Multiple algorithms** (Lomb-Scargle, FFT, Autocorrelation, Fisher's G)
- **Agreement threshold** (3+ methods agree → high confidence)
- **Robustness** (less sensitive to outliers, noise)

### Implementation

#### 4.1 Multiple Period Detection Methods

**Add consensus analysis:**

```python
def consensus_period_detection(
    self,
    time_series: np.ndarray,
    timestamps: Optional[np.ndarray] = None,
    methods: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    MetaCycle-inspired consensus period detection.
    
    Runs multiple period detection algorithms and aggregates results.
    
    Args:
        time_series: Input signal
        timestamps: Time points (optional)
        methods: List of methods to use. Options:
                 ['lomb_scargle', 'fft', 'autocorrelation', 'fisher_g']
                 If None, uses all methods.
    
    Returns:
        Dictionary with consensus period and individual method results
    """
    if timestamps is None:
        timestamps = np.arange(len(time_series)) / self.sampling_rate
    
    if methods is None:
        methods = ['lomb_scargle', 'fft', 'autocorrelation', 'fisher_g']
    
    # Run each method
    results = {}
    
    if 'lomb_scargle' in methods:
        results['lomb_scargle'] = self._detect_period_lomb_scargle(
            time_series, timestamps
        )
    
    if 'fft' in methods:
        results['fft'] = self._detect_period_fft(time_series)
    
    if 'autocorrelation' in methods:
        results['autocorrelation'] = self._detect_period_autocorrelation(
            time_series
        )
    
    if 'fisher_g' in methods:
        results['fisher_g'] = self._detect_period_fisher_g(time_series)
    
    # Calculate consensus
    consensus = self._calculate_consensus(results)
    
    return {
        'consensus_period': consensus['period'],
        'consensus_confidence': consensus['confidence'],
        'method_agreement': consensus['agreement'],
        'individual_results': results,
        'methods_used': methods
    }

def _detect_period_lomb_scargle(
    self,
    signal: np.ndarray,
    timestamps: np.ndarray
) -> Dict[str, float]:
    """Lomb-Scargle period detection"""
    ls = LombScargle(timestamps, signal)
    freq, pwr = ls.autopower()
    peak_idx = np.argmax(pwr)
    
    return {
        'period': 1.0 / freq[peak_idx] / 3600,
        'power': pwr[peak_idx],
        'confidence': 1.0 - ls.false_alarm_probability(pwr[peak_idx])
    }

def _detect_period_fft(self, signal: np.ndarray) -> Dict[str, float]:
    """Standard FFT period detection"""
    from scipy.fft import fft, fftfreq
    
    # Remove mean
    signal_centered = signal - np.mean(signal)
    
    # FFT
    n = len(signal)
    fft_vals = fft(signal_centered)
    freqs = fftfreq(n, d=1.0/self.sampling_rate)
    
    # Power spectrum (positive frequencies only)
    power = np.abs(fft_vals[:n//2])**2
    freqs = freqs[:n//2]
    
    # Find peak
    peak_idx = np.argmax(power[1:]) + 1  # Skip DC
    peak_freq = freqs[peak_idx]
    
    return {
        'period': 1.0 / peak_freq / 3600 if peak_freq > 0 else float('inf'),
        'power': power[peak_idx],
        'confidence': power[peak_idx] / np.sum(power)  # Normalized power
    }

def _detect_period_autocorrelation(
    self,
    signal: np.ndarray
) -> Dict[str, float]:
    """Autocorrelation period detection"""
    # Autocorrelation
    signal_centered = signal - np.mean(signal)
    autocorr = np.correlate(signal_centered, signal_centered, mode='full')
    autocorr = autocorr[len(autocorr)//2:]  # Keep positive lags
    autocorr = autocorr / autocorr[0]  # Normalize
    
    # Find first peak after lag 0
    # Look for local maxima
    peaks = []
    for i in range(1, len(autocorr)-1):
        if autocorr[i] > autocorr[i-1] and autocorr[i] > autocorr[i+1]:
            if autocorr[i] > 0.3:  # Threshold
                peaks.append((i, autocorr[i]))
    
    if peaks:
        # First significant peak
        lag, correlation = peaks[0]
        period = lag / self.sampling_rate / 3600  # Convert to hours
    else:
        period = float('inf')
        correlation = 0.0
    
    return {
        'period': period,
        'correlation': correlation,
        'confidence': correlation
    }

def _detect_period_fisher_g(self, signal: np.ndarray) -> Dict[str, float]:
    """Fisher's G-test period detection"""
    from scipy.fft import fft
    
    # FFT
    signal_centered = signal - np.mean(signal)
    fft_vals = np.abs(fft(signal_centered))**2
    
    # Fisher's G statistic
    g_stat = np.max(fft_vals[1:len(fft_vals)//2]) / np.sum(fft_vals[1:len(fft_vals)//2])
    
    # Find period at max power
    peak_idx = np.argmax(fft_vals[1:len(fft_vals)//2]) + 1
    period_samples = len(signal) / peak_idx
    period_hours = period_samples / self.sampling_rate / 3600
    
    # G-test p-value (approximate)
    n = len(signal) // 2
    p_value = 1.0 - (1.0 - g_stat)**(n-1)
    
    return {
        'period': period_hours,
        'g_statistic': g_stat,
        'confidence': 1.0 - p_value
    }

def _calculate_consensus(
    self,
    method_results: Dict[str, Dict[str, float]]
) -> Dict[str, Any]:
    """
    Calculate consensus period from multiple methods.
    
    Uses weighted voting based on confidence scores.
    """
    periods = []
    weights = []
    
    for method_name, result in method_results.items():
        if result['period'] < float('inf') and result['confidence'] > 0.5:
            periods.append(result['period'])
            weights.append(result['confidence'])
    
    if not periods:
        return {
            'period': float('inf'),
            'confidence': 0.0,
            'agreement': 0.0
        }
    
    periods = np.array(periods)
    weights = np.array(weights)
    
    # Weighted median (more robust than mean)
    sorted_idx = np.argsort(periods)
    sorted_periods = periods[sorted_idx]
    sorted_weights = weights[sorted_idx]
    cumsum = np.cumsum(sorted_weights)
    median_idx = np.searchsorted(cumsum, cumsum[-1] / 2)
    consensus_period = sorted_periods[median_idx]
    
    # Agreement: how close are methods to consensus?
    deviations = np.abs(periods - consensus_period) / consensus_period
    agreement = np.mean(deviations < 0.1)  # Within 10%
    
    # Confidence: weighted average of individual confidences
    consensus_confidence = np.average(weights)
    
    return {
        'period': consensus_period,
        'confidence': consensus_confidence,
        'agreement': agreement,
        'n_methods': len(periods)
    }
```

### Testing

```python
def test_consensus_period_detection():
    """Test consensus validation"""
    analyzer = SystemAnalyzer(sampling_rate=1.0)
    
    # 24h circadian signal
    t = np.linspace(0, 72, 300)
    signal = 100 + 30*np.sin(2*np.pi*t/24) + 5*np.random.randn(300)
    
    result = analyzer.consensus_period_detection(signal, t)
    
    # Should detect ~24h period
    assert 20 < result['consensus_period'] < 28
    
    # High agreement (all methods should agree)
    assert result['method_agreement'] > 0.7
    
    # High confidence
    assert result['consensus_confidence'] > 0.8
    
    # Multiple methods used
    assert len(result['individual_results']) >= 3
```

---

## 📊 Phase 1 Integration

### Modified Files

1. **`src/bioxen_fourier_vm_lib/analysis/system_analyzer.py`**
   - Add ~500 lines for Phase 1 features
   - Maintain backward compatibility (MVP methods unchanged)
   - New optional parameters with defaults

2. **`src/bioxen_fourier_vm_lib/analysis/consensus.py`** (NEW)
   - Consensus validation logic
   - Multiple period detection algorithms
   - ~300 lines

3. **`src/bioxen_fourier_vm_lib/analysis/transfer_function.py`** (NEW)
   - System identification
   - State-space models
   - ~400 lines

4. **`tests/test_phase1_features.py`** (NEW)
   - Comprehensive Phase 1 tests
   - ~500 lines

### No Breaking Changes

All MVP functionality preserved:

```python
# MVP code still works
analyzer = SystemAnalyzer()
result = analyzer.fourier_lens(signal, timestamps)  # Same as MVP

# New Phase 1 features opt-in
result = analyzer.fourier_lens(signal, timestamps, 
                                detect_harmonics=True)  # NEW
```

---

## 📈 Performance Targets

| Operation | MVP | Phase 1 Target |
|-----------|-----|----------------|
| Fourier analysis (200 samples) | 50ms | 100ms (with harmonics) |
| Wavelet analysis (200 samples) | 80ms | 150ms (with auto-select) |
| Transfer function ID (200 samples) | N/A | 200ms |
| Consensus validation (200 samples) | N/A | 500ms (4 methods) |
| Genome analysis (187 genes) | 5s | 10s (full Phase 1 features) |

---

## 📚 Documentation Requirements

1. **User Guide Update**
   - Phase 1 feature examples
   - When to use each feature
   - Performance considerations

2. **API Reference**
   - All new methods documented
   - Parameter descriptions
   - Return value specifications

3. **Research Guide** (NEW)
   - Biological interpretation of Phase 1 features
   - Publication-ready analysis workflows
   - Statistical best practices

4. **Performance Guide** (NEW)
   - Optimization tips
   - Memory management
   - Parallel processing options

---

## 🗓️ Implementation Timeline

### Week 1: Advanced Lomb-Scargle (40 hours)
- **Days 1-2:** Multi-harmonic detection
- **Days 3-4:** Phase analysis and amplitude estimation
- **Day 5:** Bootstrap confidence intervals

### Week 2: Wavelet Optimization (40 hours)
- **Days 1-2:** Wavelet selection algorithm
- **Days 3-4:** Selection metrics implementation
- **Day 5:** Multi-resolution analysis

### Week 3: Transfer Functions (40 hours)
- **Days 1-2:** ARMAX model fitting
- **Days 3-4:** State-space representation
- **Day 5:** System simulation

### Week 4: Consensus & Polish (40 hours)
- **Days 1-2:** Multiple detection methods
- **Day 3:** Consensus calculation
- **Days 4-5:** Testing, documentation, integration

**Total:** 160 hours over 4 weeks

---

## ✅ Phase 1 Acceptance Criteria

- [ ] All 4 major features implemented
- [ ] 95%+ test coverage
- [ ] No breaking changes to MVP API
- [ ] Performance targets met
- [ ] Complete documentation
- [ ] Successful analysis of Syn3A genome with Phase 1 features
- [ ] Consensus validation shows >80% agreement on test data
- [ ] Transfer function fits with R² > 0.8 on synthetic data
- [ ] Automatic wavelet selection outperforms fixed selection

---

## 🚀 Getting Started

**Ready to begin?** Start with Feature 1 (Advanced Lomb-Scargle):

```bash
# Create feature branch
git checkout -b feature/phase1-lomb-scargle dev

# Start implementation
code src/bioxen_fourier_vm_lib/analysis/system_analyzer.py
```

Let's build research-grade biological signal analysis! 🔬

---

**Version:** 1.0  
**Date:** October 1, 2025  
**Status:** Ready for Implementation  
**Branch:** dev → feature branches  
**References:** MASTER-PROMPT-MVP-FIRST-v2.1.md lines 1449-1453
