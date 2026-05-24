from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from .analysis import accuracy_metrics, analytical_complexity, iter_to_cvt_df, relative_distortion

METHOD_STYLE = {
    "LX": dict(color="#1f77b4", marker="o"), "LE": dict(color="#2ca02c", marker="s"),
    "HT": dict(color="#9467bd", marker="P"), "KN": dict(color="#ff7f0e", marker="v"),
    "LK": dict(color="#d62728", marker="d"), "HK": dict(color="#8c564b", marker="X"),
    "MB": dict(color="#17becf", marker="h"), "ANN-FQ": dict(color="#e377c2", marker="*"),
    "RP-ANN-FQ": dict(color="#bcbd22", marker="<"), "KD-ANN-FQ": dict(color="#7f7f7f", marker=">"),
    "MR-FQ": dict(color="#ff9896", marker="p"), "CE-LE": dict(color="#aec7e8", marker="^"),
    "CE-MB": dict(color="#98df8a", marker="D"), "SVD-CE-LE": dict(color="#c5b0d5", marker="H"),
    "RP-CE-LE": dict(color="#000000", marker="x"),
}


def _save(fig, save_path):
    if save_path is not None:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, bbox_inches="tight", dpi=200)
    return fig


def fig6_mean_time(results, method_style=METHOD_STYLE, save_path=None) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(10, 6))
    for name, payload in results.items():
        means = [float(np.nanmean(v)) for v in payload["all_times"]]
        style = method_style.get(name, dict(color="C0", marker="o"))
        ax.loglog(payload["R_list"], means, marker=style["marker"], color=style["color"], label=name)
    ax.set_xlabel("Discretization R"); ax.set_ylabel("Mean computational time (s)"); ax.legend(fontsize=8, ncol=2); ax.grid(True, which="both", alpha=0.3)
    return _save(fig, save_path)


def fig3_RD_boxplots(results, benchmark="LX", save_path=None) -> plt.Figure:
    df = relative_distortion(results, benchmark)
    R_values = sorted(df.R.unique()) if not df.empty else []
    ncols = min(4, max(1, len(R_values))); nrows = int(np.ceil(max(1, len(R_values)) / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(4 * ncols, 3 * nrows), squeeze=False)
    for ax, R in zip(axes.ravel(), R_values):
        sub = df[df.R == R]
        labels = list(sub.method.unique())
        data = [sub[sub.method == m].RD.to_numpy() * 100 for m in labels]
        ax.boxplot(data, labels=labels, showfliers=False); ax.tick_params(axis="x", rotation=60, labelsize=8); ax.axhline(0, color="k", ls="--", lw=0.8); ax.set_title(f"R = {R}"); ax.set_ylabel("RD vs LX (%)")
    for ax in axes.ravel()[len(R_values):]: ax.set_visible(False)
    fig.tight_layout(); return _save(fig, save_path)


def fig4_RD_trend(results, benchmark="LX", save_path=None) -> plt.Figure:
    df = relative_distortion(results, benchmark)
    fig, ax = plt.subplots(figsize=(9, 5))
    for name, sub in df.groupby("method") if not df.empty else []:
        g = sub.groupby("R").RD.mean().sort_index()
        style = METHOD_STYLE.get(name, dict(color="C0", marker="o"))
        ax.semilogx(g.index, 100 * g.values, marker=style["marker"], color=style["color"], label=name)
    ax.axhline(0, color="k", ls="--", lw=0.8); ax.set_xlabel("Discretization R"); ax.set_ylabel("Mean relative distortion vs LX (%)"); ax.legend(fontsize=8); ax.grid(True, which="both", alpha=0.3)
    return _save(fig, save_path)


def fig7_complexity(results, save_path=None) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(10, 6))
    for name, payload in results.items():
        means = np.asarray([np.nanmean(v) for v in payload["all_times"]], dtype=float)
        iters = [max(1, int(np.nanmean(v))) for v in payload["all_iter"]]
        ana = np.asarray([analytical_complexity(name, R, 3000, 50, it) for R, it in zip(payload["R_list"], iters)])
        style = METHOD_STYLE.get(name, dict(color="C0", marker="o"))
        ax.loglog(payload["R_list"], means, marker=style["marker"], color=style["color"], label=f"{name} measured")
        if np.all(ana > 0) and np.any(means > 0):
            scale = means[0] / ana[0]
            ax.loglog(payload["R_list"], ana * scale, ls="--", color=style["color"], alpha=0.55)
    ax.set_xlabel("Discretization R"); ax.set_ylabel("Time (s), analytical scaled"); ax.legend(fontsize=7, ncol=2); ax.grid(True, which="both", alpha=0.3)
    return _save(fig, save_path)


def fig8_iter_cvt(results, save_path=None) -> plt.Figure:
    df = iter_to_cvt_df(results)
    fig, ax = plt.subplots(figsize=(8, 5))
    labels, data = [], []
    for (method, R), sub in df.groupby(["method", "R"]) if not df.empty else []:
        labels.append(f"{method}\n{R}"); data.append(sub.iter.to_numpy())
    if data:
        ax.boxplot(data, labels=labels, showfliers=False); ax.tick_params(axis="x", rotation=45)
    ax.set_ylabel("Iterations to convergence"); ax.grid(True, alpha=0.3)
    return _save(fig, save_path)


def fig9_accuracy(results, X_ref, R_ref, save_path=None) -> plt.Figure:
    df = accuracy_metrics(results, X_ref, R_ref)
    fig, axes = plt.subplots(2, 2, figsize=(10, 7))
    for ax, metric in zip(axes.ravel(), ["M1", "M2", "M3", "M4"]):
        if not df.empty:
            ax.bar(df.method, df[metric]); ax.tick_params(axis="x", rotation=60)
        ax.set_title(metric); ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout(); return _save(fig, save_path)


def pareto(results, R_values=(256, 1024, 4096, 16384), save_path=None) -> plt.Figure:
    plot_R = [R for R in R_values if any(R in p["R_list"] for p in results.values())]
    fig, axes = plt.subplots(1, max(1, len(plot_R)), figsize=(5 * max(1, len(plot_R)), 4), squeeze=False)
    for ax, R in zip(axes.ravel(), plot_R):
        for name, payload in results.items():
            if R not in payload["R_list"]:
                continue
            i = payload["R_list"].index(R)
            x = float(np.nanmean(payload["all_times"][i])); y = float(np.nanmean(payload["all_sse"][i]))
            style = METHOD_STYLE.get(name, dict(color="C0", marker="o"))
            ax.scatter(x, y, color=style["color"], marker=style["marker"], s=70); ax.annotate(name, (x, y), fontsize=8, xytext=(3, 3), textcoords="offset points")
        ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlabel("Mean time (s)"); ax.set_ylabel("Mean SSE"); ax.set_title(f"R = {R}"); ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout(); return _save(fig, save_path)
