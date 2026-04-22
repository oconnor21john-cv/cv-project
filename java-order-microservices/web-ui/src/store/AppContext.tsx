import { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState, type ReactNode } from 'react'
import { apiBaseUrl, decodeJwt, getJson, shortOrigin } from '../lib/api'
import type { OrderResponse } from '../lib/api'

export type LogLevel = 'info' | 'success' | 'error' | 'system'
export type LogEntry = { id: number; t: string; level: LogLevel; msg: string }
export type Stage = 'idle' | 'auth' | 'create' | 'confirm' | 'cancel'

type AppContextValue = {
  baseUrl: string
  token: string
  username: string | null
  isAdmin: boolean
  setToken: (t: string) => void
  clearToken: () => void
  order: OrderResponse | null
  setOrder: (o: OrderResponse | null) => void
  busy: Stage
  setBusy: (s: Stage) => void
  activeStage: Stage
  setActiveStage: (s: Stage) => void
  apiHealthy: boolean | null
  logs: LogEntry[]
  addLog: (level: LogLevel, msg: string) => void
  clearLogs: () => void
}

const AppContext = createContext<AppContextValue | null>(null)

const TOKEN_STORAGE_KEY = 'order-ui.token'

export function AppProvider({ children }: { children: ReactNode }) {
  const baseUrl = useMemo(() => apiBaseUrl(), [])
  const [token, setTokenState] = useState<string>(() => localStorage.getItem(TOKEN_STORAGE_KEY) || '')
  const [order, setOrder] = useState<OrderResponse | null>(null)
  const [busy, setBusy] = useState<Stage>('idle')
  const [activeStage, setActiveStage] = useState<Stage>('idle')
  const [apiHealthy, setApiHealthy] = useState<boolean | null>(null)
  const [logs, setLogs] = useState<LogEntry[]>([])
  const logIdRef = useRef(0)

  const jwtPayload = useMemo(() => (token ? decodeJwt(token) : null), [token])
  const username = jwtPayload?.sub ?? null
  const isAdmin = jwtPayload?.roles?.includes('ADMIN') ?? false

  const setToken = useCallback((t: string) => {
    setTokenState(t)
    if (t) localStorage.setItem(TOKEN_STORAGE_KEY, t)
    else localStorage.removeItem(TOKEN_STORAGE_KEY)
  }, [])

  const clearToken = useCallback(() => {
    setTokenState('')
    localStorage.removeItem(TOKEN_STORAGE_KEY)
    setOrder(null)
    setActiveStage('idle')
  }, [])

  const addLog = useCallback((level: LogLevel, msg: string) => {
    logIdRef.current += 1
    const now = new Date()
    const t = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}`
    const entry: LogEntry = { id: logIdRef.current, t, level, msg }
    setLogs((prev) => [...prev.slice(-80), entry])
  }, [])

  const clearLogs = useCallback(() => setLogs([]), [])

  useEffect(() => {
    let cancelled = false
    addLog('system', `Connecting to ${shortOrigin(baseUrl)}`)
    getJson<{ status: string }>(`${baseUrl}/actuator/health`)
      .then((r) => {
        if (cancelled) return
        const up = r.status === 'UP'
        setApiHealthy(up)
        addLog(up ? 'success' : 'error', `order-service health: ${r.status}`)
      })
      .catch((e) => {
        if (cancelled) return
        setApiHealthy(false)
        addLog('error', `health check failed: ${e instanceof Error ? e.message : String(e)}`)
      })
    return () => {
      cancelled = true
    }
  }, [baseUrl, addLog])

  const value: AppContextValue = {
    baseUrl,
    token,
    username,
    isAdmin,
    setToken,
    clearToken,
    order,
    setOrder,
    busy,
    setBusy,
    activeStage,
    setActiveStage,
    apiHealthy,
    logs,
    addLog,
    clearLogs,
  }

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>
}

export function useApp() {
  const ctx = useContext(AppContext)
  if (!ctx) throw new Error('useApp must be used inside AppProvider')
  return ctx
}
