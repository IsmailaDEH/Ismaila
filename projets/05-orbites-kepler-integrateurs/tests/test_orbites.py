import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from simulation import (conditions_perihelie, energie, moment_cinetique, orbite,  # noqa: E402
                        periode_mesuree)


def test_orbite_circulaire_terre_un_an():
    r0, v0 = conditions_perihelie(1.0, 0.0)
    _, R, _ = orbite("RK4", r0, v0, 1e-3, 1.0)
    assert np.linalg.norm(R[-1] - r0) < 1e-6


def test_verlet_conserve_moment_cinetique():
    r0, v0 = conditions_perihelie(1.0, 0.5)
    _, R, V = orbite("Verlet", r0, v0, 1e-3, 5.0)
    L = moment_cinetique(R, V)
    assert np.max(np.abs(L - L[0])) / abs(L[0]) < 1e-10


def test_euler_derive_energie():
    r0, v0 = conditions_perihelie(1.0, 0.5)
    _, R, V = orbite("Euler", r0, v0, 1e-3, 5.0)
    E = energie(R, V)
    assert E[-1] > E[0]  # Euler injecte de l'énergie : l'orbite s'élargit


def test_periode_mars():
    r0, v0 = conditions_perihelie(1.524, 0.093)
    t, R, _ = orbite("Verlet", r0, v0, 1e-3, 6.0)
    assert abs(periode_mesuree(t, R) - 1.524**1.5) < 1e-3
