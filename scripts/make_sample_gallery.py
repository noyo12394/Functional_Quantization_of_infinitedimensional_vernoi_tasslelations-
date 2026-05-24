"""Regenerate the lightweight figure gallery committed under results/sample."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from applications.seismic_hazard.correlation import B_EPS_KM, jb2009_rho
from applications.seismic_hazard.geometry import FAULT_TABLE, LAT_PLOT, LON_PLOT, to_2d
from applications.seismic_hazard.simulation import simulate_maps
from fq import plots
from fq.algorithms import ALGORITHMS
from fq.data import synthesize_paper_data
from fq.runner import build_master_df, run_algorithm


def main() -> None:
    """Create small, visible benchmark and seismic figures for GitHub."""
    root = Path(__file__).resolve().parents[1]
    fig_dir = root / "results" / "sample" / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    X = synthesize_paper_data(nsim=120, R=256, seed=2026)
    results = {}
    for name in ["LX", "LK", "KN", "MB"]:
        alg = ALGORITHMS[name](n_quanta=8, max_iter=6, tol=1e-3)
        results[name] = run_algorithm(
            alg,
            [128, 256],
            X,
            n_exp=3,
            store_centers_for_R=128,
            verbose_every=0,
        )

    build_master_df(results).to_csv(root / "results" / "sample" / "master_summary.csv", index=False)

    plots.fig6_mean_time(results, save_path=fig_dir / "fig6_mean_time.png")
    plots.fig3_RD_boxplots(results, save_path=fig_dir / "fig3_rd_boxplots.png")
    plots.fig4_RD_trend(results, save_path=fig_dir / "fig4_rd_trend.png")
    plots.fig8_iter_cvt(results, save_path=fig_dir / "fig8_iter_cvt.png")
    plots.fig9_accuracy(results, X, 128, save_path=fig_dir / "fig9_accuracy.png")
    plots.pareto(results, R_values=(128, 256), save_path=fig_dir / "pareto_R256.png")
    plots.pareto(results, R_values=(256,), save_path=fig_dir / "pareto_R4096.png")

    fig, ax = plt.subplots(figsize=(8, 3.8))
    for row in X[:8]:
        ax.plot(row, alpha=0.72, lw=1.1)
    ax.set_title("Sample synthetic random-field realizations")
    ax.set_xlabel("Discretization index")
    ax.set_ylabel("Field value")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(fig_dir / "fig2_sample_realizations.png", dpi=200, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(LON_PLOT, LAT_PLOT, s=5, alpha=0.28, color="#1f77b4", label="Site grid")
    for node, (lat, lon) in FAULT_TABLE.items():
        ax.scatter(lon, lat, color="#d62728", s=45, zorder=4)
        ax.text(lon + 0.003, lat + 0.003, node, fontsize=10, weight="bold")
    for a, b in [("A", "B"), ("C", "D")]:
        ax.plot(
            [FAULT_TABLE[a][1], FAULT_TABLE[b][1]],
            [FAULT_TABLE[a][0], FAULT_TABLE[b][0]],
            color="black",
            lw=2,
        )
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title("Seismic application geometry: fault nodes and site grid")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(fig_dir / "seismic_geometry.png", dpi=200, bbox_inches="tight")
    plt.close(fig)

    X_sa = np.exp(simulate_maps(80, np.random.default_rng(10)))
    P = to_2d((X_sa > 0.3).mean(axis=0))
    fig, ax = plt.subplots(figsize=(7, 5))
    cf = ax.contourf(LON_PLOT, LAT_PLOT, P, levels=np.linspace(0, 1, 11), cmap="RdYlBu_r")
    plt.colorbar(cf, ax=ax, label="P[Sa > 0.3g]")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title("Sample exceedance contour from simulated Sa maps")
    fig.tight_layout()
    fig.savefig(fig_dir / "seismic_exceedance_sample.png", dpi=200, bbox_inches="tight")
    plt.close(fig)

    h = np.linspace(0, 40, 250)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(h, jb2009_rho(h), lw=2, color="#2ca02c")
    ax.axvline(B_EPS_KM, ls="--", color="black", lw=1)
    ax.axhline(np.exp(-3), ls="--", color="gray", lw=1)
    ax.set_xlabel("Separation distance h [km]")
    ax.set_ylabel("Spatial correlation rho(h)")
    ax.set_title("Jayaram & Baker 2009 corrected correlation: exp(-3h/b), b=8.5 km")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(fig_dir / "seismic_correlation_decay.png", dpi=200, bbox_inches="tight")
    plt.close(fig)

    print(f"Wrote sample gallery to {fig_dir}")


if __name__ == "__main__":
    main()
