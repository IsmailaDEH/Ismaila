import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from gp import OMEGA_VRAI, RE, ProcessusGaussien, morse, proprietes  # noqa: E402


def test_morse_minimum():
    assert np.isclose(morse(RE), -4.7446)


def test_frequence_h2():
    # ω_e expérimental de H2 : 4401 cm⁻¹
    assert abs(OMEGA_VRAI - 4401) < 10


def test_gp_interpole_sans_bruit():
    x = np.linspace(0.5, 2.5, 15)
    gp = ProcessusGaussien(amp=3, ell=0.4, bruit=1e-4).ajuster(x, morse(x), optimiser=False)
    mu, sd = gp.predire(x)
    assert np.allclose(mu, morse(x), atol=1e-3) and sd.max() < 1e-2


def test_incertitude_grandit_loin_des_donnees():
    x = np.linspace(0.6, 1.2, 8)
    gp = ProcessusGaussien().ajuster(x, morse(x))
    _, sd = gp.predire(np.array([0.9, 2.8]))
    assert sd[1] > 10 * sd[0]


def test_proprietes_morse():
    r = np.linspace(0.5, 1.2, 2000)
    r_e, k = proprietes(r, morse(r))
    assert abs(r_e - RE) < 1e-4
    assert abs(k - 2 * 4.7446 * 1.9426**2) / k < 1e-3
