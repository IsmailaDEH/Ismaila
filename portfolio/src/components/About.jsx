const INFO = [
  { label: 'Niveau',         value: 'Master 2 PFA – QAT' },
  { label: 'Laboratoire',    value: 'Institut Denis Poisson (CNRS UMR 7013)' },
  { label: 'Secteurs visés', value: 'Aérospatial-défense · Informatique quantique' },
  { label: 'Disponibilité',  value: 'Stage M2 · Fév. 2027 · 6 mois' },
]

export default function About() {
  return (
    <section className="section" id="about">
      <div className="section-inner">
        <h2 className="section-heading">À Propos</h2>
        <div className="about-grid">
          <p className="about-text">
            Étudiant en Master 2 Physique Fondamentale, parcours Théories Quantiques,
            à l'Université de Tours (Institut Denis Poisson, CNRS), je recherche un stage
            de M2 en physique théorique, simulation numérique ou informatique quantique.
            Curieux et rigoureux, je m'intéresse particulièrement à la R&D scientifique
            dans les secteurs aérospatial-défense et quantique.
          </p>
          <div className="about-info-cards">
            {INFO.map(({ label, value }) => (
              <div key={label} className="info-card">
                <div className="info-card-label">{label}</div>
                <div className="info-card-value">{value}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
