"""Étapes 1 à 3 — Inégalité CHSH : mécanique quantique vs variables cachées locales.

S = E(a,b) − E(a,b') + E(a',b) + E(a',b')
* Toute théorie locale à variables cachées : |S| ≤ 2 (borne de Bell–CHSH).
* Mécanique quantique (état singulet) : E(a,b) = −cos(a−b), |S| ≤ 2√2 (borne de Tsirelson).
"""
from __future__ import annotations

from itertools import product

import numpy as np

SIGMA_X = np.array([[0, 1], [1, 0]], dtype=complex)
SIGMA_Z = np.array([[1, 0], [0, -1]], dtype=complex)
SINGULET = np.array([0, 1, -1, 0], dtype=complex) / np.sqrt(2)  # (|01⟩ − |10⟩)/√2

ANGLES_OPTIMAUX = (0.0, np.pi / 2, np.pi / 4, 3 * np.pi / 4)  # a, a', b, b'


def observable(theta: float) -> np.ndarray:
    """Spin mesuré dans la direction θ du plan (x, z) : cos θ σz + sin θ σx."""
    return np.cos(theta) * SIGMA_Z + np.sin(theta) * SIGMA_X


def correlation_quantique(a: float, b: float, etat=SINGULET) -> float:
    """E(a,b) = ⟨ψ| A(a) ⊗ B(b) |ψ⟩, calculé avec les matrices (pas la formule)."""
    op = np.kron(observable(a), observable(b))
    return float(np.real(np.conj(etat) @ op @ etat))


def S_quantique(a, ap, b, bp, etat=SINGULET) -> float:
    E = lambda x, y: correlation_quantique(x, y, etat)  # noqa: E731
    return E(a, b) - E(a, bp) + E(ap, b) + E(ap, bp)


def mesures_quantiques(a: float, b: float, n: int, rng, etat=SINGULET) -> np.ndarray:
    """Simule n paires mesurées : tirage des résultats (±1, ±1) selon la règle de Born."""
    _, va = np.linalg.eigh(observable(a))
    _, vb = np.linalg.eigh(observable(b))
    valeurs = np.array([-1, 1])  # eigh trie par valeur propre croissante
    probas, produits = [], []
    for i, j in product(range(2), range(2)):
        proj = np.kron(va[:, i], vb[:, j])
        probas.append(abs(np.conj(proj) @ etat) ** 2)
        produits.append(valeurs[i] * valeurs[j])
    tirages = rng.choice(4, size=n, p=np.array(probas) / np.sum(probas))
    return np.array(produits)[tirages]


def S_experience(angles, n: int, rng, mesure=mesures_quantiques):
    """Estimation de S et de son erreur statistique à partir de n paires par réglage."""
    a, ap, b, bp = angles
    signes = {(a, b): 1, (a, bp): -1, (ap, b): 1, (ap, bp): 1}
    S, var = 0.0, 0.0
    for (x, y), s in signes.items():
        r = mesure(x, y, n, rng)
        S += s * r.mean()
        var += r.var() / n
    return S, np.sqrt(var)


def mesures_locales(a: float, b: float, n: int, rng) -> np.ndarray:
    """Modèle local à variable cachée λ (direction aléatoire) :
    A = sign(cos(a − λ)), B = −sign(cos(b − λ)). Corrélation en « dents de scie »."""
    lam = rng.uniform(0, 2 * np.pi, n)
    return np.sign(np.cos(a - lam)) * -np.sign(np.cos(b - lam))


def correlation_locale_exacte(a: float, b: float) -> float:
    """E(a,b) = −1 + 2|a−b|/π pour |a−b| ≤ π (modèle de Bell)."""
    d = np.abs((a - b + np.pi) % (2 * np.pi) - np.pi)
    return -1 + 2 * d / np.pi


def S_max_strategies_deterministes() -> float:
    """Énumère les 16 stratégies locales déterministes (A, A', B, B' = ±1)."""
    return max(abs(A * B - A * Bp + Ap * B + Ap * Bp)
               for A, Ap, B, Bp in product((-1, 1), repeat=4))


def etat_werner(p: float) -> np.ndarray:
    """Matrice densité de Werner : singulet mélangé à du bruit blanc (état mixte)."""
    rho_s = np.outer(SINGULET, np.conj(SINGULET))
    return p * rho_s + (1 - p) * np.eye(4) / 4


def S_werner(p: float) -> float:
    """S optimal pour l'état de Werner ρ = p|ψ⁻⟩⟨ψ⁻| + (1−p) I/4 (calcul matriciel)."""
    rho = etat_werner(p)
    a, ap, b, bp = ANGLES_OPTIMAUX
    E = lambda x, y: float(np.real(np.trace(rho @ np.kron(observable(x), observable(y)))))  # noqa
    return abs(E(a, b) - E(a, bp) + E(ap, b) + E(ap, bp))
