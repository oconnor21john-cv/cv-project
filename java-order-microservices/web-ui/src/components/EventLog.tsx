import { useEffect, useRef } from 'react'
import { useApp } from '../store/AppContext'

export function EventLog() {
  const { logs } = useApp()
  const endRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' })
  }, [logs])

  return (
    <aside className="card log">
      <header className="log-head">
        <span className="log-dot" />
        Event log
        <span className="log-count">{logs.length}</span>
      </header>
      <div className="log-body">
        {logs.length === 0 && <div className="log-empty">Waiting for activity…</div>}
        {logs.map((l) => (
          <div key={l.id} className={`log-line log-${l.level}`}>
            <span className="log-time">{l.t}</span>
            <span className="log-msg">{l.msg}</span>
          </div>
        ))}
        <div ref={endRef} />
      </div>
    </aside>
  )
}
