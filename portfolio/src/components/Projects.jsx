const PROJECTS = [
  {
    emoji: '⚛️',
    title: 'cat-qubit-simulator',
    desc: 'Simulation de qubits chats pour la correction d\'erreurs quantiques. Modélisation des états cohérents et des processus de décoherence.',
    tags: ['Python', 'Quantum', 'NumPy', 'SciPy'],
    url: 'https://github.com/IsmailaDEH/cat-qubit-simulator',
  },
  {
    emoji: '🐍',
    title: 'Apprendre Python',
    desc: 'Application CLI interactive pour apprendre Python pas à pas — 10 leçons progressives avec quiz, exercices validés et suivi XP.',
    tags: ['Python', 'CLI', 'Éducation'],
    url: 'https://github.com/IsmailaDEH/Ismaila',
  },
]

export default function Projects() {
  return (
    <section className="section" id="projets">
      <div className="section-inner">
        <h2 className="section-heading">Projets</h2>
        <div className="projects-grid">
          {PROJECTS.map((p) => (
            <div key={p.title} className="card project-card">
              <div className="project-title">
                <span>{p.emoji}</span> {p.title}
              </div>
              <p className="project-desc">{p.desc}</p>
              <div className="project-tags">
                {p.tags.map(t => (
                  <span key={t} className="project-tag">{t}</span>
                ))}
              </div>
              <a
                className="project-link"
                href={p.url}
                target="_blank"
                rel="noopener noreferrer"
              >
                Voir sur GitHub →
              </a>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
