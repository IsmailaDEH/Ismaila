"""Transition de Mott et limite de Heisenberg dans le modèle de Hubbard 1D.

Lancement : python src/analyse.py   (depuis le dossier du projet, ~2 min)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from hubbard import (correlations_spin, dimension, double_occupation, energie, energie_libre,
                     energie_lieb_wu, gap_de_charge, gap_de_spin, gap_lieb_wu, heisenberg)

RACINE = Path(__file__).resolve().parents[1]
FIG = RACINE / "figures"
FIG.mkdir(exist_ok=True)
plt.rcParams.update({"figure.dpi": 130, "font.size": 10})

# L = 4n + 2 : couche fermée à U = 0 (pas de dégénérescence parasite du fondamental)
TAILLES = (6, 10)
COUL = {6: "#8fb0d3", 10: "#1f4e79"}


def main() -> dict:
    t0 = time.time()
    res: dict = {"t": 1.0, "tailles": list(TAILLES),
                 "dimension_max": dimension(10, 5, 5)}

    # ---- 1. Validation U = 0 ----
    res["ecart_U0_vs_fermions_libres"] = max(
        abs(energie(L, L // 2, L // 2, 0.0) - energie_libre(L, L // 2, L // 2)) for L in TAILLES)

    # ---- 2. Énergie et gap de charge en fonction de U ----
    U = np.array([0.0, 1, 2, 3, 4, 6, 8, 10, 12, 16, 20])
    E = {L: [energie(L, L // 2, L // 2, u) / L for u in U] for L in TAILLES}
    G = {L: [gap_de_charge(L, u) for u in U] for L in TAILLES}
    print("énergies et gaps calculés", flush=True)
    Uf = np.linspace(0, 20, 200)
    E_bethe = [energie_lieb_wu(u) for u in Uf]
    G_bethe = [gap_lieb_wu(u) if u > 0 else 0 for u in Uf]

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2))
    ax = axes[0]
    for L in TAILLES:
        ax.plot(U, E[L], "o", ms=4, color=COUL[L], label=f"ED, L = {L}")
    ax.plot(Uf, E_bethe, "k-", lw=1, label="Bethe ansatz (Lieb–Wu), L → ∞")
    ax.set_xlabel("U / t"); ax.set_ylabel("E₀ / (L t)"); ax.set_title("Énergie fondamentale, demi-remplissage")
    ax.legend(fontsize=8)
    ax = axes[1]
    for L in TAILLES:
        ax.plot(U, G[L], "o", ms=4, color=COUL[L], label=f"ED, L = {L}")
    ax.plot(Uf, G_bethe, "k-", lw=1, label="Lieb–Wu, L → ∞")
    ax.plot(Uf, Uf - 4, "k:", lw=0.8, label="U − 4t (atomique)")
    ax.set_ylim(0, 17)
    ax.set_xlabel("U / t"); ax.set_ylabel("Δ_c / t"); ax.set_title("Gap de charge : isolant de Mott")
    ax.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(FIG / "01_energie_gap_mott.png"); plt.close(fig)

    res["energie_par_site_L10"] = {f"U={u:g}": round(e, 5) for u, e in zip(U, E[10])}
    res["energie_par_site_bethe"] = {f"U={u:g}": round(energie_lieb_wu(u), 5) for u in U}
    res["gap_charge_L10"] = {f"U={u:g}": round(g, 4) for u, g in zip(U, G[10])}
    res["gap_charge_bethe"] = {f"U={u:g}": round(gap_lieb_wu(u), 4) for u in U if u > 0}

    # ---- 3. Double occupation + vérification Hellmann–Feynman ----
    Ud = np.linspace(0, 16, 17)
    D = [double_occupation(10, u) for u in Ud]
    h = 1e-3
    hf = (energie(10, 5, 5, 4 + h) - energie(10, 5, 5, 4 - h)) / (2 * h) / 10
    res["hellmann_feynman_U4"] = {"dE_dU_par_site": round(hf, 6),
                                  "double_occupation": round(double_occupation(10, 4.0), 6)}

    # ---- 4. Limite U >> t : modèle de Heisenberg, J = 4t²/U ----
    Us = np.array([4.0, 6, 8, 12, 16, 24, 32, 48])
    gap_hub = np.array([gap_de_spin(10, u) for u in Us])
    gap_heis = np.array([heisenberg(10, 4 / u, 1) - heisenberg(10, 4 / u, 0) for u in Us])
    res["gap_spin_L10"] = {f"U={u:g}": {"Hubbard": round(a, 5), "Heisenberg_J=4t2/U": round(b, 5),
                                        "rapport": round(a / b, 4)} for u, a, b in zip(Us, gap_hub, gap_heis)}
    C = correlations_spin(10, 8.0)
    res["correlations_SzSz_U8_L10"] = [round(c, 5) for c in C]
    print("Heisenberg et corrélations calculés", flush=True)

    fig, axes = plt.subplots(1, 3, figsize=(13, 3.9))
    ax = axes[0]
    ax.plot(Ud, D, "o-", ms=4, color="#1f4e79")
    ax.axhline(0.25, color="grey", ls=":", lw=1)
    ax.text(10, 0.235, "U = 0 : ⟨n↑n↓⟩ = 1/4", fontsize=8, color="grey")
    ax.set_xlabel("U / t"); ax.set_ylabel("⟨n↑ n↓⟩"); ax.set_title("Double occupation (L = 10)")
    ax = axes[1]
    ax.plot(Us, gap_hub, "o", color="#1f4e79", label="Hubbard (ED)")
    ax.plot(Us, gap_heis, "s", mfc="none", color="#b5651d", label="Heisenberg, J = 4t²/U")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xticks([4, 8, 16, 32, 48]); ax.set_xticklabels(["4", "8", "16", "32", "48"])
    ax.minorticks_off()
    ax.set_xlabel("U / t"); ax.set_ylabel("E(S=1) − E(S=0)")
    ax.set_title("Gap singulet–triplet (L = 10)")
    ax2 = ax.twinx(); ax2.plot(Us, gap_hub / gap_heis, "k--", lw=0.8); ax2.set_ylabel("rapport", fontsize=8)
    ax2.set_ylim(0.5, 1.5); ax.legend(fontsize=8, loc="lower left")
    ax = axes[2]
    r = np.arange(10)
    ax.bar(r, C, color=["#1f4e79" if c > 0 else "#b5651d" for c in C])
    ax.axhline(0, color="k", lw=0.6)
    ax.set_xlabel("distance r"); ax.set_ylabel("⟨S^z_0 S^z_r⟩")
    ax.set_title("Corrélations antiferromagnétiques (U = 8t)")
    fig.tight_layout(); fig.savefig(FIG / "02_heisenberg_correlations.png"); plt.close(fig)

    res["duree_s"] = round(time.time() - t0, 1)
    (RACINE / "resultats.json").write_text(json.dumps(res, indent=2, ensure_ascii=False))
    print(json.dumps(res, indent=2, ensure_ascii=False))
    return res


if __name__ == "__main__":
    main()
