# Seismic Hazard Application

Run `notebooks/02_seismic_hazard.ipynb` or `python scripts/run_seismic.py --N 50 200` to reproduce the Southern California spatially correlated $S_a$ map application.

The implementation preserves the correction notes from Sena's email: `B_EPS_KM = 8.5`, correlation `exp(-3h/b)`, quantizer sizes `N = 50` and `N = 200`, and latitude/longitude axes for map plots.
