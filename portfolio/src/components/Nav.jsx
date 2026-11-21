import { useState, useEffect } from 'react'

const LINKS = [
  { label: 'À propos',    href: '#about' },
  { label: 'Formation',   href: '#formation' },
  { label: 'Expériences', href: '#experiences' },
  { label: 'Compétences', href: '#competences' },
  { label: 'Projets',     href: '#projets' },
  { label: 'Contact',     href: '#contact' },
]

export default function Nav() {
  const [scrolled, setScrolled] = useState(false)
  const [open, setOpen]         = useState(false)

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 80)
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  const close = () => setOpen(false)

  return (
    <>
      <nav className={`nav${scrolled ? ' scrolled' : ''}`}>
        <a href="#" className="nav-logo" title="Ismaila Amadou Deh">IAD</a>
        <ul className="nav-links">
          {LINKS.map(l => (
            <li key={l.href}><a href={l.href}>{l.label}</a></li>
          ))}
        </ul>
        <button className="nav-burger" onClick={() => setOpen(true)} aria-label="Menu">
          <span /><span /><span />
        </button>
      </nav>

      <div className={`nav-mobile${open ? ' open' : ''}`}>
        <button className="nav-mobile-close" onClick={close} aria-label="Fermer">×</button>
        {LINKS.map(l => (
          <a key={l.href} href={l.href} onClick={close}>{l.label}</a>
        ))}
      </div>
    </>
  )
}
