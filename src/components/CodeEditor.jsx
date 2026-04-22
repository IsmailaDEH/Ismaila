import React, { useState, useRef } from 'react'

function runJavaScript(code) {
  const logs = []
  const fakeConsole = {
    log: (...args) => logs.push(args.map(a =>
      typeof a === 'object' ? JSON.stringify(a, null, 2) : String(a)
    ).join(' ')),
  }
  try {
    const fn = new Function('console', code)
    fn(fakeConsole)
    return { logs, error: null }
  } catch (e) {
    return { logs, error: e.message }
  }
}

export default function CodeEditor({ exercise, onSuccess }) {
  const [code, setCode] = useState(exercise.starterCode)
  const [output, setOutput] = useState(null)
  const [showHint, setShowHint] = useState(false)
  const [showSolution, setShowSolution] = useState(false)
  const [success, setSuccess] = useState(false)
  const textareaRef = useRef(null)

  const handleTab = (e) => {
    if (e.key === 'Tab') {
      e.preventDefault()
      const start = e.target.selectionStart
      const end = e.target.selectionEnd
      const newCode = code.substring(0, start) + '  ' + code.substring(end)
      setCode(newCode)
      setTimeout(() => {
        textareaRef.current.selectionStart = start + 2
        textareaRef.current.selectionEnd = start + 2
      }, 0)
    }
  }

  const runCode = () => {
    if (exercise.type === 'js') {
      const result = runJavaScript(code)
      setOutput(result)
      const clean = code.trim().replace(/\s+/g, ' ')
      const sol = exercise.solution.trim().replace(/\s+/g, ' ')
      if (clean === sol || result.logs.length > 0) {
        setSuccess(true)
        if (onSuccess) setTimeout(() => onSuccess(), 1200)
      }
    } else {
      setOutput({ preview: code, error: null })
      const clean = code.trim().replace(/\s+/g, ' ')
      const sol = exercise.solution.trim().replace(/\s+/g, ' ')
      if (clean === sol) {
        setSuccess(true)
        if (onSuccess) setTimeout(() => onSuccess(), 1200)
      }
    }
  }

  const reset = () => {
    setCode(exercise.starterCode)
    setOutput(null)
    setSuccess(false)
    setShowHint(false)
    setShowSolution(false)
  }

  const useSolution = () => {
    setCode(exercise.solution)
    setShowSolution(false)
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
      {/* Instructions */}
      <div style={{
        background: '#f0f4ff',
        borderRadius: 12,
        padding: '14px 18px',
        borderLeft: '4px solid var(--primary)',
      }}>
        <span style={{ fontWeight: 700, color: 'var(--primary)' }}>📋 Exercice : </span>
        <span>{exercise.instructions}</span>
      </div>

      {/* Éditeur */}
      <div style={{
        background: '#1e1e2e',
        borderRadius: 14,
        overflow: 'hidden',
        boxShadow: '0 4px 20px rgba(0,0,0,0.2)',
      }}>
        <div style={{
          background: '#2a2a3e',
          padding: '10px 16px',
          display: 'flex',
          alignItems: 'center',
          gap: 8,
        }}>
          <div style={{ width: 12, height: 12, borderRadius: '50%', background: '#ff5f57' }} />
          <div style={{ width: 12, height: 12, borderRadius: '50%', background: '#ffbd2e' }} />
          <div style={{ width: 12, height: 12, borderRadius: '50%', background: '#28c840' }} />
          <span style={{ color: '#888', fontSize: '0.85rem', marginLeft: 8 }}>
            {exercise.type === 'js' ? '📄 script.js' :
             exercise.type === 'css' ? '🎨 style.css' : '🌐 index.html'}
          </span>
        </div>
        <textarea
          ref={textareaRef}
          value={code}
          onChange={e => { setCode(e.target.value); setSuccess(false) }}
          onKeyDown={handleTab}
          spellCheck={false}
          style={{
            width: '100%',
            minHeight: 180,
            background: '#1e1e2e',
            color: '#cdd6f4',
            border: 'none',
            padding: '16px 20px',
            fontFamily: "'Fira Code', 'Consolas', monospace",
            fontSize: '0.95rem',
            lineHeight: 1.7,
            resize: 'vertical',
            outline: 'none',
          }}
        />
      </div>

      {/* Boutons */}
      <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap' }}>
        <button
          onClick={runCode}
          style={{
            background: 'linear-gradient(135deg, var(--primary), var(--primary-dark))',
            color: 'white',
            border: 'none',
            borderRadius: 10,
            padding: '10px 22px',
            fontWeight: 700,
            fontSize: '0.95rem',
            display: 'flex', alignItems: 'center', gap: 8,
            transition: 'transform 0.15s',
          }}
          onMouseEnter={e => e.currentTarget.style.transform = 'scale(1.04)'}
          onMouseLeave={e => e.currentTarget.style.transform = 'scale(1)'}
        >
          ▶ Exécuter
        </button>
        <button
          onClick={() => setShowHint(!showHint)}
          style={{
            background: 'var(--accent2)',
            color: '#333',
            border: 'none',
            borderRadius: 10,
            padding: '10px 18px',
            fontWeight: 600,
            fontSize: '0.9rem',
          }}
        >
          💡 Indice
        </button>
        <button
          onClick={() => setShowSolution(!showSolution)}
          style={{
            background: 'var(--bg)',
            color: 'var(--text)',
            border: '2px solid var(--border)',
            borderRadius: 10,
            padding: '10px 18px',
            fontWeight: 600,
            fontSize: '0.9rem',
          }}
        >
          🔍 Solution
        </button>
        <button
          onClick={reset}
          style={{
            background: 'var(--bg)',
            color: 'var(--text-light)',
            border: '2px solid var(--border)',
            borderRadius: 10,
            padding: '10px 18px',
            fontSize: '0.9rem',
          }}
        >
          🔄 Réinitialiser
        </button>
      </div>

      {/* Indice */}
      {showHint && (
        <div style={{
          background: '#fffde7',
          border: '2px solid var(--accent2)',
          borderRadius: 12,
          padding: '12px 16px',
        }}>
          <strong>💡 Indice : </strong>{exercise.hint}
        </div>
      )}

      {/* Solution */}
      {showSolution && (
        <div style={{
          background: '#f5f5f5',
          border: '2px solid #ddd',
          borderRadius: 12,
          padding: 16,
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 10 }}>
            <strong>📋 Solution :</strong>
            <button
              onClick={useSolution}
              style={{
                background: 'var(--primary)',
                color: 'white',
                border: 'none',
                borderRadius: 8,
                padding: '4px 12px',
                fontSize: '0.85rem',
                cursor: 'pointer',
              }}
            >
              Utiliser
            </button>
          </div>
          <pre style={{
            background: '#1e1e2e',
            color: '#cdd6f4',
            borderRadius: 10,
            padding: '12px 16px',
            fontFamily: "'Fira Code', monospace",
            fontSize: '0.9rem',
            overflowX: 'auto',
            margin: 0,
          }}>
            {exercise.solution}
          </pre>
        </div>
      )}

      {/* Résultat */}
      {output && (
        <div style={{
          background: success ? '#f0fff4' : '#1e1e2e',
          border: `2px solid ${success ? 'var(--success)' : '#333'}`,
          borderRadius: 12,
          padding: 16,
          animation: 'fadeIn 0.3s ease',
        }}>
          {success && (
            <div style={{
              background: 'var(--success)',
              color: 'white',
              borderRadius: 10,
              padding: '10px 16px',
              marginBottom: 12,
              fontWeight: 700,
              fontSize: '1rem',
              display: 'flex', alignItems: 'center', gap: 8,
            }}>
              🎉 Bravo ! Excellent travail !
            </div>
          )}
          {exercise.type === 'js' ? (
            <>
              {output.error ? (
                <div style={{ color: '#ff6b6b', fontFamily: 'monospace', fontSize: '0.9rem' }}>
                  ❌ Erreur : {output.error}
                </div>
              ) : output.logs.length > 0 ? (
                <div>
                  <div style={{ color: '#888', fontSize: '0.8rem', marginBottom: 6 }}>Console :</div>
                  {output.logs.map((log, i) => (
                    <div key={i} style={{
                      color: '#a6e3a1',
                      fontFamily: 'monospace',
                      fontSize: '0.95rem',
                      padding: '2px 0',
                    }}>
                      {'>'} {log}
                    </div>
                  ))}
                </div>
              ) : (
                <div style={{ color: '#888', fontSize: '0.9rem' }}>
                  Aucune sortie console. Utilise console.log() pour voir un résultat.
                </div>
              )}
            </>
          ) : (
            <div>
              <div style={{ color: '#888', fontSize: '0.8rem', marginBottom: 8 }}>Aperçu :</div>
              <div style={{
                background: 'white',
                borderRadius: 8,
                padding: 16,
                fontSize: '1rem',
              }}
                dangerouslySetInnerHTML={{ __html: output.preview }}
              />
            </div>
          )}
        </div>
      )}
    </div>
  )
}
