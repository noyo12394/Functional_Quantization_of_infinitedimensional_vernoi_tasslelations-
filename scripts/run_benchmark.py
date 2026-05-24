from pathlib import Path
import argparse

from fq.algorithms import ALGORITHMS
from fq.data import synthesize_paper_data
from fq.runner import build_master_df, run_algorithm


def main():
    parser = argparse.ArgumentParser(description="Run the FQ clustering benchmark.")
    parser.add_argument("--n_exp", type=int, default=5)
    parser.add_argument("--nsim", type=int, default=300)
    parser.add_argument("--R", type=int, nargs="+", default=[128, 256, 512])
    parser.add_argument("--methods", nargs="+", default=["LX", "LK", "KN", "MB"])
    parser.add_argument("--results", default="results/runtime")
    args = parser.parse_args()
    X = synthesize_paper_data(nsim=args.nsim, R=max(args.R), seed=0)
    results = {}
    for name in args.methods:
        cls = ALGORITHMS[name]
        alg = cls(n_quanta=20, max_iter=10, tol=1e-4)
        results[name] = run_algorithm(alg, args.R, X, n_exp=args.n_exp, results_dir=args.results, verbose_every=0)
    out = Path(args.results) / "master_summary.csv"
    build_master_df(results).to_csv(out, index=False)
    print(out)


if __name__ == "__main__":
    main()
