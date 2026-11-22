import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from simulation import energie, integrer, lyapunov_max  # noqa: E402


def test_equilibre_reste_immobile():
    _, X = integrer(np.zeros(4), t_max=1.0, dt=1e-2)
    assert np.allclose(X, 0.0)


def test_conservation_energie():
    _, X = integrer(np.radians([90, 0, 45, 0]), t_max=5.0, dt=1e-3)
    E = energie(X)
    assert np.max(np.abs((E - E[0]) / E[0])) < 1e-6


def test_petites_oscillations_periode():
    # Mode normal en phase (m1=m2, l1=l2) : ω² = (2 - √2) g / l
    _, X = integrer(np.radians([1.0, 0, np.sqrt(2) * 1.0, 0]), t_max=10.0, dt=1e-3)
    signe = np.sign(X[:, 0])
    passages = np.where(np.diff(signe) != 0)[0]
    periode = 2 * np.mean(np.diff(passages)) * 1e-3
    attendu = 2 * np.pi / np.sqrt((2 - np.sqrt(2)) * 9.81)
    assert abs(periode - attendu) / attendu < 0.01


def test_chaos_lyapunov_positif():
    assert lyapunov_max(np.radians([120, 0, -10, 0]), t_max=20.0, dt=5e-3) > 0.5
