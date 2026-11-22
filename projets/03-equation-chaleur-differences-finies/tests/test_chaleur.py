import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from simulation import crank_nicolson_1d, ftcs_2d, solution_exacte_2d  # noqa: E402


def test_ftcs_proche_solution_exacte():
    X, Y, u = ftcs_2d(40, 0.05, r=0.2)
    assert np.abs(u - solution_exacte_2d(X, Y, 0.05)).max() < 1e-3


def test_bords_dirichlet():
    _, _, u = ftcs_2d(20, 0.02)
    assert np.all(u[0] == 0) and np.all(u[-1] == 0)


def test_crank_nicolson_grand_pas_stable():
    # r ≫ 1/2 : un schéma explicite exploserait, CN reste borné et précis
    _, u, err = crank_nicolson_1d(200, 10, 0.1)
    assert np.isfinite(u).all() and err < 1e-2
