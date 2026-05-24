import numpy as np
import pytest

from fq.algorithms import ALGORITHMS


@pytest.mark.parametrize("name,cls", ALGORITHMS.items())
def test_step_returns_valid_dict(name, cls, tiny_X, tiny_params):
    alg = cls(**tiny_params)
    out = alg.step(tiny_X, seed=0)
    assert {"time", "sse", "iter", "centers"}.issubset(out)
    assert isinstance(out["time"], float)
    assert isinstance(out["sse"], float)
    assert isinstance(out["iter"], int)
    assert isinstance(out["centers"], np.ndarray)


@pytest.mark.parametrize("name,cls", ALGORITHMS.items())
def test_sse_positive(name, cls, tiny_X, tiny_params):
    out = cls(**tiny_params).step(tiny_X, seed=1)
    assert out["sse"] > 0


@pytest.mark.parametrize("name,cls", ALGORITHMS.items())
def test_centers_shape(name, cls, tiny_X, tiny_params):
    out = cls(**tiny_params).step(tiny_X, seed=2)
    assert out["centers"].shape == (tiny_params["n_quanta"], tiny_X.shape[1])
