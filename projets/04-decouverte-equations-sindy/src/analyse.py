"""Étapes 4 et 5 — Robustesse au bruit, validation par simulation du modèle appris.

Lancement : python src/analyse.py   (depuis le dossier du projet)
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

from sindy import (LORENZ_VRAI, bibliotheque, coefficients_lorenz, coeffs_vrais, derivee,
                   equations, simuler_lorenz, stlsq)

RACINE = Path(__file__).resolve().parents[1]
FIG = RACINE / "figures"
FIG.mkdir(exist_ok=True)
plt.rcParams.update({"figure.dpi": 120, "font.size": 10})


def main() -> dict:
    res: dict = {}
    dt = 0.002
    t, X = simuler_lorenz(dt=dt)
    rng = np.random.default_rng(42)
    ecart_type = X.std(axis=0)

    # --- Étape 4 : tableau des résultats selon le niveau de bruit ---------
    tableau = []
    for bruit in (0.0, 0.001, 0.01, 0.05):
        Xb = X + bruit * ecart_type * rng.standard_normal(X.shape)
        lissage = 0 if bruit == 0 else 21
        dX = derivee(Xb, dt, lissage)
        coupe = slice(100, -100)
        Theta, noms = bibliotheque(Xb[coupe])
        Xi = stlsq(Theta, dX[coupe], seuil=0.5)
        c = coefficients_lorenz(Xi, noms)
        vrai = coeffs_vrais(noms)
        tableau.append({
            "bruit_pct": bruit * 100,
            **{k: round(v, 3) for k, v in c.items()},
            "erreur_max_pct": round(max(abs(c[k] - LORENZ_VRAI[k]) / LORENZ_VRAI[k] * 100
                                        for k in c), 2),
            "structure_exacte": bool(np.array_equal(Xi != 0, vrai != 0)),
        })
        if bruit == 0.01:
            Xi_ref, noms_ref = Xi, noms
    res["tableau_bruit"] = tableau
    res["equations_bruit_1pct"] = equations(Xi_ref, noms_ref, prec=2)

    # --- Étape 5 : on simule le modèle découvert et on compare -----------
    def modele(_t, x):
        th, _ = bibliotheque(np.atleast_2d(x))
        return (th @ Xi_ref)[0]

    tt = np.arange(0, 20, dt)
    sol = solve_ivp(modele, (0, 20), X[0], t_eval=tt, rtol=1e-10, atol=1e-10)
    Y = sol.y.T
    ecart = np.linalg.norm(Y - X[: len(Y)], axis=1)
    horizon = float(tt[np.argmax(ecart > 0.25 * np.linalg.norm(ecart_type))])
    res["horizon_prediction_s"] = round(horizon, 2)

    fig = plt.figure(figsize=(10, 4.2))
    ax = fig.add_subplot(1, 2, 1, projection="3d")
    ax.plot(*X.T, lw=0.4, color="#1f4e79", label="données")
    ax.plot(*Y.T, lw=0.4, color="#c0392b", alpha=0.7, label="modèle SINDy")
    ax.set_title("Attracteur de Lorenz")
    ax.legend(fontsize=8)
    ax2 = fig.add_subplot(1, 2, 2)
    ax2.plot(tt, X[: len(tt), 0], color="#1f4e79", lw=1, label="x vrai")
    ax2.plot(tt, Y[:, 0], "--", color="#c0392b", lw=1, label="x prédit")
    ax2.axvline(horizon, color="grey", ls=":", label=f"horizon ≈ {horizon:.1f} s")
    ax2.set_xlabel("t")
    ax2.legend(fontsize=8)
    ax2.set_title("Prédiction à partir du modèle appris (bruit 1 %)")
    fig.tight_layout()
    fig.savefig(FIG / "01_attracteur_prediction.png", bbox_inches="tight")
    plt.close(fig)

    # Carte des coefficients : vrai vs identifié
    fig, axes = plt.subplots(1, 2, figsize=(7, 4), sharey=True)
    for ax, M, titre in zip(axes, (coeffs_vrais(noms_ref), Xi_ref), ("Vrai", "Identifié (bruit 1 %)")):
        im = ax.imshow(M, cmap="RdBu_r", vmin=-30, vmax=30, aspect="auto")
        ax.set_xticks(range(3), ["ẋ", "ẏ", "ż"])
        ax.set_yticks(range(len(noms_ref)), noms_ref)
        ax.set_title(titre)
        for (i, j), v in np.ndenumerate(M):
            if v:
                ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=7)
    fig.colorbar(im, ax=axes, shrink=0.8)
    fig.savefig(FIG / "02_coefficients.png", bbox_inches="tight")
    plt.close(fig)

    (RACINE / "resultats.json").write_text(json.dumps(res, indent=2, ensure_ascii=False))
    print(json.dumps(res, indent=2, ensure_ascii=False))
    return res


if __name__ == "__main__":
    main()
