import time
from typing import Optional

import numpy as np
from sklearn.cluster import AgglomerativeClustering, KMeans, MiniBatchKMeans
from sklearn.decomposition import TruncatedSVD
from sklearn.neighbors import KDTree, NearestNeighbors
from sklearn.random_projection import GaussianRandomProjection

from fq.core import assign_labels, centroids_from_labels, compute_sse

from .base import FQAlgorithm


def _sample_centers(Xr: np.ndarray, K: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    idx = rng.choice(Xr.shape[0], size=K, replace=False)
    return Xr[idx].copy()


def _one_pass(Xr: np.ndarray, seed: int, K: int, projected: Optional[np.ndarray] = None,
              center_projected: Optional[np.ndarray] = None, use_kdtree: bool = False) -> dict:
    rng = np.random.default_rng(seed)
    centers0 = _sample_centers(Xr, K, seed)
    if projected is None:
        work_X = Xr
        work_C = centers0
    else:
        work_X = projected
        work_C = center_projected
    t0 = time.perf_counter()
    if use_kdtree:
        labels = KDTree(work_C).query(work_X, k=1, return_distance=False).ravel()
    else:
        labels = NearestNeighbors(n_neighbors=1, algorithm="auto").fit(work_C).kneighbors(work_X, return_distance=False).ravel()
    centers = centroids_from_labels(Xr, labels, K, rng)
    labels = assign_labels(Xr, centers)
    sse = compute_sse(Xr, centers, labels)
    return dict(time=time.perf_counter() - t0, sse=sse, iter=1, centers=centers)


def _kmeans_step(Xr: np.ndarray, seed: int, K: int, max_iter: int, tol: float,
                 algorithm: str = "lloyd", init: str | np.ndarray = "random") -> dict:
    km = KMeans(n_clusters=K, init=init, n_init=1, max_iter=max_iter, tol=tol,
                algorithm=algorithm, random_state=seed)
    t0 = time.perf_counter()
    km.fit(Xr)
    return dict(time=time.perf_counter() - t0, sse=float(km.inertia_),
                iter=int(km.n_iter_), centers=km.cluster_centers_.copy())

class ANNFQ(FQAlgorithm):
    name = "ANN-FQ"

    def step(self, Xr: np.ndarray, seed: int) -> dict:
        return _one_pass(Xr, seed, self.K)
