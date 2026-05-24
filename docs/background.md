# Background

A random field is a collection of random variables indexed by space, time, or another continuum. In this paper each realization is a curve or map, so one simulation is a vector after discretization, but the mathematical object is a function.

Functional quantization (FQ) approximates a random field by a finite set of representative functions called quanta. Each quantum owns a tassel, the set of realizations closer to that quantum than to any other. The approximation is useful when a full Monte Carlo ensemble is too large but downstream calculations need probabilities, fields, and spatial dependence.

Centroidal Voronoi tessellation (CVT) is the fixed-point condition for optimal squared-error quantization: every quantum equals the conditional mean of the realizations in its tassel. Lloyd's algorithm alternates between assigning each realization to the nearest quantum and replacing each quantum by the mean of its assigned realizations. This monotonically decreases distortion until the assignments and centroids stabilize.

The benchmark studies how different clustering algorithms reach, approximate, or avoid the CVT condition. One-pass methods are fast but generally do not satisfy CVT. Lloyd-family methods cost more but usually produce lower distortion and better distributional fidelity.
