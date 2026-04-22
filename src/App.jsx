import React, { useState } from 'react'
import Header from './components/Header'
import Dashboard from './components/Dashboard'
import LessonView from './components/LessonView'
import { useProgress } from './hooks/useProgress'
import './App.css'

export default function App() {
  const [page, setPage] = useState('home')
  const [activeLessonId, setActiveLessonId] = useState(null)
  const { progress, completeLesson, completeQuiz } = useProgress()

  const navigate = (target, id) => {
    setPage(target)
    if (id) setActiveLessonId(id)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const handleLessonComplete = (lessonId, xp, quizId, quizScore) => {
    completeLesson(lessonId, xp)
    if (quizId) completeQuiz(quizId, quizScore)
  }

  return (
    <div style={{ minHeight: '100vh', background: 'var(--bg)' }}>
      <Header currentPage={page} onNavigate={navigate} progress={progress} />
      <main>
        {page === 'home' && (
          <Dashboard progress={progress} onNavigate={navigate} />
        )}
        {page === 'lesson' && activeLessonId && (
          <LessonView
            lessonId={activeLessonId}
            progress={progress}
            onComplete={handleLessonComplete}
            onNavigate={navigate}
          />
        )}
      </main>
    </div>
  )
}
