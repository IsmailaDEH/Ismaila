"""Étapes 2 à 4 — Simulation, mesure du chaos et génération des figures.

Lancement : python src/analyse.py   (depuis le dossier du projet)
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from simulation import energie, integrer, lyapunov_max, positions

RACINE = Path(__file__).resolve().parents[1]
FIG = RACINE / "figures"
FIG.mkdir(exist_ok=True)
plt.rcParams.update({"figure.dpi": 120, "font.size": 10})


def main() -> dict:
    res: dict = {}

    # --- Étape 2 : trajectoire chaotique -------------------------------
    x0 = np.radians([120.0, 0.0, -10.0, 0.0])
    t, X = integrer(x0, t_max=30.0, dt=1e-3)
    x1, y1, x2, y2 = positions(X)
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.plot(x2, y2, lw=0.4, color="#1f4e79")
    ax.plot([0, x1[-1], x2[-1]], [0, y1[-1], y2[-1]], "o-", color="#c0392b")
    ax.set_aspect("equal")
    ax.set_title("Trajectoire de la masse 2 (θ1=120°, θ2=-10°)")
    fig.savefig(FIG / "01_trajectoire.png", bbox_inches="tight")
    plt.close(fig)

    # --- Étape 3 : conservation de l'énergie vs pas de temps ----------
    derives = {}
    fig, ax = plt.subplots(figsize=(6, 3.5))
    for dt in (1e-2, 5e-3, 1e-3):
        t_, X_ = integrer(x0, t_max=30.0, dt=dt)
        E = energie(X_)
        err = np.abs((E - E[0]) / E[0])
        derives[str(dt)] = float(err.max())
        ax.semilogy(t_[1:], err[1:] + 1e-18, label=f"dt = {dt:g} s")
    ax.set_xlabel("t (s)")
    ax.set_ylabel("|ΔE / E0|")
    ax.set_title("Dérive relative de l'énergie (RK4)")
    ax.legend()
    fig.savefig(FIG / "02_energie.png", bbox_inches="tight")
    plt.close(fig)
    res["derive_energie_max"] = derives
    pente = np.polyfit(np.log([1e-2, 5e-3, 1e-3]), np.log(list(derives.values())), 1)[0]
    res["ordre_convergence_energie"] = round(float(pente), 2)

    # --- Étape 4 : sensibilité aux conditions initiales --------------
    xb = x0 + np.array([1e-9, 0, 0, 0])
    _, Xb = integrer(xb, t_max=30.0, dt=1e-3)
    sep = np.linalg.norm(X - Xb, axis=1)
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.semilogy(t, sep + 1e-20, color="#1f4e79")
    ax.set_xlabel("t (s)")
    ax.set_ylabel("‖ΔX(t)‖")
    ax.set_title("Divergence de deux trajectoires (Δθ1 = 1e-9 rad)")
    fig.savefig(FIG / "03_divergence.png", bbox_inches="tight")
    plt.close(fig)

    # Exposants de Lyapunov : régime régulier vs chaotique
    regimes = {"petites oscillations (10°, 10°)": [10, 0, 10, 0],
               "intermédiaire (60°, 60°)": [60, 0, 60, 0],
               "chaotique (120°, -10°)": [120, 0, -10, 0]}
    lyap = {}
    for nom, angles in regimes.items():
        lyap[nom] = round(lyapunov_max(np.radians(angles), t_max=60.0, dt=2e-3), 3)
    res["lyapunov"] = lyap

    # Carte du chaos : λ en fonction de (θ1, θ2) initiaux
    grille = np.linspace(-170, 170, 15)
    carte = np.array([[lyapunov_max(np.radians([a, 0, b, 0]), t_max=20.0, dt=5e-3)
                       for a in grille] for b in grille])
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    im = ax.imshow(carte, origin="lower", extent=[-170, 170, -170, 170], cmap="magma")
    fig.colorbar(im, label="λ max (s⁻¹)")
    ax.set_xlabel("θ1 initial (°)")
    ax.set_ylabel("θ2 initial (°)")
    ax.set_title("Carte des exposants de Lyapunov")
    fig.savefig(FIG / "04_carte_lyapunov.png", bbox_inches="tight")
    plt.close(fig)
    res["fraction_chaotique"] = round(float((carte > 0.5).mean()), 3)

    (RACINE / "resultats.json").write_text(json.dumps(res, indent=2, ensure_ascii=False))
    print(json.dumps(res, indent=2, ensure_ascii=False))
    return res


if __name__ == "__main__":
    main()
