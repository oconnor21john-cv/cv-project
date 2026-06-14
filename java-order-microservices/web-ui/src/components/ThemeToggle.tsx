import { useEffect, useState } from 'react'

function getInitialTheme(): 'dark' | 'light' {
  if (typeof window === 'undefined') return 'light'
  const stored = window.__themePreference
  if (stored === 'light' || stored === 'dark') return stored
  return 'light'
}

declare global {
  interface Window {
    __themePreference?: string
  }
}

export function ThemeToggle() {
  const [theme, setTheme] = useState<'dark' | 'light'>(getInitialTheme)

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
    window.__themePreference = theme
  }, [theme])

  function toggle() {
    setTheme((prev) => (prev === 'dark' ? 'light' : 'dark'))
  }

  return (
    <button
      className="btn-ghost btn-sm theme-toggle"
      onClick={toggle}
      aria-label={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
      title={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
    >
      {theme === 'dark' ? '☀' : '☾'}
    </button>
  )
}
