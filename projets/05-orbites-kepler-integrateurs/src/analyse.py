"""Étapes 2 à 4 — Comparaison des intégrateurs, vérification des lois de Kepler.

Lancement : python src/analyse.py   (depuis le dossier du projet)
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from simulation import (conditions_perihelie, energie, moment_cinetique, orbite,
                        periode_mesuree)

RACINE = Path(__file__).resolve().parents[1]
FIG = RACINE / "figures"
FIG.mkdir(exist_ok=True)
plt.rcParams.update({"figure.dpi": 120, "font.size": 10})
COULEURS = {"Euler": "#c0392b", "RK4": "#1f4e79", "Verlet": "#27ae60"}


def main() -> dict:
    res: dict = {}

    # --- Étape 2 : orbite excentrique (e = 0.6) sur 50 ans, dt = 1/200 an ----
    r0, v0 = conditions_perihelie(1.0, 0.6)
    dt, t_max = 1 / 200, 50.0
    traj = {m: orbite(m, r0, v0, dt, t_max) for m in ("Euler", "RK4", "Verlet")}

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    for m, (t, R, V) in traj.items():
        axes[0].plot(R[:, 0], R[:, 1], lw=0.5, color=COULEURS[m], label=m)
        E = energie(R, V)
        axes[1].semilogy(t[1:], np.abs((E[1:] - E[0]) / E[0]) + 1e-16, lw=0.8,
                         color=COULEURS[m], label=m)
    axes[0].plot(0, 0, "o", color="orange", ms=8)
    axes[0].set_aspect("equal")
    axes[0].set_xlim(-2.2, 1.2)
    axes[0].set_ylim(-1.5, 1.5)
    axes[0].set_title("Orbite e = 0,6 sur 50 révolutions")
    axes[0].legend(fontsize=8)
    axes[1].set_xlabel("t (années)")
    axes[1].set_ylabel("|ΔE / E0|")
    axes[1].set_title("Dérive de l'énergie")
    axes[1].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "01_integrateurs.png", bbox_inches="tight")
    plt.close(fig)

    tableau = {}
    for m, (t, R, V) in traj.items():
        E = energie(R, V)
        L = moment_cinetique(R, V)
        tableau[m] = {
            "derive_energie_finale": f"{abs((E[-1] - E[0]) / E[0]):.1e}",
            "derive_L_finale": f"{abs((L[-1] - L[0]) / L[0]):.1e}",
            "evaluations_force_par_pas": {"Euler": 1, "RK4": 4, "Verlet": 1}[m],
        }
    res["comparaison_50_ans"] = tableau

    # --- Étape 3 : ordre de convergence (erreur de position après 1 période) --
    pas = np.array([1 / 100, 1 / 200, 1 / 400, 1 / 800])
    ordres = {}
    fig, ax = plt.subplots(figsize=(5.5, 3.8))
    for m in ("Euler", "RK4", "Verlet"):
        err = []
        for h in pas:
            _, R, _ = orbite(m, r0, v0, h, 1.0)
            err.append(np.linalg.norm(R[-1] - r0))
        ordres[m] = round(float(np.polyfit(np.log(pas), np.log(err), 1)[0]), 2)
        ax.loglog(pas, err, "o-", color=COULEURS[m], label=f"{m} (pente {ordres[m]})")
    ax.set_xlabel("dt (années)")
    ax.set_ylabel("erreur de position après 1 an (UA)")
    ax.legend(fontsize=8)
    ax.set_title("Ordre de convergence")
    fig.savefig(FIG / "02_convergence.png", bbox_inches="tight")
    plt.close(fig)
    res["ordres_convergence"] = ordres

    # --- Étape 4 : 3e loi de Kepler sur les planètes du système solaire ------
    planetes = {"Mercure": (0.387, 0.206), "Vénus": (0.723, 0.007), "Terre": (1.0, 0.017),
                "Mars": (1.524, 0.093), "Jupiter": (5.203, 0.049), "Saturne": (9.537, 0.056)}
    a_list, T_list = [], []
    for nom, (a, e) in planetes.items():
        r0p, v0p = conditions_perihelie(a, e)
        T_th = a**1.5
        t, R, _ = orbite("Verlet", r0p, v0p, T_th / 2000, 3.2 * T_th)
        a_list.append(a)
        T_list.append(periode_mesuree(t, R))
    pente, ordonnee = np.polyfit(np.log(a_list), np.log(T_list), 1)
    res["kepler_3"] = {
        "pente_logT_loga": round(float(pente), 4),
        "theorique": 1.5,
        "periodes_annees": {n: round(T, 3) for n, T in zip(planetes, T_list)},
    }
    fig, ax = plt.subplots(figsize=(5.5, 3.8))
    ax.loglog(a_list, T_list, "o", color="#1f4e79")
    for n, a, T in zip(planetes, a_list, T_list):
        ax.annotate(n, (a, T), textcoords="offset points", xytext=(5, -10), fontsize=8)
    aa = np.logspace(np.log10(0.3), np.log10(12), 50)
    ax.loglog(aa, np.exp(ordonnee) * aa**pente, "--", color="grey",
              label=f"ajustement : T ∝ a^{pente:.3f}")
    ax.set_xlabel("demi-grand axe a (UA)")
    ax.set_ylabel("période T (années)")
    ax.legend(fontsize=8)
    ax.set_title("3e loi de Kepler retrouvée par simulation")
    fig.savefig(FIG / "03_kepler.png", bbox_inches="tight")
    plt.close(fig)

    (RACINE / "resultats.json").write_text(json.dumps(res, indent=2, ensure_ascii=False))
    print(json.dumps(res, indent=2, ensure_ascii=False))
    return res


if __name__ == "__main__":
    main()
