"""Monte-Carlo cinétique (algorithme BKL / « n-fold way ») pour la croissance
épitaxiale sous-monocouche sur un réseau carré.

Modèle (« bond counting ») :
    - dépôt : flux F atomes par site et par unité de temps (on prend F = 1) ;
    - diffusion : un adatome ayant n voisins latéraux saute vers un site voisin
      vide avec le taux  h_n = h0 * exp(-n * Eb / kT),
      où h0 = D/F (taux de saut d'un adatome isolé, en unités de F).
    - Eb/kT = inf  -> agrégation irréversible (îlot critique i* = 1).

Algorithme BKL (Bortz, Kalos, Lebowitz 1975) : sans rejet.
    1. On range les atomes en classes selon n (0 à 4) : taux identiques dans une classe.
    2. Taux total R = F*L^2 + sum_n N_n * h_n.
    3. On tire une classe avec la probabilité (N_n h_n)/R, puis un atome au hasard.
    4. Le temps avance de dt = -ln(u)/R  (loi exponentielle).
"""
from __future__ import annotations

import math

import numpy as np
from scipy import ndimage


class EpitaxieKMC:
    def __init__(self, L: int, D_sur_F: float, Eb_kT: float = math.inf, seed: int = 0,
                 flux: float = 1.0):
        self.L = L
        self.flux = flux
        self.N = L * L
        self.rng = np.random.default_rng(seed)
        self.occ = np.zeros(self.N, dtype=np.int8)
        # voisins (conditions périodiques), indices plats
        i = np.arange(self.N)
        x, y = i % L, i // L
        self.voisins = np.stack([
            ((x + 1) % L) + y * L, ((x - 1) % L) + y * L,
            x + ((y + 1) % L) * L, x + ((y - 1) % L) * L,
        ], axis=1)
        self.vois = self.voisins.tolist()
        self.h = [D_sur_F * (math.exp(-n * Eb_kT) if math.isfinite(Eb_kT) else (1.0 if n == 0 else 0.0))
                  for n in range(5)]
        self.classes: list[list[int]] = [[] for _ in range(5)]
        self.ou: dict[int, tuple[int, int]] = {}   # site -> (classe, position dans la liste)
        self.t = 0.0
        self.n_depots = 0
        self.n_sauts = 0

    # ---------- gestion des classes ----------
    def _nvois(self, s: int) -> int:
        o = self.occ
        v = self.vois[s]
        return int(o[v[0]] + o[v[1]] + o[v[2]] + o[v[3]])

    def _retirer(self, s: int) -> None:
        c, p = self.ou.pop(s)
        lst = self.classes[c]
        dernier = lst[-1]
        lst[p] = dernier
        lst.pop()
        if dernier != s:
            self.ou[dernier] = (c, p)

    def _ajouter(self, s: int) -> None:
        c = self._nvois(s)
        self.classes[c].append(s)
        self.ou[s] = (c, len(self.classes[c]) - 1)

    def _rafraichir(self, s: int) -> None:
        if self.occ[s] and self._nvois(s) != self.ou[s][0]:
            self._retirer(s)
            self._ajouter(s)

    def _poser(self, s: int) -> None:
        self.occ[s] = 1
        self._ajouter(s)
        for v in self.vois[s]:
            self._rafraichir(v)

    def _enlever(self, s: int) -> None:
        self._retirer(s)
        self.occ[s] = 0
        for v in self.vois[s]:
            self._rafraichir(v)

    # ---------- dynamique ----------
    def taux_total(self) -> float:
        return self.flux * self.N + sum(len(c) * h for c, h in zip(self.classes, self.h))

    def pas(self) -> None:
        rng = self.rng
        poids = [self.flux * self.N] + [len(c) * h for c, h in zip(self.classes, self.h)]
        R = sum(poids)
        self.t += -math.log(1.0 - rng.random()) / R
        u = rng.random() * R
        if u < poids[0]:                      # dépôt sur un site vide
            while True:
                s = int(rng.integers(self.N))
                if not self.occ[s]:
                    break
            self._poser(s)
            self.n_depots += 1
            return
        u -= poids[0]
        for n in range(5):
            if u < poids[n + 1]:
                break
            u -= poids[n + 1]
        lst = self.classes[n]
        s = lst[int(rng.integers(len(lst)))]
        cible = self.vois[s][int(rng.integers(4))]
        self.n_sauts += 1
        if self.occ[cible]:                   # saut bloqué : rien ne bouge
            return
        self._enlever(s)
        self._poser(cible)

    def deposer_jusqua(self, couverture: float) -> None:
        cible = int(round(couverture * self.N))
        while self.n_depots < cible:
            self.pas()

    # ---------- observables ----------
    @property
    def couverture(self) -> float:
        return float(self.occ.sum()) / self.N

    def grille(self) -> np.ndarray:
        return self.occ.reshape(self.L, self.L).copy()

    def ilots(self, taille_min: int = 2) -> np.ndarray:
        """Tailles des îlots (amas connexes, conditions périodiques)."""
        return tailles_amas(self.grille(), taille_min)


def tailles_amas(g: np.ndarray, taille_min: int = 1) -> np.ndarray:
    lab, n = ndimage.label(g)
    if n == 0:
        return np.zeros(0, dtype=int)
    parent = np.arange(n + 1)

    def racine(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for a, b in list(zip(lab[0, :], lab[-1, :])) + list(zip(lab[:, 0], lab[:, -1])):
        if a and b:
            ra, rb = racine(a), racine(b)
            if ra != rb:
                parent[max(ra, rb)] = min(ra, rb)
    racines = np.array([racine(k) for k in range(n + 1)])
    tailles = np.bincount(racines[lab.ravel()], minlength=n + 1)[1:]
    tailles = tailles[tailles > 0]
    return tailles[tailles >= taille_min]


def exposant_nucleation(i_star: int) -> float:
    """Théorie de la nucléation (Venables) : N ∝ (D/F)^(-chi), chi = i*/(i*+2)."""
    return i_star / (i_star + 2)
