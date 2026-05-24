# Contributing

Contributions should keep the repository reproducible, readable, and faithful to the paper workflow.

## Development setup

```bash
conda env create -f environment.yml
conda activate fq-rf
pip install -e ".[dev]"
pytest tests/ -q
```

## Adding an algorithm

1. Create `fq/algorithms/my_method.py`.
2. Subclass `FQAlgorithm`.
3. Return at least `time`, `sse`, `iter`, and `centers` from `step(Xr, seed)`.
4. Register the class in `fq/algorithms/__init__.py`.
5. Run `pytest tests/test_algorithms.py -q`.
6. Add a short method note to `docs/algorithms.md`.

Use `notebooks/03_add_your_own_method.ipynb` as the worked example.

## Results and figures

Small curated figures are welcome when they make the repository easier to inspect. Do not commit large runtime files, stale paper outputs, or generated `.pkl` checkpoints. Full runs should live under `results/runtime/` unless the maintainers intentionally curate a release artifact.

## Style

- Keep prose aimed at graduate students who know k-means but may not know functional quantization.
- Explain acronyms on first use.
- Use Google-style docstrings for public functions.
- Avoid `import *`.
- Avoid deprecated pandas APIs such as `applymap`.
