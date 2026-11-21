const EXPERIENCES = [
  {
    year: '2025 – 2026',
    title: 'Stage de recherche – Master 1',
    institution: 'Institut Denis Poisson (UMR 7013, CNRS) · Pr. S. Nicolis',
    bullets: [
      'Étude du modèle de Freund (1981) : variables cachées fermioniques et corrélations EPR',
      'Algèbre de Grassmann, intégration de Berezin, inégalités de Bell et CHSH',
      "Rédaction d'un rapport scientifique complet (46 pages, LaTeX) et d'une synthèse illustrée (20 pages)",
    ],
  },
  {
    year: '2025 – 2026',
    title: 'Travaux pratiques avancés – Master 1',
    institution: 'Université de Tours',
    bullets: [
      'RPE/Zeeman (DPPH), spectroscopie laser He-Ne et sodium, couplage spin-orbite',
      'Magnétométrie par centres NV (ODMR)',
      "Simulations Monte Carlo (algorithme de Metropolis, modèle d'Ising 2D)",
    ],
  },
  {
    year: '2024 – 2025',
    title: 'Projet de modélisation – Licence 3',
    institution: 'Université de Tours',
    bullets: [
      'Modélisation du pendule double : résolution numérique par la méthode de Runge-Kutta 4',
      'Analyse du comportement chaotique, implémentation en Python/Matplotlib',
    ],
  },
]

export default function Experience() {
  return (
    <section className="section" id="experiences">
      <div className="section-inner">
        <h2 className="section-heading">Expériences</h2>
        <div className="timeline">
          {EXPERIENCES.map((e) => (
            <div key={e.title + e.year} className="timeline-item">
              <div className="card">
                <div className="timeline-year">{e.year}</div>
                <div className="timeline-title">{e.title}</div>
                <div className="timeline-institution">{e.institution}</div>
                <ul className="timeline-bullets">
                  {e.bullets.map((b) => (
                    <li key={b}>{b}</li>
                  ))}
                </ul>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
