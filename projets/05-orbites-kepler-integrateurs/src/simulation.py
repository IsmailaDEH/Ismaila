"""Étape 1 — Problème à deux corps (gravitation) et trois intégrateurs.

Unités astronomiques : distances en UA, temps en années, G·M_soleil = 4π².
Comparaison : Euler explicite, RK4, Verlet-vitesse (symplectique).
"""
from __future__ import annotations

import numpy as np

GM = 4 * np.pi**2


def acceleration(r: np.ndarray) -> np.ndarray:
    return -GM * r / np.linalg.norm(r) ** 3


def energie(r, v):
    r = np.atleast_2d(r)
    v = np.atleast_2d(v)
    return 0.5 * np.sum(v**2, axis=1) - GM / np.linalg.norm(r, axis=1)


def moment_cinetique(r, v):
    r = np.atleast_2d(r)
    v = np.atleast_2d(v)
    return r[:, 0] * v[:, 1] - r[:, 1] * v[:, 0]


def pas_euler(r, v, dt):
    return r + dt * v, v + dt * acceleration(r)


def pas_rk4(r, v, dt):
    def f(etat):
        return np.concatenate([etat[2:], acceleration(etat[:2])])

    x = np.concatenate([r, v])
    k1 = f(x)
    k2 = f(x + dt / 2 * k1)
    k3 = f(x + dt / 2 * k2)
    k4 = f(x + dt * k3)
    x = x + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    return x[:2], x[2:]


def pas_verlet(r, v, dt):
    a = acceleration(r)
    r_new = r + v * dt + 0.5 * a * dt**2
    v_new = v + 0.5 * (a + acceleration(r_new)) * dt
    return r_new, v_new


INTEGRATEURS = {"Euler": pas_euler, "RK4": pas_rk4, "Verlet": pas_verlet}


def orbite(methode: str, r0, v0, dt: float, t_max: float):
    pas = INTEGRATEURS[methode]
    n = int(round(t_max / dt))
    R = np.empty((n + 1, 2))
    V = np.empty((n + 1, 2))
    R[0], V[0] = r0, v0
    for i in range(n):
        R[i + 1], V[i + 1] = pas(R[i], V[i], dt)
    return np.linspace(0, n * dt, n + 1), R, V


def conditions_perihelie(a: float, e: float):
    """Position/vitesse au périhélie pour une orbite de demi-grand axe a et excentricité e."""
    rp = a * (1 - e)
    vp = np.sqrt(GM * (1 + e) / rp)
    return np.array([rp, 0.0]), np.array([0.0, vp])


def periode_mesuree(t, R) -> float:
    """Période par les retours successifs sur le demi-axe y = 0, x > 0."""
    y = R[:, 1]
    croisements = np.where((y[:-1] < 0) & (y[1:] >= 0) & (R[:-1, 0] > 0))[0]
    # interpolation linéaire de l'instant du croisement
    tc = t[croisements] - y[croisements] * (t[croisements + 1] - t[croisements]) / (
        y[croisements + 1] - y[croisements])
    return float(np.mean(np.diff(tc)))
