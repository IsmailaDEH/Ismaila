"""Ion piégé : spectre de bandes latérales, thermométrie, refroidissement.

Lancement : python src/analyse.py   (depuis le dossier du projet, ~40 s)
Unités : fréquences en unités de la fréquence du piège ν (ν = 1).
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

from ion import (deplacement, etat_stationnaire, excitation, lindbladien, nombre_phonons,
                 rabi_exact, rabi_lamb_dicke, refroidissement, taux_lamb_dicke,
                 thermique, thermometrie)

RACINE = Path(__file__).resolve().parents[1]
FIG = RACINE / "figures"
FIG.mkdir(exist_ok=True)
plt.rcParams.update({"figure.dpi": 130, "font.size": 10})
BLEU, ORANGE, ROUGE = "#1f4e79", "#b5651d", "#b22222"
t_debut = time.time()
res = {}

NU, ETA = 1.0, 0.1

# 1. Fréquences de Rabi : formule de Laguerre contre Lamb-Dicke --------------
fig, ax = plt.subplots(1, 2, figsize=(10, 3.8), constrained_layout=True)
n = np.arange(0, 41)
for k, eta in enumerate((0.1, 0.3)):
    D = np.abs(deplacement(45, eta))
    for m_off, lab, col in ((-1, "rouge n→n−1", ROUGE), (+1, "bleue n→n+1", BLEU), (0, "porteuse", "k")):
        nn = n[n + m_off >= 0]
        ex = [rabi_exact(i, i + m_off, eta) for i in nn]
        ld = [rabi_lamb_dicke(i, i + m_off, eta) for i in nn]
        ax[k].plot(nn, ex, "-", color=col, label=f"{lab} (exact)")
        ax[k].plot(nn, ld, ":", color=col, lw=1)
        ax[k].plot(nn[::5], [D[i + m_off, i] for i in nn[::5]], "o", ms=3, color=col)
    ax[k].set(title=f"η = {eta}", xlabel="nombre de phonons n", ylabel="Ω(n→m) / Ω")
ax[0].legend(fontsize=8)
fig.suptitle("Fréquences de Rabi : formule de Laguerre (trait), Lamb-Dicke (pointillés), matrice exp(iη(a+a†)) (points)")
fig.savefig(FIG / "01_frequences_rabi.png")
plt.close(fig)
D = np.abs(deplacement(45, 0.3))
res["ecart_max_laguerre_vs_matrice"] = float(max(abs(D[m, i] - rabi_exact(i, m, 0.3))
                                                 for i in range(40) for m in range(40)))
res["rouge_n20_eta0.3_exact_sur_LD"] = rabi_exact(20, 19, 0.3) / rabi_lamb_dicke(20, 19, 0.3)

# 2. Spectre de bandes latérales et thermométrie ------------------------------
N, OM = 30, 0.04
t_pi = np.pi / (ETA * OM)                     # impulsion π de la bande bleue pour n = 0
deltas = np.linspace(-1.25, 1.25, 1001)
fig, ax = plt.subplots(figsize=(9, 3.8), constrained_layout=True)
spectres = {}
for nbar, col in ((2.0, ORANGE), (0.05, BLEU)):
    pn = thermique(N, nbar)
    P = np.array([excitation(N, NU, dl, OM, ETA, t_pi / 2, pn) for dl in deltas])
    spectres[nbar] = P
    ax.plot(deltas, P, color=col, label=f"n̄ = {nbar}")
ax.set(xlabel="désaccord Δ / ν", ylabel="probabilité d'excitation P_e",
       title=f"Spectre d'un ion piégé (η = {ETA}, Ω = {OM} ν, impulsion t = π/(2ηΩ))")
for x, lab in ((-1, "bande rouge"), (0, "porteuse"), (1, "bande bleue")):
    ax.annotate(lab, (x + 0.06 * np.sign(x if x else 1), 0.88), ha="left" if x >= 0 else "right", fontsize=9)
ax.set_ylim(0, 1.05)
ax.legend(loc="center left", bbox_to_anchor=(0.62, 0.55))
fig.savefig(FIG / "02_spectre_bandes_laterales.png")
plt.close(fig)

thermo = []
for nbar in (0.05, 0.3, 1.0, 2.0, 5.0):
    pn = thermique(45, nbar)
    pr = excitation(45, NU, -NU, OM, ETA, t_pi / 2, pn)
    pb = excitation(45, NU, +NU, OM, ETA, t_pi / 2, pn)
    thermo.append({"nbar_vrai": nbar, "P_rouge": round(pr, 6), "P_bleue": round(pb, 6),
                   "nbar_mesure": round(thermometrie(pr, pb), 4)})
res["thermometrie"] = thermo

# 3. Refroidissement par bande latérale ----------------------------------------
OMc, GAMc, Nc = 0.1, 0.5, 20
temps = np.linspace(0, 4.0e4, 81)
n_t = refroidissement(Nc, NU, OMc, ETA, GAMc, 2.0, temps)
n_inf_th, W_th = taux_lamb_dicke(NU, -NU, OMc, ETA, GAMc)
f = lambda t, n0, W, ninf: ninf + (n0 - ninf) * np.exp(-W * t)  # noqa: E731
p, cov = curve_fit(f, temps, n_t, p0=(2, 2e-4, 0.08))
res["refroidissement"] = {
    "Omega": OMc, "Gamma": GAMc, "eta": ETA,
    "W_ajuste": [float(p[1]), float(np.sqrt(cov[1, 1]))], "W_theorie_LD": float(W_th),
    "n_inf_ajuste": float(p[2]),
    "n_final_lindblad": float(n_t[-1]), "n_inf_theorie_LD": float(n_inf_th),
}

gammas = np.logspace(-1, np.log10(3), 9)
n_num, n_th = [], []
for g in gammas:
    r = etat_stationnaire(lindbladien(15, NU, -NU, 0.02, ETA, g), 30)
    n_num.append(nombre_phonons(r, 15))
    n_th.append(taux_lamb_dicke(NU, -NU, 0.02, ETA, g)[0])
n_num, n_th = np.array(n_num), np.array(n_th)
res["n_stationnaire_vs_Gamma"] = {
    "Gamma": gammas.round(4).tolist(), "lindblad": n_num.round(6).tolist(),
    "taux_LD": n_th.round(6).tolist(),
    "ecart_relatif_max": float(np.max(np.abs(n_num / n_th - 1))),
    "pente_loglog_Gamma<=0.5": float(np.polyfit(np.log(gammas[gammas <= 0.5]), np.log(n_num[gammas <= 0.5]), 1)[0]),
}

fig, ax = plt.subplots(1, 2, figsize=(10.5, 3.9), constrained_layout=True)
ax[0].plot(temps / 1e3, n_t, "o", ms=3, color=BLEU, label="Lindblad (exact)")
ax[0].plot(temps / 1e3, f(temps, *p), "-", color=ORANGE, label=f"ajustement W = {p[1]:.2e} ν")
ax[0].axhline(n_inf_th, color="k", ls=":", label=f"limite théorique n̄∞ = {n_inf_th:.3f}")
ax[0].set(xlabel="temps (10³ / ν)", ylabel="⟨n⟩", title="Refroidissement sur la bande rouge (Δ = −ν)")
ax[0].legend(fontsize=8)
ax[1].loglog(gammas, n_num, "o", color=BLEU, label="Lindblad : état stationnaire")
ax[1].loglog(gammas, n_th, "-", color=ORANGE, label="équations de taux (Lamb-Dicke)")
ax[1].set(xlabel="largeur de raie Γ / ν", ylabel="n̄ stationnaire", title="Limite du refroidissement")
ax[1].legend(fontsize=8)
fig.savefig(FIG / "03_refroidissement.png")
plt.close(fig)

res["duree_s"] = round(time.time() - t_debut, 1)
(RACINE / "resultats.json").write_text(json.dumps(res, indent=2, ensure_ascii=False))
print(json.dumps(res, indent=1, ensure_ascii=False))
