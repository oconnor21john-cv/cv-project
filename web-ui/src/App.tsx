import { useMemo, useState } from 'react'
import './App.css'

type TokenResponse = { accessToken: string; tokenType: string }
type OrderResponse = { id: string; status: string; totalAmount: number }

function apiBaseUrl() {
  return import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8081'
}

async function postJson<T>(
  url: string,
  body: unknown,
  token?: string,
): Promise<T> {
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
    throw new Error(`${res.status} ${res.statusText}${text ? ` — ${text}` : ''}`)
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
    throw new Error(`${res.status} ${res.statusText}${text ? ` — ${text}` : ''}`)
  }

  return (await res.json()) as T
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

  const baseUrl = useMemo(() => apiBaseUrl(), [])

  async function onLogin() {
    setError('')
    setStatus('Logging in…')
    try {
      const resp = await postJson<TokenResponse>(`${baseUrl}/auth/token`, {
        username,
        password,
      })
      setToken(resp.accessToken)
      setStatus('Logged in.')
    } catch (e) {
      setStatus('')
      setError(e instanceof Error ? e.message : String(e))
    }
  }

  async function onCreateOrder() {
    setError('')
    setStatus('Creating order…')
    try {
      const created = await postJson<OrderResponse>(
        `${baseUrl}/orders`,
        { items: [{ sku, quantity, unitPrice }] },
        token,
      )
      setOrder(created)
      setStatus(`Order created: ${created.id}`)
    } catch (e) {
      setStatus('')
      setError(e instanceof Error ? e.message : String(e))
    }
  }

  async function onGetOrder() {
    if (!order) return
    setError('')
    setStatus('Refreshing order…')
    try {
      const fetched = await getJson<OrderResponse>(
        `${baseUrl}/orders/${order.id}`,
        token,
      )
      setOrder(fetched)
      setStatus('Order refreshed.')
    } catch (e) {
      setStatus('')
      setError(e instanceof Error ? e.message : String(e))
    }
  }

  async function onConfirmOrder() {
    if (!order) return
    setError('')
    setStatus('Confirming (reserve stock → pay)…')
    try {
      const confirmed = await postJson<OrderResponse>(
        `${baseUrl}/orders/${order.id}/confirm`,
        {},
        token,
      )
      setOrder(confirmed)
      setStatus(`Order status: ${confirmed.status}`)
    } catch (e) {
      setStatus('')
      setError(e instanceof Error ? e.message : String(e))
    }
  }

  async function onCancelOrder() {
    if (!order) return
    setError('')
    setStatus('Cancelling order (releasing inventory)…')
    try {
      const cancelled = await postJson<OrderResponse>(
        `${baseUrl}/orders/${order.id}/cancel`,
        {},
        token,
      )
      setOrder(cancelled)
      setStatus(`Order status: ${cancelled.status}`)
    } catch (e) {
      setStatus('')
      setError(e instanceof Error ? e.message : String(e))
    }
  }

  return (
    <>
      <div style={{ maxWidth: 920, margin: '0 auto', padding: 24 }}>
        <h1 style={{ marginBottom: 8 }}>Order Microservices UI</h1>
        <p style={{ opacity: 0.8, marginTop: 0 }}>
          API: <code>{baseUrl}</code>
        </p>

        <div className="card" style={{ textAlign: 'left' }}>
          <h2 style={{ marginTop: 0 }}>1) Login (JWT)</h2>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
            <label>
              Username
              <input
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                style={{ width: '100%' }}
              />
            </label>
            <label>
              Password
              <input
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                type="password"
                style={{ width: '100%' }}
              />
            </label>
          </div>
          <div style={{ marginTop: 12, display: 'flex', gap: 12, alignItems: 'center' }}>
            <button onClick={onLogin}>Get token</button>
            <span style={{ opacity: 0.8 }}>
              Token: {token ? `${token.slice(0, 18)}…` : '(none)'}
            </span>
          </div>
          <p style={{ marginBottom: 0, opacity: 0.75 }}>
            Demo accounts: <code>customer/password</code> or <code>admin/password</code>
          </p>
        </div>

        <div className="card" style={{ textAlign: 'left', marginTop: 16 }}>
          <h2 style={{ marginTop: 0 }}>2) Create an order</h2>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 12 }}>
            <label>
              SKU
              <select value={sku} onChange={(e) => setSku(e.target.value)} style={{ width: '100%' }}>
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
                style={{ width: '100%' }}
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
                style={{ width: '100%' }}
              />
            </label>
          </div>
          <div style={{ marginTop: 12, display: 'flex', gap: 12 }}>
            <button onClick={onCreateOrder} disabled={!token}>
              Create order
            </button>
            <button onClick={onGetOrder} disabled={!token || !order}>
              Refresh order
            </button>
          </div>
          {order && (
            <div style={{ marginTop: 12, padding: 12, border: '1px solid #2a2a2a', borderRadius: 8 }}>
              <div>
                <strong>Order ID:</strong> <code>{order.id}</code>
              </div>
              <div>
                <strong>Status:</strong> {order.status}
              </div>
              <div>
                <strong>Total:</strong> {order.totalAmount}
              </div>
            </div>
          )}
        </div>

        <div className="card" style={{ textAlign: 'left', marginTop: 16 }}>
          <h2 style={{ marginTop: 0 }}>3) Confirm order</h2>
          <p style={{ marginTop: 0, opacity: 0.8 }}>
            Runs the flow: reserve stock in inventory-service → create payment in payment-service.
          </p>
          <button onClick={onConfirmOrder} disabled={!token || !order}>
            Confirm
          </button>
        </div>

        <div className="card" style={{ textAlign: 'left', marginTop: 16 }}>
          <h2 style={{ marginTop: 0 }}>4) Cancel order</h2>
          <p style={{ marginTop: 0, opacity: 0.8 }}>
            Cancels the order. If CONFIRMED, releases reserved inventory as compensation.
          </p>
          <button
            onClick={onCancelOrder}
            disabled={!token || !order}
            style={{ background: '#8b2500' }}
          >
            Cancel order
          </button>
        </div>

        {!!status && (
          <p style={{ marginTop: 16, opacity: 0.9 }}>
            <strong>Status:</strong> {status}
          </p>
        )}
        {!!error && (
          <pre style={{ marginTop: 16, padding: 12, background: '#2b1b1b', border: '1px solid #6b2a2a', borderRadius: 8, overflowX: 'auto' }}>
{error}
          </pre>
        )}
      </div>
    </>
  )
}

export default App
