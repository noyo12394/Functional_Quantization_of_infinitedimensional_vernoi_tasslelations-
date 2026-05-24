import numpy as np
import pandas as pd
from typing import Optional

from .core import interpolate_dataset


def relative_distortion(results: dict, benchmark: str = "LX") -> pd.DataFrame:
    """Compute relative distortion against a benchmark method."""
    base = results[benchmark]
    rows = []
    for name, payload in results.items():
        if name == benchmark:
            continue
        for R in payload.get("R_list", []):
            if R not in base.get("R_list", []):
                continue
            i = payload["R_list"].index(R); j = base["R_list"].index(R)
            sse_m = np.asarray(payload["all_sse"][i], dtype=float)
            sse_b = np.asarray(base["all_sse"][j], dtype=float)
            n = min(len(sse_m), len(sse_b))
            if n == 0:
                continue
            rd = (sse_m[:n] - sse_b[:n]) / np.where(sse_b[:n] == 0, np.nan, sse_b[:n])
            for exp, val in enumerate(rd):
                if np.isfinite(val):
                    rows.append(dict(method=name, R=int(R), exp=exp, RD=float(val)))
    return pd.DataFrame(rows)


def empirical_pdf(values, grid_n=128, lo=None, hi=None):
    v = np.asarray(values, dtype=float).ravel(); v = v[np.isfinite(v)]
    if lo is None: lo = float(v.min())
    if hi is None: hi = float(v.max())
    bins = np.linspace(lo, hi, grid_n + 1)
    h, edges = np.histogram(v, bins=bins, density=True)
    centers = 0.5 * (edges[:-1] + edges[1:])
    return centers, h, edges


def empirical_acf(samples: np.ndarray, max_lag: Optional[int] = None) -> np.ndarray:
    """Estimate row-wise autocorrelation averaged over samples."""
    samples = np.asarray(samples, dtype=float)
    _, R = samples.shape
    if max_lag is None:
        max_lag = R - 1
    out = np.zeros(max_lag + 1, dtype=float)
    centered = samples - samples.mean(axis=1, keepdims=True)
    var = (centered ** 2).mean(axis=1, keepdims=True) + 1e-12
    centered = centered / np.sqrt(var)
    for lag in range(max_lag + 1):
        out[lag] = 1.0 if lag == 0 else float(np.mean(centered[:, :R - lag] * centered[:, lag:]))
    return out


def accuracy_metrics(results: dict, X_ref: np.ndarray, R_ref: int) -> pd.DataFrame:
    """Compute M1-M4 PDF and autocorrelation fidelity metrics."""
    Xr = interpolate_dataset(X_ref, R_ref) if X_ref.shape[1] != R_ref else X_ref
    _, ref_pdf, edges = empirical_pdf(Xr, grid_n=128)
    ref_acf = empirical_acf(Xr, max_lag=min(200, R_ref - 1))
    rows = []
    for name, payload in results.items():
        centers_list = payload.get("centers_ref") or []
        vals = []
        for centers in centers_list:
            C = np.asarray(centers, dtype=float)
            if C.ndim != 2 or C.shape[1] != R_ref:
                continue
            qpdf, _ = np.histogram(C.ravel(), bins=edges, density=True)
            qacf = empirical_acf(C, max_lag=min(200, R_ref - 1))
            diff_pdf = np.abs(qpdf - ref_pdf)
            diff_acf = np.abs(qacf - ref_acf)
            vals.append((diff_pdf.mean(), diff_pdf.max(), diff_acf.mean(), diff_acf.max()))
        if vals:
            arr = np.asarray(vals, dtype=float)
            rows.append(dict(method=name, n=len(vals), M1=arr[:, 0].mean(), M2=arr[:, 1].mean(),
                             M3=arr[:, 2].mean(), M4=arr[:, 3].mean()))
    return pd.DataFrame(rows)


def iter_to_cvt_df(results: dict, methods=("LX", "LK", "LE")) -> pd.DataFrame:
    """Return recorded iterations for CVT-capable methods."""
    rows = []
    for method in methods:
        if method not in results:
            continue
        payload = results[method]
        for i, R in enumerate(payload.get("R_list", [])):
            for exp, n_iter in enumerate(payload.get("all_iter", [])[i]):
                rows.append(dict(method=method, R=int(R), exp=exp, iter=int(n_iter)))
    return pd.DataFrame(rows)


def analytical_complexity(name: str, R: int, N_sim: int, N_quanta: int, n_iter: int) -> float:
    """Evaluate the paper Big-O expression up to a constant factor."""
    M, K, n = float(N_sim), float(N_quanta), max(float(n_iter), 1.0)
    formulas = {
        "LX": M * K * R * n,
        "LE": M * K * R + K * K * R * n,
        "HT": (M - K) ** 2 * R,
        "KN": M * K * R,
        "LK": M * K * R * n,
        "HK": (M - K) ** 2 * R + M * K * R * n,
        "MB": M * K * R,
        "ANN-FQ": M * K * R,
        "RP-ANN-FQ": M * R * 64 + M * K * 64,
        "KD-ANN-FQ": M * K * R,
        "MR-FQ": M * K * min(R, 512) + M * K * R * 5,
        "CE-LE": M * K * R * n,
        "CE-MB": M * K * R,
        "SVD-CE-LE": M * 32 * R + M * K * R * 2,
        "RP-CE-LE": M * R * 64 + M * K * 64 * n,
    }
    return float(formulas[name])
