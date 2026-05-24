# Reproducibility Guide

This guide describes the clean-clone path from an empty machine to regenerated benchmark and seismic-hazard artifacts. The committed images under `results/sample/` are deliberately small so GitHub renders the project clearly; they are not the final updated paper figures.

## 1. Create the environment

```bash
conda env create -f environment.yml
conda activate fq-rf
pip install -e ".[dev]"
```

If conda is unavailable, a virtual environment also works:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## 2. Verify the repository

```bash
pytest tests/ -q
jupyter nbconvert --to script notebooks/01_algorithm_benchmark.ipynb
jupyter nbconvert --to script notebooks/02_seismic_hazard.ipynb
```

## 3. Run a lightweight sample

Use this when checking a fresh clone, testing a pull request, or refreshing the visible GitHub gallery.

```bash
python scripts/make_sample_gallery.py
```

The sample intentionally uses fewer experiments, fewer simulations, and fewer resolutions than the paper. It is a software check, not a scientific result.

## 4. Run the full benchmark

The full benchmark follows the paper-scale sweep:

```bash
python scripts/run_benchmark.py \
  --n_exp 100 \
  --nsim 3000 \
  --R 128 256 512 1024 2048 4096 8192 16384 \
  --methods LX LE HT KN LK HK MB ANN-FQ RP-ANN-FQ KD-ANN-FQ MR-FQ CE-LE CE-MB SVD-CE-LE RP-CE-LE \
  --results results/runtime/benchmark_full
```

Heavy methods such as hierarchical Ward clustering and Elkan variants may take substantially longer at high resolution. Keep large pickle checkpoints in `results/runtime/`; do not commit result `.pkl` files or large generated artifacts.

## 5. Run the seismic application

```bash
python scripts/run_seismic.py \
  --N 50 200 \
  --max_iter 150 \
  --out results/runtime/seismic_full
```

The seismic modules preserve the domain-specific corrections used by the project:

- `B_EPS_KM = 8.5` for Jayaram and Baker (2009) at `T = 0.1 s`.
- The spatial correlation is `exp(-3h/b)`.
- The quantizer sizes are `N = 50` and `N = 200`.
- Contour figures use latitude/longitude axes for map interpretation.

## 6. Artifact policy

Commit:

- source code,
- notebooks,
- small CSV summaries,
- small curated PNGs that make the repository readable.

Do not commit:

- large `.pkl` checkpoints,
- full runtime directories,
- generated notebooks from smoke execution,
- raw unpublished result sets unless the authors explicitly approve them.

This policy keeps the repository useful for reviewers and students while avoiding stale or oversized artifacts.
