.PHONY: setup test smoke sample benchmark seismic clean

setup:
	pip install -e ".[dev]"

test:
	pytest tests/ -q

smoke:
	jupyter nbconvert --to script notebooks/01_algorithm_benchmark.ipynb
	jupyter nbconvert --to script notebooks/02_seismic_hazard.ipynb

sample:
	python scripts/make_sample_gallery.py

benchmark:
	python scripts/run_benchmark.py --n_exp 100 --nsim 3000 --R 128 256 512 1024 2048 4096 8192 16384 --methods LX LE HT KN LK HK MB ANN-FQ RP-ANN-FQ KD-ANN-FQ MR-FQ CE-LE CE-MB SVD-CE-LE RP-CE-LE --results results/runtime/benchmark_full

seismic:
	python scripts/run_seismic.py --N 50 200 --max_iter 150 --out results/runtime/seismic_full

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type d -name ".ipynb_checkpoints" -prune -exec rm -rf {} +
