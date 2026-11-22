<div align="center">

# Ismaila DEH · Physique numérique & modélisation

**Simuler, mesurer, valider.** Je construis des modèles numériques de systèmes physiques (chaos, physique statistique, EDP, mécanique céleste) et je les confronte à la théorie. J'y ajoute de l'apprentissage automatique pour retrouver des lois physiques à partir de données.

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white) ![NumPy](https://img.shields.io/badge/NumPy-013243?logo=numpy&logoColor=white) ![SciPy](https://img.shields.io/badge/SciPy-8CAAE6?logo=scipy&logoColor=white) ![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c) ![LaTeX](https://img.shields.io/badge/LaTeX-008080?logo=latex&logoColor=white) ![tests](https://github.com/IsmailaDEH/Ismaila/actions/workflows/tests.yml/badge.svg)

[🌐 Portfolio](https://ismailadeh.github.io/Ismaila/) · [📄 Portfolio PDF](cv/portfolio.pdf) · [💼 GitHub](https://github.com/IsmailaDEH)

</div>

---

## 📈 En chiffres

| **5** projets | **19** tests automatiques | **0,9 %** d'erreur sur T_c (Ising) | **0,13 %** d'erreur sur Lorenz (SINDy, 1 % de bruit) |
|---|---|---|---|

## 🗂 Projets

| # | Projet | Domaine | Résultat clé |
|---|---|---|---|
| 01 | [🌀 Pendule double : mesurer le chaos](projets/01-pendule-double-chaos) | Mécanique non linéaire | Exposant de Lyapunov λ = 0,75 s⁻¹ ; énergie conservée à 2 × 10⁻⁷ près |
| 02 | [🧲 Modèle d'Ising 2D par Monte-Carlo](projets/02-modele-ising-monte-carlo) | Physique statistique | T_c = 2,249 contre 2,269 exact (Onsager) |
| 03 | [🔥 Équation de la chaleur](projets/03-equation-chaleur-differences-finies) | EDP, analyse numérique | Ordre 2,01 mesuré ; seuil de stabilité r = 1/4 retrouvé |
| 04 | [🤖 Découverte d'équations (SINDy)](projets/04-decouverte-equations-sindy) | Physique + Machine Learning | Équations de Lorenz retrouvées à 0,13 % près avec 1 % de bruit |
| 05 | [🪐 Orbites et intégrateurs](projets/05-orbites-kepler-integrateurs) | Mécanique céleste | 3ᵉ loi de Kepler : pente 1,5000 ; Verlet conserve L à 10⁻¹⁵ |

<p align="center">
  <img src="projets/02-modele-ising-monte-carlo/figures/03_configurations.png" width="49%">
  <img src="projets/01-pendule-double-chaos/figures/04_carte_lyapunov.png" width="34%">
</p>

## 🧪 Méthode commune à tous les projets

1. **Partir de la physique** : équations écrites et expliquées dans chaque README.
2. **Coder les algorithmes moi-même** (RK4, Metropolis, Verlet, STLSQ...) plutôt que d'appeler une boîte noire.
3. **Valider contre une solution exacte** (Onsager, Kepler, solution analytique) avant d'interpréter.
4. **Mesurer, pas seulement montrer** : ordres de convergence, erreurs relatives, tableaux de résultats.
5. **Reproductible** : `python src/analyse.py` régénère toutes les figures et `resultats.json` ; les tests tournent automatiquement sur GitHub Actions.

## 🚀 Démarrage rapide

```bash
git clone https://github.com/IsmailaDEH/Ismaila.git
cd Ismaila
pip install -r requirements.txt
cd projets/02-modele-ising-monte-carlo && python src/analyse.py
```

## 📁 Organisation du dépôt

```
Ismaila/
├── projets/
│   ├── 01-pendule-double-chaos/
│   ├── 02-modele-ising-monte-carlo/
│   ├── 03-equation-chaleur-differences-finies/
│   ├── 04-decouverte-equations-sindy/
│   └── 05-orbites-kepler-integrateurs/
│       ├── src/            # simulation.py + analyse.py
│       ├── tests/          # pytest
│       ├── figures/        # générées automatiquement
│       ├── resultats.json  # métriques générées automatiquement
│       └── README.md
├── docs/                   # site portfolio (GitHub Pages)
├── cv/                     # portfolio LaTeX → PDF
├── profil-github/          # README de profil à copier
├── .github/workflows/      # tests automatiques
├── requirements.txt
└── LICENSE (MIT)
```

## 🛠 Compétences

**Physique :** mécanique analytique, physique statistique, transferts thermiques, systèmes dynamiques et chaos, mécanique céleste<br>
**Numérique :** intégration d'EDO (Euler, RK4, Verlet), différences finies, Monte-Carlo, analyse de convergence et de stabilité<br>
**Données / ML :** régression creuse, identification de systèmes, NumPy, SciPy, Matplotlib<br>
**Outils :** Python, Git/GitHub, pytest, GitHub Actions, LaTeX

---

<div align="center"><sub>© 2026 Ismaila DEH · Licence MIT</sub></div>
