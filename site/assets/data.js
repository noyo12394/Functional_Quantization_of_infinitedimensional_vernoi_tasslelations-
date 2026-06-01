// ============================================================
//  Research data — transcribed from the paper's results tables
//  "Computational techniques for disaster scenario selection"
//  Mursel, Chatterjee, Conus, Huang, Miranda & Bocchini (2026)
// ============================================================

// Table 5 — Composite time–quality trade-off score (w_t = w_q = 0.5). Lower = better.
const COMPOSITE = [
  { code: "Ultra-Fast", name: "Ultra-Fast CVT",  score: 0.089, cvt: "Approx." },
  { code: "LK",         name: "Lloyd + k-means++ (LK)", score: 0.143, cvt: "Yes" },
  { code: "ANN-FQ",     name: "Ball-Tree ANN-FQ", score: 0.157, cvt: "No" },
  { code: "RP-ANN-FQ",  name: "Random-Projection ANN", score: 0.198, cvt: "No" },
  { code: "MR-FQ",      name: "Multi-resolution FQ", score: 0.213, cvt: "No" },
  { code: "KD-ANN-FQ",  name: "KD-Tree ANN-FQ", score: 0.231, cvt: "No" },
  { code: "KN",         name: "Exhaustive k-NN (KN)", score: 0.254, cvt: "No" },
  { code: "MB",         name: "MiniBatch k-means", score: 0.312, cvt: "No" },
  { code: "LE",         name: "Lloyd–Elkan (LE)", score: 0.387, cvt: "Yes" },
  { code: "LX",         name: "Lloyd exhaustive (LX)", score: 0.401, cvt: "Yes" },
  { code: "KM",         name: "k-means++ (KM)", score: 0.445, cvt: "No" },
  { code: "HT",         name: "Hierarchical / Ward (HT)", score: 0.712, cvt: "No" },
  { code: "EM/GMM",     name: "EM / Gaussian Mixture", score: 0.982, cvt: "No" },
];

// Table 2 — Mean wall-clock time (s) per algorithm at each resolution R.
const R_LEVELS = [128, 256, 512, 1024, 2048, 4096, 8192, 16384];
const TIMING = {
  "LX":         [0.0197, 0.0276, 0.0402, 0.0559, 0.1139, 0.2228, 0.4485, 0.8724],
  "LE":         [0.0216, 0.0261, 0.0366, 0.0547, 0.1029, 0.2030, 0.3962, 0.7711],
  "LK":         [0.0219, 0.0335, 0.0460, 0.0666, 0.1256, 0.2447, 0.4319, 0.8691],
  "HT":         [0.1869, 0.3070, 0.5699, 1.1668, 2.1726, 4.4644, 8.3403, 16.338],
  "KN":         [0.00567,0.00581,0.00681,0.00795,0.01416,0.02313,0.04599,0.07558],
  "KM":         [0.0380, 0.3707, 0.5120, 0.9507, 1.7021, 2.1472, 4.9141, 10.591],
  "EM/GMM":     [1.1849, 1.2912, 2.5816, 2.1576, 3.3106, 4.2880, 6.8119, 12.991],
  "ANN-FQ":     [0.2945, 0.7305, 1.9098, 4.0156, 8.3514, 16.855, 29.676, 53.829],
  "RP-ANN-FQ":  [0.1962, 0.4406, 0.4632, 0.4617, 0.5583, 0.9724, 1.4671, 1.9036],
  "KD-ANN-FQ":  [0.3559, 1.0629, 2.0880, 4.4204, 9.1021, 18.048, 31.858, 57.796],
  "MB":         [0.1088, 0.4822, 0.7668, 1.1971, 1.8797, 2.8433, 6.0285, 10.956],
  "HK":         [0.1143, 0.4502, 0.5142, 1.2094, 2.4524, 4.2521, 7.1113, 11.523],
  "MR-FQ":      [0.0409, 0.0449, 0.0512, 0.3803, 0.7233, 1.1073, 1.7846, 3.0643],
  "Ultra-Fast": [0.3174, 0.2807, 0.2844, 0.3183, 0.3252, 0.3180, 0.3139, 0.2957],
};

// Table 3 — Algorithms ranked by mean time across all R.
const MEAN_TIME = [
  { code: "KN", t: 0.0231 }, { code: "LE", t: 0.2015 }, { code: "LX", t: 0.2251 },
  { code: "LK", t: 0.2299 }, { code: "Ultra-Fast", t: 0.3067 }, { code: "RP-ANN-FQ", t: 0.8079 },
  { code: "MR-FQ", t: 0.8996 }, { code: "KM", t: 2.6532 }, { code: "MB", t: 3.0328 },
  { code: "HK", t: 3.4534 }, { code: "HT", t: 4.1932 }, { code: "EM/GMM", t: 4.3271 },
  { code: "ANN-FQ", t: 14.458 }, { code: "KD-ANN-FQ", t: 15.591 },
];

// Algorithm registry — complexity & character (paper Table 1 + narrative).
const ALGOS = {
  "Ultra-Fast": { color:"#ff7a3d", cvt:"Approx.", novel:true,  big:"O(N·N·d·n_burst)", blurb:"Continuation warm-starts + random projection + adaptive early stopping. Wall-clock time is essentially independent of resolution R." },
  "LK":         { color:"#d62246", cvt:"Yes",     novel:true,  big:"O(N·N·R·n_iter)", blurb:"Lloyd with k-NN (k-means++) initialization. Same CVT quality as LX but fewer iterations — the recommended default." },
  "LE":         { color:"#e8590c", cvt:"Yes",     novel:false, big:"O(N·N·R + N²·R·n_iter)", blurb:"Lloyd accelerated by Elkan's triangle inequality. The most accurate fast alternative to LX (~66% faster at high R)." },
  "LX":         { color:"#868e96", cvt:"Yes",     novel:false, big:"O(N·N·R·n_iter)", blurb:"Exhaustive Lloyd search — the baseline FQ-IDCVT loop. Exact CVT, but cost scales linearly in R." },
  "KN":         { color:"#2fd07f", cvt:"No",      novel:false, big:"O(N·N·R)", blurb:"Exhaustive k-NN one-pass. The fastest method at every resolution (0.006 → 0.076 s); ideal when approximate scenarios suffice." },
  "MR-FQ":      { color:"#4dabf7", cvt:"No",      novel:true,  big:"O(N·N·R_coarse + N·N·R·n_fine)", blurb:"Multi-resolution FQ: cluster cheaply on a coarse grid, lift centroids, then refine on the fine grid." },
  "RP-ANN-FQ":  { color:"#9775fa", cvt:"No",      novel:true,  big:"O(N·R·d + N·N·d)", blurb:"Random-projection dimensionality reduction feeding approximate nearest-neighbour CVT. Strong at high R under memory limits." },
  "ANN-FQ":     { color:"#3bc9db", cvt:"No",      novel:false, big:"O(N·N·R)", blurb:"Ball-Tree approximate NN CVT. Low distortion, but tree rebuilds each iteration make it costly at high R." },
  "KD-ANN-FQ":  { color:"#1098ad", cvt:"No",      novel:false, big:"O(N·N·R)", blurb:"KD-Tree variant of ANN-FQ. Same iterative tree-rebuild overhead — slowest at high R despite low per-query cost." },
  "MB":         { color:"#f783ac", cvt:"Approx.", novel:false, big:"O(N·N·R)", blurb:"MiniBatch k-means. Processes data in chunks — the choice for streaming or memory-bound pipelines." },
  "KM":         { color:"#ffd43b", cvt:"No",      novel:false, big:"O(N·N·R·n_iter)", blurb:"Standard k-means++ — simple and widely available; good for prototyping moderate problems." },
  "HK":         { code:"HK", color:"#a9e34b", cvt:"Yes", novel:true, big:"O((N−N)²·R + N·N·R·n_iter)", blurb:"Hierarchical-init then Lloyd refine — reaches CVT but inherits the quadratic cost of the hierarchical seeding." },
  "HT":         { color:"#7048e8", cvt:"No",      novel:false, big:"O((N−N)²·R)", blurb:"Agglomerative Ward hierarchical tree. Highest distortion and largest cost on big sample sets — avoid for high-D FQ." },
  "EM/GMM":     { color:"#f06595", cvt:"No",      novel:false, big:"O(R³ per iter)", blurb:"Expectation–Maximization with Gaussian mixtures. The O(R³) covariance dominates — slowest above R = 512." },
};

// Practical selection guide — Table 7.
const GUIDE = [
  { use:"Small problem (R ≤ 512, N_sim ≤ 1,000)", rec:"LX or LK", why:"Full CVT accuracy guaranteed; cost < 0.1 s per run." },
  { use:"Moderate problem (512 < R ≤ 2048)", rec:"LK or LE", why:"Same CVT quality as LX with fewer iterations and stable init; LE adds triangle-inequality acceleration." },
  { use:"High-resolution (R > 2048)", rec:"Ultra-Fast CVT / RP-ANN-FQ", why:"~2 orders of magnitude faster than LX at near-CVT quality. Ultra-Fast minimizes distortion; RP-ANN-FQ saves memory." },
  { use:"CVT required, high R", rec:"LK", why:"Best CVT-achieving method overall; LE second; LX when reproducibility outranks speed." },
  { use:"Approximate OK, time-critical", rec:"KN or ANN-FQ", why:"KN is fastest at every R; ANN-FQ gives lower distortion at modest extra cost." },
  { use:"Batch or streaming data", rec:"MB", why:"Mini-batch updates avoid loading the full realization set into memory." },
  { use:"Exploration / prototyping", rec:"KM (k-means++)", why:"Simple, widely available, good accuracy on moderate problems." },
];

// ---- Seismic Hazard-Quantization application (this study's recalculation) ----
// Method comparison at high-resolution grid (smoke-test config, N = 50).
const SEISMIC_METHODS = [
  { code:"LX",    label:"Lloyd (random init)",     sse:"1.600e5", rd:"+0.00", iters:7,  fit:0.05, varc:26.8, exc:0.2880 },
  { code:"LK",    label:"Lloyd (k-means++)",       sse:"1.605e5", rd:"+0.34", iters:8,  fit:0.14, varc:27.0, exc:0.2730 },
  { code:"LE",    label:"Elkan (k-means++)",       sse:"1.593e5", rd:"-0.44", iters:10, fit:0.07, varc:27.2, exc:0.2720 },
  { code:"MB",    label:"MiniBatch k-means",       sse:"1.591e5", rd:"-0.55", iters:34, fit:0.30, varc:26.0, exc:0.2665 },
  { code:"MR-FQ", label:"Multi-resolution FQ",     sse:"1.585e5", rd:"-0.90", iters:2,  fit:0.13, varc:27.2, exc:0.2710 },
];

// N-sensitivity sweep (Lloyd k-means++).
const SEISMIC_N = [
  { N:50,  varc:27.3, exc:0.3130, acf:0.6176 },
  { N:100, varc:28.1, exc:0.2615, acf:0.5862 },
  { N:200, varc:29.8, exc:0.2174, acf:0.5646 },
];

// Resolution-scaling study (LK).
const SEISMIC_RES = [
  { label:"Base 16×14",  sites:224, fit:0.063, exc:0.2625, acf:0.6784 },
  { label:"High 24×21",  sites:504, fit:0.143, exc:0.2710, acf:0.6383 },
];
