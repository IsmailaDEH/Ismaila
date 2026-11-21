export default function Hero() {
  return (
    <section className="hero" id="home">
      <div className="hero-bg" />
      <div className="hero-stars" />
      <div className="hero-content">
        <div className="hero-photo-wrap">
          <picture>
            <source
              srcSet="/images/ismaila-200.webp 200w, /images/ismaila-400.webp 400w, /images/ismaila-870.webp 870w"
              sizes="(max-width: 480px) 150px, (max-width: 768px) 180px, 220px"
              type="image/webp"
            />
            <img
              src="/images/ismaila-870.webp"
              alt="Ismaila Amadou Deh"
              width="220"
              height="220"
            />
          </picture>
        </div>

        <h1 className="hero-name">Ismaila Amadou Deh</h1>
        <p className="hero-subtitle">Stage de M2 — Physique Théorique &amp; Simulation</p>

        <div className="hero-tags">
          {['Informatique Quantique', 'Institut Denis Poisson', 'Université de Tours'].map(t => (
            <span key={t} className="hero-tag">{t}</span>
          ))}
        </div>

        <div className="hero-cta">
          <a
            className="btn btn-primary"
            href="/cv/Ismaila_Amadou_Deh_CV.pdf"
            target="_blank"
            rel="noopener noreferrer"
            download="Ismaila_Amadou_Deh_CV.pdf"
          >
            ↓ Télécharger le CV
          </a>
          <a className="btn btn-outline" href="#contact">
            Me contacter
          </a>
        </div>
      </div>
    </section>
  )
}
