"""Étapes 2 à 4 — Balayage en température, effet de taille finie, estimation de T_c.

Lancement : python src/analyse.py   (depuis le dossier du projet)
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from simulation import T_C_ONSAGER, m_onsager, mesurer

RACINE = Path(__file__).resolve().parents[1]
FIG = RACINE / "figures"
FIG.mkdir(exist_ok=True)
plt.rcParams.update({"figure.dpi": 120, "font.size": 10})

TAILLES = (8, 16, 32)
TEMPS = np.round(np.concatenate([np.linspace(1.5, 2.1, 5), np.linspace(2.15, 2.45, 13),
                                 np.linspace(2.6, 3.5, 5)]), 3)


def main() -> dict:
    data = {}
    for L in TAILLES:
        lignes = []
        s = None
        for T in TEMPS:  # on part de l'état précédent (recuit) pour thermaliser vite
            r = mesurer(L, T, n_therm=800, n_mes=4000, seed=int(T * 1000) + L, s0=s)
            s = r.pop("etat")
            lignes.append({k: float(v) for k, v in r.items()})
        data[L] = lignes
        print(f"L={L} terminé")

    noms = {"m": "⟨|m|⟩", "e": "⟨e⟩", "chi": "χ", "cv": "C_v"}
    fig, axes = plt.subplots(2, 2, figsize=(9, 6.5))
    for ax, cle in zip(axes.ravel(), noms):
        for L in TAILLES:
            ax.plot(TEMPS, [d[cle] for d in data[L]], "o-", ms=3, label=f"L = {L}")
        if cle == "m":
            Tf = np.linspace(1.5, 3.5, 400)
            ax.plot(Tf, m_onsager(Tf), "k--", lw=1, label="Onsager (L→∞)")
        ax.axvline(T_C_ONSAGER, color="grey", ls=":", lw=1)
        ax.set_xlabel("T (J/k_B)")
        ax.set_ylabel(noms[cle])
    axes[0, 0].legend(fontsize=8)
    fig.suptitle("Ising 2D — observables thermodynamiques")
    fig.tight_layout()
    fig.savefig(FIG / "01_observables.png", bbox_inches="tight")
    plt.close(fig)

    # T_c(L) par le pic de susceptibilité (ajustement parabolique local)
    tc_L = {}
    for L in TAILLES:
        chi = np.array([d["chi"] for d in data[L]])
        k = int(np.argmax(chi))
        k = min(max(k, 1), len(TEMPS) - 2)
        a, b, _ = np.polyfit(TEMPS[k - 1:k + 2], chi[k - 1:k + 2], 2)
        tc_L[L] = float(-b / (2 * a))

    # Taille finie : T_c(L) = T_c(∞) + a / L  (ν = 1 en 2D)
    invL = np.array([1 / L for L in TAILLES])
    pente, tc_inf = np.polyfit(invL, [tc_L[L] for L in TAILLES], 1)
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.plot(invL, [tc_L[L] for L in TAILLES], "o", label="pic de χ")
    xx = np.linspace(0, invL.max() * 1.05, 50)
    ax.plot(xx, tc_inf + pente * xx, "--", label=f"extrapolation : T_c = {tc_inf:.3f}")
    ax.axhline(T_C_ONSAGER, color="k", ls=":", label=f"Onsager : {T_C_ONSAGER:.3f}")
    ax.set_xlabel("1 / L")
    ax.set_ylabel("T_c(L)")
    ax.legend(fontsize=8)
    ax.set_title("Analyse de taille finie")
    fig.savefig(FIG / "02_taille_finie.png", bbox_inches="tight")
    plt.close(fig)

    # Instantanés de configurations
    fig, axes = plt.subplots(1, 3, figsize=(9, 3.2))
    for ax, T in zip(axes, (1.8, T_C_ONSAGER, 3.2)):
        s = mesurer(64, T, n_therm=1500, n_mes=1, seed=1)["etat"]
        ax.imshow(s, cmap="Greys", interpolation="nearest")
        ax.set_title(f"T = {T:.2f}")
        ax.axis("off")
    fig.suptitle("Configurations de spins (L = 64)")
    fig.savefig(FIG / "03_configurations.png", bbox_inches="tight")
    plt.close(fig)

    res = {
        "Tc_par_taille": {str(L): round(v, 3) for L, v in tc_L.items()},
        "Tc_extrapole": round(float(tc_inf), 3),
        "Tc_onsager": round(float(T_C_ONSAGER), 3),
        "erreur_relative_pct": round(float(abs(tc_inf - T_C_ONSAGER) / T_C_ONSAGER * 100), 2),
    }
    (RACINE / "resultats.json").write_text(json.dumps(res, indent=2, ensure_ascii=False))
    print(json.dumps(res, indent=2, ensure_ascii=False))
    return res


if __name__ == "__main__":
    main()
