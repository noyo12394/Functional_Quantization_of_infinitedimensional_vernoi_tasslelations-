# Algorithms

The code names match the paper and the benchmark notebook. Each algorithm implements `FQAlgorithm.step(Xr, seed)` and returns time, SSE, iteration count, and centers.


| Code | Full name | Paper section | Big-O complexity | Achieves CVT | Novel in this paper |
|------|-----------|---------------|-----------------|--------------|---------------------|
| LX | Lloyd exhaustive (random init) | 2.2.1 | O(N_sim · N · R · n_iter) | Yes | No |
| LE | Lloyd + Elkan triangle inequality | 2.2.2 | O(N_sim · N · R + N² · R · n_iter) | Yes | No |
| HT | Agglomerative hierarchical (Ward) | 2.2.3 | O((N_sim − N)² · R) | No | No |
| KN | Exhaustive k-NN one-pass | 2.2.5 | O(N_sim · N · R) | No | No |
| LK | Lloyd with k-means++ init | 2.2.7 | O(N_sim · N · R · n_iter) | Yes | Yes (hybrid) |
| HK | Hierarchical-init → Lloyd refine | — | O((N_sim−N)²·R + N_sim·N·R·n_iter) | Yes | Yes |
| MB | MiniBatch k-means | — | O(N_sim · N · R) | Approx | No |
| ANN-FQ | NearestNeighbors one-pass | — | O(N_sim · N · R) | No | No |
| RP-ANN-FQ | Random Projection + ANN | — | O(N_sim · R · d + N_sim · N · d) | No | Yes |
| KD-ANN-FQ | KDTree ANN one-pass | — | O(N_sim · N · R) | No | No |
| MR-FQ | Multi-resolution FQ | — | O(N_sim·N·R_coarse + N_sim·N·R·n_fine) | Yes | Yes |
| CE-LE | Continuation Elkan across R | — | O(N_sim · N · R · n_iter) warm | Yes | Yes |
| CE-MB | Continuation MiniBatch across R | — | O(N_sim · N · R) warm | Approx | Yes |
| SVD-CE-LE | TruncatedSVD + Elkan refine | — | O(N_sim · p · R + N_sim · N · R · 2) | Yes | Yes |
| RP-CE-LE | Random Projection + Continuation Elkan | — | O(N_sim · R · d + N_sim · N · d · n_iter) | Yes | Yes |


To extend the benchmark, subclass `fq.algorithms.base.FQAlgorithm`, implement `step`, and register the class in `fq.algorithms.ALGORITHMS`.
