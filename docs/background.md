# Background

A random field is a collection of random variables indexed by space, time, or another continuum. In this paper each realization is a curve or map, so one simulation is stored as a vector after discretization, but the mathematical object is a function.

Functional quantization (FQ) approximates a random field by a finite set of representative functions called quanta. Each quantum owns a tassel, the set of realizations closer to that quantum than to any other under an $L^2$ distance. The approximation is useful when a full Monte Carlo ensemble is too large but downstream calculations still need probabilities, fields, and spatial dependence.

The multidimensional FQ-IDCVT workflow has four moving parts. First, simulate realizations from a prescribed probabilistic description such as a spectrum, marginal distribution, or spatial correlation model. Second, assign each realization to its nearest quantum. Third, update each quantum to the average of the realizations in its tassel. Fourth, repeat assignment and averaging until the distortion, or total within-tassel squared error, stabilizes. After convergence, estimate each quantum's probability mass from the fraction of simulations assigned to its tassel.

Centroidal Voronoi tessellation (CVT) is the fixed-point condition for optimal squared-error quantization: every quantum equals the conditional mean of the realizations in its tassel. Lloyd's algorithm alternates between assigning each realization to the nearest quantum and replacing each quantum by the mean of its assigned realizations. This monotonically decreases distortion until the assignments and centroids stabilize.

The benchmark studies how different clustering algorithms reach, approximate, or avoid the CVT condition. One-pass methods are fast but generally do not satisfy CVT. Lloyd-family methods cost more but usually produce lower distortion and better distributional fidelity. The central engineering tradeoff is therefore not simply "which method is most accurate," but which method gives enough fidelity for a target random-field application at a feasible computational cost.

This repository intentionally separates theory, implementation, and results. The theory notes summarize the method and notation; package modules contain executable algorithms; `results/sample/` contains small visible outputs for repository inspection; large paper-scale outputs belong in `results/runtime/` unless explicitly curated for release.
