import math

import numpy as np
import pytest

from applications.seismic_hazard.correlation import jb2009_rho
from applications.seismic_hazard.fq_idcvt import fq_idcvt
from applications.seismic_hazard.geometry import R_GRID
from applications.seismic_hazard.gmm import as97_ln_sa
from applications.seismic_hazard.simulation import simulate_maps


def test_as97_spot_checks():
    expected = 0.6549653117711524
    assert float(np.exp(as97_ln_sa(M=6.5, rrup=10))) == pytest.approx(expected, rel=0.01)


def test_jb2009_rho_at_zero():
    assert jb2009_rho(0) == pytest.approx(1.0)


def test_jb2009_rho_decay():
    assert jb2009_rho(8.5) == pytest.approx(math.exp(-3), rel=1e-5)


def test_simulate_maps_shape():
    out = simulate_maps(3, np.random.default_rng(0))
    assert out.shape == (3, R_GRID)


def test_fq_idcvt_distortion_decreases():
    _, _, info = fq_idcvt(3, np.random.default_rng(1), max_iter=5, nsim_factor=5, npsim_factor=5)
    d = info["distortions"]
    assert all(b <= a + 1e-12 for a, b in zip(d, d[1:]))
