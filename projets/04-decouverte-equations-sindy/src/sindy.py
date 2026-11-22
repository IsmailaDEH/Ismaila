"""Étapes 1 à 3 — Découverte automatique d'équations différentielles (SINDy).

SINDy (Sparse Identification of Nonlinear Dynamics, Brunton et al. 2016) cherche
dX/dt ≈ Θ(X) Ξ avec Θ une bibliothèque de fonctions candidates et Ξ creuse.
Implémentation « from scratch » : NumPy + régression creuse STLSQ.
"""
from __future__ import annotations

from itertools import combinations_with_replacement

import numpy as np
from scipy.integrate import solve_ivp
from scipy.signal import savgol_filter

LORENZ_VRAI = {"sigma": 10.0, "rho": 28.0, "beta": 8.0 / 3.0}


def lorenz(t, X, sigma=10.0, rho=28.0, beta=8.0 / 3.0):
    x, y, z = X
    return [sigma * (y - x), x * (rho - z) - y, x * y - beta * z]


def simuler_lorenz(t_max=20.0, dt=0.002, x0=(-8.0, 7.0, 27.0)):
    t = np.arange(0, t_max, dt)
    sol = solve_ivp(lorenz, (0, t_max), x0, t_eval=t, rtol=1e-10, atol=1e-10)
    return t, sol.y.T


def bibliotheque(X: np.ndarray, degre=2, noms_var=("x", "y", "z")):
    """Θ(X) : monômes jusqu'au degré donné (1, x, y, z, x², xy, ...)."""
    n, d = X.shape
    colonnes = [np.ones(n)]
    noms = ["1"]
    for k in range(1, degre + 1):
        for combo in combinations_with_replacement(range(d), k):
            colonnes.append(np.prod(X[:, combo], axis=1))
            noms.append("".join(noms_var[i] for i in combo))
    return np.column_stack(colonnes), noms


def derivee(X: np.ndarray, dt: float, lissage: int = 0) -> np.ndarray:
    """Dérivée numérique ; lissage > 0 → filtre de Savitzky–Golay (robuste au bruit)."""
    if lissage:
        return savgol_filter(X, window_length=lissage, polyorder=3, deriv=1, delta=dt, axis=0)
    return np.gradient(X, dt, axis=0)


def stlsq(Theta: np.ndarray, dX: np.ndarray, seuil=0.1, n_iter=10) -> np.ndarray:
    """Sequentially Thresholded Least Squares."""
    norme = np.linalg.norm(Theta, axis=0)
    Th = Theta / norme
    Xi = np.linalg.lstsq(Th, dX, rcond=None)[0]
    for _ in range(n_iter):
        petit = np.abs(Xi / norme[:, None]) < seuil  # seuil sur les coefficients physiques
        Xi[petit] = 0
        for j in range(dX.shape[1]):
            actif = ~petit[:, j]
            if actif.any():
                Xi[actif, j] = np.linalg.lstsq(Th[:, actif], dX[:, j], rcond=None)[0]
    return Xi / norme[:, None]


def equations(Xi: np.ndarray, noms, cibles=("dx/dt", "dy/dt", "dz/dt"), prec=3) -> list[str]:
    lignes = []
    for j, c in enumerate(cibles):
        termes = [f"{Xi[i, j]:+.{prec}f}·{n}" if n != "1" else f"{Xi[i, j]:+.{prec}f}"
                  for i, n in enumerate(noms) if Xi[i, j] != 0]
        lignes.append(f"{c} = " + " ".join(termes))
    return lignes


def coefficients_lorenz(Xi: np.ndarray, noms) -> dict:
    """Extrait σ, ρ, β des coefficients identifiés."""
    idx = {n: i for i, n in enumerate(noms)}
    return {"sigma": float(Xi[idx["y"], 0]),
            "rho": float(Xi[idx["x"], 1]),
            "beta": float(-Xi[idx["z"], 2])}


def coeffs_vrais(noms) -> np.ndarray:
    s, r, b = LORENZ_VRAI.values()
    Xi = np.zeros((len(noms), 3))
    idx = {n: i for i, n in enumerate(noms)}
    Xi[idx["x"], 0], Xi[idx["y"], 0] = -s, s
    Xi[idx["x"], 1], Xi[idx["y"], 1], Xi[idx["xz"], 1] = r, -1, -1
    Xi[idx["xy"], 2], Xi[idx["z"], 2] = 1, -b
    return Xi
