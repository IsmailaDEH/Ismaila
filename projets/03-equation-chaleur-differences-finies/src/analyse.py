"""Étapes 2 à 4 — Validation, ordre de convergence, stabilité (CFL), cas d'application.

Lancement : python src/analyse.py   (depuis le dossier du projet)
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from simulation import crank_nicolson_1d, ftcs_2d, solution_exacte_2d

RACINE = Path(__file__).resolve().parents[1]
FIG = RACINE / "figures"
FIG.mkdir(exist_ok=True)
plt.rcParams.update({"figure.dpi": 120, "font.size": 10})
T_FIN = 0.05


def main() -> dict:
    res: dict = {}

    # --- Étape 2 : convergence spatiale du schéma FTCS --------------
    tailles = [10, 20, 40, 80]
    erreurs = []
    for n in tailles:
        X, Y, u = ftcs_2d(n, T_FIN, r=0.2)
        erreurs.append(float(np.abs(u - solution_exacte_2d(X, Y, T_FIN)).max()))
    ordre = -np.polyfit(np.log(tailles), np.log(erreurs), 1)[0]
    res["ftcs_erreurs_Linf"] = {str(n): f"{e:.2e}" for n, e in zip(tailles, erreurs)}
    res["ftcs_ordre_spatial"] = round(float(ordre), 2)

    # Crank–Nicolson : ordre 2 en temps (h fixe très fin)
    pas = [10, 20, 40, 80]
    err_cn = [crank_nicolson_1d(2000, k, 0.1)[2] for k in pas]
    res["cn_ordre_temporel"] = round(float(-np.polyfit(np.log(pas), np.log(err_cn), 1)[0]), 2)

    fig, ax = plt.subplots(figsize=(5.5, 3.8))
    h = 1 / np.array(tailles)
    ax.loglog(h, erreurs, "o-", label=f"FTCS 2D (pente {ordre:.2f})")
    ax.loglog(h, erreurs[0] * (h / h[0]) ** 2, "k--", lw=1, label="référence O(h²)")
    ax.set_xlabel("h")
    ax.set_ylabel("erreur max")
    ax.legend()
    ax.set_title("Convergence spatiale")
    fig.savefig(FIG / "01_convergence.png", bbox_inches="tight")
    plt.close(fig)

    # --- Étape 3 : condition de stabilité r ≤ 1/4 --------------------
    rs = [0.10, 0.20, 0.25, 0.26, 0.30]
    stab = {}
    rng = np.random.default_rng(0)
    for r in rs:
        X, Y, _ = ftcs_2d(40, 0, r=r)
        u0 = solution_exacte_2d(X, Y, 0) + 1e-6 * rng.standard_normal(X.shape)
        u0[[0, -1], :] = 0
        u0[:, [0, -1]] = 0
        _, _, u = ftcs_2d(40, T_FIN, r=r, u0=u0)
        stab[str(r)] = "stable" if np.abs(u).max() < 1.0 else "instable"
    res["stabilite"] = stab

    # --- Étape 4 : cas d'application — plaque avec source chaude ------
    n = 80
    x = np.linspace(0, 1, n + 1)
    X, Y = np.meshgrid(x, x, indexing="ij")
    u0 = np.where((X - 0.35) ** 2 + (Y - 0.6) ** 2 < 0.02, 100.0, 0.0)
    u0 += np.where((np.abs(X - 0.7) < 0.08) & (np.abs(Y - 0.3) < 0.15), 60.0, 0.0)
    fig, axes = plt.subplots(1, 4, figsize=(12, 3.1))
    t_prec = 0.0
    u = u0
    for ax, t in zip(axes, (0.0, 0.002, 0.01, 0.04)):
        if t > t_prec:
            _, _, u = ftcs_2d(n, t - t_prec, r=0.24, u0=u)
            t_prec = t
        im = ax.imshow(u.T, origin="lower", extent=[0, 1, 0, 1], cmap="inferno", vmin=0, vmax=100)
        ax.set_title(f"t = {t:g}")
        ax.axis("off")
    fig.colorbar(im, ax=axes, label="température (u.a.)", shrink=0.85)
    fig.suptitle("Diffusion de la chaleur dans une plaque (bords à 0)")
    fig.savefig(FIG / "02_diffusion_plaque.png", bbox_inches="tight")
    plt.close(fig)

    (RACINE / "resultats.json").write_text(json.dumps(res, indent=2, ensure_ascii=False))
    print(json.dumps(res, indent=2, ensure_ascii=False))
    return res


if __name__ == "__main__":
    main()
