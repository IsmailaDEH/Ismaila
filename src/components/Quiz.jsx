import React, { useState } from 'react'
import { QUIZZES } from '../data/quizzes'

export default function Quiz({ quizId, onComplete, onSkip }) {
  const quiz = QUIZZES[quizId]
  const [current, setCurrent] = useState(0)
  const [selected, setSelected] = useState(null)
  const [answered, setAnswered] = useState(false)
  const [results, setResults] = useState([])
  const [done, setDone] = useState(false)

  if (!quiz) return null

  const question = quiz.questions[current]
  const score = Math.round((results.filter(Boolean).length / quiz.questions.length) * 100)

  const handleSelect = (idx) => {
    if (answered) return
    setSelected(idx)
    setAnswered(true)
    const correct = idx === question.correct
    setResults(prev => [...prev, correct])
  }

  const next = () => {
    if (current + 1 < quiz.questions.length) {
      setCurrent(c => c + 1)
      setSelected(null)
      setAnswered(false)
    } else {
      setDone(true)
      onComplete(score)
    }
  }

  if (done) {
    const correct = results.filter(Boolean).length
    return (
      <div style={{
        background: 'white',
        borderRadius: 24,
        padding: '40px 32px',
        textAlign: 'center',
        boxShadow: 'var(--shadow)',
        maxWidth: 520,
        margin: '0 auto',
      }}>
        <div style={{ fontSize: '4rem', marginBottom: 16 }}>
          {score === 100 ? '🎯' : score >= 66 ? '🌟' : score >= 33 ? '👍' : '💪'}
        </div>
        <h2 style={{ fontSize: '1.8rem', fontWeight: 800, marginBottom: 8 }}>
          {score === 100 ? 'Parfait !' : score >= 66 ? 'Bien joué !' : 'Continue !'}
        </h2>
        <p style={{ color: 'var(--text-light)', marginBottom: 24, fontSize: '1.05rem' }}>
          Tu as obtenu {correct}/{quiz.questions.length} bonnes réponses
        </p>
        <div style={{
          background: score === 100 ? '#f0fff4' : score >= 66 ? '#f0f4ff' : '#fff3f0',
          borderRadius: 16,
          padding: '20px',
          marginBottom: 28,
        }}>
          <div style={{
            fontSize: '3rem',
            fontWeight: 900,
            color: score === 100 ? 'var(--success)' : score >= 66 ? 'var(--primary)' : 'var(--secondary)',
          }}>
            {score}%
          </div>
          <div style={{ color: 'var(--text-light)' }}>
            +{score === 100 ? 60 : 30} XP gagnés
          </div>
        </div>
        {score < 100 && (
          <p style={{ color: 'var(--text-light)', fontSize: '0.9rem', marginBottom: 20 }}>
            Relis la leçon et réessaie pour améliorer ton score !
          </p>
        )}
        <button
          onClick={onSkip}
          style={{
            background: 'linear-gradient(135deg, var(--primary), var(--primary-dark))',
            color: 'white',
            border: 'none',
            borderRadius: 14,
            padding: '14px 32px',
            fontWeight: 700,
            fontSize: '1rem',
            cursor: 'pointer',
          }}
        >
          Continuer →
        </button>
      </div>
    )
  }

  return (
    <div style={{
      background: 'white',
      borderRadius: 24,
      padding: '32px',
      boxShadow: 'var(--shadow)',
      maxWidth: 580,
      margin: '0 auto',
    }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div style={{
          background: 'var(--bg)',
          borderRadius: 20,
          padding: '4px 12px',
          fontWeight: 600,
          fontSize: '0.9rem',
          color: 'var(--primary)',
        }}>
          Question {current + 1}/{quiz.questions.length}
        </div>
        <div style={{ display: 'flex', gap: 6 }}>
          {quiz.questions.map((_, i) => (
            <div key={i} style={{
              width: 10, height: 10, borderRadius: '50%',
              background: i < results.length
                ? (results[i] ? 'var(--success)' : 'var(--error)')
                : i === current ? 'var(--primary)' : '#e0e0e0',
              transition: 'background 0.3s',
            }} />
          ))}
        </div>
      </div>

      {/* Question */}
      <h3 style={{ fontSize: '1.2rem', fontWeight: 700, marginBottom: 20, lineHeight: 1.5 }}>
        {question.question}
      </h3>

      {/* Options */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 10, marginBottom: 20 }}>
        {question.options.map((option, idx) => {
          let bg = 'var(--bg)'
          let border = 'var(--border)'
          let color = 'var(--text)'

          if (answered) {
            if (idx === question.correct) {
              bg = '#f0fff4'; border = 'var(--success)'; color = '#1a7a3a'
            } else if (idx === selected && idx !== question.correct) {
              bg = '#fff0f0'; border = 'var(--error)'; color = '#c0392b'
            }
          } else if (idx === selected) {
            bg = '#f0f4ff'; border = 'var(--primary)'
          }

          return (
            <button
              key={idx}
              onClick={() => handleSelect(idx)}
              style={{
                background: bg,
                border: `2px solid ${border}`,
                borderRadius: 12,
                padding: '14px 18px',
                textAlign: 'left',
                cursor: answered ? 'default' : 'pointer',
                color,
                fontWeight: answered && idx === question.correct ? 700 : 500,
                fontSize: '0.95rem',
                display: 'flex',
                alignItems: 'center',
                gap: 10,
                transition: 'all 0.2s',
                transform: !answered && idx === selected ? 'scale(1.01)' : 'scale(1)',
              }}
            >
              <span style={{
                width: 28, height: 28,
                borderRadius: '50%',
                background: answered && idx === question.correct ? 'var(--success)' :
                             answered && idx === selected && idx !== question.correct ? 'var(--error)' :
                             idx === selected ? 'var(--primary)' : '#ddd',
                color: 'white',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontSize: '0.85rem', fontWeight: 700, flexShrink: 0,
              }}>
                {answered && idx === question.correct ? '✓' :
                 answered && idx === selected && idx !== question.correct ? '✗' :
                 String.fromCharCode(65 + idx)}
              </span>
              {option}
            </button>
          )
        })}
      </div>

      {/* Explication */}
      {answered && (
        <div style={{
          background: selected === question.correct ? '#f0fff4' : '#fff0f0',
          border: `2px solid ${selected === question.correct ? 'var(--success)' : 'var(--error)'}`,
          borderRadius: 12,
          padding: '12px 16px',
          marginBottom: 16,
          fontSize: '0.9rem',
          animation: 'fadeIn 0.3s ease',
        }}>
          <strong>{selected === question.correct ? '✅ Correct !' : '❌ Pas tout à fait...'}</strong>
          <br />
          {question.explanation}
        </div>
      )}

      {answered && (
        <button
          onClick={next}
          style={{
            width: '100%',
            background: 'linear-gradient(135deg, var(--primary), var(--primary-dark))',
            color: 'white',
            border: 'none',
            borderRadius: 12,
            padding: '14px',
            fontWeight: 700,
            fontSize: '1rem',
            cursor: 'pointer',
          }}
        >
          {current + 1 < quiz.questions.length ? 'Question suivante →' : 'Voir les résultats 🎉'}
        </button>
      )}
    </div>
  )
}
