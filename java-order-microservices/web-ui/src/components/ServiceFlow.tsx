import { useEffect, useState } from 'react'
import { useApp } from '../store/AppContext'

type FlowPhase =
  | 'idle'
  | 'create-send'
  | 'create-process'
  | 'create-done'
  | 'confirm-inventory'
  | 'confirm-inventory-ok'
  | 'confirm-payment'
  | 'confirm-payment-ok'
  | 'confirm-done'
  | 'cancel-send'
  | 'cancel-release'
  | 'cancel-done'
  | 'failed-stock'
  | 'failed-payment'

export function ServiceFlow() {
  const { activeStage, order } = useApp()
  const [phase, setPhase] = useState<FlowPhase>('idle')

  useEffect(() => {
    if (activeStage === 'create') {
      setPhase('create-send')
      const t1 = setTimeout(() => setPhase('create-process'), 600)
      const t2 = setTimeout(() => setPhase('create-done'), 1400)
      return () => { clearTimeout(t1); clearTimeout(t2) }
    }
    if (activeStage === 'confirm') {
      setPhase('confirm-inventory')
      const t1 = setTimeout(() => setPhase('confirm-inventory-ok'), 800)
      const t2 = setTimeout(() => setPhase('confirm-payment'), 1400)
      const t3 = setTimeout(() => setPhase('confirm-payment-ok'), 2200)
      const t4 = setTimeout(() => setPhase('confirm-done'), 2800)
      return () => { clearTimeout(t1); clearTimeout(t2); clearTimeout(t3); clearTimeout(t4) }
    }
    if (activeStage === 'cancel') {
      setPhase('cancel-send')
      const t1 = setTimeout(() => setPhase('cancel-release'), 600)
      const t2 = setTimeout(() => setPhase('cancel-done'), 1400)
      return () => { clearTimeout(t1); clearTimeout(t2) }
    }
  }, [activeStage])

  // React to terminal states from polling
  useEffect(() => {
    if (order?.status === 'STOCK_FAILED') setPhase('failed-stock')
    if (order?.status === 'PAYMENT_FAILED') setPhase('failed-payment')
    if (order?.status === 'CONFIRMED' && activeStage === 'idle') setPhase('confirm-done')
    if (order?.status === 'CANCELLED' && activeStage === 'idle') setPhase('cancel-done')
    if (!order) setPhase('idle')
  }, [order?.status, activeStage])

  const isActive = activeStage !== 'idle'

  // Node states
  const orderNode = getNodeState('order', phase)
  const inventoryNode = getNodeState('inventory', phase)
  const paymentNode = getNodeState('payment', phase)
  const dbNode = getNodeState('db', phase)
  const sqsNode = getNodeState('sqs', phase)

  // Edge states
  const edgeClientOrder = getEdgeState('client-order', phase)
  const edgeOrderDb = getEdgeState('order-db', phase)
  const edgeOrderInventory = getEdgeState('order-inventory', phase)
  const edgeOrderPayment = getEdgeState('order-payment', phase)
  const edgeOrderSqs = getEdgeState('order-sqs', phase)

  return (
    <section className={`sflow ${isActive ? 'sflow-active' : ''}`}>
      <div className="sflow-label">Service communication</div>
      <svg className="sflow-svg" viewBox="0 0 680 200" fill="none" xmlns="http://www.w3.org/2000/svg">
        {/* ── Edges (drawn first, behind nodes) ── */}
        <Edge id="e-co"  d="M 90 100 L 220 100"     state={edgeClientOrder} />
        <Edge id="e-od"  d="M 310 140 L 310 180"     state={edgeOrderDb} />
        <Edge id="e-oi"  d="M 370 80  L 460 50"      state={edgeOrderInventory} />
        <Edge id="e-op"  d="M 370 120 L 460 150"     state={edgeOrderPayment} />
        <Edge id="e-os"  d="M 370 100 L 590 100"     state={edgeOrderSqs} />

        {/* ── Travelling packets ── */}
        {edgeClientOrder === 'active' && <Packet pathD="M 90 100 L 220 100" />}
        {edgeOrderDb === 'active' && <Packet pathD="M 310 140 L 310 180" />}
        {edgeOrderInventory === 'active' && <Packet pathD="M 370 80 L 460 50" />}
        {edgeOrderPayment === 'active' && <Packet pathD="M 370 120 L 460 150" />}
        {edgeOrderSqs === 'active' && <Packet pathD="M 370 100 L 590 100" />}

        {/* ── Nodes ── */}
        <ServiceNode x={220} y={60} w={160} h={80} label="order-service"    icon="O" state={orderNode} />
        <ServiceNode x={460} y={15} w={150} h={55} label="inventory-service" icon="I" state={inventoryNode} />
        <ServiceNode x={460} y={130} w={150} h={55} label="payment-service"  icon="P" state={paymentNode} />
        <ServiceNode x={250} y={170} w={120} h={30} label="PostgreSQL"      icon="D" state={dbNode} small />
        <ServiceNode x={570} y={75}  w={100} h={50} label="SQS"             icon="Q" state={sqsNode} />

        {/* ── Browser client (left) ── */}
        <g className="sflow-client">
          <rect x="20" y="75" width="70" height="50" rx="8" className="sflow-client-box" />
          <text x="55" y="96" textAnchor="middle" className="sflow-client-icon">{'{ }'}</text>
          <text x="55" y="113" textAnchor="middle" className="sflow-client-label">React UI</text>
        </g>
      </svg>

      {/* Status label below */}
      <div className={`sflow-status ${phase !== 'idle' ? 'sflow-status-visible' : ''}`}>
        {statusLabel(phase)}
      </div>
    </section>
  )
}

/* ── Sub-components ── */

type NodeState = 'idle' | 'active' | 'success' | 'error'
type EdgeState = 'idle' | 'active' | 'done'

function ServiceNode({ x, y, w, h, label, icon, state, small }: {
  x: number; y: number; w: number; h: number; label: string; icon: string; state: NodeState; small?: boolean
}) {
  return (
    <g className={`sflow-node sflow-node-${state}`}>
      <rect x={x} y={y} width={w} height={h} rx={small ? 6 : 10} className="sflow-node-bg" />
      {!small && (
        <circle cx={x + 24} cy={y + h / 2} r={12} className="sflow-node-badge" />
      )}
      {!small && (
        <text x={x + 24} y={y + h / 2 + 4} textAnchor="middle" className="sflow-node-icon">{icon}</text>
      )}
      <text
        x={small ? x + w / 2 : x + 44}
        y={y + h / 2 + (small ? 4 : 5)}
        textAnchor={small ? 'middle' : 'start'}
        className={`sflow-node-label ${small ? 'sflow-node-label-sm' : ''}`}
      >
        {label}
      </text>
      {state === 'active' && (
        <rect x={x} y={y} width={w} height={h} rx={small ? 6 : 10} className="sflow-node-pulse" />
      )}
    </g>
  )
}

function Edge({ id, d, state }: { id: string; d: string; state: EdgeState }) {
  return (
    <path
      id={id}
      d={d}
      className={`sflow-edge sflow-edge-${state}`}
      strokeWidth={2}
      strokeDasharray={state === 'idle' ? '4 4' : 'none'}
    />
  )
}

function Packet({ pathD }: { pathD: string }) {
  const id = `pkt-${pathD.replace(/\s/g, '')}`
  return (
    <>
      <path id={id} d={pathD} fill="none" stroke="none" />
      <circle r="4" className="sflow-packet">
        <animateMotion dur="0.6s" repeatCount="indefinite">
          <mpath href={`#${id}`} />
        </animateMotion>
      </circle>
    </>
  )
}

/* ── State logic ── */

function getNodeState(node: string, phase: FlowPhase): NodeState {
  switch (node) {
    case 'order':
      if (phase === 'idle') return 'idle'
      if (phase.startsWith('failed')) return 'error'
      if (phase.includes('cancel-done')) return 'idle'
      if (phase.includes('done')) return 'success'
      return 'active'
    case 'inventory':
      if (phase === 'confirm-inventory' || phase === 'cancel-release') return 'active'
      if (phase === 'confirm-inventory-ok') return 'success'
      if (phase === 'failed-stock') return 'error'
      if (phase === 'confirm-done') return 'success'
      return 'idle'
    case 'payment':
      if (phase === 'confirm-payment') return 'active'
      if (phase === 'confirm-payment-ok' || phase === 'confirm-done') return 'success'
      if (phase === 'failed-payment') return 'error'
      return 'idle'
    case 'db':
      if (phase === 'create-process' || phase === 'create-done') return 'active'
      if (phase.includes('done')) return 'success'
      return 'idle'
    case 'sqs':
      if (phase.includes('done') || phase.startsWith('failed')) return 'active'
      return 'idle'
    default:
      return 'idle'
  }
}

function getEdgeState(edge: string, phase: FlowPhase): EdgeState {
  switch (edge) {
    case 'client-order':
      if (phase === 'create-send' || phase === 'cancel-send') return 'active'
      if (phase !== 'idle') return 'done'
      return 'idle'
    case 'order-db':
      if (phase === 'create-process') return 'active'
      if (phase !== 'idle' && phase !== 'create-send') return 'done'
      return 'idle'
    case 'order-inventory':
      if (phase === 'confirm-inventory' || phase === 'cancel-release') return 'active'
      if (phase === 'confirm-inventory-ok' || phase === 'confirm-payment' || phase === 'confirm-payment-ok' || phase === 'confirm-done' || phase === 'cancel-done') return 'done'
      if (phase === 'failed-stock') return 'done'
      return 'idle'
    case 'order-payment':
      if (phase === 'confirm-payment') return 'active'
      if (phase === 'confirm-payment-ok' || phase === 'confirm-done') return 'done'
      if (phase === 'failed-payment') return 'done'
      return 'idle'
    case 'order-sqs':
      if (phase.includes('done') || phase.startsWith('failed')) return 'active'
      return 'idle'
    default:
      return 'idle'
  }
}

function statusLabel(phase: FlowPhase): string {
  switch (phase) {
    case 'idle':                return ''
    case 'create-send':        return 'POST /orders → order-service'
    case 'create-process':     return 'Persisting to PostgreSQL…'
    case 'create-done':        return 'Order created,event published to SQS'
    case 'confirm-inventory':  return 'Reserving stock → inventory-service'
    case 'confirm-inventory-ok': return 'Stock reserved ✓'
    case 'confirm-payment':    return 'Processing payment → payment-service'
    case 'confirm-payment-ok': return 'Payment accepted ✓'
    case 'confirm-done':       return 'Order confirmed,all services responded'
    case 'cancel-send':        return 'POST /orders/{id}/cancel → order-service'
    case 'cancel-release':     return 'Releasing reservation → inventory-service'
    case 'cancel-done':        return 'Order cancelled,stock released'
    case 'failed-stock':       return 'Inventory reservation failed ✗'
    case 'failed-payment':     return 'Payment declined,stock released ✗'
  }
}
