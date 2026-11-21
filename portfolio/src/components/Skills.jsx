import { useEffect, useRef } from 'react'

const PHYSICS = [
  'Mécanique quantique', 'Théorie classique des champs',
  'Physique statistique quantique', 'Physique subatomique',
  'Spectroscopie', 'Magnétométrie', 'Physique expérimentale',
]

const PROGRAMMING = [
  'Python', 'NumPy', 'SciPy', 'Matplotlib',
  'Méthode de Monte Carlo', "Modèle d'Ising",
  'Algorithme de Metropolis', 'Runge-Kutta',
]

const TOOLS = ['LaTeX (Overleaf)', 'Mathematica', 'Maple', 'ROOT', 'Git']

const LANGUAGES = [
  { name: 'Pular',    level: 'Langue maternelle', pct: 100 },
  { name: 'Français', level: 'C2',                 pct: 95 },
  { name: 'Wolof',    level: 'Courant',             pct: 80 },
  { name: 'Anglais',  level: 'B2 scientifique',     pct: 70 },
]

function ChipGroup({ chips }) {
  return (
    <div>
      {chips.map(c => <span key={c} className="skill-chip">{c}</span>)}
    </div>
  )
}

function LangBars() {
  const ref = useRef(null)

  useEffect(() => {
    const bars = ref.current?.querySelectorAll('.lang-bar-fill')
    if (!bars) return

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            bars.forEach(bar => {
              bar.style.width = bar.dataset.pct + '%'
            })
            observer.disconnect()
          }
        })
      },
      { threshold: 0.3 }
    )
    observer.observe(ref.current)
    return () => observer.disconnect()
  }, [])

  return (
    <div ref={ref}>
      {LANGUAGES.map(l => (
        <div key={l.name} className="lang-bar-wrap">
          <div className="lang-bar-label">
            <span style={{ fontWeight: 600 }}>{l.name}</span>
            <span style={{ color: 'var(--gold)', fontSize: '0.82rem' }}>{l.level}</span>
          </div>
          <div className="lang-bar-track">
            <div
              className="lang-bar-fill animated"
              data-pct={l.pct}
              style={{ width: 0 }}
            />
          </div>
        </div>
      ))}
    </div>
  )
}

export default function Skills() {
  return (
    <section className="section" id="competences">
      <div className="section-inner">
        <h2 className="section-heading">Compétences</h2>
        <div className="skills-grid">
          <div className="card">
            <div className="skills-category-title">Physique</div>
            <ChipGroup chips={PHYSICS} />
          </div>
          <div className="card">
            <div className="skills-category-title">Simulation &amp; Programmation</div>
            <ChipGroup chips={PROGRAMMING} />
          </div>
          <div className="card">
            <div className="skills-category-title">Logiciels &amp; Outils</div>
            <ChipGroup chips={TOOLS} />
          </div>
          <div className="card">
            <div className="skills-category-title">Langues</div>
            <LangBars />
          </div>
        </div>
      </div>
    </section>
  )
}
