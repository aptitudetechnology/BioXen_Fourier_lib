# Wavelet Analysis for Biological Signals - MVP Research Questions

## Research Question 1: Multi-Signal Wavelet Analysis Libraries

**Research Goal:** Identify existing Python libraries that support wavelet coherence and cross-wavelet analysis for biological time series.

**Specific Questions:**
1. What Python libraries support wavelet coherence analysis?
   - Does PyWavelets support cross-wavelet analysis?
   - What capabilities does `pycwt` (Python Continuous Wavelet Transform) offer?
   - Does `ssqueezepy` support multi-signal analysis?
   - Can `scipy.signal.coherence` be adapted for wavelet analysis?

2. What are the key features and limitations of each library?
   - Supported wavelet types (especially Morlet for biological signals)
   - Computational performance characteristics
   - Documentation quality and examples
   - Active maintenance status (commits in 2023-2025)
   - License compatibility (MIT/BSD preferred)

3. Are there reference implementations from published papers?
   - Grinsted et al. (2004) implementations
   - Torrence & Compo (1998) reference code
   - MATLAB code that has been ported to Python

4. What biological examples exist in these libraries?
   - Example datasets included
   - Circadian rhythm or cell cycle applications
   - Signal coupling analysis demonstrations

---

## Research Question 2: Validation Datasets for Biological Wavelet Analysis

**Research Goal:** Find publicly available biological datasets with known periodicities that have been used to validate wavelet analysis tools.

**Specific Questions:**
1. What public biological datasets are commonly used for wavelet validation?
   - CircaDB (http://circadb.hogeneschlab.org/) datasets
   - Published papers with supplementary data
   - BioClock database examples
   - Test datasets from existing wavelet tool repositories

2. What datasets have verified ground truth periodicities?
   - Circadian rhythm data with confirmed 24h periods
   - Cell cycle data with known phase durations
   - Gene expression time series with validated oscillations

3. What validation protocols are used in published wavelet studies?
   - Acceptable error margins for period detection
   - Statistical measures of accuracy
   - Comparison benchmarks between methods

4. Are there synthetic biological signal generators?
   - Libraries for generating test signals
   - Parameterized biological waveform models
   - Noise characteristics for realistic testing

---

## Research Question 3: Statistical Significance Testing for Wavelets

**Research Goal:** Identify established methods and existing implementations for testing statistical significance of wavelet analysis results.

**Specific Questions:**
1. What significance testing methods are built into existing libraries?
   - Does `pycwt` include significance testing modules?
   - What does PyWavelets offer for hypothesis testing?
   - What approach does R's `WaveletComp` use?

2. What are the standard statistical approaches for wavelet significance?
   - Red noise (AR1) null hypothesis models
   - Surrogate data methods
   - Permutation testing approaches
   - Monte Carlo significance estimation

3. What Python libraries support the required statistical methods?
   - `scipy.stats` for AR model fitting
   - `statsmodels` for time series analysis
   - `arch` library for ARMA/GARCH models
   - Existing implementations we can adapt

4. What are the computational requirements?
   - Typical number of surrogate iterations needed
   - Performance benchmarks if available
   - Trade-offs between methods

---

## Research Question 4: Interactive Visualization Libraries for Wavelets

**Research Goal:** Identify JavaScript/Python visualization libraries suitable for creating interactive 2D scalogram heatmaps in web applications.

**Specific Questions:**
1. What are the leading libraries for interactive heatmap visualization?
   - Plotly.js capabilities and features
   - D3.js wavelet visualization examples
   - Bokeh interactive plotting
   - Chart.js or other alternatives
   - Matplotlib + mpld3 for Python-to-JS conversion

2. Are there existing wavelet visualization implementations?
   - GitHub repositories with wavelet scalogram code
   - Open-source wavelet visualization tools
   - Examples we can adapt or learn from

3. What are the key features and trade-offs?
   - Mobile responsiveness
   - Performance with large datasets
   - Customization flexibility
   - Documentation and community support
   - Integration complexity

4. What specific features are needed for biological wavelet visualization?
   - Hover tooltips showing time/frequency/power
   - Cone of influence (COI) overlay
   - Significance contours
   - Color scale customization
   - Export capabilities

---

## Research Priority Framework

For each question, please provide:
- **Available libraries/tools** with version information and maintenance status
- **Feature comparison matrix** (top 3-5 options)
- **Code examples** or links to implementations
- **Performance characteristics** if documented
- **Licensing information** (MIT/BSD/Apache preferred)
- **Community adoption metrics** (GitHub stars, PyPI downloads, citations)
- **Recommendation** based on feature completeness, ease of use, and maintenance

## Focus Areas

Priority on:
1. **Production-ready solutions** over research prototypes
2. **Well-documented libraries** with active communities
3. **Proven biological applications** over general-purpose tools
4. **Recent implementations** (2020-2025) with modern Python practices

Minimize:
- Theoretical discussions (focus on practical implementations)
- Custom algorithm development (use existing validated methods)
- Comparison of mathematical approaches (focus on library capabilities)