"""Expériences numériques : densité d'îlots N(D/F), exposant chi, distribution de tailles.

Lancement : python src/analyse.py   (depuis le dossier du projet, ~3 min)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from kmc import EpitaxieKMC, exposant_nucleation

RACINE = Path(__file__).resolve().parents[1]
FIG = RACINE / "figures"
FIG.mkdir(exist_ok=True)
plt.rcParams.update({"figure.dpi": 130, "font.size": 10})

L = 160
THETA = 0.10
SEEDS = (1, 2)


def densite(D_sur_F: float, Eb_kT: float, seed: int):
    k = EpitaxieKMC(L, D_sur_F, Eb_kT=Eb_kT, seed=seed)
    k.deposer_jusqua(THETA)
    il = k.ilots(2)
    return len(il) / k.N, il, k


def balayage(ratios, Eb_kT):
    N_moy, N_err, toutes_tailles = [], [], {}
    for r in ratios:
        vals = []
        for s in SEEDS:
            n, il, _ = densite(r, Eb_kT, s)
            vals.append(n)
            toutes_tailles.setdefault(r, []).extend(il.tolist())
        N_moy.append(np.mean(vals))
        N_err.append(np.std(vals) / np.sqrt(len(vals)))
        print(f"  Eb/kT={Eb_kT}  D/F={r:.0e}  N={np.mean(vals):.5f}", flush=True)
    return np.array(N_moy), np.array(N_err), toutes_tailles


def ajuste(ratios, N):
    p = np.polyfit(np.log(ratios), np.log(N), 1)
    return -p[0], p


def main() -> dict:
    t0 = time.time()
    r_irr = np.array([1e3, 1e4, 1e5, 1e6, 1e7])
    r_rev = np.array([1e3, 1e4, 1e5, 1e6])
    EB = 4.0

    print("Agrégation irréversible (i* = 1)")
    N_irr, e_irr, tailles = balayage(r_irr, np.inf)
    chi_irr, p_irr = ajuste(r_irr[1:], N_irr[1:])
    print(f"Liaison finie Eb/kT = {EB}")
    N_rev, e_rev, _ = balayage(r_rev, EB)
    chi_rev, p_rev = ajuste(r_rev[-2:], N_rev[-2:])

    # ---- Figure 1 : loi d'échelle ----
    fig, ax = plt.subplots(figsize=(6.2, 4.4))
    ax.errorbar(r_irr, N_irr, e_irr, fmt="o", color="#1f4e79", label="KMC, irréversible (i* = 1)")
    x = np.logspace(3, 7, 50)
    ax.plot(x, np.exp(np.polyval(p_irr, np.log(x))), "-", color="#1f4e79", lw=1,
            label=f"ajustement : χ = {chi_irr:.3f}")
    ax.errorbar(r_rev, N_rev, e_rev, fmt="s", color="#b5651d", label=f"KMC, E_b/kT = {EB:g}")
    ref = N_irr[1] * (x / r_irr[1]) ** (-1 / 3)
    ax.plot(x, ref, "k:", lw=1, label="théorie : χ = 1/3")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("D/F"); ax.set_ylabel("densité d'îlots N (par site)")
    ax.set_title(f"Densité d'îlots à θ = {THETA:.2f} MC, réseau {L}×{L}")
    ax.legend(fontsize=8); fig.tight_layout(); fig.savefig(FIG / "01_loi_echelle.png"); plt.close(fig)

    # ---- Figure 2 : morphologies ----
    fig, axes = plt.subplots(1, 3, figsize=(10.5, 3.7))
    for ax, (r, eb, titre) in zip(axes, [(1e4, np.inf, "D/F = 10⁴"), (1e6, np.inf, "D/F = 10⁶"),
                                         (1e6, EB, f"D/F = 10⁶, E_b/kT = {EB:g}")]):
        _, il, k = densite(r, eb, 3)
        ax.imshow(k.grille(), cmap="Greys", interpolation="nearest")
        ax.set_title(f"{titre}\n{len(il)} îlots", fontsize=9); ax.set_xticks([]); ax.set_yticks([])
    fig.suptitle(f"Surface à θ = {THETA:.2f} MC (atomes déposés en noir)", fontsize=10)
    fig.tight_layout(); fig.savefig(FIG / "02_morphologies.png"); plt.close(fig)

    # ---- Figure 3 : distribution de tailles réduite ----
    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    for r in r_irr[1:]:
        s = np.array(tailles[r], float)
        sm = s.mean()
        h, b = np.histogram(s / sm, bins=np.linspace(0, 3, 16), density=True)
        ax.plot(0.5 * (b[1:] + b[:-1]), h, "o-", ms=3, label=f"D/F = {r:.0e}")
    ax.set_xlabel("s / ⟨s⟩"); ax.set_ylabel("distribution réduite")
    ax.set_title("Invariance d'échelle de la distribution de tailles")
    ax.legend(fontsize=8); fig.tight_layout(); fig.savefig(FIG / "03_distribution_tailles.png"); plt.close(fig)

    res = {
        "reseau": L, "couverture_MC": THETA, "graines": list(SEEDS),
        "irreversible": {"D_sur_F": r_irr.tolist(), "N": N_irr.tolist(),
                          "chi_mesure": round(float(chi_irr), 4),
                          "chi_theorie": round(exposant_nucleation(1), 4)},
        "liaison_finie": {"Eb_kT": EB, "D_sur_F": r_rev.tolist(), "N": N_rev.tolist(),
                           "chi_local_haut_D_sur_F": round(float(chi_rev), 4)},
        "duree_s": round(time.time() - t0, 1),
    }
    (RACINE / "resultats.json").write_text(json.dumps(res, indent=2, ensure_ascii=False))
    print(json.dumps(res, indent=2, ensure_ascii=False))
    return res


if __name__ == "__main__":
    main()
