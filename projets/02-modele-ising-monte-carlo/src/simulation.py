"""Étape 1 — Modèle d'Ising 2D et algorithme de Metropolis (mise à jour en damier).

Hamiltonien : H = -J Σ_<ij> s_i s_j  (J = 1, k_B = 1, conditions périodiques).
La mise à jour en damier (sous-réseaux pair/impair) permet de vectoriser
Metropolis avec NumPy tout en respectant le bilan détaillé.
"""
from __future__ import annotations

import numpy as np

T_C_ONSAGER = 2.0 / np.log(1.0 + np.sqrt(2.0))  # ≈ 2.269185


def somme_voisins(s: np.ndarray) -> np.ndarray:
    return (np.roll(s, 1, 0) + np.roll(s, -1, 0) + np.roll(s, 1, 1) + np.roll(s, -1, 1))


def energie_par_spin(s: np.ndarray) -> float:
    # Chaque liaison comptée une fois : voisins droite + bas
    return float(-np.mean(s * (np.roll(s, 1, 0) + np.roll(s, 1, 1))))


def magnetisation_par_spin(s: np.ndarray) -> float:
    return float(np.mean(s))


def balayage(s: np.ndarray, beta: float, rng: np.random.Generator, masques) -> None:
    """Un balayage Monte-Carlo complet (modifie s en place)."""
    for m in masques:
        dE = 2.0 * s * somme_voisins(s)
        accepte = (rng.random(s.shape) < np.exp(-beta * dE)) & m
        s[accepte] *= -1


def masques_damier(L: int):
    i, j = np.indices((L, L))
    pair = (i + j) % 2 == 0
    return pair, ~pair


def mesurer(L: int, T: float, n_therm: int, n_mes: int, seed: int = 0, s0=None):
    """Thermalise puis mesure <|m|>, <e>, χ et C_v à la température T."""
    rng = np.random.default_rng(seed)
    s = np.ones((L, L), dtype=np.int8) if s0 is None else s0.copy()
    masques = masques_damier(L)
    beta = 1.0 / T
    for _ in range(n_therm):
        balayage(s, beta, rng, masques)
    M = np.empty(n_mes)
    E = np.empty(n_mes)
    for k in range(n_mes):
        balayage(s, beta, rng, masques)
        M[k] = abs(magnetisation_par_spin(s))
        E[k] = energie_par_spin(s)
    N = L * L
    return {
        "m": M.mean(),
        "e": E.mean(),
        "chi": N * beta * (np.mean(M**2) - M.mean() ** 2),
        "cv": N * beta**2 * (np.mean(E**2) - E.mean() ** 2),
        "binder": 1 - np.mean(M**4) / (3 * np.mean(M**2) ** 2),
        "etat": s,
    }


def m_onsager(T: np.ndarray) -> np.ndarray:
    """Aimantation spontanée exacte (Onsager–Yang) pour L → ∞."""
    T = np.asarray(T, dtype=float)
    out = np.zeros_like(T)
    bas = T < T_C_ONSAGER
    out[bas] = (1 - np.sinh(2 / T[bas]) ** -4) ** 0.125
    return out
