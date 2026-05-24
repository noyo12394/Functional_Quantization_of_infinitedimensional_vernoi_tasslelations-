import numpy as np


def interpolate_dataset(X: np.ndarray, R_new: int) -> np.ndarray:
    """Linearly interpolate rows of a dataset onto a new grid length."""
    X = np.asarray(X, dtype=float)
    n_rows, R_old = X.shape
    if R_new == R_old:
        return X.copy()
    old_grid = np.linspace(0.0, 1.0, R_old)
    new_grid = np.linspace(0.0, 1.0, R_new)
    out = np.empty((n_rows, R_new), dtype=float)
    for i in range(n_rows):
        out[i] = np.interp(new_grid, old_grid, X[i])
    return out


def interpolate_centroids(C_old: np.ndarray, R_target: int) -> np.ndarray:
    """Linearly interpolate centroids onto a target grid length."""
    C_old = np.asarray(C_old, dtype=float)
    k_rows, R_old = C_old.shape
    if R_target == R_old:
        return C_old.copy()
    old_grid = np.linspace(0.0, 1.0, R_old)
    new_grid = np.linspace(0.0, 1.0, R_target)
    out = np.empty((k_rows, R_target), dtype=float)
    for k in range(k_rows):
        out[k] = np.interp(new_grid, old_grid, C_old[k])
    return out


def assign_labels(X: np.ndarray, centers: np.ndarray) -> np.ndarray:
    """Assign every row in ``X`` to its nearest center."""
    x2 = np.sum(X * X, axis=1, keepdims=True)
    c2 = np.sum(centers * centers, axis=1, keepdims=True).T
    d2 = np.maximum(x2 + c2 - 2.0 * (X @ centers.T), 0.0)
    return np.argmin(d2, axis=1)


def compute_sse(X: np.ndarray, centers: np.ndarray, labels: np.ndarray) -> float:
    """Compute sum of squared Euclidean distances to assigned centers."""
    return float(np.sum((X - centers[np.asarray(labels, dtype=int)]) ** 2))


def compute_distortion(X: np.ndarray, centers: np.ndarray) -> float:
    """Compute nearest-center distortion without requiring precomputed labels."""
    labels = assign_labels(np.asarray(X, dtype=float), np.asarray(centers, dtype=float))
    return compute_sse(X, centers, labels)


def centroids_from_labels(X: np.ndarray, labels: np.ndarray, K: int, rng: np.random.Generator) -> np.ndarray:
    """Compute cluster means, reseeding empty clusters from data rows."""
    centers = np.zeros((K, X.shape[1]), dtype=float)
    labels = np.asarray(labels, dtype=int)
    for k in range(K):
        idx = np.where(labels == k)[0]
        centers[k] = X[idx].mean(axis=0) if idx.size else X[rng.integers(0, X.shape[0])]
    return centers
