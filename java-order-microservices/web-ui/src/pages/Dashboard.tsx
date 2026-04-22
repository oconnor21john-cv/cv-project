import { useEffect, useState } from 'react'
import { Navigate, useLocation } from 'react-router-dom'
import { EventLog } from '../components/EventLog'
import { toast } from '../components/Toast'
import { getJson, postJson, type OrderResponse } from '../lib/api'
import { useApp, type Stage } from '../store/AppContext'

function StatusPill({ status }: { status: string }) {
  return <span className={`status-pill s-${status}`}>{status}</span>
}

const CATALOG: Record<string, { name: string; price: number }> = {
  'SKU-APPLE':  { name: 'Apple',  price: 0.50 },
  'SKU-BANANA': { name: 'Banana', price: 0.30 },
  'SKU-COFFEE': { name: 'Coffee', price: 4.99 },
}

export function Dashboard() {
  const location = useLocation()
  const {
    baseUrl,
    token,
    order,
    setOrder,
    busy,
    setBusy,
    setActiveStage,
    addLog,
  } = useApp()

  const [sku, setSku] = useState('SKU-APPLE')
  const [quantity, setQuantity] = useState(2)
  const [error, setError] = useState('')

  // Poll order status every 5 seconds when an active order exists
  useEffect(() => {
    if (!order || !token) return
    const terminal = ['CANCELLED', 'STOCK_FAILED', 'PAYMENT_FAILED']
    if (terminal.includes(order.status)) return

    const interval = setInterval(async () => {
      try {
        const fetched = await getJson<OrderResponse>(`${baseUrl}/orders/${order.id}`, token)
        if (fetched.status !== order.status) {
          setOrder(fetched)
          addLog('info', `Status updated → ${fetched.status}`)
          toast('info', `Order status: ${fetched.status}`)
        }
      } catch {
        // silently ignore polling errors
      }
    }, 5000)

    return () => clearInterval(interval)
  }, [order?.id, order?.status, token, baseUrl, setOrder, addLog])

  const product = CATALOG[sku]
  const unitPrice = product.price

  if (!token) {
    return <Navigate to="/login" state={{ from: location.pathname }} replace />
  }

  function wrap<T>(name: Stage, fn: () => Promise<T>, startMsg: string) {
    return async () => {
      setError('')
      setBusy(name)
      setActiveStage(name)
      addLog('info', startMsg)
      try {
        await fn()
        toast('success', `${name === 'create' ? 'Order created' : name === 'confirm' ? 'Order confirmed' : name === 'cancel' ? 'Order cancelled' : 'Done'}`)
      } catch (e) {
        const msg = e instanceof Error ? e.message : String(e)
        setError(msg)
        addLog('error', msg)
        toast('error', msg)
      } finally {
        setBusy('idle')
        setActiveStage('idle')
      }
    }
  }

  const onCreateOrder = wrap(
    'create',
    async () => {
      const created = await postJson<OrderResponse>(
        `${baseUrl}/orders`,
        { items: [{ sku, quantity }] },
        token,
      )
      setOrder(created)
      addLog('success', `Order ${created.id.slice(0, 8)}… created · £${created.totalAmount.toFixed(2)} · ${created.status}`)
    },
    `POST /orders — ${quantity} × ${sku} @ £${unitPrice.toFixed(2)}`,
  )

  const onRefresh = wrap(
    'idle',
    async () => {
      if (!order) return
      const fetched = await getJson<OrderResponse>(`${baseUrl}/orders/${order.id}`, token)
      setOrder(fetched)
      addLog('info', `GET /orders/${fetched.id.slice(0, 8)}… → ${fetched.status}`)
    },
    `GET /orders/${order?.id.slice(0, 8) ?? ''}… — refreshing`,
  )

  const onConfirm = wrap(
    'confirm',
    async () => {
      if (!order) return
      const confirmed = await postJson<OrderResponse>(`${baseUrl}/orders/${order.id}/confirm`, {}, token)
      setOrder(confirmed)
      addLog('success', `inventory-service reserved stock · payment-service accepted · ${confirmed.status}`)
    },
    'POST /orders/{id}/confirm — reserving stock + charging',
  )

  const onCancel = wrap(
    'cancel',
    async () => {
      if (!order) return
      const cancelled = await postJson<OrderResponse>(`${baseUrl}/orders/${order.id}/cancel`, {}, token)
      setOrder(cancelled)
      addLog('success', `Order ${cancelled.status.toLowerCase()}`)
    },
    'POST /orders/{id}/cancel — releasing reservation',
  )

  let stageIndex = 1
  if (order) stageIndex = 2
  if (order?.status === 'CONFIRMED') stageIndex = 3
  const cancelled = order?.status === 'CANCELLED'

  return (
    <>
      <section className="page-head">
        <div className="page-head-eyebrow">Live workflow</div>
        <h1 className="page-head-h">Place an order</h1>
        <p className="page-head-sub">
          Each click hits the real Spring Boot service on AWS. Watch the event log on the right — every step narrates itself.
        </p>
      </section>

      <section className="pipeline">
        {[
          { n: 1, label: 'Authenticate' },
          { n: 2, label: 'Create order' },
          { n: 3, label: 'Confirm' },
          { n: 4, label: cancelled ? 'Cancelled' : 'Done' },
        ].map((s, i) => {
          const done = !cancelled && i < stageIndex
          const active = !cancelled && i === stageIndex
          const isCancelStep = cancelled && i === 3
          return (
            <div
              key={s.n}
              className={`step ${done ? 'step-done' : ''} ${active ? 'step-active' : ''} ${isCancelStep ? 'step-cancelled' : ''}`}
            >
              <div className="step-num">{done ? '✓' : isCancelStep ? '×' : s.n}</div>
              <div className="step-label">{s.label}</div>
            </div>
          )
        })}
      </section>

      <div className="grid">
        <div className="col">
          <section className={`card panel ${order ? 'panel-done' : ''}`}>
            <header className="panel-head">
              <div className="panel-num">1</div>
              <h2>Create order</h2>
            </header>
            <div className="fields fields-2">
              <label>
                <span>Product</span>
                <select value={sku} onChange={(e) => setSku(e.target.value)} disabled={busy !== 'idle'}>
                  {Object.entries(CATALOG).map(([code, p]) => (
                    <option key={code} value={code}>
                      {p.name} — £{p.price.toFixed(2)}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                <span>Quantity</span>
                <input
                  type="number"
                  min={1}
                  value={quantity}
                  onChange={(e) => setQuantity(Number(e.target.value))}
                  disabled={busy !== 'idle'}
                />
              </label>
            </div>
            <div className="row">
              <button className="btn-primary" onClick={onCreateOrder} disabled={busy !== 'idle'}>
                {busy === 'create' ? <span className="spin" /> : null}
                Create order
              </button>
              <button className="btn-ghost" onClick={onRefresh} disabled={!order || busy !== 'idle'}>
                Refresh
              </button>
              <div className="total-preview">
                Preview: <strong>£{(quantity * unitPrice).toFixed(2)}</strong>
              </div>
            </div>

            {order && (
              <div className="order-card">
                <div className="order-card-head">
                  <span className="order-card-title">Order</span>
                  <StatusPill status={order.status} />
                </div>
                <div className="order-card-grid">
                  <div>
                    <div className="kv-key">ID</div>
                    <div className="kv-val mono">{order.id}</div>
                  </div>
                  <div>
                    <div className="kv-key">Total</div>
                    <div className="kv-val big">£{order.totalAmount.toFixed(2)}</div>
                  </div>
                </div>
                {order.items && order.items.length > 0 && (
                  <div className="order-items">
                    <div className="order-items-head">Line items</div>
                    <table className="order-items-table">
                      <thead>
                        <tr>
                          <th>Product</th>
                          <th>Qty</th>
                          <th>Unit price</th>
                          <th>Subtotal</th>
                        </tr>
                      </thead>
                      <tbody>
                        {order.items.map((item, idx) => (
                          <tr key={idx}>
                            <td>{CATALOG[item.sku]?.name ?? item.sku}</td>
                            <td className="mono">{item.quantity}</td>
                            <td className="mono">£{item.unitPrice.toFixed(2)}</td>
                            <td className="mono">£{(item.quantity * item.unitPrice).toFixed(2)}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            )}
          </section>

          <section className="card panel panel-split">
            <div>
              <header className="panel-head">
                <div className="panel-num">2</div>
                <h2>Confirm</h2>
              </header>
              <p className="panel-desc">
                Reserves stock in <code>inventory-service</code> then creates payment in <code>payment-service</code>.
              </p>
              <button
                className="btn-primary"
                onClick={onConfirm}
                disabled={!order || order.status !== 'PLACED' || busy !== 'idle'}
              >
                {busy === 'confirm' ? <span className="spin" /> : null}
                Confirm order
              </button>
            </div>
            <div>
              <header className="panel-head">
                <div className="panel-num">3</div>
                <h2>Cancel</h2>
              </header>
              <p className="panel-desc">
                Cancels the order. If already confirmed, reserved inventory is released.
              </p>
              <button
                className="btn-danger"
                onClick={onCancel}
                disabled={!order || order.status === 'CANCELLED' || busy !== 'idle'}
              >
                {busy === 'cancel' ? <span className="spin" /> : null}
                Cancel order
              </button>
            </div>
          </section>

          {error && <div className="error-box">{error}</div>}
        </div>

        <EventLog />
      </div>
    </>
  )
}
