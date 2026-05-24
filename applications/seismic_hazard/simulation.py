import numpy as np
from typing import Optional

from .correlation import SIGMA_EPS, jb2009_rho
from .geometry import R_GRID, fault_segs, points_xy, pt_to_seg_dist, rupture_endpoints
from .gmm import as97_ln_sa, rupture_length_km


def distance_matrix(points=points_xy) -> np.ndarray:
    """Compute the inter-site distance matrix."""
    diff = points[:, None, :] - points[None, :, :]
    return np.sqrt(np.sum(diff ** 2, axis=2))


def cholesky_factor(points=points_xy) -> np.ndarray:
    """Build the Cholesky factor for corrected J&B 2009 residual covariance."""
    H = distance_matrix(points)
    C = SIGMA_EPS ** 2 * jb2009_rho(H)
    C[np.arange(C.shape[0]), np.arange(C.shape[0])] += 1e-8
    return np.linalg.cholesky(C)


def sample_epsilon(rng: np.random.Generator, L_chol: Optional[np.ndarray] = None) -> np.ndarray:
    """Draw one spatially correlated intra-event residual field."""
    if L_chol is None:
        L_chol = cholesky_factor()
    return L_chol @ rng.standard_normal(R_GRID)


def simulate_maps(nsim: int, rng: np.random.Generator, L_chol: Optional[np.ndarray] = None) -> np.ndarray:
    """Generate spatially correlated ln(Sa) intensity-measure maps."""
    if L_chol is None:
        L_chol = cholesky_factor()
    X = np.empty((int(nsim), R_GRID), dtype=float)
    for i in range(int(nsim)):
        seg = "AB" if rng.uniform() < 0.5 else "CD"
        p0, p1 = fault_segs[seg]
        t = rng.uniform()
        epi = (1.0 - t) * p0 + t * p1
        M = float(rng.triangular(5.5, 6.0, 6.5))
        d = float(rng.triangular(2.0, 4.0, 6.0))
        L = rupture_length_km(M)
        rs, re = rupture_endpoints(epi, seg, L)
        hd = pt_to_seg_dist(points_xy, rs, re)
        X[i] = as97_ln_sa(M, np.sqrt(hd ** 2 + d ** 2)) + sample_epsilon(rng, L_chol)
    return X
