"""Étape 1 — Modèle physique du pendule double et intégrateur RK4.

Équations de Lagrange pour deux masses ponctuelles m1, m2 reliées par des tiges
rigides sans masse de longueurs l1, l2. État : (θ1, ω1, θ2, ω2).
"""
from __future__ import annotations

import numpy as np

G = 9.81


def derivees(etat: np.ndarray, m1=1.0, m2=1.0, l1=1.0, l2=1.0, g=G) -> np.ndarray:
    """Second membre dX/dt = f(X) des équations du mouvement."""
    t1, w1, t2, w2 = etat
    d = t1 - t2
    den = 2 * m1 + m2 - m2 * np.cos(2 * d)

    a1 = (
        -g * (2 * m1 + m2) * np.sin(t1)
        - m2 * g * np.sin(t1 - 2 * t2)
        - 2 * np.sin(d) * m2 * (w2**2 * l2 + w1**2 * l1 * np.cos(d))
    ) / (l1 * den)

    a2 = (
        2 * np.sin(d)
        * (w1**2 * l1 * (m1 + m2) + g * (m1 + m2) * np.cos(t1) + w2**2 * l2 * m2 * np.cos(d))
    ) / (l2 * den)

    return np.array([w1, a1, w2, a2])


def energie(etat: np.ndarray, m1=1.0, m2=1.0, l1=1.0, l2=1.0, g=G) -> np.ndarray:
    """Énergie mécanique totale (fonctionne sur un état ou un tableau (N, 4))."""
    etat = np.atleast_2d(etat)
    t1, w1, t2, w2 = etat.T
    ec = 0.5 * m1 * (l1 * w1) ** 2 + 0.5 * m2 * (
        (l1 * w1) ** 2 + (l2 * w2) ** 2 + 2 * l1 * l2 * w1 * w2 * np.cos(t1 - t2)
    )
    ep = -(m1 + m2) * g * l1 * np.cos(t1) - m2 * g * l2 * np.cos(t2)
    return ec + ep


def rk4_pas(f, x: np.ndarray, dt: float) -> np.ndarray:
    k1 = f(x)
    k2 = f(x + 0.5 * dt * k1)
    k3 = f(x + 0.5 * dt * k2)
    k4 = f(x + dt * k3)
    return x + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)


def integrer(x0, t_max: float, dt: float) -> tuple[np.ndarray, np.ndarray]:
    """Intègre la trajectoire et renvoie (t, X) avec X de forme (N, 4)."""
    n = int(round(t_max / dt))
    X = np.empty((n + 1, 4))
    X[0] = x0
    for i in range(n):
        X[i + 1] = rk4_pas(derivees, X[i], dt)
    return np.linspace(0, n * dt, n + 1), X


def positions(X: np.ndarray, l1=1.0, l2=1.0):
    """Coordonnées cartésiennes des deux masses."""
    x1 = l1 * np.sin(X[:, 0])
    y1 = -l1 * np.cos(X[:, 0])
    x2 = x1 + l2 * np.sin(X[:, 2])
    y2 = y1 - l2 * np.cos(X[:, 2])
    return x1, y1, x2, y2


def lyapunov_max(x0, t_max=60.0, dt=1e-3, d0=1e-8, renorm_every=10) -> float:
    """Plus grand exposant de Lyapunov par la méthode de Benettin.

    On suit deux trajectoires séparées de d0 et on renormalise périodiquement
    la séparation ; λ = <ln(d/d0)> / temps.
    """
    a = np.array(x0, dtype=float)
    b = a + np.array([d0, 0, 0, 0])
    somme_log = 0.0
    n = int(round(t_max / dt))
    for i in range(1, n + 1):
        a = rk4_pas(derivees, a, dt)
        b = rk4_pas(derivees, b, dt)
        if i % renorm_every == 0:
            d = np.linalg.norm(b - a)
            somme_log += np.log(d / d0)
            b = a + (b - a) * (d0 / d)
    return somme_log / (n * dt)
