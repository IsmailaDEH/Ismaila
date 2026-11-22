import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from simulation import energie_par_spin, m_onsager, mesurer  # noqa: E402


def test_energie_etat_ordonne():
    assert energie_par_spin(np.ones((8, 8))) == -2.0


def test_energie_damier_antiferro():
    i, j = np.indices((8, 8))
    s = np.where((i + j) % 2 == 0, 1, -1)
    assert energie_par_spin(s) == 2.0


def test_basse_temperature_ordonnee():
    assert mesurer(16, 1.0, 200, 200)["m"] > 0.99


def test_haute_temperature_desordonnee():
    assert mesurer(16, 5.0, 200, 500)["m"] < 0.2


def test_onsager_bornes():
    assert m_onsager(np.array([3.0]))[0] == 0.0
    assert 0.98 < m_onsager(np.array([1.5]))[0] < 1.0
