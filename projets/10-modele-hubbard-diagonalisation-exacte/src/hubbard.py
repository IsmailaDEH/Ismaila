"""Diagonalisation exacte du modèle de Hubbard 1D et du modèle de Heisenberg.

    H = -t Σ_{<ij>,σ} (c†_{iσ} c_{jσ} + h.c.) + U Σ_i n_{i↑} n_{i↓}

Construction de la base : un état est un couple (configuration ↑, configuration ↓),
chacune codée par un entier dont les bits sont les occupations des sites.
Comme le nombre d'électrons de chaque spin est conservé :

    H = T↑ ⊗ 1 + 1 ⊗ T↓ + U · diag(nombre de doubles occupations)

où T_σ est la matrice de saut dans le secteur à N_σ fermions (taille C(L, N_σ)).
En rangeant tous les opérateurs ↑ avant les ↓, un saut d'électron ↓ traverse les
N↑ opérateurs ↑ deux fois : aucun signe supplémentaire. Le signe fermionique d'un saut
c†_a c_b vaut (-1)^(nombre de fermions entre a et b) : il ne joue que sur la liaison
qui ferme l'anneau (L-1 → 0), où il vaut (-1)^(N_σ - 1).
"""
from __future__ import annotations

from itertools import combinations
from math import comb

import numpy as np
import scipy.sparse as sp
from scipy import integrate, special
from scipy.sparse.linalg import eigsh


# ---------------------------------------------------------------- base
def secteur(L: int, N: int) -> np.ndarray:
    """Toutes les configurations de N fermions sur L sites (entiers triés)."""
    etats = [sum(1 << i for i in c) for c in combinations(range(L), N)]
    return np.array(sorted(etats), dtype=np.int64)


def matrice_saut(L: int, N: int, t: float = 1.0, periodique: bool = True) -> sp.csr_matrix:
    base = secteur(L, N)
    index = {int(s): k for k, s in enumerate(base)}
    lignes, cols, vals = [], [], []
    liaisons = [(i, i + 1) for i in range(L - 1)]
    if periodique and L > 2:
        liaisons.append((L - 1, 0))
    for k, s in enumerate(base):
        s = int(s)
        for i, j in liaisons:
            for a, b in ((i, j), (j, i)):         # c†_a c_b
                if (s >> b) & 1 and not (s >> a) & 1:
                    s2 = s ^ (1 << b) ^ (1 << a)
                    # signe : nombre de fermions strictement entre a et b
                    lo, hi = min(a, b), max(a, b)
                    entre = bin(s & (((1 << hi) - 1) ^ ((1 << (lo + 1)) - 1))).count("1")
                    lignes.append(index[s2]); cols.append(k)
                    vals.append(-t * (-1) ** entre)
    n = len(base)
    return sp.csr_matrix((vals, (lignes, cols)), shape=(n, n))


def hamiltonien(L: int, Nup: int, Ndn: int, U: float, t: float = 1.0, periodique: bool = True):
    Tu = matrice_saut(L, Nup, t, periodique)
    Td = matrice_saut(L, Ndn, t, periodique)
    bu, bd = secteur(L, Nup), secteur(L, Ndn)
    doubles = np.array([[bin(int(u) & int(d)).count("1") for d in bd] for u in bu]).ravel()
    H = sp.kron(Tu, sp.identity(len(bd))) + sp.kron(sp.identity(len(bu)), Td) + U * sp.diags(doubles.astype(float))
    return H.tocsr(), bu, bd, doubles


def etat_fondamental(L, Nup, Ndn, U, t=1.0, periodique=True, k=1):
    H, bu, bd, doubles = hamiltonien(L, Nup, Ndn, U, t, periodique)
    if H.shape[0] <= 400:
        w, v = np.linalg.eigh(H.toarray())
        return w[:k], v[:, :k], bu, bd, doubles
    w, v = eigsh(H, k=k, which="SA", tol=1e-10)
    o = np.argsort(w)
    return w[o], v[:, o], bu, bd, doubles


# ---------------------------------------------------------------- observables
def double_occupation(L, U, t=1.0):
    """<n↑ n↓> par site à demi-remplissage."""
    w, v, *_, doubles = etat_fondamental(L, L // 2, L // 2, U, t)
    return float(np.sum(np.abs(v[:, 0]) ** 2 * doubles) / L)


def correlations_spin(L, U, t=1.0):
    """C(r) = <S^z_0 S^z_r> à demi-remplissage."""
    w, v, bu, bd, _ = etat_fondamental(L, L // 2, L // 2, U, t)
    p = np.abs(v[:, 0]) ** 2
    nu = ((bu[:, None] >> np.arange(L)) & 1).astype(float)
    nd = ((bd[:, None] >> np.arange(L)) & 1).astype(float)
    sz = 0.5 * (nu[:, None, :] - nd[None, :, :]).reshape(-1, L)
    return np.array([np.sum(p * sz[:, 0] * sz[:, r]) for r in range(L)])


def energie(L, Nup, Ndn, U, t=1.0):
    return float(etat_fondamental(L, Nup, Ndn, U, t)[0][0])


def gap_de_charge(L, U, t=1.0):
    """Δc = E(N+1) + E(N-1) - 2 E(N) à demi-remplissage N = L."""
    n = L // 2
    return energie(L, n + 1, n, U, t) + energie(L, n, n - 1, U, t) - 2 * energie(L, n, n, U, t)


def gap_de_spin(L, U, t=1.0):
    """Écart entre le fondamental Sz = 0 et le plus bas état Sz = 1 (triplet)."""
    n = L // 2
    return energie(L, n + 1, n - 1, U, t) - energie(L, n, n, U, t)


def energie_libre(L, Nup, Ndn, t=1.0, periodique=True):
    """U = 0 : on remplit les niveaux à une particule e(k) = -2t cos k.

    Les opérateurs de fermions sont périodiques (c_L = c_0) : k = 2πm/L quel que soit N.
    (Le signe (-1)^(N-1) n'apparaîtrait qu'en passant à une chaîne de spins.)
    """
    if periodique:
        e = np.sort(-2 * t * np.cos(2 * np.pi * np.arange(L) / L))
    else:
        e = np.sort(-2 * t * np.cos(np.pi * np.arange(1, L + 1) / (L + 1)))
    return float(e[:Nup].sum() + e[:Ndn].sum())


# ---------------------------------------------------------------- Bethe ansatz (Lieb & Wu 1968)
def energie_lieb_wu(U, t=1.0):
    """Énergie par site, limite thermodynamique, demi-remplissage."""
    if U == 0:
        return -4 * t / np.pi
    u = U / t
    f = lambda w: special.j0(w) * special.j1(w) / w * special.expit(-w * u / 2)
    val, _ = integrate.quad(f, 0, np.inf, limit=400)
    return -4 * t * val


def gap_lieb_wu(U, t=1.0):
    """Gap de Mott (Ovchinnikov 1970) : Δ = U - 4t + 8t ∫ J1(w) / (w (1 + e^{wU/2t})) dw."""
    u = U / t
    f = lambda w: special.j1(w) / w * special.expit(-w * u / 2)
    val, _ = integrate.quad(f, 0, np.inf, limit=400)
    return t * (u - 4 + 8 * val)


# ---------------------------------------------------------------- Heisenberg
def heisenberg(L: int, J: float = 1.0, Sz_total: int = 0, periodique: bool = True):
    """H = J Σ S_i·S_{i+1} dans le secteur Sz fixé (spins 1/2). Renvoie la plus basse énergie."""
    n_up = L // 2 + Sz_total
    base = secteur(L, n_up)
    index = {int(s): k for k, s in enumerate(base)}
    liaisons = [(i, i + 1) for i in range(L - 1)] + ([(L - 1, 0)] if periodique else [])
    lig, col, val = [], [], []
    for k, s in enumerate(base):
        s = int(s)
        diag = 0.0
        for i, j in liaisons:
            si, sj = (s >> i) & 1, (s >> j) & 1
            diag += 0.25 * J if si == sj else -0.25 * J
            if si != sj:
                lig.append(index[s ^ (1 << i) ^ (1 << j)]); col.append(k); val.append(0.5 * J)
        lig.append(k); col.append(k); val.append(diag)
    H = sp.csr_matrix((val, (lig, col)), shape=(len(base), len(base)))
    if H.shape[0] <= 400:
        return float(np.linalg.eigvalsh(H.toarray())[0])
    return float(eigsh(H, k=1, which="SA", tol=1e-10)[0][0])


def dimension(L: int, Nup: int, Ndn: int) -> int:
    return comb(L, Nup) * comb(L, Ndn)
