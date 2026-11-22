import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from md import Simulation, forces, reseau_cfc  # noqa: E402


def test_reseau_cfc():
    pos, L = reseau_cfc(3, 0.8)
    assert pos.shape == (108, 3)
    assert np.isclose(108 / L**3, 0.8)


def test_troisieme_loi_newton():
    pos, L = reseau_cfc(2, 0.8)
    pos = pos + np.random.default_rng(0).normal(0, 0.05, pos.shape)
    F, _, _ = forces(pos, L)
    assert np.allclose(F.sum(axis=0), 0, atol=1e-10)


def test_force_egale_moins_gradient():
    pos, L = reseau_cfc(2, 0.8)
    pos = pos + np.random.default_rng(1).normal(0, 0.05, pos.shape)
    F, U0, _ = forces(pos, L)
    h = 1e-6
    p = pos.copy()
    p[3, 1] += h
    _, U1, _ = forces(p, L)
    assert np.isclose(-(U1 - U0) / h, F[3, 1], rtol=1e-4)


def test_conservation_energie_et_impulsion():
    s = Simulation(n_cell=2, densite=0.8, T=1.0, dt=0.002)
    E0 = s.energie_totale()
    for _ in range(500):
        s.pas()
    assert abs(s.energie_totale() - E0) / abs(E0) < 1e-3
    assert np.allclose(s.vel.sum(axis=0), 0, atol=1e-10)
