import { useMemo, useState } from 'react'
import './App.css'

type TokenResponse = { accessToken: string; tokenType: string }
type OrderResponse = { id: string; status: string; totalAmount: number }

function apiBaseUrl() {
  return import.meta.env.VITE_API_BASE_URL || 'http://localhost:8081'
}

async function postJson<T>(url: string, body: unknown, token?: string): Promise<T> {
  const res = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: JSON.stringify(body),
  })
  if (!res.ok) {
    const text = await res.text().catch(() => '')
    throw new Error(`${res.status} ${res.statusText}${text ? `\n${text}` : ''}`)
  }
  return (await res.json()) as T
}

async function getJson<T>(url: string, token: string): Promise<T> {
  const res = await fetch(url, {
    method: 'GET',
    headers: { Authorization: `Bearer ${token}` },
  })
  if (!res.ok) {
    const text = await res.text().catch(() => '')
    throw new Error(`${res.status} ${res.statusText}${text ? `\n${text}` : ''}`)
  }
  return (await res.json()) as T
}

function StatusBadge({ status }: { status: string }) {
  return <span className={`status-badge ${status}`}>{status}</span>
}

function App() {
  const [username, setUsername] = useState('customer')
  const [password, setPassword] = useState('password')
  const [token, setToken] = useState<string>('')

  const [sku, setSku] = useState('SKU-APPLE')
  const [quantity, setQuantity] = useState(2)
  const [unitPrice, setUnitPrice] = useState(0.5)

  const [order, setOrder] = useState<OrderResponse | null>(null)
  const [status, setStatus] = useState<string>('')
  const [error, setError] = useState<string>('')
  const [loading, setLoading] = useState(false)

  const baseUrl = useMemo(() => apiBaseUrl(), [])

  function wrap<T>(fn: () => Promise<T>) {
    return async () => {
      setError('')
      setLoading(true)
      try {
        await fn()
      } catch (e) {
        setStatus('')
        setError(e instanceof Error ? e.message : String(e))
      } finally {
        setLoading(false)
      }
    }
  }

  const onLogin = wrap(async () => {
    setStatus('Logging in…')
    const resp = await postJson<TokenResponse>(`${baseUrl}/auth/token`, { username, password })
    setToken(resp.accessToken)
    setStatus('Logged in.')
  })

  const onCreateOrder = wrap(async () => {
    setStatus('Creating order…')
    const created = await postJson<OrderResponse>(
      `${baseUrl}/orders`,
      { items: [{ sku, quantity, unitPrice }] },
      token,
    )
    setOrder(created)
    setStatus(`Order created.`)
  })

  const onGetOrder = wrap(async () => {
    if (!order) return
    setStatus('Refreshing…')
    const fetched = await getJson<OrderResponse>(`${baseUrl}/orders/${order.id}`, token)
    setOrder(fetched)
    setStatus('Order refreshed.')
  })

  const onConfirmOrder = wrap(async () => {
    if (!order) return
    setStatus('Confirming order…')
    const confirmed = await postJson<OrderResponse>(`${baseUrl}/orders/${order.id}/confirm`, {}, token)
    setOrder(confirmed)
    setStatus(`Order ${confirmed.status}.`)
  })

  const onCancelOrder = wrap(async () => {
    if (!order) return
    setStatus('Cancelling order…')
    const cancelled = await postJson<OrderResponse>(`${baseUrl}/orders/${order.id}/cancel`, {}, token)
    setOrder(cancelled)
    setStatus(`Order ${cancelled.status}.`)
  })

  return (
    <>
      <div className="app-header">
        <h1>Order Microservices</h1>
        <span className="api-url">{baseUrl}</span>
      </div>

      {/* Step 1 — Login */}
      <div className="card">
        <div className="card-title">
          <span className="step-num">1</span>
          <h2>Login</h2>
          <div className={`token-badge ${token ? 'active' : ''}`} style={{ marginLeft: 'auto' }}>
            <span className="dot" />
            {token ? `${token.slice(0, 16)}…` : 'no token'}
          </div>
        </div>
        <div className="field-row field-row-2">
          <label>
            Username
            <input value={username} onChange={(e) => setUsername(e.target.value)} />
          </label>
          <label>
            Password
            <input value={password} onChange={(e) => setPassword(e.target.value)} type="password" />
          </label>
        </div>
        <div className="btn-row">
          <button className="primary" onClick={onLogin} disabled={loading}>
            Get token
          </button>
        </div>
        <p className="hint">Demo: <code>customer / password</code> or <code>admin / password</code></p>
      </div>

      {/* Step 2 — Create order */}
      <div className="card">
        <div className="card-title">
          <span className="step-num">2</span>
          <h2>Create order</h2>
        </div>
        <div className="field-row field-row-3">
          <label>
            SKU
            <select value={sku} onChange={(e) => setSku(e.target.value)}>
              <option value="SKU-APPLE">SKU-APPLE</option>
              <option value="SKU-BANANA">SKU-BANANA</option>
              <option value="SKU-COFFEE">SKU-COFFEE</option>
            </select>
          </label>
          <label>
            Quantity
            <input
              value={quantity}
              onChange={(e) => setQuantity(Number(e.target.value))}
              type="number"
              min={1}
            />
          </label>
          <label>
            Unit price
            <input
              value={unitPrice}
              onChange={(e) => setUnitPrice(Number(e.target.value))}
              type="number"
              min={0}
              step={0.01}
            />
          </label>
        </div>
        <div className="btn-row">
          <button onClick={onCreateOrder} disabled={!token || loading}>Create order</button>
          <button onClick={onGetOrder} disabled={!token || !order || loading}>Refresh</button>
        </div>

        {order && (
          <div className="order-result">
            <div className="order-result-row">
              <span className="label">ID</span>
              <span className="val">{order.id}</span>
            </div>
            <div className="order-result-row">
              <span className="label">Status</span>
              <span className="val"><StatusBadge status={order.status} /></span>
            </div>
            <div className="order-result-row">
              <span className="label">Total</span>
              <span className="val">£{order.totalAmount.toFixed(2)}</span>
            </div>
          </div>
        )}
      </div>

      {/* Step 3 — Confirm */}
      <div className="card">
        <div className="card-title">
          <span className="step-num">3</span>
          <h2>Confirm order</h2>
        </div>
        <p className="card-desc">
          Reserves stock in inventory-service then creates payment in payment-service.
        </p>
        <div className="btn-row">
          <button className="primary" onClick={onConfirmOrder} disabled={!token || !order || loading}>
            Confirm
          </button>
        </div>
      </div>

      {/* Step 4 — Cancel */}
      <div className="card">
        <div className="card-title">
          <span className="step-num">4</span>
          <h2>Cancel order</h2>
        </div>
        <p className="card-desc">
          Cancels the order. If already confirmed, releases the reserved inventory.
        </p>
        <div className="btn-row">
          <button className="danger" onClick={onCancelOrder} disabled={!token || !order || loading}>
            Cancel order
          </button>
        </div>
      </div>

      {!!status && !error && (
        <div className="status-bar">{status}</div>
      )}
      {!!error && (
        <div className="error-box">{error}</div>
      )}
    </>
  )
}

export default App
