import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from ion import (deplacement, etat_stationnaire, excitation, hamiltonien,  # noqa: E402
                 lindbladien, nombre_phonons, rabi_exact, rabi_lamb_dicke,
                 refroidissement, taux_lamb_dicke, thermique, thermometrie)


def test_laguerre_egale_element_de_matrice():
    D = np.abs(deplacement(30, 0.25))
    for n in range(25):
        for m in range(25):
            assert D[m, n] == pytest.approx(rabi_exact(n, m, 0.25), abs=1e-12)


def test_limite_lamb_dicke():
    eta = 0.01
    for n in range(1, 10):
        assert rabi_exact(n, n - 1, eta) == pytest.approx(rabi_lamb_dicke(n, n - 1, eta), rel=1e-3)
        assert rabi_exact(n, n + 1, eta) == pytest.approx(rabi_lamb_dicke(n, n + 1, eta), rel=1e-3)


def test_hamiltonien_hermitien():
    H = hamiltonien(10, 1.0, -1.0, 0.1, 0.2)
    assert np.allclose(H, H.conj().T)


def test_thermique_moyenne():
    p = thermique(200, 3.0)
    assert np.sum(np.arange(200) * p) == pytest.approx(3.0, rel=1e-9)


def test_pas_de_bande_rouge_dans_le_fondamental():
    """|g, 0⟩ ne peut pas perdre de phonon : la bande rouge est noire."""
    pn = np.zeros(20)
    pn[0] = 1.0
    om, eta = 0.04, 0.1
    t = np.pi / (eta * om)
    assert excitation(20, 1.0, -1.0, om, eta, t, pn) < 1e-2
    # impulsion π bleue : ~96 % seulement, la porteuse hors résonance déplace
    # la raie (déplacement lumineux δ ≈ Ω²/2ν) : P_max = 1/(1 + (δ/ηΩ)²) ≈ 0,96
    assert excitation(20, 1.0, +1.0, om, eta, t, pn) > 0.95


def test_thermometrie_par_bandes_laterales():
    om, eta, N = 0.04, 0.1, 40
    t = np.pi / (2 * eta * om)
    pn = thermique(N, 1.5)
    pr = excitation(N, 1.0, -1.0, om, eta, t, pn)
    pb = excitation(N, 1.0, +1.0, om, eta, t, pn)
    assert thermometrie(pr, pb) == pytest.approx(1.5, rel=1e-2)


@pytest.mark.parametrize("gamma", [0.2, 1.0])
def test_etat_stationnaire_contre_equations_de_taux(gamma):
    r = etat_stationnaire(lindbladien(15, 1.0, -1.0, 0.02, 0.1, gamma), 30)
    assert np.trace(r).real == pytest.approx(1.0)
    assert np.all(np.linalg.eigvalsh(r) > -1e-10)
    n_th, _ = taux_lamb_dicke(1.0, -1.0, 0.02, 0.1, gamma)
    assert nombre_phonons(r, 15) == pytest.approx(n_th, rel=0.03)


def test_refroidissement_fait_baisser_n():
    n = refroidissement(12, 1.0, 0.1, 0.1, 0.5, 1.0, [0.0, 5e3, 4e4])
    assert n[0] == pytest.approx(1.0, rel=0.02)
    assert n[2] < n[1] < n[0]
    assert n[2] < 0.1
