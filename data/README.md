# Data Inputs

The repository can run without external downloads. If the benchmark CSV used by the authors is unavailable, `fq.data.synthesize_paper_data()` generates a synthetic lognormal random field from the spectrum described in the paper workflow.

## Optional benchmark CSV

Place an optional CSV here or point the notebooks/scripts to another path:

```text
data/samples.csv
```

Expected shape:

- one realization per row,
- one discretization point per column,
- numeric values only,
- at least as many rows as the requested `--nsim`.

## Seismic application

The seismic application is parameterized in code. Fault geometry, ground-motion coefficients, spatial correlation, and quantizer settings are stored in `applications/seismic_hazard/`, so no external seismic data file is required for the provided workflow.

## What not to commit

Do not commit large raw data or runtime checkpoint files. Put large local runs under `results/runtime/`, which is ignored by git.
