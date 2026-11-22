"""Étapes 4 et 5 — Expérience de Bell simulée, optimisation des angles, bruit (état de Werner).

Lancement : python src/analyse.py   (depuis le dossier du projet)
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize

from chsh import (ANGLES_OPTIMAUX, S_experience, S_max_strategies_deterministes,
                  S_quantique, S_werner, correlation_locale_exacte, correlation_quantique,
                  mesures_locales)

RACINE = Path(__file__).resolve().parents[1]
FIG = RACINE / "figures"
FIG.mkdir(exist_ok=True)
plt.rcParams.update({"figure.dpi": 120, "font.size": 10})


def main() -> dict:
    rng = np.random.default_rng(2026)
    res: dict = {}

    # --- Corrélations : quantique vs modèle local --------------------------
    d = np.linspace(0, np.pi, 200)
    fig, ax = plt.subplots(figsize=(5.8, 3.8))
    ax.plot(d, [correlation_quantique(0, x) for x in d], label="quantique : −cos(a−b)")
    ax.plot(d, correlation_locale_exacte(0, d), "--", label="modèle local de Bell")
    pts = np.linspace(0, np.pi, 13)
    ax.plot(pts, [mesures_locales(0, x, 20000, rng).mean() for x in pts], "o", ms=3,
            color="#c0392b", label="modèle local simulé")
    ax.set_xlabel("a − b (rad)")
    ax.set_ylabel("E(a, b)")
    ax.set_title("Corrélations de spin pour l'état singulet")
    ax.legend(fontsize=8)
    fig.savefig(FIG / "01_correlations.png", bbox_inches="tight")
    plt.close(fig)

    # --- Étape 4 : expérience simulée -----------------------------------------
    S_th = S_quantique(*ANGLES_OPTIMAUX)
    S_q, e_q = S_experience(ANGLES_OPTIMAUX, 10000, rng)
    S_l, e_l = S_experience(ANGLES_OPTIMAUX, 10000, rng, mesure=mesures_locales)
    res["experience_10000_paires_par_reglage"] = {
        "S_quantique_theorie": round(S_th, 4),
        "S_quantique_mesure": [round(float(S_q), 3), round(float(e_q), 3)],
        "violation_en_ecarts_types": round(float((abs(S_q) - 2) / e_q), 1),
        "S_modele_local": [round(float(S_l), 3), round(float(e_l), 3)],
        "S_max_16_strategies_deterministes": S_max_strategies_deterministes(),
    }

    # --- Étape 5a : optimisation numérique des angles (borne de Tsirelson) -----
    meilleur = max((minimize(lambda t: -abs(S_quantique(*t)), rng.uniform(0, np.pi, 4))
                    for _ in range(20)), key=lambda r: -r.fun)
    res["S_max_optimise"] = round(float(-meilleur.fun), 6)
    res["tsirelson_2rac2"] = round(float(2 * np.sqrt(2)), 6)

    # Histogramme : distribution de S sur 500 expériences de 1000 paires
    Sq = [abs(S_experience(ANGLES_OPTIMAUX, 1000, rng)[0]) for _ in range(500)]
    Sl = [abs(S_experience(ANGLES_OPTIMAUX, 1000, rng, mesure=mesures_locales)[0])
          for _ in range(500)]
    fig, ax = plt.subplots(figsize=(5.8, 3.6))
    ax.hist(Sl, bins=30, alpha=0.7, color="#c0392b", label="modèle local")
    ax.hist(Sq, bins=30, alpha=0.7, color="#1f4e79", label="mécanique quantique")
    ax.axvline(2, color="k", ls="--", label="borne de Bell : 2")
    ax.axvline(2 * np.sqrt(2), color="grey", ls=":", label="Tsirelson : 2√2")
    ax.set_xlabel("|S|")
    ax.set_title("500 expériences simulées (1000 paires par réglage)")
    ax.legend(fontsize=8)
    fig.savefig(FIG / "02_distribution_S.png", bbox_inches="tight")
    plt.close(fig)

    # --- Étape 5b : décohérence — état de Werner ------------------------------
    ps = np.linspace(0, 1, 101)
    Sw = np.array([S_werner(p) for p in ps])
    p_seuil = float(ps[np.argmax(Sw > 2)])
    res["werner_seuil_violation"] = {"numerique": round(p_seuil, 3),
                                     "theorique_1_sur_rac2": round(1 / np.sqrt(2), 3)}
    fig, ax = plt.subplots(figsize=(5.8, 3.6))
    ax.plot(ps, Sw, color="#1f4e79")
    ax.axhline(2, color="k", ls="--", lw=1)
    ax.axvline(1 / np.sqrt(2), color="grey", ls=":", label="p = 1/√2")
    ax.fill_between(ps, 2, Sw, where=Sw > 2, color="#1f4e79", alpha=0.15,
                    label="violation de Bell")
    ax.set_xlabel("pureté p de l'état de Werner")
    ax.set_ylabel("S maximal")
    ax.set_title("Bruit et non-localité")
    ax.legend(fontsize=8)
    fig.savefig(FIG / "03_werner.png", bbox_inches="tight")
    plt.close(fig)

    (RACINE / "resultats.json").write_text(json.dumps(res, indent=2, ensure_ascii=False))
    print(json.dumps(res, indent=2, ensure_ascii=False))
    return res


if __name__ == "__main__":
    main()
