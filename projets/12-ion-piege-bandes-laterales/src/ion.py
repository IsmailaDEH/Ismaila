"""Ion piégé : qubit optique couplé à son mouvement dans le piège (code maison).

Modèle (ħ = 1), dans le référentiel tournant à la fréquence du laser :
    H = ν a†a − (Δ/2) σ_z + (Ω/2) [ σ_+ exp(iη(a + a†)) + h.c. ]
* ν : fréquence du piège, a : phonons du mode axial ;
* Δ = ω_laser − ω_atome : désaccord ; Δ = −ν → bande latérale rouge,
  Δ = 0 → porteuse, Δ = +ν → bande latérale bleue ;
* η : paramètre de Lamb-Dicke (rapport taille du paquet d'onde / longueur d'onde).

Émission spontanée (taux Γ) avec recul le long de l'axe du piège :
    L_± = √(Γ/2) σ_− exp(± iη(a + a†))
Base : |e⟩ ⊗ |n⟩ puis |g⟩ ⊗ |n⟩ (indice 0..N−1 pour e, N..2N−1 pour g).
"""
from __future__ import annotations

import numpy as np
import scipy.linalg as la
import scipy.sparse as sp
from scipy.special import eval_genlaguerre, gammaln

SP = np.array([[0, 1], [0, 0]], dtype=complex)   # σ_+ = |e⟩⟨g|
SM = SP.T.copy()                                  # σ_−
SZ = np.diag([1.0, -1.0]).astype(complex)
EE = np.diag([1.0, 0.0]).astype(complex)


def destroy(N: int) -> np.ndarray:
    return np.diag(np.sqrt(np.arange(1, N)), k=1).astype(complex)


def deplacement(N: int, eta: float) -> np.ndarray:
    """exp(iη(a + a†)), calculé dans un espace élargi puis tronqué (exact sur
    les N premiers niveaux tant que la marge est suffisante)."""
    M = N + 30
    a = destroy(M)
    return la.expm(1j * eta * (a + a.conj().T))[:N, :N]


# --------------------------------------------------------------------------- #
# Fréquences de Rabi des transitions |g, n⟩ → |e, m⟩                           #
# --------------------------------------------------------------------------- #


def rabi_exact(n: int, m: int, eta: float) -> float:
    """|⟨m| exp(iη(a+a†)) |n⟩| = e^(−η²/2) η^|m−n| √(n<!/n>!) L_{n<}^{|m−n|}(η²).

    Formule analytique (Wineland et al. 1998) ; renvoie Ω_{n,m}/Ω.
    """
    n_lt, n_gt = min(n, m), max(n, m)
    d = n_gt - n_lt
    log_pref = -eta**2 / 2 + d * np.log(eta) + 0.5 * (gammaln(n_lt + 1) - gammaln(n_gt + 1))
    return float(abs(np.exp(log_pref) * eval_genlaguerre(n_lt, d, eta**2)))


def rabi_lamb_dicke(n: int, m: int, eta: float) -> float:
    """Limite η√n ≪ 1 : porteuse 1, rouge η√n, bleue η√(n+1)."""
    if m == n:
        return 1.0
    if m == n - 1:
        return eta * np.sqrt(n)
    if m == n + 1:
        return eta * np.sqrt(n + 1)
    return 0.0


# --------------------------------------------------------------------------- #
# Hamiltonien, spectre, thermométrie                                          #
# --------------------------------------------------------------------------- #


def hamiltonien(N: int, nu: float, delta: float, omega: float, eta: float) -> np.ndarray:
    a = destroy(N)
    Id = np.eye(N)
    D = deplacement(N, eta)
    H = nu * np.kron(np.eye(2), a.conj().T @ a) - 0.5 * delta * np.kron(SZ, Id)
    C = 0.5 * omega * np.kron(SP, D)
    return H + C + C.conj().T


def thermique(N: int, nbar: float) -> np.ndarray:
    """Populations p_n = n̄ⁿ/(n̄+1)^(n+1) (normalisées sur la troncature)."""
    n = np.arange(N)
    p = (nbar / (nbar + 1)) ** n / (nbar + 1)
    return p / p.sum()


def excitation(N: int, nu: float, delta: float, omega: float, eta: float,
               t: float, pn: np.ndarray) -> float:
    """P_e après une impulsion de durée t, l'ion partant de |g⟩ ⊗ Σ p_n |n⟩⟨n|.

    Évolution unitaire exacte par diagonalisation de H (une fois par Δ).
    """
    E, V = la.eigh(hamiltonien(N, nu, delta, omega, eta))
    U = (V * np.exp(-1j * E * t)) @ V.conj().T
    Ue = U[:N, N:]                       # amplitudes |g, n⟩ → |e, ·⟩
    return float(np.sum(pn * np.sum(np.abs(Ue) ** 2, axis=0)))


def thermometrie(P_rouge: float, P_bleue: float) -> float:
    """Pour un état thermique, P_rouge/P_bleue = n̄/(n̄+1) exactement
    (car p_{n+1}/p_n = n̄/(n̄+1) et Ω_{n+1,n} = Ω_{n,n+1}) ; d'où n̄."""
    r = P_rouge / P_bleue
    return r / (1 - r)


# --------------------------------------------------------------------------- #
# Refroidissement par bande latérale                                          #
# --------------------------------------------------------------------------- #


def lindbladien(N: int, nu: float, delta: float, omega: float, eta: float,
                gamma: float) -> sp.csr_matrix:
    """Superopérateur de Lindblad creux (vectorisation par colonnes)."""
    H = hamiltonien(N, nu, delta, omega, eta)
    d = 2 * N
    Id = np.eye(d)
    L = -1j * (np.kron(Id, H) - np.kron(H.T, Id))
    D = deplacement(N, eta)
    for s in (+1, -1):
        c = np.sqrt(gamma / 2) * np.kron(SM, D if s > 0 else D.conj())
        cdc = c.conj().T @ c
        L += np.kron(c.conj(), c) - 0.5 * np.kron(Id, cdc) - 0.5 * np.kron(cdc.T, Id)
    return sp.csr_matrix(L)


def nombre_phonons(rho: np.ndarray, N: int) -> float:
    n_op = np.kron(np.eye(2), np.diag(np.arange(N)))
    return float(np.real(np.trace(n_op @ rho)))


def etat_stationnaire(L: sp.csr_matrix, d: int) -> np.ndarray:
    """Noyau de ℒ : on remplace une équation par la normalisation Tr ρ = 1."""
    A = L.toarray()
    A[0, :] = 0.0
    A[0, np.arange(d) * (d + 1)] = 1.0          # indices diagonaux de vec(ρ)
    b = np.zeros(d * d, dtype=complex)
    b[0] = 1.0
    rho = la.solve(A, b).reshape(d, d, order="F")
    return 0.5 * (rho + rho.conj().T)


def refroidissement(N, nu, omega, eta, gamma, nbar0, temps):
    """⟨n⟩(t) sous refroidissement par bande rouge (Δ = −ν), état initial
    |g⟩ ⊗ thermique(n̄₀). On diagonalise ℒ une fois : ρ(t) = Σ c_k e^(λ_k t) v_k,
    ce qui permet d'atteindre des temps ≫ 1/ν sans intégrer pas à pas."""
    d = 2 * N
    L = lindbladien(N, nu, -nu, omega, eta, gamma).toarray()
    lam, V = la.eig(L)
    rho0 = np.zeros((d, d), dtype=complex)
    rho0[N:, N:] = np.diag(thermique(N, nbar0))
    c = la.solve(V, rho0.reshape(-1, order="F"))
    return np.array([nombre_phonons((V @ (c * np.exp(lam * t))).reshape(d, d, order="F"), N)
                     for t in temps])


def taux_lamb_dicke(nu, delta, omega, eta, gamma):
    """Équations de taux dans la limite de Lamb-Dicke et de faible saturation.

    R(δ) = Ω² Γ / (Γ² + 4δ²) : taux d'excitation d'un atome à deux niveaux.
    A₋ = η² [R(Δ + ν) + R(Δ)]  (refroidissement n → n−1)
    A₊ = η² [R(Δ − ν) + R(Δ)]  (chauffage n → n+1)
    Le terme R(Δ) vient du recul à l'émission (émission le long de l'axe).
    n̄_∞ = A₊ / (A₋ − A₊), taux de refroidissement W = A₋ − A₊.
    """
    R = lambda dd: omega**2 * gamma / (gamma**2 + 4 * dd**2)  # noqa: E731
    Am = eta**2 * (R(delta + nu) + R(delta))
    Ap = eta**2 * (R(delta - nu) + R(delta))
    return Ap / (Am - Ap), Am - Ap
