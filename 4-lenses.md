
Based on our recent research-driven work, we're up to 4 lenses in the BioXen system! Let me check the current documentation to confirm:

Searched text for four-lens|Four-Lens|4 lenses|fourth lens (**/*.{html,md}), 20 results
4 Lenses - The Complete BioXen System 🔬
Here's the current lineup:

1. 🌊 Fourier Lens (Steady-State Periodic Analysis)
Method: Lomb-Scargle Periodogram (biology standard)
Use Case: Circadian rhythms, stable oscillations
Best For: Stationary signals, irregular sampling
Library: astropy.timeseries.LombScargle, scipy.fft
2. 📈 Wavelet Lens ⭐ (The Fourth Lens - NEW!)
Method: Continuous/Discrete Wavelet Transform (CWT/DWT)
Use Case: Non-stationary signals, transient events
Best For: Cell cycle transitions, stress responses, damping oscillations
Library: pywt (PyWavelets), scipy.signal.cwt
Why Essential: Biological signals change frequency over time - Fourier can't detect WHEN changes occur
3. ⚙️ Laplace Lens (System Stability Analysis)
Method: Transfer Functions, State-Space Models
Use Case: Feedback control, homeostasis
Best For: System stability, control design
Library: python-control, scipy.signal
4. 📊 Z-Transform Lens (Discrete-Time Filtering)
Method: Digital Filters, Kalman Filtering
Use Case: Sampled data, real-time monitoring
Best For: Discrete measurements, noise reduction
Library: scipy.signal, custom implementations
Evolution: 3 → 4 Lenses
Started with: Fourier, Laplace, Z-Transform (the classical signal processing trio)

Added after research review: Wavelet Transform as the fourth lens because:

✅ Biological signals are non-stationary (frequency changes over time)
✅ Needed for transient events (stress responses, neural spikes)
✅ Provides time-frequency localization (Fourier cannot)
✅ Essential, not optional according to peer-reviewed biology research
Why These 4?
Each lens addresses a different biological data challenge:

Challenge	Lens Solution
Irregular sampling	Fourier (Lomb-Scargle)
Non-stationary signals	Wavelet ⭐
System stability	Laplace
Discrete measurements	Z-Transform
Nonlinear coupling	(Future: HOSA/Bispectrum)
The research showed that no single lens works for biological data - you need the complementary toolkit! 🎯