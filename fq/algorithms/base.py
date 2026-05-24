from abc import ABC, abstractmethod

import numpy as np


class FQAlgorithm(ABC):
    """Abstract interface for one functional quantization algorithm."""

    name: str
    heavy: bool = False

    def __init__(self, n_quanta: int, max_iter: int, tol: float) -> None:
        self.K = int(n_quanta)
        self.max_iter = int(max_iter)
        self.tol = float(tol)

    @property
    def supports_warm_start(self) -> bool:
        """Return whether the algorithm carries centers between resolutions."""
        return False

    @abstractmethod
    def step(self, Xr: np.ndarray, seed: int) -> dict:
        """Run one experiment.

        Args:
            Xr: Interpolated realizations with shape ``(N_sim, R)``.
            seed: Experiment seed.

        Returns:
            Dictionary containing ``time``, ``sse``, ``iter``, and ``centers``.
        """
