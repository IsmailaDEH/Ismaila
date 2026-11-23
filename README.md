<div align="center">

# Ismaila AMADOU DEH · Simulation numérique, matière condensée & physique quantique

**Master 2 Physique Fondamentale, parcours Théories Quantiques (QAT) · Université de Tours · Institut Denis Poisson (CNRS UMR 7013)**

🎯 **Je recherche un stage de M2 (puis une thèse) en simulation numérique, matière condensée et technologies quantiques.**

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white) ![NumPy](https://img.shields.io/badge/NumPy-013243?logo=numpy&logoColor=white) ![SciPy](https://img.shields.io/badge/SciPy-8CAAE6?logo=scipy&logoColor=white) ![LaTeX](https://img.shields.io/badge/LaTeX-008080?logo=latex&logoColor=white) ![Mathematica](https://img.shields.io/badge/Mathematica-DD1100?logo=wolframmathematica&logoColor=white) ![ROOT](https://img.shields.io/badge/ROOT-CERN-1f4e79) ![tests](https://github.com/IsmailaDEH/Ismaila/actions/workflows/tests.yml/badge.svg)

[🌐 Portfolio](https://ismailadeh.github.io/Ismaila/) · [📄 Portfolio PDF](cv/portfolio.pdf) · [💼 LinkedIn](https://www.linkedin.com/in/ismaila-amadou-deh) · [🐙 GitHub](https://github.com/IsmailaDEH)

</div>

---

## 📈 En chiffres

| **11** projets | **61** tests automatiques | **63 504** états diagonalisés exactement | **χ = 0,313** (théorie 1/3) en croissance épitaxiale | **0,9 %** d'erreur sur T_c (Ising) |
|---|---|---|---|---|

## ⭐ Projets phares

| # | Projet | Ce qu'il montre | Résultat clé |
|---|---|---|---|
| 09 | [🧱 Croissance épitaxiale par Monte-Carlo cinétique](projets/09-epitaxie-monte-carlo-cinetique) | Algorithme BKL sans rejet, nucléation, loi d'échelle | N ∝ (D/F)^(−χ) avec χ = 0,313 (théorie 1/3) |
| 10 | [🔬 Modèle de Hubbard : transition de Mott](projets/10-modele-hubbard-diagonalisation-exacte) | Diagonalisation exacte, signes fermioniques, Lanczos | Bethe ansatz à 1,7 % ; J = 4t²/U retrouvé à 0,2 % |
| 11 | [⚛️ Décohérence d'un qubit (Lindblad)](projets/11-qubit-decoherence-lindblad) | Systèmes quantiques ouverts, protocoles T₁ / Ramsey / Rabi | T₂ = 17,14 ± 0,09 µs extrait des « mesures » |
| 06 | [⚛️ Dynamique moléculaire de l'argon](projets/06-dynamique-moleculaire-lennard-jones) | Verlet, conditions périodiques, thermostat, g(r) | 3 phases ; D(liquide) ≈ 3,5 × 10⁻⁵ cm²/s |

<p align="center">
  <img src="projets/09-epitaxie-monte-carlo-cinetique/figures/02_morphologies.png" width="96%">
</p>

## 🗂 Tous les projets, par thème

### Matière condensée et matériaux

| # | Projet | Méthode | Résultat clé |
|---|---|---|---|
| 09 | [🧱 Croissance épitaxiale](projets/09-epitaxie-monte-carlo-cinetique) | Monte-Carlo cinétique (BKL) | χ = 0,313 ; îlots ramifiés ou compacts selon E_b |
| 10 | [🔬 Modèle de Hubbard](projets/10-modele-hubbard-diagonalisation-exacte) | Diagonalisation exacte (Lanczos) | Gap de Mott ; super-échange J = 4t²/U |
| 02 | [🧲 Modèle d'Ising 2D](projets/02-modele-ising-monte-carlo) | Metropolis, taille finie | T_c à 0,9 % de la valeur exacte (Onsager) |
| 06 | [⚛️ Dynamique moléculaire](projets/06-dynamique-moleculaire-lennard-jones) | Verlet-vitesse, viriel | Solide, liquide, gaz ; Maxwell–Boltzmann vérifiée |
| 07 | [📉 Potentiel appris + incertitude](projets/07-potentiel-interatomique-incertitude) | Processus gaussien, apprentissage actif | r_e(H₂) = 0,7400 ± 0,0021 Å ; −34 % d'erreur |

### Physique quantique et qubits

| # | Projet | Méthode | Résultat clé |
|---|---|---|---|
| 11 | [⚛️ Décohérence d'un qubit](projets/11-qubit-decoherence-lindblad) | Lindblad, RK4 maison | T₁, T₂ extraits par ajustement ; T₂ ≤ 2T₁ |
| 08 | [🔗 Inégalités de Bell–CHSH](projets/08-inegalites-bell-chsh) | Règle de Born, variables cachées (stage M1) | S = 2,848 ± 0,014 ; Tsirelson 2√2 |

### Méthodes numériques et systèmes dynamiques

| # | Projet | Méthode | Résultat clé |
|---|---|---|---|
| 01 | [🌀 Pendule double](projets/01-pendule-double-chaos) | RK4, exposants de Lyapunov (projet de L3) | λ = 0,75 s⁻¹ ; énergie conservée à 2 × 10⁻⁷ |
| 03 | [🔥 Équation de la chaleur](projets/03-equation-chaleur-differences-finies) | FTCS, Crank–Nicolson | Ordre 2,01 ; seuil de stabilité retrouvé |
| 04 | [🤖 Découverte d'équations (SINDy)](projets/04-decouverte-equations-sindy) | Régression creuse | Lorenz retrouvé à 0,13 % avec 1 % de bruit |
| 05 | [🪐 Orbites et intégrateurs](projets/05-orbites-kepler-integrateurs) | Euler, RK4, Verlet symplectique | Kepler : pente 1,5000 ; L conservé à 10⁻¹⁵ |

## 🧪 Méthode commune à tous les projets

1. **Partir de la physique** : les équations sont écrites et expliquées dans chaque README.
2. **Coder les algorithmes moi-même** (BKL, Lanczos, Lindblad, Verlet, Metropolis, RK4, processus gaussien, STLSQ) plutôt que d'appeler une boîte noire.
3. **Valider contre une solution exacte** (Bethe ansatz, équations de Bloch, Onsager, Kepler, Maxwell–Boltzmann, Tsirelson) avant d'interpréter.
4. **Quantifier l'incertitude** : erreurs statistiques, ordres de convergence, barres d'erreur propagées.
5. **Reproductible** : `python src/analyse.py` régénère toutes les figures et `resultats.json` ; les tests tournent automatiquement sur GitHub Actions.

## 🎓 Parcours

| Période | Formation / expérience |
|---|---|
| 2026 – 2027 | **Master 2 Physique Fondamentale, parcours Théories Quantiques (QAT)**, Université de Tours, Institut Denis Poisson |
| 2025 – 2026 | **Stage de recherche M1**, Institut Denis Poisson (Pr. S. Nicolis) : modèle de Freund, variables cachées fermioniques, inégalités de Bell et CHSH ; rapport de 46 pages en LaTeX |
| 2025 – 2026 | **Master 1 Physique Fondamentale et Applications**, Université de Tours ; TP avancés : Monte-Carlo, magnétométrie NV (ODMR), RPE, spectroscopie |
| 2022 – 2025 | **Licence de Physique**, Université de Tours ; projet de modélisation du pendule double (L3) |
| 2021 – 2022 | Licence 1 Sciences et Techniques, Université Cheikh Anta Diop (UCAD), Dakar |

## 🛠 Compétences

**Physique :** physique statistique quantique, électrons corrélés, transport quantique, intrication et décohérence, mécanique quantique, théorie classique des champs, physique subatomique, spectroscopie, magnétométrie<br>
**Simulation :** Monte-Carlo cinétique (BKL), diagonalisation exacte (Lanczos), équation de Lindblad, dynamique moléculaire, Monte-Carlo (Metropolis), intégration d'EDO (RK4, Verlet), différences finies, processus gaussiens, quantification d'incertitude<br>
**Outils :** Python (NumPy, SciPy, Matplotlib), pytest, Git/GitHub, GitHub Actions, LaTeX (Overleaf), Mathematica, Maple, ROOT<br>
**Langues :** français (C2), anglais scientifique (B2), pular (langue maternelle), wolof

## 📁 Organisation du dépôt

```
Ismaila/
├── projets/01 … 11/        # chaque projet : src/, tests/, figures/, resultats.json, README.md
├── docs/                   # site portfolio (GitHub Pages)
├── cv/                     # portfolio LaTeX → PDF
├── profil-github/          # README de profil à copier
├── .github/workflows/      # tests automatiques
├── requirements.txt
└── LICENSE (MIT)
```

## 🚀 Démarrage rapide

```bash
git clone https://github.com/IsmailaDEH/Ismaila.git
cd Ismaila
pip install -r requirements.txt
cd projets/10-modele-hubbard-diagonalisation-exacte && python src/analyse.py   # ~40 s
```

---

<div align="center"><sub>© 2026 Ismaila AMADOU DEH · Licence MIT</sub></div>
