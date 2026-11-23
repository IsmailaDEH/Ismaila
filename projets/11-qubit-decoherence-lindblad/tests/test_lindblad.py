import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from lindblad import (EXC, FOND, T2_theorique, bloch, etat_stationnaire, evoluer,  # noqa: E402
                      hamiltonien, operateurs_saut, population_stationnaire_bloch)


def test_trace_hermiticite_positivite():
    _, r = evoluer(FOND, hamiltonien(0.3, 2.0), operateurs_saut(0.1, 0.05), 20, dt=0.005)
    assert np.allclose(np.trace(r, axis1=1, axis2=2), 1, atol=1e-10)
    assert np.allclose(r, np.conj(np.transpose(r, (0, 2, 1))))
    assert np.all(np.linalg.eigvalsh(r) > -1e-10)


def test_rabi_sans_dissipation():
    """Sans bruit : P_e(t) = sin²(Ω t / 2) exactement."""
    om = 2.0
    t, r = evoluer(FOND, hamiltonien(0, om), [], 10, dt=0.002)
    assert np.allclose(np.real(r[:, 0, 0]), np.sin(om * t / 2) ** 2, atol=1e-8)


def test_relaxation_T1():
    t, r = evoluer(EXC, hamiltonien(0, 0), operateurs_saut(0.2, 0.0), 10, dt=0.002)
    assert np.allclose(np.real(r[:, 0, 0]), np.exp(-0.2 * t), atol=1e-9)


def test_dephasage_T2():
    g1, gp = 0.1, 0.3
    plus = 0.5 * np.ones((2, 2), complex)
    t, r = evoluer(plus, hamiltonien(0, 0), operateurs_saut(g1, gp), 10, dt=0.002)
    assert np.allclose(2 * np.abs(r[:, 0, 1]), np.exp(-t / T2_theorique(g1, gp)), atol=1e-9)


def test_T2_borne_2T1():
    assert T2_theorique(0.1, 0.0) == pytest.approx(2 / 0.1)
    assert T2_theorique(0.1, 0.5) < 2 / 0.1


@pytest.mark.parametrize("delta", [0.0, 0.4, -1.0])
def test_etat_stationnaire_bloch(delta):
    H, ops = hamiltonien(delta, 0.7), operateurs_saut(0.3, 0.2)
    rho = etat_stationnaire(H, ops)
    assert np.real(rho[0, 0]) == pytest.approx(population_stationnaire_bloch(delta, 0.7, 0.3, 0.2), abs=1e-10)


def test_bloch_etats_purs():
    assert np.allclose(bloch(EXC[None])[0], [0, 0, 1])
    assert np.allclose(bloch(0.5 * np.ones((2, 2), complex)[None])[0], [1, 0, 0])
