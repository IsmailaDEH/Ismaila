"""Étape 1 — Dynamique moléculaire d'un fluide de Lennard-Jones (unités réduites).

Potentiel : V(r) = 4ε[(σ/r)^12 − (σ/r)^6], tronqué et décalé à r_c = 2,5σ.
Unités réduites : σ = ε = m = k_B = 1 (pour l'argon : σ = 3,405 Å, ε/k_B = 119,8 K).
Intégrateur Verlet-vitesse, conditions périodiques et convention de l'image minimale.
"""
from __future__ import annotations

import numpy as np

RC = 2.5
V_RC = 4 * (RC**-12 - RC**-6)


def reseau_cfc(n_cell: int, densite: float):
    """Positions sur un réseau cubique à faces centrées : N = 4 n_cell³ atomes."""
    base = np.array([[0, 0, 0], [0.5, 0.5, 0], [0.5, 0, 0.5], [0, 0.5, 0.5]])
    cellules = np.array([[i, j, k] for i in range(n_cell) for j in range(n_cell)
                         for k in range(n_cell)])
    pos = (cellules[:, None, :] + base[None, :, :]).reshape(-1, 3)
    N = len(pos)
    L = (N / densite) ** (1 / 3)
    return pos * (L / n_cell), L


def vitesses_initiales(N: int, T: float, rng: np.random.Generator) -> np.ndarray:
    v = rng.standard_normal((N, 3)) * np.sqrt(T)
    v -= v.mean(axis=0)  # quantité de mouvement totale nulle
    return v * np.sqrt(T / temperature(v))


def temperature(v: np.ndarray) -> float:
    N = len(v)
    return float(np.sum(v**2) / (3 * (N - 1)))


def forces(pos: np.ndarray, L: float):
    """Forces, énergie potentielle et viriel (toutes les paires, O(N²) vectorisé)."""
    d = pos[:, None, :] - pos[None, :, :]
    d -= L * np.round(d / L)
    r2 = np.sum(d**2, axis=-1)
    np.fill_diagonal(r2, np.inf)
    dans = r2 < RC**2
    inv2 = np.where(dans, 1.0 / r2, 0.0)
    inv6 = inv2**3
    # f(r)/r = 24 (2 r^-12 − r^-6) / r²
    f_sur_r = 24 * inv2 * (2 * inv6**2 - inv6)
    F = np.sum(f_sur_r[:, :, None] * d, axis=1)
    U = 0.5 * np.sum(np.where(dans, 4 * (inv6**2 - inv6) - V_RC, 0.0))
    W = 0.5 * np.sum(f_sur_r * np.where(dans, r2, 0.0))  # viriel Σ r·f
    return F, float(U), float(W)


class Simulation:
    def __init__(self, n_cell=4, densite=0.8, T=1.0, dt=0.005, seed=0):
        self.rng = np.random.default_rng(seed)
        self.pos, self.L = reseau_cfc(n_cell, densite)
        self.N = len(self.pos)
        self.rho = densite
        self.dt = dt
        self.vel = vitesses_initiales(self.N, T, self.rng)
        self.F, self.U, self.W = forces(self.pos, self.L)
        self.deplacement = np.zeros_like(self.pos)  # positions non repliées (pour le MSD)

    def pas(self):
        dt = self.dt
        self.vel += 0.5 * dt * self.F
        dx = dt * self.vel
        self.pos = (self.pos + dx) % self.L
        self.deplacement += dx
        self.F, self.U, self.W = forces(self.pos, self.L)
        self.vel += 0.5 * dt * self.F

    def thermostat(self, T_cible: float):
        """Remise à l'échelle des vitesses (utilisée seulement pendant l'équilibrage)."""
        self.vel *= np.sqrt(T_cible / temperature(self.vel))

    def energie_totale(self) -> float:
        return 0.5 * float(np.sum(self.vel**2)) + self.U

    def pression(self) -> float:
        V = self.L**3
        return self.rho * temperature(self.vel) + self.W / (3 * V)

    def equilibrer(self, T: float, n_pas: int, tous=10):
        for i in range(n_pas):
            self.pas()
            if i % tous == 0:
                self.thermostat(T)


def g_de_r(pos: np.ndarray, L: float, n_bins=100, r_max=None):
    """Fonction de distribution radiale g(r)."""
    r_max = r_max or L / 2
    d = pos[:, None, :] - pos[None, :, :]
    d -= L * np.round(d / L)
    r = np.sqrt(np.sum(d**2, axis=-1))[np.triu_indices(len(pos), 1)]
    hist, bords = np.histogram(r, bins=n_bins, range=(0, r_max))
    centres = 0.5 * (bords[1:] + bords[:-1])
    coquille = 4 / 3 * np.pi * (bords[1:] ** 3 - bords[:-1] ** 3)
    N = len(pos)
    ideal = coquille * N / L**3 * N / 2
    return centres, hist / ideal
