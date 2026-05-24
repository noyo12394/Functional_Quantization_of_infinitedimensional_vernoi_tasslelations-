import numpy as np
import pytest

from fq.data import synthesize_paper_data


@pytest.fixture(scope="session")
def tiny_X():
    return synthesize_paper_data(nsim=200, R=64, seed=0)


@pytest.fixture(scope="session")
def tiny_params():
    return dict(n_quanta=10, max_iter=10, tol=1e-3)
