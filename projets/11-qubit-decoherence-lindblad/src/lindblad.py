"""Qubit ouvert : équation maîtresse de Lindblad résolue par Runge-Kutta 4 (code maison).

    dρ/dt = -i [H, ρ] + Σ_k ( L_k ρ L_k† - ½ {L_k† L_k, ρ} )

Qubit piloté, dans le référentiel tournant à la fréquence du laser / micro-onde :
    H = (Δ/2) σ_z + (Ω/2) σ_x          (ħ = 1)
Deux canaux de décohérence :
    L_1 = sqrt(γ1) σ_-            relaxation d'énergie  -> T1 = 1/γ1
    L_φ = sqrt(γφ/2) σ_z          déphasage pur         -> T2 = 1/(γ1/2 + γφ)
On a donc toujours T2 <= 2 T1.

Convention : |0> = |e> (excité, σ_z = +1), |1> = |g> (fondamental).
"""
from __future__ import annotations

import numpy as np

SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)
SM = np.array([[0, 0], [1, 0]], dtype=complex)      # σ_- = |g><e|
EXC = np.array([[1, 0], [0, 0]], dtype=complex)     # |e><e|
FOND = np.array([[0, 0], [0, 1]], dtype=complex)    # |g><g|


def hamiltonien(delta: float, omega: float) -> np.ndarray:
    return 0.5 * delta * SZ + 0.5 * omega * SX


def operateurs_saut(gamma1: float, gamma_phi: float) -> list[np.ndarray]:
    ops = []
    if gamma1 > 0:
        ops.append(np.sqrt(gamma1) * SM)
    if gamma_phi > 0:
        ops.append(np.sqrt(gamma_phi / 2) * SZ)
    return ops


def lindbladien(rho, H, ops):
    d = -1j * (H @ rho - rho @ H)
    for L in ops:
        LdL = L.conj().T @ L
        d += L @ rho @ L.conj().T - 0.5 * (LdL @ rho + rho @ LdL)
    return d


def evoluer(rho0, H, ops, t_max: float, dt: float = 1e-3, n_sorties: int = 400):
    """Intégration RK4. Renvoie les temps et les matrices densité échantillonnées."""
    n_pas = int(round(t_max / dt))
    tous = max(1, n_pas // n_sorties)
    rho = rho0.astype(complex).copy()
    ts, rhos = [0.0], [rho.copy()]
    for k in range(1, n_pas + 1):
        k1 = lindbladien(rho, H, ops)
        k2 = lindbladien(rho + 0.5 * dt * k1, H, ops)
        k3 = lindbladien(rho + 0.5 * dt * k2, H, ops)
        k4 = lindbladien(rho + dt * k3, H, ops)
        rho = rho + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        if k % tous == 0:
            ts.append(k * dt)
            rhos.append(rho.copy())
    return np.array(ts), np.array(rhos)


def bloch(rhos) -> np.ndarray:
    """Vecteur de Bloch (x, y, z) = Tr(ρ σ)."""
    return np.real(np.stack([np.einsum("tij,ji->t", rhos, S) for S in (SX, SY, SZ)], axis=1))


def etat_stationnaire(H, ops) -> np.ndarray:
    """Noyau du superopérateur de Lindblad (vectorisation colonne par colonne)."""
    I = np.eye(2)
    M = -1j * (np.kron(I, H) - np.kron(H.T, I))
    for L in ops:
        LdL = L.conj().T @ L
        M += np.kron(L.conj(), L) - 0.5 * (np.kron(I, LdL) + np.kron(LdL.T, I))
    w, v = np.linalg.eig(M)
    rho = v[:, np.argmin(np.abs(w))].reshape(2, 2, order="F")
    return rho / np.trace(rho)


def population_stationnaire_bloch(delta, omega, gamma1, gamma_phi) -> float:
    """Solution analytique des équations de Bloch optiques : ρ_ee = ½ s/(1+s)."""
    T1 = 1 / gamma1
    T2 = 1 / (gamma1 / 2 + gamma_phi)
    s = omega ** 2 * T1 * T2 / (1 + (delta * T2) ** 2)
    return 0.5 * s / (1 + s)


def T2_theorique(gamma1, gamma_phi) -> float:
    return 1 / (gamma1 / 2 + gamma_phi)
