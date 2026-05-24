import gc
import pickle
import time
from pathlib import Path
from typing import Dict, Optional, Union

import numpy as np
import pandas as pd

from .core import interpolate_dataset
from .algorithms.base import FQAlgorithm


def save_checkpoint(results_dir: Union[str, Path], name: str, payload: dict) -> Path:
    """Save one algorithm payload as a pickle checkpoint."""
    results_path = Path(results_dir)
    results_path.mkdir(parents=True, exist_ok=True)
    fp = results_path / f"{name}_results.pkl"
    with fp.open("wb") as f:
        pickle.dump(payload, f)
    return fp


def run_algorithm(algorithm: FQAlgorithm, R_list, X_full: np.ndarray, n_exp: int = 100,
                  store_centers_for_R: Optional[int] = None, results_dir: Optional[Union[str, Path]] = None,
                  verbose_every: int = 10) -> dict:
    """Run an algorithm across resolutions and repeated experiments.

    Args:
        algorithm: Configured ``FQAlgorithm`` instance.
        R_list: Iterable of discretization sizes.
        X_full: Full-resolution realizations.
        n_exp: Number of experiments per resolution.
        store_centers_for_R: Optional resolution whose centers are retained.
        results_dir: Optional checkpoint directory.
        verbose_every: Print cadence for long runs.

    Returns:
        Payload with timings, distortions, iterations, and optional centers.
    """
    all_times, all_sse, all_iter = [], [], []
    centers_for_ref = []
    grand_t0 = time.perf_counter()
    name = algorithm.name
    for iR, R in enumerate(R_list, start=1):
        Xr = interpolate_dataset(X_full, int(R))
        ts, ss, iters = [], [], []
        store_here = store_centers_for_R is not None and int(R) == int(store_centers_for_R)
        for exp in range(int(n_exp)):
            try:
                t0 = time.perf_counter()
                out = algorithm.step(Xr, exp)
                dt = time.perf_counter() - t0
                ts.append(float(out.get("time", dt)))
                ss.append(float(out.get("sse", np.nan)))
                iters.append(int(out.get("iter", 0)))
                if store_here and "centers" in out:
                    centers_for_ref.append(np.asarray(out["centers"], dtype=float))
            except Exception:
                ts.append(float("nan")); ss.append(float("nan")); iters.append(0)
                raise
            if verbose_every and ((exp + 1) % verbose_every == 0):
                print(f"{name} R={R} exp={exp + 1}/{n_exp} time={ts[-1]:.4f}s")
        all_times.append(ts); all_sse.append(ss); all_iter.append(iters)
        del Xr; gc.collect()
    payload = dict(name=name, R_list=[int(r) for r in R_list], all_times=all_times,
                   all_sse=all_sse, all_iter=all_iter,
                   centers_ref=centers_for_ref if store_centers_for_R is not None else None,
                   store_centers_for_R=store_centers_for_R,
                   total_seconds=time.perf_counter() - grand_t0)
    if results_dir is not None:
        save_checkpoint(results_dir, name, payload)
    return payload


def load_all_results(results_dir: Union[str, Path]) -> Dict[str, dict]:
    """Load every ``*_results.pkl`` file in a directory."""
    out = {}
    for fp in sorted(Path(results_dir).glob("*_results.pkl")):
        with fp.open("rb") as f:
            payload = pickle.load(f)
        out[payload.get("name", fp.stem.replace("_results", ""))] = payload
    return out


def build_master_df(results: dict) -> pd.DataFrame:
    """Build a tidy summary table from benchmark payloads."""
    rows = []
    for name, payload in results.items():
        for i, R in enumerate(payload.get("R_list", [])):
            rows.append(dict(
                method=name,
                R=int(R),
                mean_time=float(np.nanmean(payload["all_times"][i])),
                std_time=float(np.nanstd(payload["all_times"][i], ddof=1)) if len(payload["all_times"][i]) > 1 else 0.0,
                mean_sse=float(np.nanmean(payload["all_sse"][i])),
                mean_iter=float(np.nanmean(payload["all_iter"][i])),
            ))
    return pd.DataFrame(rows).sort_values(["method", "R"]).reset_index(drop=True)
