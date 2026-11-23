import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from kmc import EpitaxieKMC, exposant_nucleation, tailles_amas  # noqa: E402


def test_exposant_theorique():
    assert exposant_nucleation(1) == 1 / 3
    assert exposant_nucleation(2) == 0.5


def test_couverture_exacte():
    k = EpitaxieKMC(40, 1e3, seed=0)
    k.deposer_jusqua(0.05)
    assert k.couverture == round(0.05 * 1600) / 1600


def test_classes_coherentes():
    """Chaque atome est rangé dans la classe correspondant à son nombre de voisins."""
    k = EpitaxieKMC(30, 1e3, Eb_kT=3.0, seed=4)
    k.deposer_jusqua(0.2)
    total = 0
    for n, lst in enumerate(k.classes):
        for s in lst:
            assert k._nvois(s) == n
        total += len(lst)
    assert total == int(k.occ.sum())


def test_marche_aleatoire_diffusion():
    """Sans dépôt, un adatome seul diffuse : <r^2> = h0 * t (pas a = 1).

    On teste ici le moteur BKL lui-même (horloge exponentielle + choix des sauts).
    """
    h0, T, L = 2.0, 40.0, 101
    msd = []
    for seed in range(400):
        k = EpitaxieKMC(L, h0, seed=seed, flux=0.0)
        s0 = (L // 2) * L + L // 2
        k._poser(s0)
        while True:
            k.pas()
            if k.t > T:
                break
            pos = k.classes[0][0]
        x, y = pos % L - L // 2, pos // L - L // 2
        msd.append(x * x + y * y)
    assert abs(np.mean(msd) / (h0 * T) - 1) < 0.12


def test_amas_periodiques():
    g = np.zeros((6, 6), int)
    g[0, 2] = g[5, 2] = 1          # relié par le bord haut/bas
    g[3, 0] = g[3, 5] = 1          # relié par le bord gauche/droite
    g[2, 2] = 1                    # isolé
    assert sorted(tailles_amas(g).tolist()) == [1, 2, 2]


def test_densite_diminue_avec_D_sur_F():
    def N(r):
        k = EpitaxieKMC(60, r, seed=2)
        k.deposer_jusqua(0.1)
        return len(k.ilots())
    assert N(1e3) > N(1e5)
