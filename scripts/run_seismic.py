import argparse
from pathlib import Path

import numpy as np

from applications.seismic_hazard.fq_idcvt import fq_idcvt


def main():
    parser = argparse.ArgumentParser(description="Run seismic FQ-IDCVT quantizers.")
    parser.add_argument("--N", type=int, nargs="+", default=[50, 200])
    parser.add_argument("--max_iter", type=int, default=20)
    parser.add_argument("--out", default="results/runtime/seismic")
    args = parser.parse_args()
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    for N in args.N:
        q, w, info = fq_idcvt(N, np.random.default_rng(42 + N), max_iter=args.max_iter, verbose=True)
        np.savez_compressed(out / f"fq_idcvt_N{N}.npz", quanta=q, weights=w, distortions=np.asarray(info["distortions"]))
        print(f"N={N}: {info}")


if __name__ == "__main__":
    main()
