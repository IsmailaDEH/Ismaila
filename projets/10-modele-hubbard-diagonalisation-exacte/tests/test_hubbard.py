import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from hubbard import (double_occupation, energie, energie_libre, energie_lieb_wu,  # noqa: E402
                     gap_de_charge, gap_de_spin, heisenberg, matrice_saut, secteur)


def test_dimension_secteur():
    assert len(secteur(6, 3)) == 20


@pytest.mark.parametrize("L", [4, 6, 8])
def test_U0_fermions_libres(L):
    assert energie(L, L // 2, L // 2, 0.0) == pytest.approx(energie_libre(L, L // 2, L // 2), abs=1e-10)


def test_saut_hermitien():
    T = matrice_saut(6, 3).toarray()
    assert np.allclose(T, T.T)


def test_signe_fermionique_jordan_wigner():
    """Comparaison avec des opérateurs de Jordan-Wigner construits explicitement."""
    L = 4
    a = np.array([[0.0, 1.0], [0.0, 0.0]]); Z = np.diag([1.0, -1.0]); I = np.eye(2)

    def c(i):
        M = np.array([[1.0]])
        for o in ([Z] * i + [a] + [I] * (L - i - 1))[::-1]:
            M = np.kron(M, o)
        return M

    H = sum(-(c(i).T @ c((i + 1) % L) + c((i + 1) % L).T @ c(i)) for i in range(L))
    for N in (1, 2, 3):
        idx = [s for s in range(2 ** L) if bin(s).count("1") == N]
        assert np.allclose(np.linalg.eigvalsh(H[np.ix_(idx, idx)]),
                           np.linalg.eigvalsh(matrice_saut(L, N).toarray()))


def test_dimere_analytique():
    """2 sites, 2 électrons : E0 = (U - sqrt(U² + 16 t²)) / 2."""
    for U in (0.5, 4.0, 10.0):
        assert energie(2, 1, 1, U) == pytest.approx((U - np.sqrt(U ** 2 + 16)) / 2)


def test_hellmann_feynman():
    h = 1e-4
    dE = (energie(6, 3, 3, 3 + h) - energie(6, 3, 3, 3 - h)) / (2 * h) / 6
    assert dE == pytest.approx(double_occupation(6, 3.0), abs=1e-5)


def test_proche_bethe_ansatz():
    assert energie(10, 5, 5, 4.0) / 10 == pytest.approx(energie_lieb_wu(4.0), rel=0.03)


def test_gap_de_mott_grand_U():
    assert gap_de_charge(8, 20.0) > 15.0


def test_limite_heisenberg():
    U = 40.0
    g_heis = heisenberg(8, 4 / U, 1) - heisenberg(8, 4 / U, 0)
    assert gap_de_spin(8, U) == pytest.approx(g_heis, rel=0.03)


def test_heisenberg_4_sites():
    assert heisenberg(4) == pytest.approx(-2.0)
