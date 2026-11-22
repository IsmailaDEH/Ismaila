"""Étapes 1 et 2 — Potentiel interatomique appris par processus gaussien (GP).

Données « de référence » : courbe d'énergie de H2 donnée par un potentiel de Morse
(paramètres spectroscopiques), bruitée pour imiter des calculs ab initio imparfaits.
Le GP fournit une énergie ET une incertitude, que l'on propage ensuite aux
grandeurs physiques (distance d'équilibre, fréquence de vibration).
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import minimize

# Morse pour H2 : De (eV), a (1/Å), re (Å)
DE, A, RE = 4.7446, 1.9426, 0.7414
MU_KG = 0.50391 * 1.66054e-27          # masse réduite de H2
EV_A2_EN_N_M = 16.0218                  # 1 eV/Å² = 16,0218 N/m
C_CM_S = 2.99792458e10


def morse(r):
    return DE * (1 - np.exp(-A * (np.asarray(r) - RE))) ** 2 - DE


def nombre_onde(k_ev_a2):
    """Nombre d'onde harmonique (cm⁻¹) pour une raideur k en eV/Å²."""
    return np.sqrt(np.asarray(k_ev_a2) * EV_A2_EN_N_M / MU_KG) / (2 * np.pi * C_CM_S)


OMEGA_VRAI = float(nombre_onde(2 * DE * A**2))  # ≈ 4396 cm⁻¹


def noyau(x1, x2, amp, ell):
    return amp**2 * np.exp(-0.5 * (x1[:, None] - x2[None, :]) ** 2 / ell**2)


class ProcessusGaussien:
    def __init__(self, amp=3.0, ell=0.4, bruit=0.02):
        self.amp, self.ell, self.bruit = amp, ell, bruit

    def _nll(self, log_p, x, y):
        amp, ell, bruit = np.exp(log_p)
        K = noyau(x, x, amp, ell) + (bruit**2 + 1e-10) * np.eye(len(x))
        try:
            Lc = np.linalg.cholesky(K)
        except np.linalg.LinAlgError:
            return 1e10
        alpha = np.linalg.solve(Lc.T, np.linalg.solve(Lc, y))
        return 0.5 * y @ alpha + np.sum(np.log(np.diag(Lc))) + 0.5 * len(x) * np.log(2 * np.pi)

    def ajuster(self, x, y, optimiser=True):
        self.x = np.asarray(x, float)
        self.moy_y = float(np.mean(y))
        self.y = np.asarray(y, float) - self.moy_y
        if optimiser:  # maximum de vraisemblance marginale, plusieurs départs
            meilleurs = None
            for ell0 in (0.2, 0.5, 1.0):
                r = minimize(self._nll, np.log([np.std(self.y) + 1e-3, ell0, 0.05]),
                             args=(self.x, self.y), method="L-BFGS-B",
                             bounds=[(-5, 5), (np.log(0.05), np.log(5)), (np.log(1e-3), 0)])
                if meilleurs is None or r.fun < meilleurs.fun:
                    meilleurs = r
            self.amp, self.ell, self.bruit = np.exp(meilleurs.x)
        K = noyau(self.x, self.x, self.amp, self.ell) + self.bruit**2 * np.eye(len(self.x))
        self.Lc = np.linalg.cholesky(K)
        self.alpha = np.linalg.solve(self.Lc.T, np.linalg.solve(self.Lc, self.y))
        return self

    def predire(self, xs, cov=False):
        Ks = noyau(xs, self.x, self.amp, self.ell)
        mu = Ks @ self.alpha + self.moy_y
        v = np.linalg.solve(self.Lc, Ks.T)
        C = noyau(xs, xs, self.amp, self.ell) - v.T @ v
        if cov:
            return mu, C
        return mu, np.sqrt(np.clip(np.diag(C), 0, None))

    def echantillons(self, xs, n, rng):
        mu, C = self.predire(xs, cov=True)
        Lc = np.linalg.cholesky(C + 1e-8 * np.eye(len(xs)))
        return mu + (Lc @ rng.standard_normal((len(xs), n))).T


def proprietes(r, E, demi_fenetre=0.1):
    """Distance d'équilibre et raideur k = E''(r_e).

    Polynôme de degré 4 ajusté autour du minimum : il absorbe l'anharmonicité,
    contrairement à une simple parabole qui biaiserait r_e et k.
    """
    i = int(np.argmin(E))
    fen = (r > r[i] - demi_fenetre) & (r < r[i] + demi_fenetre)
    p = np.polynomial.Polynomial.fit(r[fen], E[fen], 4)
    racines = p.deriv().roots()
    racines = racines[np.isreal(racines)].real
    r_e = racines[np.argmin(np.abs(racines - r[i]))] if len(racines) else r[i]
    return float(r_e), float(p.deriv(2)(r_e))
