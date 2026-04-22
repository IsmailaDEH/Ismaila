import React from 'react'

export default function Header({ currentPage, onNavigate, progress }) {
  const xpToNextLevel = 200
  const xpInCurrentLevel = progress.xp % xpToNextLevel
  const xpPercent = (xpInCurrentLevel / xpToNextLevel) * 100

  return (
    <header style={{
      background: 'white',
      borderBottom: '2px solid var(--border)',
      padding: '12px 24px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      position: 'sticky',
      top: 0,
      zIndex: 100,
      boxShadow: '0 2px 12px rgba(108,99,255,0.08)',
    }}>
      <button
        onClick={() => onNavigate('home')}
        style={{
          background: 'none',
          border: 'none',
          fontSize: '1.4rem',
          fontWeight: 800,
          color: 'var(--primary)',
          display: 'flex',
          alignItems: 'center',
          gap: 8,
          cursor: 'pointer',
        }}
      >
        🚀 <span>CodeDébutant</span>
      </button>

      <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
        <div style={{
          background: 'var(--bg)',
          borderRadius: 50,
          padding: '6px 14px',
          display: 'flex',
          alignItems: 'center',
          gap: 8,
          fontSize: '0.9rem',
          fontWeight: 600,
        }}>
          <span>⭐</span>
          <span style={{ color: 'var(--primary)' }}>{progress.xp} XP</span>
        </div>

        <div style={{
          background: 'var(--bg)',
          borderRadius: 50,
          padding: '6px 14px',
          display: 'flex',
          alignItems: 'center',
          gap: 6,
          fontSize: '0.9rem',
        }}>
          <span>🏆</span>
          <span style={{ fontWeight: 700, color: 'var(--secondary)' }}>Niv. {progress.level}</span>
          <div style={{
            width: 60,
            height: 8,
            background: '#eee',
            borderRadius: 4,
            overflow: 'hidden',
          }}>
            <div style={{
              width: `${xpPercent}%`,
              height: '100%',
              background: 'linear-gradient(90deg, var(--primary), var(--secondary))',
              borderRadius: 4,
              transition: 'width 0.5s ease',
            }} />
          </div>
        </div>

        {progress.badges.length > 0 && (
          <div style={{ display: 'flex', gap: 4 }}>
            {progress.badges.slice(-3).map(badge => (
              <span key={badge} title={badge} style={{ fontSize: '1.2rem' }}>
                {badge === 'first_lesson' ? '🌟' :
                 badge === 'five_lessons' ? '🔥' :
                 badge === 'ten_lessons' ? '💎' :
                 badge === 'perfect_quiz' ? '🎯' : '🏅'}
              </span>
            ))}
          </div>
        )}
      </div>
    </header>
  )
}
