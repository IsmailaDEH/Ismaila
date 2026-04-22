import React, { useState, useEffect } from 'react'
import { getLessonById, getModuleByLessonId, MODULES } from '../data/lessons'
import CodeEditor from './CodeEditor'
import Quiz from './Quiz'

function MarkdownRenderer({ content }) {
  const lines = content.trim().split('\n')
  const elements = []
  let i = 0
  let key = 0

  while (i < lines.length) {
    const line = lines[i]

    if (line.startsWith('```')) {
      const lang = line.slice(3).trim()
      const codeLines = []
      i++
      while (i < lines.length && !lines[i].startsWith('```')) {
        codeLines.push(lines[i])
        i++
      }
      elements.push(
        <pre key={key++} style={{
          background: '#1e1e2e',
          color: '#cdd6f4',
          borderRadius: 12,
          padding: '16px 20px',
          margin: '12px 0',
          overflowX: 'auto',
          fontFamily: "'Fira Code', 'Consolas', monospace",
          fontSize: '0.92rem',
          lineHeight: 1.7,
        }}>
          <code>{codeLines.join('\n')}</code>
        </pre>
      )
    } else if (line.startsWith('# ')) {
      elements.push(<h1 key={key++} style={{ fontSize: '1.7rem', fontWeight: 800, marginTop: 8, marginBottom: 12, color: 'var(--primary)' }}>{line.slice(2)}</h1>)
    } else if (line.startsWith('## ')) {
      elements.push(<h2 key={key++} style={{ fontSize: '1.3rem', fontWeight: 700, marginTop: 20, marginBottom: 8 }}>{line.slice(3)}</h2>)
    } else if (line.startsWith('> ')) {
      elements.push(
        <blockquote key={key++} style={{
          background: '#f0f4ff',
          borderLeft: '4px solid var(--primary)',
          padding: '10px 16px',
          borderRadius: '0 10px 10px 0',
          margin: '10px 0',
          fontStyle: 'italic',
        }}>
          {renderInline(line.slice(2))}
        </blockquote>
      )
    } else if (line.match(/^\|.*\|$/)) {
      const tableLines = [line]
      i++
      while (i < lines.length && lines[i].match(/^\|.*\|$/)) {
        tableLines.push(lines[i])
        i++
      }
      const headers = tableLines[0].split('|').filter(Boolean).map(h => h.trim())
      const rows = tableLines.slice(2).map(r => r.split('|').filter(Boolean).map(c => c.trim()))
      elements.push(
        <table key={key++} style={{ borderCollapse: 'collapse', margin: '12px 0', width: '100%' }}>
          <thead>
            <tr>
              {headers.map((h, j) => (
                <th key={j} style={{
                  background: 'var(--primary)', color: 'white',
                  padding: '8px 14px', textAlign: 'left', fontSize: '0.9rem',
                  borderRadius: j === 0 ? '8px 0 0 0' : j === headers.length - 1 ? '0 8px 0 0' : 0,
                }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row, ri) => (
              <tr key={ri} style={{ background: ri % 2 === 0 ? '#f8f9ff' : 'white' }}>
                {row.map((cell, ci) => (
                  <td key={ci} style={{ padding: '8px 14px', border: '1px solid var(--border)', fontSize: '0.9rem' }}>
                    <code style={{ background: '#f0f0f0', padding: '2px 6px', borderRadius: 4 }}>{cell}</code>
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      )
      continue
    } else if (line === '') {
      // skip empty lines
    } else {
      elements.push(<p key={key++} style={{ margin: '8px 0', lineHeight: 1.75 }}>{renderInline(line)}</p>)
    }
    i++
  }

  return <div style={{ fontSize: '1rem' }}>{elements}</div>
}

function renderInline(text) {
  const parts = []
  const regex = /(`[^`]+`|\*\*[^*]+\*\*|\*[^*]+\*)/g
  let last = 0
  let match

  while ((match = regex.exec(text)) !== null) {
    if (match.index > last) parts.push(text.slice(last, match.index))
    const m = match[0]
    if (m.startsWith('**')) {
      parts.push(<strong key={match.index}>{m.slice(2, -2)}</strong>)
    } else if (m.startsWith('*')) {
      parts.push(<em key={match.index}>{m.slice(1, -1)}</em>)
    } else {
      parts.push(
        <code key={match.index} style={{
          background: '#f0f2ff',
          color: 'var(--primary-dark)',
          padding: '2px 6px',
          borderRadius: 5,
          fontFamily: "'Fira Code', monospace",
          fontSize: '0.9em',
        }}>
          {m.slice(1, -1)}
        </code>
      )
    }
    last = match.index + m.length
  }
  if (last < text.length) parts.push(text.slice(last))
  return parts
}

export default function LessonView({ lessonId, progress, onComplete, onNavigate }) {
  const lesson = getLessonById(lessonId)
  const module_ = getModuleByLessonId(lessonId)
  const [phase, setPhase] = useState('theory') // theory | exercise | quiz
  const [exerciseDone, setExerciseDone] = useState(false)
  const [showCelebration, setShowCelebration] = useState(false)

  useEffect(() => {
    setPhase('theory')
    setExerciseDone(false)
    setShowCelebration(false)
    window.scrollTo(0, 0)
  }, [lessonId])

  if (!lesson || !module_) return null

  const moduleIdx = MODULES.indexOf(module_)
  const lessonIdx = module_.lessons.indexOf(lesson)
  const nextLesson = module_.lessons[lessonIdx + 1] ||
    (MODULES[moduleIdx + 1]?.lessons[0])
  const prevLesson = module_.lessons[lessonIdx - 1] ||
    (moduleIdx > 0 ? MODULES[moduleIdx - 1].lessons.slice(-1)[0] : null)

  const isAlreadyDone = progress.completedLessons.includes(lessonId)

  const handleExerciseDone = () => {
    setExerciseDone(true)
    setShowCelebration(true)
    setTimeout(() => setShowCelebration(false), 2000)
  }

  const handleQuizComplete = (score) => {
    if (!isAlreadyDone) onComplete(lessonId, lesson.xp, lesson.quizId, score)
  }

  const goToNext = () => {
    if (nextLesson) onNavigate('lesson', nextLesson.id)
    else onNavigate('home')
  }

  return (
    <div style={{ maxWidth: 860, margin: '0 auto', padding: '28px 20px' }}>
      {showCelebration && (
        <div style={{
          position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          pointerEvents: 'none', zIndex: 1000,
        }}>
          <div style={{
            background: 'var(--success)',
            color: 'white',
            borderRadius: 20,
            padding: '24px 40px',
            fontSize: '1.5rem',
            fontWeight: 800,
            boxShadow: '0 8px 32px rgba(67,233,123,0.4)',
            animation: 'bounceIn 0.5s ease',
          }}>
            🎉 Super ! Exercice réussi !
          </div>
        </div>
      )}

      {/* Breadcrumb */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 20, fontSize: '0.9rem', color: 'var(--text-light)' }}>
        <button onClick={() => onNavigate('home')} style={{ background: 'none', border: 'none', color: 'var(--primary)', cursor: 'pointer', fontWeight: 600 }}>
          🏠 Accueil
        </button>
        <span>/</span>
        <span style={{ color: module_.color, fontWeight: 600 }}>{module_.icon} {module_.title}</span>
        <span>/</span>
        <span style={{ fontWeight: 600, color: 'var(--text)' }}>{lesson.title}</span>
      </div>

      {/* Header leçon */}
      <div style={{
        background: `linear-gradient(135deg, ${module_.color}22, ${module_.color}11)`,
        border: `2px solid ${module_.color}44`,
        borderRadius: 20,
        padding: '24px 28px',
        marginBottom: 28,
        display: 'flex',
        alignItems: 'center',
        gap: 16,
      }}>
        <div style={{
          background: module_.colorLight,
          borderRadius: 16,
          width: 64, height: 64,
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: '2rem', flexShrink: 0,
        }}>
          {lesson.icon}
        </div>
        <div>
          <div style={{ fontSize: '0.85rem', color: module_.color, fontWeight: 600, marginBottom: 4 }}>
            Leçon {lessonIdx + 1}/{module_.lessons.length}
          </div>
          <h1 style={{ fontSize: '1.5rem', fontWeight: 800, margin: 0 }}>{lesson.title}</h1>
          <div style={{ color: 'var(--text-light)', fontSize: '0.9rem', marginTop: 4 }}>
            +{lesson.xp} XP • {isAlreadyDone ? '✅ Complétée' : ''}
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div style={{
        display: 'flex',
        gap: 4,
        background: 'var(--bg)',
        borderRadius: 14,
        padding: 6,
        marginBottom: 24,
        width: 'fit-content',
      }}>
        {['theory', 'exercise', 'quiz'].map(tab => (
          <button
            key={tab}
            onClick={() => setPhase(tab)}
            style={{
              background: phase === tab ? 'white' : 'transparent',
              border: 'none',
              borderRadius: 10,
              padding: '8px 18px',
              fontWeight: phase === tab ? 700 : 500,
              color: phase === tab ? 'var(--primary)' : 'var(--text-light)',
              boxShadow: phase === tab ? '0 2px 8px rgba(0,0,0,0.08)' : 'none',
              transition: 'all 0.2s',
              fontSize: '0.9rem',
              display: 'flex', alignItems: 'center', gap: 6,
            }}
          >
            {tab === 'theory' ? '📖 Cours' : tab === 'exercise' ? '⌨️ Exercice' : '❓ Quiz'}
            {tab === 'exercise' && exerciseDone && <span style={{ color: 'var(--success)' }}>✓</span>}
            {tab === 'quiz' && progress.completedQuizzes.find(q => q.id === lesson.quizId) &&
              <span style={{ color: 'var(--success)' }}>✓</span>}
          </button>
        ))}
      </div>

      {/* Contenu */}
      <div style={{
        background: 'white',
        borderRadius: 20,
        padding: '28px 32px',
        boxShadow: 'var(--shadow)',
        marginBottom: 24,
      }}>
        {phase === 'theory' && (
          <div>
            <MarkdownRenderer content={lesson.theory} />
            <div style={{ marginTop: 28, display: 'flex', gap: 12 }}>
              <button
                onClick={() => setPhase('exercise')}
                style={{
                  background: 'linear-gradient(135deg, var(--primary), var(--primary-dark))',
                  color: 'white',
                  border: 'none',
                  borderRadius: 12,
                  padding: '12px 24px',
                  fontWeight: 700,
                  fontSize: '1rem',
                  cursor: 'pointer',
                }}
              >
                Pratiquer ⌨️
              </button>
            </div>
          </div>
        )}

        {phase === 'exercise' && (
          <CodeEditor
            exercise={lesson.exercise}
            onSuccess={handleExerciseDone}
          />
        )}

        {phase === 'quiz' && (
          <Quiz
            quizId={lesson.quizId}
            onComplete={handleQuizComplete}
            onSkip={goToNext}
          />
        )}
      </div>

      {/* Navigation */}
      <div style={{ display: 'flex', justifyContent: 'space-between', gap: 12 }}>
        <button
          onClick={() => prevLesson ? onNavigate('lesson', prevLesson.id) : onNavigate('home')}
          style={{
            background: 'white',
            border: '2px solid var(--border)',
            borderRadius: 12,
            padding: '12px 20px',
            fontWeight: 600,
            cursor: 'pointer',
            display: 'flex', alignItems: 'center', gap: 8,
          }}
        >
          ← {prevLesson ? 'Précédent' : 'Accueil'}
        </button>

        {phase !== 'quiz' && (
          <button
            onClick={() => phase === 'theory' ? setPhase('exercise') : setPhase('quiz')}
            style={{
              background: 'linear-gradient(135deg, var(--primary), var(--primary-dark))',
              color: 'white',
              border: 'none',
              borderRadius: 12,
              padding: '12px 24px',
              fontWeight: 700,
              cursor: 'pointer',
              display: 'flex', alignItems: 'center', gap: 8,
            }}
          >
            {phase === 'theory' ? 'Exercice →' : 'Quiz →'}
          </button>
        )}

        {nextLesson && (
          <button
            onClick={goToNext}
            style={{
              background: 'white',
              border: '2px solid var(--border)',
              borderRadius: 12,
              padding: '12px 20px',
              fontWeight: 600,
              cursor: 'pointer',
              display: 'flex', alignItems: 'center', gap: 8,
            }}
          >
            Suivant →
          </button>
        )}
      </div>
    </div>
  )
}
