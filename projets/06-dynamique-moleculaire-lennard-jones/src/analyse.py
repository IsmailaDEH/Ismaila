"""Étapes 2 à 5 — Validation NVE, distribution des vitesses, structure g(r), diffusion.

Lancement : python src/analyse.py   (depuis le dossier du projet)
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from md import Simulation, g_de_r, temperature

RACINE = Path(__file__).resolve().parents[1]
FIG = RACINE / "figures"
FIG.mkdir(exist_ok=True)
plt.rcParams.update({"figure.dpi": 120, "font.size": 10})

# Argon : conversion des unités réduites
EPS_K, SIGMA_A, TAU_PS = 119.8, 3.405, 2.156

PHASES = {  # (densité réduite, température réduite)
    "solide": (1.10, 0.50),
    "liquide": (0.80, 1.00),
    "gaz": (0.05, 2.00),
}


def main() -> dict:
    res: dict = {}

    # --- Étape 2 : conservation de l'énergie (NVE) selon dt -----------------
    derives = {}
    fig, ax = plt.subplots(figsize=(6, 3.5))
    for dt in (0.010, 0.005, 0.0025):
        s = Simulation(n_cell=3, densite=0.8, T=1.0, dt=dt, seed=1)
        s.equilibrer(1.0, int(1.0 / dt))
        E0 = s.energie_totale()
        t_tot = 5.0
        E = []
        for _ in range(int(t_tot / dt)):
            s.pas()
            E.append(s.energie_totale())
        E = np.array(E)
        derives[dt] = float(np.std(E) / abs(E0))
        ax.plot(np.arange(len(E)) * dt, (E - E0) / s.N, lw=0.8, label=f"dt = {dt}")
    ax.set_xlabel("t (unités réduites)")
    ax.set_ylabel("(E − E0) / N")
    ax.set_title("Conservation de l'énergie (Verlet-vitesse, NVE)")
    ax.legend(fontsize=8)
    fig.savefig(FIG / "01_energie_nve.png", bbox_inches="tight")
    plt.close(fig)
    pente = np.polyfit(np.log(list(derives)), np.log(list(derives.values())), 1)[0]
    res["fluctuation_energie_relative"] = {str(k): f"{v:.1e}" for k, v in derives.items()}
    res["ordre_fluctuation_energie"] = round(float(pente), 2)

    # --- Étapes 3 à 5 : trois phases -----------------------------------------
    figg, axg = plt.subplots(figsize=(6, 3.8))
    figm, axm = plt.subplots(figsize=(6, 3.8))
    phases = {}
    for nom, (rho, T) in PHASES.items():
        s = Simulation(n_cell=4, densite=rho, T=T, dt=0.005, seed=2)
        s.equilibrer(T, 3000)
        s.deplacement[:] = 0
        g_acc = None
        msd, temps, Ts, Ps, Us, vit = [], [], [], [], [], []
        for i in range(4000):
            s.pas()
            if i % 20 == 0:
                msd.append(float(np.mean(np.sum(s.deplacement**2, axis=1))))
                temps.append((i + 1) * s.dt)
                Ts.append(temperature(s.vel))
                Ps.append(s.pression())
                Us.append(s.U / s.N)
                vit.append(s.vel.copy())
            if i % 100 == 0:
                r, g = g_de_r(s.pos, s.L, n_bins=120)
                g_acc = g if g_acc is None else g_acc + g
        g_moy = g_acc / 40
        temps, msd = np.array(temps), np.array(msd)
        # Einstein : MSD = 6 D t (ajusté sur la seconde moitié, régime diffusif)
        moitie = len(temps) // 2
        D = float(np.polyfit(temps[moitie:], msd[moitie:], 1)[0] / 6)
        phases[nom] = {
            "densite": rho, "T_cible": T,
            "T_mesuree": round(float(np.mean(Ts)), 3),
            "pression": round(float(np.mean(Ps)), 3),
            "energie_potentielle_par_atome": round(float(np.mean(Us)), 3),
            "D": float(f"{D:.3g}"),
            "D_argon_cm2_s": float(f"{D * (SIGMA_A * 1e-8) ** 2 / (TAU_PS * 1e-12):.2g}"),
            "premier_pic_g": round(float(r[np.argmax(g_moy)]), 3),
            "hauteur_pic_g": round(float(g_moy.max()), 2),
        }
        axg.plot(r, g_moy, lw=1.2, label=f"{nom} (ρ={rho}, T={T})")
        axm.plot(temps, msd, lw=1.2, label=f"{nom} : D = {D:.3g}")
        if nom == "liquide":
            v = np.concatenate(vit).ravel()
            vit_liquide, T_liq = v, float(np.mean(Ts))
        print(nom, phases[nom])
    axg.axhline(1, color="grey", lw=0.6, ls=":")
    axg.set_xlim(0, 3.3)
    axg.set_xlabel("r / σ")
    axg.set_ylabel("g(r)")
    axg.set_title("Fonction de distribution radiale (N = 256)")
    axg.legend(fontsize=8)
    figg.savefig(FIG / "02_g_de_r.png", bbox_inches="tight")
    axm.set_xlabel("t (unités réduites)")
    axm.set_ylabel("⟨|r(t) − r(0)|²⟩")
    axm.set_yscale("symlog", linthresh=0.1)
    axm.set_title("Déplacement quadratique moyen")
    axm.legend(fontsize=8)
    figm.savefig(FIG / "03_msd_diffusion.png", bbox_inches="tight")
    plt.close("all")
    res["phases"] = phases

    # Distribution des vitesses vs Maxwell–Boltzmann (une composante)
    fig, ax = plt.subplots(figsize=(5.5, 3.5))
    ax.hist(vit_liquide, bins=80, density=True, alpha=0.6, color="#1f4e79", label="simulation")
    x = np.linspace(-5, 5, 300)
    mb = np.exp(-x**2 / (2 * T_liq)) / np.sqrt(2 * np.pi * T_liq)
    ax.plot(x, mb, "k--", label=f"Maxwell–Boltzmann, T = {T_liq:.3f}")
    ax.set_xlabel("v_x")
    ax.set_title("Distribution des vitesses (liquide)")
    ax.legend(fontsize=8)
    fig.savefig(FIG / "04_maxwell_boltzmann.png", bbox_inches="tight")
    plt.close(fig)
    h, b = np.histogram(vit_liquide, bins=80, range=(-5, 5), density=True)
    c = 0.5 * (b[1:] + b[:-1])
    res["ecart_max_maxwell"] = round(float(np.max(np.abs(
        h - np.exp(-c**2 / (2 * T_liq)) / np.sqrt(2 * np.pi * T_liq)))), 4)
    res["kurtosis_vx"] = round(float(np.mean(vit_liquide**4) / np.mean(vit_liquide**2) ** 2), 3)

    (RACINE / "resultats.json").write_text(json.dumps(res, indent=2, ensure_ascii=False))
    print(json.dumps(res, indent=2, ensure_ascii=False))
    return res


if __name__ == "__main__":
    main()
