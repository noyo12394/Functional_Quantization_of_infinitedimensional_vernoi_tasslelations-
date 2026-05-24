from pathlib import Path
from typing import Optional, Union

import numpy as np
import pandas as pd


def synthesize_paper_data(nsim: int = 3000, R: int = 512, b: float = 1.0,
                          sigma: float = 1.0, mu: float = 2.0,
                          seed: int = 20260120) -> np.ndarray:
    """Generate the synthetic lognormal process used as a paper fallback.

    Args:
        nsim: Number of random-field realizations.
        R: Number of discretization points.
        b: Correlation-scale parameter in the spectrum.
        sigma: Gaussian-process scale.
        mu: Lognormal location parameter.
        seed: Random seed.

    Returns:
        Array with shape ``(nsim, R)``.
    """
    rng = np.random.default_rng(seed)
    omega_u = 30.0
    m_terms = 512
    domega = omega_u / m_terms
    omegas = (np.arange(m_terms) + 0.5) * domega
    spectrum = (sigma ** 2) * (b ** 3) * (omegas ** 2) / 4.0 * np.exp(-b * omegas ** 2)
    amp = np.sqrt(2.0 * spectrum * domega)
    x = np.linspace(0.0, 200.0, R)
    phases = rng.uniform(0.0, 2.0 * np.pi, size=(nsim, m_terms))
    gaussian = np.zeros((nsim, R), dtype=np.float64)
    for k, omega in enumerate(omegas):
        gaussian += amp[k] * np.cos(omega * x[None, :] + phases[:, k:k + 1])
    return np.exp(mu + gaussian).astype(np.float64)


def load_csv(path: Union[str, Path], nsim: Optional[int] = None) -> np.ndarray:
    """Load realizations from a CSV file.

    Args:
        path: CSV path with one realization per row.
        nsim: Optional number of rows to keep.

    Returns:
        Numeric array of realizations.
    """
    data = pd.read_csv(Path(path), header=None).to_numpy(dtype=float)
    return data[:nsim].copy() if nsim is not None else data
