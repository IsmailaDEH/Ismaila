"""Étapes 3 à 5 — Propagation d'incertitude, apprentissage actif, erreur de modèle.

Lancement : python src/analyse.py   (depuis le dossier du projet)
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

from gp import (OMEGA_VRAI, RE, ProcessusGaussien, morse, nombre_onde, proprietes)

RACINE = Path(__file__).resolve().parents[1]
FIG = RACINE / "figures"
FIG.mkdir(exist_ok=True)
plt.rcParams.update({"figure.dpi": 120, "font.size": 10})
BRUIT = 0.02  # eV, bruit des « calculs de référence »
GRILLE = np.linspace(0.45, 3.0, 600)


def main() -> dict:
    rng = np.random.default_rng(7)
    res: dict = {}

    # --- Étape 3 : GP sur 14 points bruités, propagation de l'incertitude ---
    x = np.sort(np.concatenate([np.linspace(0.5, 1.2, 8), np.linspace(1.4, 2.9, 6)]))
    y = morse(x) + BRUIT * rng.standard_normal(len(x))
    gp = ProcessusGaussien().ajuster(x, y)
    mu, sd = gp.predire(GRILLE)
    vrai = morse(GRILLE)
    couverture = float(np.mean(np.abs(mu - vrai) < 1.96 * sd))

    ech = gp.echantillons(GRILLE, 2000, rng)
    props = np.array([proprietes(GRILLE, e) for e in ech])
    r_e, k = props[:, 0], props[:, 1]
    om = nombre_onde(np.clip(k, 1e-6, None))
    res["gp"] = {
        "hyperparametres": {"amplitude_eV": round(float(gp.amp), 3),
                            "longueur_A": round(float(gp.ell), 3),
                            "bruit_estime_eV": round(float(gp.bruit), 4),
                            "bruit_reel_eV": BRUIT},
        "couverture_intervalle_95pct": round(couverture, 3),
        "r_e_A": [round(float(r_e.mean()), 4), round(float(r_e.std()), 4)],
        "r_e_vrai_A": RE,
        "omega_cm-1": [round(float(om.mean()), 0), round(float(om.std()), 0)],
        "omega_vrai_cm-1": round(OMEGA_VRAI, 0),
    }

    fig, axes = plt.subplots(1, 3, figsize=(13, 3.8), gridspec_kw={"width_ratios": [1.6, 1, 1]})
    ax = axes[0]
    ax.fill_between(GRILLE, mu - 1.96 * sd, mu + 1.96 * sd, color="#1f4e79", alpha=0.2,
                    label="GP : intervalle à 95 %")
    ax.plot(GRILLE, vrai, "k--", lw=1, label="référence (Morse)")
    ax.plot(GRILLE, mu, color="#1f4e79", label="GP : moyenne")
    ax.plot(x, y, "o", color="#c0392b", ms=4, label="données bruitées")
    ax.set_ylim(-5.2, 1.5)
    ax.set_xlabel("distance H–H (Å)")
    ax.set_ylabel("énergie (eV)")
    ax.set_title("Potentiel H₂ appris avec incertitude")
    ax.legend(fontsize=7)
    axes[1].hist(r_e, bins=40, color="#1f4e79", alpha=0.7)
    axes[1].axvline(RE, color="k", ls="--", label="vrai")
    axes[1].set_xlabel("r_e (Å)")
    axes[1].set_title("Distance d'équilibre")
    axes[1].legend(fontsize=7)
    axes[2].hist(om, bins=40, color="#27ae60", alpha=0.7)
    axes[2].axvline(OMEGA_VRAI, color="k", ls="--", label="vrai")
    axes[2].set_xlabel("ω_e (cm⁻¹)")
    axes[2].set_title("Fréquence de vibration")
    axes[2].legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(FIG / "01_gp_incertitude.png", bbox_inches="tight")
    plt.close(fig)

    # --- Étape 4 : apprentissage actif (on calcule là où le GP doute le plus) ---
    def erreur(xx, yy):
        g = ProcessusGaussien().ajuster(xx, yy)
        m, s = g.predire(GRILLE)
        zone = GRILLE < 2.5
        return g, float(np.sqrt(np.mean((m - vrai)[zone] ** 2))), float(np.mean(s[zone]))

    rng2 = np.random.default_rng(3)
    depart = np.array([0.55, 0.9, 1.6, 2.8])
    courbes = {}
    for strategie in ("actif", "aleatoire"):
        xx = depart.copy()
        yy = morse(xx) + BRUIT * rng2.standard_normal(len(xx))
        rmse = []
        for _ in range(14):
            g, e, _ = erreur(xx, yy)
            rmse.append(e)
            if strategie == "actif":
                _, s = g.predire(GRILLE)
                xn = GRILLE[np.argmax(s)]
            else:
                xn = rng2.uniform(0.45, 3.0)
            xx = np.append(xx, xn)
            yy = np.append(yy, morse(xn) + BRUIT * rng2.standard_normal())
        courbes[strategie] = rmse
    n_pts = np.arange(len(depart), len(depart) + 14)
    fig, ax = plt.subplots(figsize=(5.5, 3.6))
    ax.semilogy(n_pts, courbes["actif"], "o-", label="actif (max. d'incertitude)")
    ax.semilogy(n_pts, courbes["aleatoire"], "s--", label="aléatoire")
    ax.axhline(BRUIT, color="grey", ls=":", label="niveau de bruit")
    ax.set_xlabel("nombre de calculs de référence")
    ax.set_ylabel("RMSE (eV)")
    ax.set_title("Apprentissage actif")
    ax.legend(fontsize=8)
    fig.savefig(FIG / "02_apprentissage_actif.png", bbox_inches="tight")
    plt.close(fig)
    res["apprentissage_actif_rmse_eV_apres_12_points"] = {
        "actif": round(courbes["actif"][8], 4), "aleatoire": round(courbes["aleatoire"][8], 4)}

    # --- Étape 5 : erreur de forme du modèle (Lennard-Jones ajusté aux mêmes données) ---
    def lj(r, eps, sig):
        return 4 * eps * ((sig / r) ** 12 - (sig / r) ** 6)

    p, cov = curve_fit(lj, x, y, p0=[4.7, 0.66])
    e_p = np.sqrt(np.diag(cov))
    ech_lj = rng.multivariate_normal(p, cov, 2000)
    props_lj = np.array([proprietes(GRILLE, lj(GRILLE, *q)) for q in ech_lj])
    om_lj = nombre_onde(props_lj[:, 1])
    res["lennard_jones"] = {
        "r_e_A": [round(float(props_lj[:, 0].mean()), 4), round(float(props_lj[:, 0].std()), 4)],
        "omega_cm-1": [round(float(om_lj.mean()), 0), round(float(om_lj.std()), 0)],
        "parametres": {"eps_eV": [round(p[0], 3), round(e_p[0], 3)],
                       "sigma_A": [round(p[1], 4), round(e_p[1], 4)]},
    }
    fig, ax = plt.subplots(figsize=(5.5, 3.6))
    ax.plot(GRILLE, vrai, "k--", lw=1, label="référence")
    ax.plot(GRILLE, mu, color="#1f4e79", label="GP")
    ax.plot(GRILLE, lj(GRILLE, *p), color="#c0392b", label="Lennard-Jones ajusté")
    ax.plot(x, y, "o", color="grey", ms=3)
    ax.set_ylim(-5.2, 1.5)
    ax.set_xlabel("distance H–H (Å)")
    ax.set_ylabel("énergie (eV)")
    ax.set_title("Erreur de forme : un modèle trop rigide")
    ax.legend(fontsize=8)
    fig.savefig(FIG / "03_erreur_de_modele.png", bbox_inches="tight")
    plt.close(fig)

    (RACINE / "resultats.json").write_text(json.dumps(res, indent=2, ensure_ascii=False))
    print(json.dumps(res, indent=2, ensure_ascii=False))
    return res


if __name__ == "__main__":
    main()
