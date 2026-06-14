import React, { useEffect, useState } from 'react'
import { Navigate, useLocation } from 'react-router-dom'
import { getJson, type OrderResponse } from '../lib/api'
import { useApp } from '../store/AppContext'

function StatusPill({ status }: { status: string }) {
  return <span className={`status-pill s-${status}`}>{status}</span>
}

function formatDate(iso: string) {
  const d = new Date(iso)
  return d.toLocaleDateString('en-GB', {
    day: 'numeric',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit',
  })
}

export function Admin() {
  const location = useLocation()
  const { baseUrl, token, isAdmin, addLog } = useApp()
  const [orders, setOrders] = useState<OrderResponse[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [expandedId, setExpandedId] = useState<string | null>(null)

  useEffect(() => {
    if (!token || !isAdmin) return
    setLoading(true)
    setError('')
    addLog('info', 'GET /orders:fetching all orders (admin)')
    getJson<OrderResponse[]>(`${baseUrl}/orders`, token)
      .then((data) => {
        setOrders(data)
        addLog('success', `Loaded ${data.length} orders`)
      })
      .catch((e) => {
        const msg = e instanceof Error ? e.message : String(e)
        setError(msg)
        addLog('error', msg)
      })
      .finally(() => setLoading(false))
  }, [baseUrl, token, isAdmin, addLog])

  if (!token) {
    return <Navigate to="/login" state={{ from: location.pathname }} replace />
  }

  if (!isAdmin) {
    return (
      <section className="narrow">
        <div className="card">
          <div className="card-label">Access denied</div>
          <h2 className="simple-h">Admin only</h2>
          <p className="panel-desc">
            This page is restricted to administrators. Log in with <code>admin / password</code> to view all orders.
          </p>
        </div>
      </section>
    )
  }

  return (
    <>
      <section className="page-head">
        <div className="page-head-eyebrow">Administrator</div>
        <h1 className="page-head-h">All orders</h1>
        <p className="page-head-sub">
          View every order placed by any user. Customer accounts only see their own orders.
        </p>
      </section>

      <section className="card">
        {loading && <div className="loading-msg">Loading orders…</div>}
        {error && <div className="error-box">{error}</div>}

        {!loading && !error && orders.length === 0 && (
          <div className="empty-msg">No orders yet. Be the first to place one!</div>
        )}

        {!loading && orders.length > 0 && (
          <div className="orders-table-wrap">
            <table className="orders-table">
              <thead>
                <tr>
                  <th>Order ID</th>
                  <th>User</th>
                  <th>Status</th>
                  <th>Total</th>
                  <th>Created</th>
                </tr>
              </thead>
              <tbody>
                {orders.map((o) => (
                  <React.Fragment key={o.id}>
                    <tr
                      className="order-row-clickable"
                      onClick={() => setExpandedId(expandedId === o.id ? null : o.id)}
                    >
                      <td className="mono">{o.id.slice(0, 8)}…</td>
                      <td>
                        <span className="user-badge">{o.createdBy}</span>
                      </td>
                      <td>
                        <StatusPill status={o.status} />
                      </td>
                      <td className="mono">£{o.totalAmount.toFixed(2)}</td>
                      <td className="text-dim">{formatDate(o.createdAt)}</td>
                    </tr>
                    {expandedId === o.id && o.items && o.items.length > 0 && (
                      <tr className="order-detail-row">
                        <td colSpan={5}>
                          <div className="order-detail-inner">
                            <table className="order-items-table">
                              <thead>
                                <tr>
                                  <th>SKU</th>
                                  <th>Qty</th>
                                  <th>Unit price</th>
                                  <th>Subtotal</th>
                                </tr>
                              </thead>
                              <tbody>
                                {o.items.map((item, idx) => (
                                  <tr key={idx}>
                                    <td className="mono">{item.sku}</td>
                                    <td className="mono">{item.quantity}</td>
                                    <td className="mono">£{item.unitPrice.toFixed(2)}</td>
                                    <td className="mono">£{(item.quantity * item.unitPrice).toFixed(2)}</td>
                                  </tr>
                                ))}
                              </tbody>
                            </table>
                          </div>
                        </td>
                      </tr>
                    )}
                  </React.Fragment>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>

      <section className="card admin-stats">
        <div className="stat">
          <div className="stat-value">{orders.length}</div>
          <div className="stat-label">Total orders</div>
        </div>
        <div className="stat">
          <div className="stat-value">{orders.filter((o) => o.status === 'CONFIRMED').length}</div>
          <div className="stat-label">Confirmed</div>
        </div>
        <div className="stat">
          <div className="stat-value">{orders.filter((o) => o.status === 'CANCELLED').length}</div>
          <div className="stat-label">Cancelled</div>
        </div>
        <div className="stat">
          <div className="stat-value">
            £{orders.filter((o) => o.status === 'CONFIRMED').reduce((sum, o) => sum + o.totalAmount, 0).toFixed(2)}
          </div>
          <div className="stat-label">Revenue</div>
        </div>
      </section>
    </>
  )
}
