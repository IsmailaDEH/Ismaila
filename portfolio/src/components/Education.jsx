const EDUCATION = [
  {
    year: '2026 – 2027',
    degree: 'Master 2 – Physique Fondamentale, parcours Théories Quantiques',
    institution: 'Université de Tours · Institut Denis Poisson (CNRS UMR 7013)',
    desc: 'En cours — sous la direction du Pr. Stamatios Nicolis.',
    badge: 'En cours',
  },
  {
    year: '2025 – 2026',
    degree: 'Master 1 – Physique Fondamentale et Applications',
    institution: 'Université de Tours',
    desc: 'Mécanique quantique 2, théorie classique des champs, physique statistique quantique, physique subatomique.',
  },
  {
    year: '2022 – 2025',
    degree: 'Licence de Physique',
    institution: 'Université de Tours',
    desc: 'Mécanique, électromagnétisme, thermodynamique, optique, mécanique quantique.',
  },
  {
    year: '2021 – 2022',
    degree: 'Licence 1 – Sciences et Techniques',
    institution: 'Université Cheikh Anta Diop (UCAD), Dakar',
    desc: null,
  },
  {
    year: '2018',
    degree: 'Baccalauréat Scientifique (Série S)',
    institution: 'Lycée Limamoulaye, Dakar',
    desc: null,
  },
]

export default function Education() {
  return (
    <section className="section" id="formation">
      <div className="section-inner">
        <h2 className="section-heading">Formation</h2>
        <div className="timeline">
          {EDUCATION.map((e) => (
            <div key={e.degree} className="timeline-item">
              <div className="card">
                <div className="timeline-year">{e.year}</div>
                <div className="timeline-title">
                  {e.degree}
                  {e.badge && (
                    <span style={{
                      marginLeft: '10px',
                      fontSize: '0.72rem',
                      padding: '2px 10px',
                      background: 'rgba(201,168,76,0.15)',
                      color: 'var(--gold)',
                      borderRadius: '20px',
                      fontWeight: 700,
                      verticalAlign: 'middle',
                    }}>
                      {e.badge}
                    </span>
                  )}
                </div>
                <div className="timeline-institution">{e.institution}</div>
                {e.desc && <p className="timeline-desc">{e.desc}</p>}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
