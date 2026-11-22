import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from chsh import (ANGLES_OPTIMAUX, S_max_strategies_deterministes, S_quantique,  # noqa: E402
                  S_werner, correlation_locale_exacte, correlation_quantique,
                  mesures_locales, mesures_quantiques)


def test_correlation_singulet_formule():
    for a, b in [(0, 0), (0.3, 1.2), (2.0, -0.5)]:
        assert np.isclose(correlation_quantique(a, b), -np.cos(a - b))


def test_tsirelson():
    assert np.isclose(abs(S_quantique(*ANGLES_OPTIMAUX)), 2 * np.sqrt(2))


def test_borne_locale_deterministe():
    assert S_max_strategies_deterministes() == 2


def test_modele_local_suit_formule():
    rng = np.random.default_rng(0)
    assert abs(mesures_locales(0, 1.0, 200000, rng).mean() - correlation_locale_exacte(0, 1.0)) < 0.01


def test_mesures_quantiques_statistiques():
    rng = np.random.default_rng(1)
    r = mesures_quantiques(0, np.pi / 3, 200000, rng)
    assert set(np.unique(r)) <= {-1, 1}
    assert abs(r.mean() + np.cos(np.pi / 3)) < 0.01


def test_werner():
    assert np.isclose(S_werner(1.0), 2 * np.sqrt(2))
    assert np.isclose(S_werner(1 / np.sqrt(2)), 2.0)
