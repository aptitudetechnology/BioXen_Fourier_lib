# Deep Research Prompt: Wavelet Analysis for Biological Systems - Phase 2 Critical Questions

**Project:** BioXen Four-Lens Signal Analysis Library  
**Document Version:** 2.0  
**Date:** October 2, 2025  
**Status:** Pre-Phase 2 Research Requirements  
**Related Files:**
- `research/interactive-fourier-series/lenses/wavelets.html`
- `research/interactive-fourier-series/research/Wavelet Analysis for Biological Signals.md`

---

## 🎯 Research Objective

This document identifies **12 critical research questions** that emerged from analysis of the BioXen wavelet implementation roadmap and associated research documentation. These questions must be answered to advance from Phase 1 (basic wavelet analysis) to Phase 2 (production-ready multi-lens system) and establish BioXen as a research-grade tool for biological signal analysis.

---

## 🔴 CRITICAL PATH QUESTIONS (Must Answer for Week 3)

### Question 1: Wavelet Coherence & Cross-Wavelet Analysis

**Research Need:**  
Phase 1 Week 3 requires transfer function implementation for multi-signal biological systems. We need to determine the optimal approach for analyzing coupling between biological signals using wavelets.

**Specific Questions:**
1. **Algorithm Selection:**
   - Should we implement wavelet cross-spectrum, wavelet coherence, or both?
   - Which coherence measure: magnitude-squared coherence? Phase coherence? Both?
   - Is wavelet phase difference analysis sufficient for biological causality detection?

2. **Mathematical Implementation:**
   - Grinsted et al. (2004) vs. Torrence & Compo (1998) implementations - which is better for biological signals?
   - How to compute cone of influence for cross-wavelet analysis?
   - Significance testing: AR(1) red noise model appropriate for biological data?

3. **Biological Use Cases:**
   - Input-output transfer functions: e.g., glucose → insulin dynamics
   - Phase synchronization: circadian genes (Per2 vs. Bmal1)
   - Driver-response relationships: stress signal → gene expression response

4. **Computational Considerations:**
   - Can we leverage FFT convolution for cross-wavelet speedup?
   - Memory requirements for 2 signals × N timepoints × M scales?
   - Parallel processing strategy (multi-core? GPU?)

**Deliverable Needed:**
- Technical specification document for wavelet coherence implementation
- Comparison table: Grinsted vs. Torrence vs. Liu et al. (2007) methods
- Python pseudocode for cross-wavelet transform with biological example

**Research Resources to Review:**
- Grinsted, A., Moore, J. C., & Jevrejeva, S. (2004). "Application of the cross wavelet transform and wavelet coherence to geophysical time series." *Nonlinear Processes in Geophysics*, 11, 561-566.
- Issler, J. V., & Vahid, F. (2006). "The missing link: using the NBER recession indicator to construct coincident and leading indices of economic activity." *Journal of Econometrics*, 132(1), 281-303.
- Cazelles, B., et al. (2008). "Wavelet analysis of ecological time series." *Oecologia*, 156(2), 287-304.

---

### Question 2: Validation Dataset Selection & Ground Truth

**Research Need:**  
Cannot claim "research-grade" quality without validation against known biological phenomena. Need public datasets with established ground truth for wavelet detection benchmarking.

**Specific Questions:**
1. **Circadian Rhythm Datasets:**
   - Where can we obtain mouse SCN (suprachiasmatic nucleus) multi-unit recordings with known 24h periodicity?
   - Are there published Per2::Luc bioluminescence time-series with independently verified periods?
   - What about single-cell circadian data (CircaDB, Hughey et al. 2016)?

2. **Cell Cycle Datasets:**
   - FUCCI reporter datasets: Which publications provide raw time-series data?
   - Expected period range: 8-24 hours depending on cell type - how to handle variability?
   - Are there synchronized populations (serum shock, mitotic shake-off) with known phase distributions?

3. **Stress Response Datasets:**
   - Heat shock time-series: expected exponential decay with what time constants?
   - Osmotic stress: periodic vs. single-pulse dynamics?
   - Are there multimodal stress datasets (multiple stressors × multiple readouts)?

4. **Ground Truth Establishment:**
   - How were "true" periods determined in published studies?
   - Independent validation methods: autocorrelation? FFT? Lomb-Scargle?
   - What confidence intervals exist on ground truth values?

5. **Benchmark Metrics:**
   - How to quantify wavelet performance: Period detection accuracy? Phase estimation error? Amplitude reconstruction?
   - Should we use synthetic data first (known parameters) before biological data?
   - What's an acceptable error tolerance (±5%? ±10%?) for biological systems?

**Deliverable Needed:**
- Curated list of ≥5 public datasets with metadata (source, sample rate, known features)
- Validation protocol document specifying metrics and acceptance criteria
- Python notebook: "BioXen Wavelet Validation Suite" with automated testing

**Research Resources to Review:**
- CircaDB: http://circadb.hogeneschlab.org/
- Hughey, J. J., et al. (2016). "Robust meta-analysis of gene expression using the elastic net." *Nucleic Acids Research*, 44(20), e137.
- FUCCI datasets: Sakaue-Sawano papers + Zenodo repositories
- BioClock database (if accessible)

---

### Question 3: Higher-Order Spectral Analysis (HOSA) Integration Strategy

**Research Need:**  
Bio-signal.html emphasizes HOSA for nonlinear biological systems, but integration with wavelet analysis is undefined. Need architectural decision: Does HOSA complement or replace wavelets for certain signals?

**Specific Questions:**
1. **Theoretical Foundation:**
   - What biological phenomena require bispectral analysis (phase coupling, harmonic generation)?
   - When is wavelet bispectrum superior to standard wavelet spectrum?
   - Can we detect biological nonlinearity with wavelets alone, or is HOSA essential?

2. **Implementation Approaches:**
   - **Option A:** Wavelet bispectrum (2D scale analysis of phase coupling)
   - **Option B:** Wavelet bicoherence (normalized, 0-1 scale for interpretability)
   - **Option C:** Higher-order wavelet polyspectra (computationally feasible?)

3. **Computational Complexity:**
   - Standard CWT: O(N log N) via FFT
   - Wavelet bispectrum: O(N²) or worse?
   - Is there a fast algorithm (e.g., recursive, sparse)?
   - Memory requirements: 3D arrays (time × scale1 × scale2)?

4. **Biological Examples Requiring HOSA:**
   - Phase-amplitude coupling: circadian (phase) modulates ultradian (amplitude)?
   - Harmonic generation: cell cycle checkpoints as nonlinear oscillators?
   - Cross-frequency coupling: Are there documented cases in biological literature?

5. **Tool Comparison:**
   - Does any existing biology tool implement wavelet HOSA? (per2py? WaveletComp?)
   - If not, is this a competitive advantage or a warning sign?

**Deliverable Needed:**
- Decision matrix: When to use HOSA vs. standard wavelets for biological signals
- Computational complexity analysis with Big-O notation
- Prototype implementation: Wavelet bicoherence on synthetic phase-coupled signal

**Research Resources to Review:**
- Nikias, C. L., & Mendel, J. M. (1993). "Signal processing with higher-order spectra." *IEEE Signal Processing Magazine*, 10(3), 10-37.
- Van Milligen, B. P., et al. (1995). "Wavelet bicoherence: a new turbulence analysis tool." *Physics of Plasmas*, 2(8), 3017-3032.
- Biological phase-amplitude coupling: Canolty & Knight (2010) review

---

## 🟡 HIGH PRIORITY QUESTIONS (Phase 2 Requirements)

### Question 4: Wavelet Selection Optimization & Validation

**Research Need:**  
Current implementation plans auto-selection from 7+ wavelets (Morlet, Mexican Hat, Haar, db4, db8, sym4, coif2). Need rigorous validation that selection algorithm picks the "correct" wavelet.

**Specific Questions:**
1. **Selection Criteria:**
   - What metric determines "best" wavelet: Maximum energy concentration? Minimum edge artifacts? Biological interpretability?
   - Should we use cross-validation (train/test split) or information criteria (AIC, BIC)?
   - How to handle the bias-variance tradeoff (narrow vs. wide wavelets)?

2. **Biological Signal Properties:**
   - Smooth oscillations (circadian): Morlet complex wavelet optimal?
   - Sharp transients (stress response): Haar or Mexican Hat better?
   - Mixed signals (cell cycle with checkpoints): Daubechies multi-resolution?

3. **Validation Methodology:**
   - Synthetic data with known wavelet basis: Can we reconstruct perfectly?
   - Real data with independent validation: Does our selection match expert choice?
   - Robustness testing: Add noise, downsample, introduce gaps - does selection remain stable?

4. **Adaptive Selection:**
   - Should wavelet type change across time (non-stationary signals)?
   - Should scale-dependent selection be allowed (different wavelets at different frequencies)?
   - Computational cost of trying all wavelets vs. intelligent pre-screening?

**Deliverable Needed:**
- Wavelet selection algorithm specification with mathematical justification
- Validation results on ≥3 biological datasets showing selection accuracy
- Comparison table: Auto-selection vs. manual expert selection vs. fixed Morlet

**Research Resources to Review:**
- Addison, P. S. (2017). "The Illustrated Wavelet Transform Handbook" - Chapter 4: Wavelet Selection
- Mallat, S. (2008). "A Wavelet Tour of Signal Processing" - Best basis selection
- Samar, V. J., et al. (1999). "Wavelet analysis of neuroelectric waveforms." *Brain and Language*, 66(1), 7-60.

---

### Question 5: Computational Performance Benchmarking & Scalability

**Research Need:**  
Timeline claims "< 5 seconds for 5000 samples," but modern single-cell experiments have 100k+ cells × 1000+ timepoints = 100M+ datapoints. Need realistic performance characterization.

**Specific Questions:**
1. **Benchmark Design:**
   - Test datasets: 1k, 10k, 100k, 1M, 10M timepoints
   - Wavelet types: Morlet (complex), db4 (real), various scales (10-1000)
   - Hardware: CPU-only, multi-core, GPU (if implemented)

2. **Bottleneck Analysis:**
   - Is convolution the bottleneck? (O(N log N) via FFT should be fast)
   - Is scale loop the issue? (Parallelizable across scales?)
   - Memory transfer vs. computation time?

3. **Optimization Strategies:**
   - **NumPy/SciPy:** Current baseline performance
   - **Numba JIT:** Can we accelerate inner loops?
   - **CuPy/PyTorch:** GPU acceleration - what speedup factor?
   - **Dask/Vaex:** Out-of-core computation for massive datasets?

4. **Downsampling Strategy:**
   - For 1M+ timepoints, is downsampling acceptable?
   - Anti-aliasing requirements before decimation?
   - Adaptive sampling: High density near transients, low density in stable regions?

5. **Production Requirements:**
   - What's acceptable latency for interactive analysis? (< 1 second? < 10 seconds?)
   - Batch processing: Can we process 1000 cells overnight?
   - Cloud deployment: Memory limits (AWS Lambda = 10GB, need more?)

**Deliverable Needed:**
- Performance benchmark report: Dataset size × Wavelet type × Hardware → Time
- Optimization recommendations with expected speedup factors
- Scalability roadmap: When to use CPU, multi-core, GPU, cloud

**Research Resources to Review:**
- PyWavelets benchmark comparisons
- CWT performance: Torrence & Compo code vs. modern implementations
- GPU wavelet papers: Tenreiro Machado et al. (2015) CUDA CWT

---

### Question 6: Statistical Significance Testing Framework

**Research Need:**  
Cannot publish/trust results without significance testing. Need rigorous framework to distinguish real biological rhythms from noise artifacts.

**Specific Questions:**
1. **Null Hypothesis Models:**
   - **White noise:** Simple but unrealistic for biology
   - **Red noise (AR1):** Torrence & Compo default - appropriate for biological signals?
   - **ARMA models:** Better fit for biological autocorrelation?
   - **Surrogate data:** Phase randomization (IAAFT) vs. parametric models?

2. **Test Statistics:**
   - Global wavelet spectrum: Point-by-point chi-square test?
   - Scale-averaged power: Are we testing for specific frequency bands?
   - Wavelet coherence: Different null distribution than single-signal?

3. **Multiple Testing Correction:**
   - Testing across time × scale → thousands of comparisons
   - FDR correction (Benjamini-Hochberg)? Bonferroni (too conservative)?
   - Field significance: Correct for spatial/temporal autocorrelation?

4. **Biological Considerations:**
   - Should we require sustained significance (e.g., ≥3 consecutive cycles)?
   - Amplitude threshold: Biologically relevant vs. statistically significant?
   - Phase consistency: Significant period but random phase = noise?

5. **Computational Efficiency:**
   - Monte Carlo: How many surrogates needed? (100? 1000? 10000?)
   - Can we pre-compute null distributions for common scenarios?
   - Parallel surrogate generation?

**Deliverable Needed:**
- Statistical testing protocol document with mathematical formulation
- Python implementation: `wavelet_significance_test(signal, wavelet, alpha=0.05)`
- Validation: Known significant signals (synthetic) correctly identified at 95% power

**Research Resources to Review:**
- Torrence, C., & Compo, G. P. (1998). "A practical guide to wavelet analysis." *Bulletin of the American Meteorological Society*, 79(1), 61-78. [Appendix C: Significance testing]
- Maraun, D., & Kurths, J. (2004). "Cross wavelet analysis: significance testing and pitfalls." *Nonlinear Processes in Geophysics*, 11(4), 505-514.
- Benjamini, Y., & Hochberg, Y. (1995). "Controlling the false discovery rate." *Journal of the Royal Statistical Society*, 57(1), 289-300.

---

### Question 7: Visualization Strategy for Interactive HTML Dashboard

**Research Need:**  
Current wavelets.html uses Chart.js for 1D plots, but wavelet scalograms are 2D (time × scale). Need responsive, interactive visualization solution.

**Specific Questions:**
1. **Library Selection:**
   - **Plotly.js:** 2D heatmaps, interactive zoom/pan, good mobile support?
   - **D3.js:** Maximum flexibility but requires custom coding?
   - **Bokeh/Holoviews:** Python-first, can export to JavaScript?
   - **Chart.js plugins:** Any heatmap extensions?

2. **Scalogram Requirements:**
   - Color map: Jet (controversial), Viridis (perceptually uniform), custom biological?
   - Logarithmic scale axis: Periods (hours) or frequencies (Hz)?
   - Cone of influence overlay: How to show visually without cluttering?
   - Ridge lines: Overlay dominant frequency trajectory?

3. **Interactivity Features:**
   - Click on scalogram → show time-series at that scale?
   - Hover → display exact time, period, power value?
   - Zoom into specific time window or frequency band?
   - Export high-resolution image for publication?

4. **Mobile Responsiveness:**
   - 2D heatmaps hard to read on phone screens
   - Should we show simplified 1D projections on mobile?
   - Touch gestures: pinch-zoom, two-finger pan?

5. **Performance:**
   - 1000 timepoints × 100 scales = 100k pixels to render
   - Canvas vs. SVG: Which is faster for large heatmaps?
   - Downsampling for display vs. full resolution for computation?

**Deliverable Needed:**
- Visualization library comparison matrix (features, performance, mobile support)
- Prototype HTML page: Interactive wavelet scalogram with all planned features
- User testing feedback from ≥3 biologists (ease of interpretation)

**Research Resources to Review:**
- Plotly.js heatmap documentation + biological examples
- D3.js wavelet visualizations (GitHub search)
- Best practices: "Visualizing Time-Frequency Decompositions" (Cohen, 2019)

---

## 🟢 MEDIUM PRIORITY QUESTIONS (Phase 2-3 Optimization)

### Question 8: Multi-Resolution Analysis (MRA) Optimal Decomposition Levels

**Research Need:**  
Phase 1.5 implements 5-level MRA, but biological timescales vary widely. Need principled approach to determine decomposition depth.

**Specific Questions:**
1. **Biological Timescale Hierarchies:**
   - **Circadian (24h):** Sub-scales needed? 24h, 12h, 8h, 6h, 4h?
   - **Cell cycle (8-24h):** Does MRA capture G1, S, G2, M phases separately?
   - **Neural spikes (ms):** Completely different scale range - same MRA approach?

2. **Mathematical Criteria:**
   - Mallat's MRA theory: Decompose until residual is "white noise"?
   - Energy concentration: Stop when <5% variance remains in detail coefficients?
   - Sampling theorem: Nyquist limit determines maximum levels?

3. **Computational Considerations:**
   - Each level doubles computation time
   - Diminishing returns: Do levels 6-10 add biological insight or just noise?
   - Memory: Storing all approximation + detail coefficients

4. **Adaptive MRA:**
   - Should level count adapt to signal length? (100 pts → 3 levels, 10k pts → 8 levels?)
   - Different level counts for different biological systems?
   - User override: Expert specifies levels based on domain knowledge?

**Deliverable Needed:**
- MRA level selection algorithm with biological justification
- Case studies: 3 biological signals with optimal level analysis
- Sensitivity analysis: Performance vs. level count (1-10 levels)

---

### Question 9: Edge Effect Mitigation Strategies

**Research Need:**  
Cone of influence (COI) affects 10-20% of signal at boundaries. Critical transient events (stress onset, cell division) may occur at edges.

**Specific Questions:**
1. **Padding Strategies:**
   - **Zero padding:** Simple but introduces artificial discontinuity
   - **Symmetric padding:** Reflects signal at boundaries - assumes periodicity?
   - **Periodic padding:** Best for circadian, wrong for transient events
   - **Predictive padding:** Extrapolate using AR model - computational cost?

2. **Boundary Wavelets:**
   - Cohen-Daubechies-Vial (CDV) boundary wavelets: Worth implementing?
   - Do they truly eliminate COI or just reduce it?
   - Computational overhead vs. benefit?

3. **COI Handling:**
   - **Mask COI:** Don't report values in COI (loss of data)
   - **Report with uncertainty:** Show COI but mark as "low confidence"
   - **Extrapolate:** Use model to estimate what would happen if signal continued

4. **Biological Considerations:**
   - If transient event is at boundary, is any method reliable?
   - Should we require "buffer zones" in experimental design (record longer than needed)?
   - Can we validate edge estimates against extended recordings?

**Deliverable Needed:**
- Edge effect mitigation comparison: Padding methods × Biological signal types
- CDV boundary wavelet implementation (if justified)
- Best practices guide: "Designing Wavelet Experiments for Biological Edges"

---

### Question 10: Custom Biological Wavelets - Research Novelty or Over-Engineering?

**Research Need:**  
Standard wavelets (Morlet, Daubechies) are generic. Could custom wavelets optimized for biological shapes improve performance?

**Specific Questions:**
1. **Biological Waveform Shapes:**
   - **Circadian:** Asymmetric (12h day, 12h night but different amplitudes)
   - **Cell cycle:** Exponential growth + sharp division = sawtooth-like
   - **Stress response:** Exponential decay with overshoot
   - **Action potentials:** Stereotyped spike shape in neural recordings

2. **Custom Wavelet Design:**
   - Can we parameterize biological shape (e.g., skewed Gaussian for circadian)?
   - Matching pursuit: Learn optimal wavelet basis from data?
   - Admissibility condition: Do custom shapes satisfy wavelet requirements?

3. **Performance Gains:**
   - Synthetic test: Custom vs. Morlet for known biological shape
   - Real data: Does custom wavelet improve period detection accuracy?
   - Is improvement significant enough to justify added complexity?

4. **Research Precedents:**
   - Are there published custom wavelets for biological signals?
   - EEG analysis: Custom wavelets for specific brain rhythms?
   - Genomics: Wavelets for DNA sequence analysis?

5. **Competitive Advantage:**
   - Would "circadian wavelet" be a publishable contribution?
   - Patent potential? (Probably not, but worth considering)
   - Marketing value: "Wavelets designed by biologists, for biologists"

**Deliverable Needed:**
- Literature review: Custom wavelets in signal processing (20+ papers)
- Prototype: Parameterized "circadian wavelet" implementation
- Performance comparison: Custom vs. Morlet on ≥5 circadian datasets
- Decision: Implement if >10% accuracy improvement, else use standard wavelets

---

### Question 11: Real-Time Streaming Wavelet Analysis

**Research Need:**  
Future applications (bioreactor monitoring, continuous physiological recording) require online analysis. Need causal, low-latency implementation.

**Specific Questions:**
1. **Causal Wavelets:**
   - Standard CWT uses future data (non-causal)
   - Can we design causal wavelets? (Half-width, asymmetric?)
   - What's the latency tradeoff? (1 cycle delay? 3 cycles?)

2. **Streaming Algorithms:**
   - **Sliding window:** Recompute CWT on last N points - inefficient
   - **Recursive update:** Can we update CWT incrementally? (New data → update scalogram)
   - **Batch processing:** Accumulate data, process every M minutes

3. **Latency Requirements:**
   - **Bioreactor:** 1-hour delay acceptable? (Slow dynamics)
   - **Neural recording:** <100ms required? (Fast dynamics)
   - **Cell imaging:** Frame rate determines max latency (1-10 seconds)

4. **Computational Constraints:**
   - Embedded systems (Raspberry Pi): Can they run real-time CWT?
   - Cloud streaming: AWS Kinesis + Lambda architecture?
   - Edge computing: Process locally vs. send to server?

5. **Triggering & Alerts:**
   - Detect anomalies in real-time: Period shift, amplitude drop
   - Automated alerts: "Circadian rhythm disrupted, check culture conditions"
   - False alarm rate: How to balance sensitivity vs. specificity?

**Deliverable Needed:**
- Streaming wavelet architecture diagram (data flow, processing nodes)
- Latency benchmarks: Sliding window vs. recursive update
- Prototype: Real-time wavelet monitor for synthetic data stream
- Decision: Implement in Phase 3 or defer to future product version

---

### Question 12: Competitive Tool Analysis - BioXen Positioning

**Research Need:**  
Multiple wavelet tools exist for biological signals. Need clear differentiation strategy and feature parity analysis.

**Specific Questions:**
1. **Direct Competitors:**
   - **per2py** (single-cell circadian wavelets): What features do they have?
   - **WaveletComp** (R package for biological time series): Functionality overlap?
   - **MetaCycle** (Lomb-Scargle for circadian): When to use wavelets vs. LS?

2. **Feature Comparison Matrix:**
   - Wavelet types supported (continuous, discrete, wavelet packets)
   - Biological validation datasets included
   - Statistical significance testing methods
   - Visualization quality (static plots vs. interactive)
   - Performance (small datasets vs. large-scale)
   - Ease of use (API design, documentation, tutorials)

3. **Unique Value Propositions:**
   - **Four-Lens Integration:** Only tool combining wavelets + Fourier + Laplace + Z?
   - **Interactive HTML Dashboard:** No coding required for biologists?
   - **Consensus Algorithm:** Multi-method validation built-in?
   - **Research-grade Validation:** Peer-reviewed benchmarks?

4. **Market Segments:**
   - **Academic researchers:** Need publication-quality plots, reproducible workflows
   - **Pharma/biotech:** Need validated, auditable methods (FDA/regulatory)
   - **Core facilities:** Need easy-to-use tools for non-expert users

5. **Pricing/Licensing Strategy:**
   - Open-source (MIT/BSD) for academic goodwill?
   - Freemium model: Basic free, advanced features paid?
   - Commercial license for industry users?

**Deliverable Needed:**
- Competitive analysis table: BioXen vs. per2py vs. WaveletComp vs. MetaCycle (15+ features)
- SWOT analysis (Strengths, Weaknesses, Opportunities, Threats)
- Market positioning statement: "BioXen is the only..."
- Feature roadmap: Gaps to fill to achieve competitive advantage

**Research Resources to Review:**
- per2py GitHub + documentation
- WaveletComp R package vignettes
- User reviews/discussions on biological forums (Biostars, ResearchGate)
- Citation counts: Which tools are most used in published research?

---

## 📋 Research Prioritization Matrix

| Question | Priority | Effort | Impact | Timeline |
|----------|----------|--------|--------|----------|
| Q1: Wavelet Coherence | 🔴 Critical | High | High | Week 3 (by Oct 15) |
| Q2: Validation Datasets | 🔴 Critical | Medium | Critical | Week 3 (by Oct 15) |
| Q3: HOSA Integration | 🔴 Critical | High | High | Week 3 (by Oct 20) |
| Q4: Wavelet Selection | 🟡 High | Medium | High | Phase 2 (by Nov 1) |
| Q5: Performance Benchmarks | 🟡 High | Medium | Critical | Phase 2 (by Nov 1) |
| Q6: Statistical Testing | 🟡 High | High | Critical | Phase 2 (by Nov 15) |
| Q7: Visualization Strategy | 🟡 High | High | Medium | Phase 2 (by Nov 15) |
| Q8: MRA Optimization | 🟢 Medium | Low | Medium | Phase 2-3 (by Dec 1) |
| Q9: Edge Effects | 🟢 Medium | Medium | Medium | Phase 3 (by Dec 15) |
| Q10: Custom Wavelets | 🟢 Medium | High | Low-Medium | Phase 3+ (TBD) |
| Q11: Real-Time Streaming | 🟢 Medium | High | Medium | Phase 3+ (2026) |
| Q12: Competitive Analysis | 🟡 High | Low | High | Ongoing |

---

## 🎓 Recommended Research Methodology

### For Each Question, Follow This Process:

1. **Literature Review** (2-4 hours per question)
   - Search Google Scholar, PubMed, arXiv
   - Focus on papers from last 5 years + seminal older papers
   - Create annotated bibliography with key takeaways

2. **Code Review** (1-2 hours per question)
   - Examine existing implementations (GitHub, MATLAB Central)
   - Note design decisions, optimizations, pitfalls
   - Test code on sample data to understand behavior

3. **Prototype Implementation** (4-8 hours per question)
   - Quick-and-dirty implementation in Jupyter notebook
   - Test on synthetic data with known ground truth
   - Iterate based on results

4. **Expert Consultation** (1-2 hours per question)
   - Biologist: "Is this biologically meaningful?"
   - Statistician: "Is this test statistically sound?"
   - Engineer: "Can this scale to production?"

5. **Decision Documentation** (1 hour per question)
   - Write 1-2 page summary: Question → Options → Recommendation → Justification
   - Add to BioXen technical documentation
   - Create GitHub issue to track implementation

### Total Estimated Research Time:
- **Critical questions (Q1-Q3):** ~60 hours (1.5 weeks full-time)
- **High priority (Q4-Q7):** ~80 hours (2 weeks full-time)
- **Medium priority (Q8-Q12):** ~100 hours (2.5 weeks full-time)
- **TOTAL:** ~240 hours (6 weeks full-time equivalent)

### Suggested Allocation:
- **Week 3 (Oct 7-13):** Q1 (Coherence) + Q2 (Validation) - 40 hours
- **Week 4 (Oct 14-20):** Q3 (HOSA) + Q4 (Selection) - 40 hours
- **Weeks 5-6 (Oct 21-Nov 3):** Q5-Q7 (Performance, Stats, Viz) - 60 hours
- **Weeks 7-10 (Nov 4-Dec 1):** Q8-Q12 (Optimization, polish) - 100 hours

---

## 📚 Essential Bibliography

### Wavelet Theory & Methods:
1. Mallat, S. (2008). *A Wavelet Tour of Signal Processing* (3rd ed.). Academic Press.
2. Addison, P. S. (2017). *The Illustrated Wavelet Transform Handbook* (2nd ed.). CRC Press.
3. Torrence, C., & Compo, G. P. (1998). A practical guide to wavelet analysis. *Bulletin of the American Meteorological Society*, 79(1), 61-78.

### Biological Applications:
4. Cazelles, B., et al. (2008). Wavelet analysis of ecological time series. *Oecologia*, 156(2), 287-304.
5. Leise, T. L. (2013). Wavelet analysis of circadian and ultradian behavioral rhythms. *Journal of Circadian Rhythms*, 11(1), 5.
6. Zhu, J., Shen, L., Blackburn, L., & Byun, D. Y. (2019). Wavelet-based analysis for biological signals. *Frontiers in Bioengineering and Biotechnology*, 7, 106.

### Statistical Methods:
7. Maraun, D., & Kurths, J. (2004). Cross wavelet analysis: significance testing and pitfalls. *Nonlinear Processes in Geophysics*, 11(4), 505-514.
8. Grinsted, A., Moore, J. C., & Jevrejeva, S. (2004). Application of the cross wavelet transform and wavelet coherence to geophysical time series. *Nonlinear Processes in Geophysics*, 11, 561-566.

### Higher-Order Spectral Analysis:
9. Nikias, C. L., & Mendel, J. M. (1993). Signal processing with higher-order spectra. *IEEE Signal Processing Magazine*, 10(3), 10-37.
10. Van Milligen, B. P., et al. (1995). Wavelet bicoherence: a new turbulence analysis tool. *Physics of Plasmas*, 2(8), 3017-3032.

### Computational Performance:
11. Torrence, C., & Webster, P. J. (1999). Interdecadal changes in the ENSO–monsoon system. *Journal of Climate*, 12(8), 2679-2690.
12. Liu, Y., Liang, X. S., & Weisberg, R. H. (2007). Rectification of the bias in the wavelet power spectrum. *Journal of Atmospheric and Oceanic Technology*, 24(12), 2093-2102.

---

## 🚀 Success Criteria

We will know we have successfully answered these research questions when:

1. ✅ **Technical Specification Complete:** Each question has a 2-5 page technical document with implementation details
2. ✅ **Prototype Validated:** Working code demonstrations for Q1-Q7 on real biological data
3. ✅ **Performance Benchmarked:** Quantitative metrics showing BioXen meets or exceeds existing tools
4. ✅ **Expert Review:** ≥2 external biologists + ≥1 biostatistician review and approve approach
5. ✅ **Documentation Updated:** All decisions incorporated into BioXen technical docs and API design
6. ✅ **Roadmap Adjusted:** Phase 2-3 timeline updated based on research findings

---

## 📞 Next Steps & Action Items

**Immediate Actions (This Week):**
1. [ ] Assign question ownership (who researches what?)
2. [ ] Set up shared bibliography (Zotero, Mendeley, or Notion database)
3. [ ] Create research progress tracking board (GitHub Projects or Trello)
4. [ ] Schedule weekly research review meetings (30-60 min)

**Week 3 Deliverables (Critical Path):**
1. [ ] Q1: Wavelet coherence technical spec + prototype
2. [ ] Q2: ≥3 validation datasets downloaded + metadata documented
3. [ ] Q3: HOSA integration decision document + architecture diagram

**Phase 2 Deliverables (By Nov 15):**
1. [ ] Q4-Q7: All high-priority questions answered with prototypes
2. [ ] Validation results: BioXen wavelets tested on ≥5 biological datasets
3. [ ] Performance report: Benchmarks on 1k-1M timepoint datasets
4. [ ] Updated Phase 2 timeline based on research findings

---

## 📝 Document Change Log

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2025-10-02 | 2.0 | Initial deep research prompt created from Phase 1 analysis | Analysis of wavelets.html + research doc |

---

## 🔗 Related Documents

- **Phase 1 Implementation:** `research/interactive-fourier-series/lenses/wavelets.html`
- **Research Foundation:** `research/interactive-fourier-series/research/Wavelet Analysis for Biological Signals.md`
- **Original Research Prompt:** `wavelets-deep-research-prompt.md` (if exists)
- **BioXen Architecture:** `research/interactive-fourier-series/research/BioXen Signal Analysis Research Plan.md`

---

**END OF DEEP RESEARCH PROMPT**

*This document is a living document and should be updated as research questions are answered and new questions emerge.*
