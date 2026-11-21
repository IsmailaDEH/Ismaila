export default function Contact() {
  return (
    <section className="section" id="contact">
      <div className="section-inner">
        <h2 className="section-heading">Contact</h2>
        <div className="contact-center">
          <a className="contact-email" href="mailto:dehismailaamadou@gmail.com">
            dehismailaamadou@gmail.com
          </a>

          <div className="contact-links">
            <a
              className="btn btn-outline"
              href="https://linkedin.com/in/ismaila-amadou-deh"
              target="_blank"
              rel="noopener noreferrer"
            >
              LinkedIn
            </a>
            <a
              className="btn btn-outline"
              href="https://github.com/IsmailaDEH"
              target="_blank"
              rel="noopener noreferrer"
            >
              GitHub
            </a>
            <a
              className="btn btn-primary"
              href="/cv/Ismaila_Amadou_Deh_CV.pdf"
              target="_blank"
              rel="noopener noreferrer"
              download="Ismaila_Amadou_Deh_CV.pdf"
            >
              ↓ CV
            </a>
          </div>

          <p className="contact-note">
            Disponible pour un <span>stage de M2</span> en physique théorique,
            simulation numérique ou informatique quantique,{' '}
            <span>à partir de février 2027</span> (durée 6 mois).
          </p>
        </div>
      </div>
    </section>
  )
}
