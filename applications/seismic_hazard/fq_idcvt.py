import gc
import time

import numpy as np

from .simulation import simulate_maps


def fq_idcvt(N: int, rng: np.random.Generator, max_iter: int = 150, tol: float = 1e-4,
             nsim_factor: int = 100, npsim_factor: int = 1000, verbose: bool = False):
    """Run FQ-IDCVT for the seismic hazard application.

    Args:
        N: Quantizer size. The paper uses N = 50 and N = 200.
        rng: Random number generator.
        max_iter: Maximum Lloyd iterations.
        tol: Five-step relative distortion tolerance.
        nsim_factor: Training samples per quantum.
        npsim_factor: Weight-estimation samples per quantum.
        verbose: Print convergence progress.

    Returns:
        Tuple ``(quanta, weights, info)`` in ln(Sa) space.
    """
    N_sim = int(nsim_factor * N)
    N_psim = int(npsim_factor * N)
    chunk = 20_000
    t0 = time.perf_counter()
    X = simulate_maps(N_sim, rng)
    quanta = X[rng.choice(N_sim, int(N), replace=False)].copy()
    distortions = []
    for it in range(1, int(max_iter) + 1):
        X2 = np.sum(X * X, axis=1, keepdims=True)
        Q2 = np.sum(quanta * quanta, axis=1, keepdims=True).T
        D2 = np.maximum(X2 + Q2 - 2.0 * (X @ quanta.T), 0.0)
        labels = np.argmin(D2, axis=1)
        new_q = np.zeros_like(quanta)
        for j in range(int(N)):
            idx = np.where(labels == j)[0]
            new_q[j] = X[idx].mean(axis=0) if idx.size else X[rng.integers(0, N_sim)]
        delta = float(np.sum(np.min(D2, axis=1)))
        if distortions and delta > distortions[-1]:
            delta = distortions[-1]
        distortions.append(delta)
        quanta = new_q
        if verbose and (it == 1 or it % 10 == 0):
            print(f"iter {it:3d} distortion={delta:.4e}")
        if it >= 5:
            rel = abs(distortions[-5] - delta) / max(delta, 1e-12)
            if rel < tol:
                break
    counts = np.zeros(int(N), dtype=np.int64)
    done = 0
    Q2 = np.sum(quanta * quanta, axis=1, keepdims=True).T
    while done < N_psim:
        nc = min(chunk, N_psim - done)
        Xp = simulate_maps(nc, rng)
        X2p = np.sum(Xp * Xp, axis=1, keepdims=True)
        D2p = np.maximum(X2p + Q2 - 2.0 * (Xp @ quanta.T), 0.0)
        counts += np.bincount(np.argmin(D2p, axis=1), minlength=int(N))
        done += nc
        del Xp, X2p, D2p
        gc.collect()
    weights = counts / max(N_psim, 1)
    info = dict(n_iter=it, distortions=distortions, final_distortion=distortions[-1], elapsed=time.perf_counter() - t0)
    return quanta, weights, info
