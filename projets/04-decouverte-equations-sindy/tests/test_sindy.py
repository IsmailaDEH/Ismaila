import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from sindy import bibliotheque, coeffs_vrais, derivee, simuler_lorenz, stlsq  # noqa: E402


def test_bibliotheque_taille():
    Theta, noms = bibliotheque(np.ones((5, 3)), degre=2)
    assert Theta.shape == (5, 10) and noms[:4] == ["1", "x", "y", "z"]


def test_stlsq_retrouve_modele_lineaire():
    rng = np.random.default_rng(0)
    X = rng.standard_normal((500, 3))
    Theta, noms = bibliotheque(X)
    Xi = np.zeros((len(noms), 1))
    Xi[noms.index("x")] = 2.0
    Xi[noms.index("yz")] = -3.0
    est = stlsq(Theta, Theta @ Xi, seuil=0.1)
    assert np.allclose(est, Xi, atol=1e-8)


def test_lorenz_sans_bruit_structure_exacte():
    t, X = simuler_lorenz(t_max=10)
    Theta, noms = bibliotheque(X)
    Xi = stlsq(Theta, derivee(X, t[1] - t[0]), seuil=0.5)
    assert np.array_equal(Xi != 0, coeffs_vrais(noms) != 0)
    assert np.allclose(Xi, coeffs_vrais(noms), rtol=1e-2, atol=1e-2)
