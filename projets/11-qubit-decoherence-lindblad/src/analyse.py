"""Mesures « virtuelles » d'un qubit : T1, Ramsey (T2*), oscillations de Rabi amorties.

On simule les protocoles d'un laboratoire de qubits puis on les dépouille comme
de vraies données : ajustement des courbes pour extraire T1 et T2.

Lancement : python src/analyse.py   (depuis le dossier du projet, ~20 s)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

from lindblad import (EXC, FOND, SX, bloch, etat_stationnaire, evoluer, hamiltonien,
                      operateurs_saut, population_stationnaire_bloch, T2_theorique)

RACINE = Path(__file__).resolve().parents[1]
FIG = RACINE / "figures"
FIG.mkdir(exist_ok=True)
plt.rcParams.update({"figure.dpi": 130, "font.size": 10})

# Unités : temps en µs, fréquences en rad/µs (ordres de grandeur d'un qubit réel)
GAMMA1 = 1 / 20.0          # T1 = 20 µs
GAMMA_PHI = 1 / 30.0       # déphasage pur
BLEU, ORANGE = "#1f4e79", "#b5651d"
TIRS = 400                 # répétitions par point : bruit de projection quantique
RNG = np.random.default_rng(7)


def mesure_bruitee(p):
    """Comme au labo : on ne lit qu'un nombre fini de 0/1 par point."""
    return RNG.binomial(TIRS, np.clip(p, 0, 1)) / TIRS


def main() -> dict:
    t0 = time.time()
    ops = operateurs_saut(GAMMA1, GAMMA_PHI)
    res = {"T1_vrai_us": 1 / GAMMA1, "T2_vrai_us": T2_theorique(GAMMA1, GAMMA_PHI)}

    # ---- 1. Mesure de T1 : on prépare |e>, on attend ----
    ts, rh = evoluer(EXC, hamiltonien(0, 0), ops, 80, dt=0.01)
    ts, rh = ts[::8], rh[::8]
    pe = mesure_bruitee(np.real(rh[:, 0, 0]))
    (T1_fit,), cov = curve_fit(lambda t, T: np.exp(-t / T), ts, pe, p0=[10])
    cov1 = cov[0, 0]
    res["T1_ajuste_us"] = [round(float(T1_fit), 3), round(float(np.sqrt(cov[0, 0])), 3)]

    # ---- 2. Ramsey : π/2 – attente (désaccord Δ) – π/2 ----
    delta = 2 * np.pi * 0.25               # 250 kHz de désaccord -> franges
    plus = 0.5 * np.array([[1, 1], [1, 1]], dtype=complex)   # après π/2 (axe y), vecteur de Bloch selon +x
    tr, rr = evoluer(plus, hamiltonien(delta, 0), ops, 40, dt=0.005, n_sorties=1600)
    x = bloch(rr)[:, 0]
    # la seconde impulsion π/2 convertit <σx> en population : P_e = (1 + x)/2
    P = mesure_bruitee(0.5 * (1 + x))
    f = lambda t, T2, w, ph: 0.5 * (1 + np.exp(-t / T2) * np.cos(w * t + ph))
    (T2_fit, w_fit, _), cov = curve_fit(f, tr, P, p0=[10, delta, 0])
    res["T2_ajuste_us"] = [round(float(T2_fit), 3), round(float(np.sqrt(cov[0, 0])), 3)]
    res["desaccord_ajuste_MHz"] = round(float(w_fit / (2 * np.pi)), 5)

    # ---- 3. Rabi amorti pour plusieurs taux de déphasage ----
    omega = 2 * np.pi * 0.5                # fréquence de Rabi 500 kHz
    rabi = {}
    for gphi in (0.0, GAMMA_PHI, 5 * GAMMA_PHI):
        tt, r = evoluer(FOND, hamiltonien(0, omega), operateurs_saut(GAMMA1, gphi), 40, dt=0.005,
                        n_sorties=4000)
        rabi[gphi] = (tt, np.real(r[:, 0, 0]))
        if gphi == GAMMA_PHI:
            traj = bloch(r)
    rho_ss = etat_stationnaire(hamiltonien(0, omega), ops)
    res["rabi_population_stationnaire"] = {
        "Lindblad": round(float(np.real(rho_ss[0, 0])), 6),
        "Bloch_analytique": round(population_stationnaire_bloch(0, omega, GAMMA1, GAMMA_PHI), 6)}

    # ---- 4. T2 ≤ 2 T1 : balayage du déphasage pur ----
    gphis = np.array([0, 0.01, 0.02, 0.05, 0.1, 0.2])
    T2s = []
    for g in gphis:
        tg, rg = evoluer(plus, hamiltonien(0, 0), operateurs_saut(GAMMA1, g), 60, dt=0.02)
        coh = np.abs(rg[:, 0, 1]) * 2
        (T2g,), _ = curve_fit(lambda t, T: np.exp(-t / T), tg, coh, p0=[10])
        T2s.append(T2g)
    res["T2_vs_gamma_phi"] = [{"gamma_phi": float(g), "T2_mesure": round(float(a), 3),
                               "T2_theorie": round(T2_theorique(GAMMA1, g), 3)} for g, a in zip(gphis, T2s)]

    # ---- Figures ----
    fig, axes = plt.subplots(1, 3, figsize=(13, 3.8))
    ax = axes[0]
    ax.plot(ts, pe, ".", ms=3, color=BLEU, label=f"« mesure » ({TIRS} tirs/point)")
    ax.plot(ts, np.exp(-ts / T1_fit), "--", color=ORANGE, label=f"ajustement : T₁ = {T1_fit:.1f} ± {np.sqrt(cov1):.1f} µs")
    ax.set_xlabel("attente (µs)"); ax.set_ylabel("P(|e⟩)"); ax.set_title("Relaxation : mesure de T₁")
    ax.legend(fontsize=8)
    ax = axes[1]
    ax.plot(tr, P, "-", lw=0.5, color=BLEU, label=f"« mesure » ({TIRS} tirs/point)")
    ax.plot(tr, 0.5 * (1 + np.exp(-tr / T2_fit)), ":", color=ORANGE)
    ax.plot(tr, 0.5 * (1 - np.exp(-tr / T2_fit)), ":", color=ORANGE, label=f"enveloppe : T₂ = {T2_fit:.1f} ± {np.sqrt(cov[0, 0]):.1f} µs")
    ax.set_xlabel("attente entre les π/2 (µs)"); ax.set_ylabel("P(|e⟩)"); ax.set_title("Franges de Ramsey")
    ax.legend(fontsize=8, loc="upper right")
    ax = axes[2]
    for (g, (tt, pp)), c in zip(rabi.items(), ["#8fb0d3", BLEU, ORANGE]):
        ax.plot(tt, pp, color=c, lw=0.9, label=f"γ_φ = {g:.3f} µs⁻¹")
    ax.set_xlabel("durée de l'impulsion (µs)"); ax.set_ylabel("P(|e⟩)")
    ax.set_title("Oscillations de Rabi amorties"); ax.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(FIG / "01_T1_ramsey_rabi.png"); plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(9.5, 4))
    ax = axes[0]
    ax.plot(gphis, T2s, "o", color=BLEU, label="T₂ mesuré (simulation)")
    gg = np.linspace(0, 0.2, 100)
    ax.plot(gg, 1 / (GAMMA1 / 2 + gg), "-", color="k", lw=1, label="1/(γ₁/2 + γ_φ)")
    ax.axhline(2 / GAMMA1, color=ORANGE, ls="--", lw=1, label="limite 2T₁")
    ax.set_xlabel("γ_φ (µs⁻¹)"); ax.set_ylabel("T₂ (µs)"); ax.set_title("T₂ ≤ 2T₁")
    ax.legend(fontsize=8)
    ax = axes[1]
    ax.plot(traj[:, 1], traj[:, 2], color=BLEU, lw=0.8, label="Rabi amorti (départ |g⟩)")
    th = np.linspace(0, 2 * np.pi, 200)
    ax.plot(np.cos(th), np.sin(th), color="grey", lw=0.6)
    bss = bloch(rho_ss[None])[0]
    ax.plot(bss[1], bss[2], "*", color=ORANGE, ms=12, label="état stationnaire (noyau de ℒ)")
    ax.set_aspect("equal"); ax.set_xlabel("⟨σ_y⟩"); ax.set_ylabel("⟨σ_z⟩")
    ax.set_title("Spirale vers l'intérieur de la sphère de Bloch"); ax.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(FIG / "02_T2_bloch.png"); plt.close(fig)

    res["duree_s"] = round(time.time() - t0, 1)
    (RACINE / "resultats.json").write_text(json.dumps(res, indent=2, ensure_ascii=False))
    print(json.dumps(res, indent=2, ensure_ascii=False))
    return res


if __name__ == "__main__":
    main()
