import React from 'react'
import { MODULES } from '../data/lessons'

const BADGES = {
  first_lesson: { icon: '🌟', label: 'Premier cours !', desc: 'Tu as terminé ta première leçon' },
  five_lessons: { icon: '🔥', label: '5 leçons !', desc: 'Tu as terminé 5 leçons' },
  ten_lessons: { icon: '💎', label: '10 leçons !', desc: 'Tu as terminé 10 leçons' },
  perfect_quiz: { icon: '🎯', label: 'Quiz parfait !', desc: 'Tu as eu 100% à un quiz' },
}

export default function Dashboard({ progress, onNavigate }) {
  const totalLessons = MODULES.reduce((sum, m) => sum + m.lessons.length, 0)
  const completedCount = progress.completedLessons.length
  const globalPercent = Math.round((completedCount / totalLessons) * 100)

  return (
    <div style={{ maxWidth: 900, margin: '0 auto', padding: '32px 20px' }}>
      {/* Hero */}
      <div style={{
        background: 'linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%)',
        borderRadius: 24,
        padding: '36px 40px',
        color: 'white',
        marginBottom: 32,
        position: 'relative',
        overflow: 'hidden',
      }}>
        <div style={{
          position: 'absolute', top: -30, right: -30,
          fontSize: 120, opacity: 0.15, userSelect: 'none',
        }}>🚀</div>
        <h1 style={{ fontSize: '2rem', fontWeight: 800, marginBottom: 8 }}>
          Bienvenue sur CodeDébutant ! 👋
        </h1>
        <p style={{ fontSize: '1.1rem', opacity: 0.9, marginBottom: 20 }}>
          Apprends à coder pas à pas, avec des exercices interactifs et amusants.
        </p>
        <div style={{ display: 'flex', alignItems: 'center', gap: 16, flexWrap: 'wrap' }}>
          <div style={{
            background: 'rgba(255,255,255,0.2)',
            borderRadius: 12,
            padding: '8px 16px',
            display: 'flex', alignItems: 'center', gap: 8,
          }}>
            <span style={{ fontSize: '1.3rem' }}>⭐</span>
            <span style={{ fontWeight: 700, fontSize: '1.1rem' }}>{progress.xp} XP</span>
          </div>
          <div style={{
            background: 'rgba(255,255,255,0.2)',
            borderRadius: 12,
            padding: '8px 16px',
            display: 'flex', alignItems: 'center', gap: 8,
          }}>
            <span style={{ fontSize: '1.3rem' }}>🏆</span>
            <span style={{ fontWeight: 700, fontSize: '1.1rem' }}>Niveau {progress.level}</span>
          </div>
          <div style={{
            background: 'rgba(255,255,255,0.2)',
            borderRadius: 12,
            padding: '8px 16px',
            display: 'flex', alignItems: 'center', gap: 8,
          }}>
            <span style={{ fontSize: '1.3rem' }}>📚</span>
            <span style={{ fontWeight: 700, fontSize: '1.1rem' }}>{completedCount}/{totalLessons} leçons</span>
          </div>
        </div>
      </div>

      {/* Progression globale */}
      <div style={{
        background: 'white',
        borderRadius: 16,
        padding: '20px 24px',
        marginBottom: 32,
        boxShadow: 'var(--shadow)',
        border: '1px solid var(--border)',
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 10 }}>
          <span style={{ fontWeight: 600 }}>Progression globale</span>
          <span style={{ fontWeight: 700, color: 'var(--primary)' }}>{globalPercent}%</span>
        </div>
        <div style={{
          height: 14, background: '#f0f0f0', borderRadius: 7, overflow: 'hidden',
        }}>
          <div style={{
            width: `${globalPercent}%`,
            height: '100%',
            background: 'linear-gradient(90deg, var(--primary), var(--secondary))',
            borderRadius: 7,
            transition: 'width 0.8s ease',
          }} />
        </div>
      </div>

      {/* Modules */}
      <h2 style={{ fontSize: '1.4rem', fontWeight: 700, marginBottom: 20 }}>
        📖 Les modules d'apprentissage
      </h2>
      <div style={{ display: 'grid', gap: 20, marginBottom: 40 }}>
        {MODULES.map((module, idx) => {
          const moduleCompleted = module.lessons.filter(l =>
            progress.completedLessons.includes(l.id)
          ).length
          const modulePercent = Math.round((moduleCompleted / module.lessons.length) * 100)
          const isLocked = idx > 0 &&
            MODULES[idx - 1].lessons.filter(l => progress.completedLessons.includes(l.id)).length === 0

          return (
            <div
              key={module.id}
              style={{
                background: isLocked ? '#f8f8f8' : 'white',
                borderRadius: 20,
                padding: 24,
                boxShadow: isLocked ? 'none' : 'var(--shadow)',
                border: `2px solid ${isLocked ? '#e0e0e0' : module.color + '33'}`,
                opacity: isLocked ? 0.65 : 1,
              }}
            >
              <div style={{ display: 'flex', alignItems: 'flex-start', gap: 16, marginBottom: 16 }}>
                <div style={{
                  background: isLocked ? '#e0e0e0' : module.colorLight,
                  borderRadius: 16,
                  width: 56, height: 56,
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  fontSize: '1.8rem', flexShrink: 0,
                }}>
                  {isLocked ? '🔒' : module.icon}
                </div>
                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <h3 style={{ fontSize: '1.2rem', fontWeight: 700 }}>{module.title}</h3>
                    <span style={{
                      fontWeight: 700,
                      color: modulePercent === 100 ? 'var(--success)' : 'var(--primary)',
                      fontSize: '1rem',
                    }}>
                      {moduleCompleted}/{module.lessons.length}
                    </span>
                  </div>
                  <p style={{ color: 'var(--text-light)', margin: '4px 0 10px' }}>
                    {module.description}
                  </p>
                  <div style={{ height: 8, background: '#f0f0f0', borderRadius: 4, overflow: 'hidden' }}>
                    <div style={{
                      width: `${modulePercent}%`,
                      height: '100%',
                      background: modulePercent === 100
                        ? 'var(--success)'
                        : `linear-gradient(90deg, ${module.color}, ${module.color}bb)`,
                      borderRadius: 4,
                      transition: 'width 0.6s ease',
                    }} />
                  </div>
                </div>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))', gap: 10 }}>
                {module.lessons.map((lesson, lIdx) => {
                  const isDone = progress.completedLessons.includes(lesson.id)
                  const isLessonLocked = isLocked || (lIdx > 0 && !progress.completedLessons.includes(module.lessons[lIdx - 1].id) && moduleCompleted === 0)

                  return (
                    <button
                      key={lesson.id}
                      onClick={() => !isLessonLocked && onNavigate('lesson', lesson.id)}
                      disabled={isLessonLocked}
                      style={{
                        background: isDone ? '#f0fff4' : isLessonLocked ? '#f5f5f5' : 'var(--bg)',
                        border: `2px solid ${isDone ? 'var(--success)' : isLessonLocked ? '#e0e0e0' : 'var(--border)'}`,
                        borderRadius: 12,
                        padding: '10px 14px',
                        textAlign: 'left',
                        cursor: isLessonLocked ? 'not-allowed' : 'pointer',
                        transition: 'all 0.2s',
                        display: 'flex', alignItems: 'center', gap: 8,
                      }}
                      onMouseEnter={e => {
                        if (!isLessonLocked) e.currentTarget.style.transform = 'translateY(-2px)'
                      }}
                      onMouseLeave={e => { e.currentTarget.style.transform = 'translateY(0)' }}
                    >
                      <span style={{ fontSize: '1.2rem' }}>
                        {isDone ? '✅' : isLessonLocked ? '🔒' : lesson.icon}
                      </span>
                      <div>
                        <div style={{ fontWeight: 600, fontSize: '0.85rem', color: isLessonLocked ? '#999' : 'var(--text)' }}>
                          {lesson.title}
                        </div>
                        <div style={{ fontSize: '0.75rem', color: 'var(--text-light)' }}>
                          +{lesson.xp} XP
                        </div>
                      </div>
                    </button>
                  )
                })}
              </div>
            </div>
          )
        })}
      </div>

      {/* Badges */}
      <h2 style={{ fontSize: '1.4rem', fontWeight: 700, marginBottom: 20 }}>
        🏅 Tes badges
      </h2>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: 16 }}>
        {Object.entries(BADGES).map(([key, badge]) => {
          const earned = progress.badges.includes(key)
          return (
            <div key={key} style={{
              background: earned ? 'white' : '#f5f5f5',
              borderRadius: 16,
              padding: '20px',
              textAlign: 'center',
              border: `2px solid ${earned ? 'var(--accent2)' : '#e0e0e0'}`,
              boxShadow: earned ? '0 4px 12px rgba(249,202,36,0.2)' : 'none',
              opacity: earned ? 1 : 0.5,
              transition: 'all 0.3s',
            }}>
              <div style={{ fontSize: '2.5rem', marginBottom: 8, filter: earned ? 'none' : 'grayscale(1)' }}>
                {badge.icon}
              </div>
              <div style={{ fontWeight: 700, marginBottom: 4 }}>{badge.label}</div>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-light)' }}>{badge.desc}</div>
              {!earned && (
                <div style={{
                  marginTop: 8, fontSize: '0.75rem',
                  background: '#e0e0e0', borderRadius: 20, padding: '2px 8px',
                  display: 'inline-block', color: '#777',
                }}>
                  Non obtenu
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}

