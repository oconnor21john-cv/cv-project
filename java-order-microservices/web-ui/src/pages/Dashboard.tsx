import { useEffect, useState } from 'react'
import { Navigate, useLocation } from 'react-router-dom'
import { EventLog } from '../components/EventLog'
import { ServiceFlow } from '../components/ServiceFlow'
import { toast } from '../components/Toast'
import { deleteRequest, getJson, postJson, type OrderResponse } from '../lib/api'
import { useApp, type Stage } from '../store/AppContext'

function StatusPill({ status }: { status: string }) {
  return <span className={`status-pill s-${status}`}>{status}</span>
}

const CATALOG: Record<string, { name: string; price: number }> = {
  'SKU-APPLE':  { name: 'Apple',  price: 0.50 },
  'SKU-BANANA': { name: 'Banana', price: 0.30 },
  'SKU-COFFEE': { name: 'Coffee', price: 4.99 },
}

function formatDate(iso: string) {
  try {
    return new Date(iso).toLocaleString('en-GB', {
      day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit',
    })
  } catch { return iso }
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
  const [history, setHistory] = useState<OrderResponse[]>([])
  const [historyLoading, setHistoryLoading] = useState(false)
  const [historyVersion, setHistoryVersion] = useState(0)

  function refreshHistory() {
    setHistoryVersion((v) => v + 1)
  }

  // Fetch order history on mount and whenever historyVersion bumps
  useEffect(() => {
    if (!token) return
    let cancelled = false
    setHistoryLoading(true)
    getJson<OrderResponse[]>(`${baseUrl}/orders`, token)
      .then((orders) => { if (!cancelled) setHistory(orders) })
      .catch((e) => { if (!cancelled) console.warn('Failed to load order history:', e) })
      .finally(() => { if (!cancelled) setHistoryLoading(false) })
    return () => { cancelled = true }
  }, [token, baseUrl, historyVersion])

  // Poll order status every 5 seconds when an active order exists
  useEffect(() => {
    if (!order || !token) return
    const terminal = ['CANCELLED', 'STOCK_FAILED', 'PAYMENT_FAILED', 'CONFIRMED']
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
      refreshHistory()
    },
    `POST /orders — ${quantity} × ${sku} @ £${unitPrice.toFixed(2)}`,
  )

  const onConfirm = wrap(
    'confirm',
    async () => {
      if (!order) return
      const confirmed = await postJson<OrderResponse>(`${baseUrl}/orders/${order.id}/confirm`, {}, token)
      setOrder(confirmed)
      addLog('success', `inventory-service reserved stock · payment-service accepted · ${confirmed.status}`)
      refreshHistory()
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
      refreshHistory()
    },
    'POST /orders/{id}/cancel — releasing reservation',
  )

  function onNewOrder() {
    setOrder(null)
    setError('')
  }

  async function onClearHistory() {
    try {
      await deleteRequest(`${baseUrl}/orders`, token)
      setOrder(null)
      setHistory([])
      addLog('info', 'Order history cleared')
      toast('success', 'History cleared')
    } catch (e) {
      const msg = e instanceof Error ? e.message : String(e)
      toast('error', msg)
    }
  }

  const isTerminal = order && ['CONFIRMED', 'CANCELLED', 'STOCK_FAILED', 'PAYMENT_FAILED'].includes(order.status)
  const isSuccess = order?.status === 'CONFIRMED'
  const isFailed = order && ['CANCELLED', 'STOCK_FAILED', 'PAYMENT_FAILED'].includes(order.status)

  let stageIndex = 1
  if (order) stageIndex = 2
  if (order?.status === 'CONFIRMED') stageIndex = 3
  const cancelled = order?.status === 'CANCELLED'

  return (
    <>
      <section className="page-head">
        <div className="page-head-eyebrow">Dashboard</div>
        <h1 className="page-head-h">Place an order</h1>
        <p className="page-head-sub">
          Orders are sent to order-service on ECS. Confirm triggers calls to inventory-service and payment-service. Events are logged on the right.
        </p>
      </section>

      <section className="pipeline">
        {[
          { n: 1, label: 'Authenticate' },
          { n: 2, label: 'Create order' },
          { n: 3, label: 'Confirm' },
          { n: 4, label: cancelled ? 'Cancelled' : isFailed ? 'Failed' : 'Done' },
        ].map((s, i) => {
          const done = !cancelled && !isFailed && i < stageIndex
          const active = !cancelled && !isFailed && i === stageIndex
          const isCancelStep = (cancelled || isFailed) && i === 3
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

      <ServiceFlow />

      <div className="grid">
        <div className="col">
          {/* ── Completion card (shown when order reaches a terminal state) ── */}
          {isTerminal && (
            <section className={`card completion-card ${isSuccess ? 'completion-success' : 'completion-failed'}`}>
              <div className="completion-icon">{isSuccess ? '✓' : '×'}</div>
              <h2 className="completion-title">
                {isSuccess ? 'Order confirmed' : order.status === 'CANCELLED' ? 'Order cancelled' : order.status === 'STOCK_FAILED' ? 'Out of stock' : 'Payment failed'}
              </h2>
              <p className="completion-desc">
                {isSuccess
                  ? 'Stock was reserved in inventory-service and payment was processed by payment-service.'
                  : order.status === 'CANCELLED'
                    ? 'The order was cancelled. Any reserved inventory has been released.'
                    : order.status === 'STOCK_FAILED'
                      ? 'inventory-service could not reserve the requested items.'
                      : 'payment-service declined the transaction. Reserved stock has been released.'}
              </p>
              <div className="completion-summary">
                <div className="completion-row">
                  <span className="completion-label">Order</span>
                  <span className="mono">{order.id.slice(0, 8)}…</span>
                </div>
                <div className="completion-row">
                  <span className="completion-label">Total</span>
                  <span className="mono">£{order.totalAmount.toFixed(2)}</span>
                </div>
                <div className="completion-row">
                  <span className="completion-label">Items</span>
                  <span>{order.items.map(i => `${CATALOG[i.sku]?.name ?? i.sku} ×${i.quantity}`).join(', ')}</span>
                </div>
                <div className="completion-row">
                  <span className="completion-label">Status</span>
                  <StatusPill status={order.status} />
                </div>
              </div>
              <button className="btn-primary" onClick={onNewOrder}>
                Place another order
              </button>
            </section>
          )}

          {/* ── Create order panel ── */}
          {!isTerminal && (
            <>
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
            </>
          )}

          {error && <div className="error-box">{error}</div>}

          {/* ── Order history ── */}
          <section className="card">
            <div className="history-head">
              <div className="card-label">Order history</div>
              {history.length > 0 && (
                <button className="btn-ghost btn-sm" onClick={onClearHistory}>
                  Clear history
                </button>
              )}
            </div>
            {historyLoading && <p className="loading-msg">Loading orders…</p>}
            {!historyLoading && history.length === 0 && (
              <p className="empty-msg">No orders yet. Create one above to get started.</p>
            )}
            {!historyLoading && history.length > 0 && (
              <div className="orders-table-wrap">
                <table className="orders-table">
                  <thead>
                    <tr>
                      <th>Order ID</th>
                      <th>Items</th>
                      <th>Total</th>
                      <th>Status</th>
                      <th>Date</th>
                    </tr>
                  </thead>
                  <tbody>
                    {history.map((o) => (
                      <tr key={o.id} className={order?.id === o.id ? 'history-active-row' : ''}>
                        <td className="mono">{o.id.slice(0, 8)}…</td>
                        <td>{o.items.map(i => `${CATALOG[i.sku]?.name ?? i.sku} ×${i.quantity}`).join(', ')}</td>
                        <td className="mono">£{o.totalAmount.toFixed(2)}</td>
                        <td><StatusPill status={o.status} /></td>
                        <td className="text-dim">{formatDate(o.createdAt)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </section>
        </div>

        <EventLog />
      </div>
    </>
  )
}
