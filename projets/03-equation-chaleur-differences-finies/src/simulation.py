"""Étape 1 — Solveurs de l'équation de la chaleur ∂u/∂t = α Δu.

* 2D explicite (FTCS) sur [0,1]², conditions de Dirichlet nulles.
* 1D Crank–Nicolson (implicite, inconditionnellement stable) via un solveur tridiagonal.
"""
from __future__ import annotations

import numpy as np
from scipy.linalg import solve_banded


def solution_exacte_2d(x, y, t, alpha=1.0):
    """Mode fondamental : u = sin(πx) sin(πy) e^{-2π²αt}."""
    return np.sin(np.pi * x) * np.sin(np.pi * y) * np.exp(-2 * np.pi**2 * alpha * t)


def ftcs_2d(n: int, t_final: float, alpha=1.0, r=0.2, u0=None):
    """Schéma explicite 2D. r = α dt / h² (stable si r ≤ 1/4).

    Renvoie (x, y, u) avec u à t_final.
    """
    h = 1.0 / n
    x = np.linspace(0, 1, n + 1)
    X, Y = np.meshgrid(x, x, indexing="ij")
    dt = r * h**2 / alpha
    n_pas = int(np.ceil(t_final / dt))
    dt = t_final / n_pas if n_pas else dt
    r_eff = alpha * dt / h**2
    u = solution_exacte_2d(X, Y, 0.0, alpha) if u0 is None else u0.copy()
    u[[0, -1], :] = 0.0
    u[:, [0, -1]] = 0.0
    for _ in range(n_pas):
        lap = (u[2:, 1:-1] + u[:-2, 1:-1] + u[1:-1, 2:] + u[1:-1, :-2] - 4 * u[1:-1, 1:-1])
        u[1:-1, 1:-1] += r_eff * lap
        if not np.isfinite(u).all() or np.abs(u).max() > 1e6:
            break
    return X, Y, u


def crank_nicolson_1d(n: int, n_pas: int, t_final: float, alpha=1.0):
    """Crank–Nicolson 1D sur [0,1], u0 = sin(πx). Renvoie (x, u, erreur_max)."""
    h = 1.0 / n
    dt = t_final / n_pas
    r = alpha * dt / h**2
    x = np.linspace(0, 1, n + 1)
    u = np.sin(np.pi * x)
    m = n - 1
    ab = np.zeros((3, m))
    ab[0, 1:] = -r / 2
    ab[1, :] = 1 + r
    ab[2, :-1] = -r / 2
    for _ in range(n_pas):
        rhs = (1 - r) * u[1:-1] + r / 2 * (u[2:] + u[:-2])
        u[1:-1] = solve_banded((1, 1), ab, rhs)
    exact = np.sin(np.pi * x) * np.exp(-np.pi**2 * alpha * t_final)
    return x, u, float(np.abs(u - exact).max())
