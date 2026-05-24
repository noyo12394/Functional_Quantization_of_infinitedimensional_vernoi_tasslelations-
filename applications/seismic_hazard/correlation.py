import numpy as np

B_EPS_KM = 8.5  # Jayaram & Baker (2009), T=0.1 s. Domain correction: not 20.0.
SIGMA_EPS = 0.60


def jb2009_rho(h, b: float = B_EPS_KM):
    """Jayaram and Baker (2009) spatial correlation rho(h) = exp(-3h/b)."""
    return np.exp(-3.0 * np.asarray(h, dtype=float) / b)
