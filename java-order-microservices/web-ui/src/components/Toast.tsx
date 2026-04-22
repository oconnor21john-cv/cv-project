import { useEffect, useState } from 'react'

export type ToastLevel = 'success' | 'error' | 'info'

type ToastItem = { id: number; level: ToastLevel; message: string }

let nextId = 0
let externalPush: ((t: ToastItem) => void) | null = null

export function toast(level: ToastLevel, message: string) {
  externalPush?.({ id: ++nextId, level, message })
}

export function ToastContainer() {
  const [items, setItems] = useState<ToastItem[]>([])

  useEffect(() => {
    externalPush = (t) => setItems((prev) => [...prev, t])
    return () => { externalPush = null }
  }, [])

  function dismiss(id: number) {
    setItems((prev) => prev.filter((t) => t.id !== id))
  }

  return (
    <div className="toast-container">
      {items.map((t) => (
        <ToastCard key={t.id} item={t} onDone={() => dismiss(t.id)} />
      ))}
    </div>
  )
}

function ToastCard({ item, onDone }: { item: ToastItem; onDone: () => void }) {
  useEffect(() => {
    const timer = setTimeout(onDone, 4000)
    return () => clearTimeout(timer)
  }, [onDone])

  return (
    <div className={`toast toast-${item.level}`} onClick={onDone}>
      <span className="toast-icon">
        {item.level === 'success' ? '✓' : item.level === 'error' ? '✕' : 'ℹ'}
      </span>
      <span className="toast-msg">{item.message}</span>
    </div>
  )
}
