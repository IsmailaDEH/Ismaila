import { useState, useEffect } from 'react'

const STORAGE_KEY = 'codedebutant_progress'

const defaultProgress = {
  xp: 0,
  level: 1,
  completedLessons: [],
  completedQuizzes: [],
  badges: [],
  streak: 0,
  lastVisit: null,
}

export function useProgress() {
  const [progress, setProgress] = useState(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY)
      return saved ? { ...defaultProgress, ...JSON.parse(saved) } : defaultProgress
    } catch {
      return defaultProgress
    }
  })

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(progress))
  }, [progress])

  const completeLesson = (lessonId, xpGain = 50) => {
    setProgress(prev => {
      if (prev.completedLessons.includes(lessonId)) return prev
      const newXp = prev.xp + xpGain
      const newLevel = Math.floor(newXp / 200) + 1
      const newBadges = [...prev.badges]
      const completedCount = prev.completedLessons.length + 1
      if (completedCount === 1 && !prev.badges.includes('first_lesson')) newBadges.push('first_lesson')
      if (completedCount === 5 && !prev.badges.includes('five_lessons')) newBadges.push('five_lessons')
      if (completedCount === 10 && !prev.badges.includes('ten_lessons')) newBadges.push('ten_lessons')
      return {
        ...prev,
        xp: newXp,
        level: newLevel,
        completedLessons: [...prev.completedLessons, lessonId],
        badges: newBadges,
      }
    })
  }

  const completeQuiz = (quizId, score, xpGain = 30) => {
    setProgress(prev => {
      if (prev.completedQuizzes.find(q => q.id === quizId)) return prev
      const newXp = prev.xp + (score === 100 ? xpGain * 2 : xpGain)
      const newBadges = [...prev.badges]
      if (score === 100 && !prev.badges.includes('perfect_quiz')) newBadges.push('perfect_quiz')
      return {
        ...prev,
        xp: newXp,
        level: Math.floor(newXp / 200) + 1,
        completedQuizzes: [...prev.completedQuizzes, { id: quizId, score }],
        badges: newBadges,
      }
    })
  }

  const resetProgress = () => {
    setProgress(defaultProgress)
  }

  const xpForNextLevel = (level) => level * 200
  const xpProgress = (progress.xp % 200) / 200 * 100

  return { progress, completeLesson, completeQuiz, resetProgress, xpProgress }
}
