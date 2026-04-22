import type { Stage } from '../store/AppContext'

export function Architecture({ activeStage, hasOrder }: { activeStage: Stage; hasOrder: boolean }) {
  const authFlow = activeStage === 'auth' || activeStage === 'create' || hasOrder
  const createFlow = activeStage === 'create' || activeStage === 'confirm' || activeStage === 'cancel'
  const eventFlow = activeStage === 'confirm' || activeStage === 'cancel'
  const orderActive = activeStage === 'auth' || activeStage === 'create' || activeStage === 'confirm' || activeStage === 'cancel'

  return (
    <div className="arch">
      <svg viewBox="0 0 820 230" className="arch-svg" aria-hidden="true">
        <defs>
          <filter id="glow">
            <feGaussianBlur stdDeviation="2.4" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        <path d="M 110 115 L 225 115" className={`edge ${authFlow ? 'edge-live' : ''}`} />
        <path d="M 355 115 L 470 115" className={`edge ${createFlow ? 'edge-live' : ''}`} />
        <path d="M 550 90 L 660 45" className={`edge ${eventFlow ? 'edge-live' : ''}`} />
        <path d="M 550 140 L 660 185" className={`edge ${eventFlow ? 'edge-live' : ''}`} />
        <path d="M 305 160 L 305 200 L 420 200" className="edge edge-db" />

        <g className={`node ${activeStage !== 'idle' ? 'node-active' : ''}`}>
          <rect x="20" y="80" width="90" height="70" rx="10" className="node-bg" />
          <rect x="30" y="92" width="70" height="48" rx="4" className="node-panel" />
          <circle cx="38" cy="102" r="2" className="node-dot" />
          <circle cx="46" cy="102" r="2" className="node-dot" />
          <circle cx="54" cy="102" r="2" className="node-dot" />
          <text x="65" y="162" className="node-label">Browser</text>
        </g>

        <g className={`node ${orderActive ? 'node-active' : ''}`} filter={activeStage === 'auth' || activeStage === 'create' ? 'url(#glow)' : undefined}>
          <rect x="225" y="75" width="130" height="80" rx="10" className="node-bg node-primary" />
          <text x="290" y="108" className="node-title">order-service</text>
          <text x="290" y="124" className="node-sub">Spring Boot · JWT</text>
          <text x="290" y="138" className="node-sub">:8081</text>
          <text x="290" y="175" className="node-label">Postgres: orders</text>
        </g>

        <g className={`node ${eventFlow ? 'node-active' : ''}`}>
          <rect x="470" y="85" width="80" height="60" rx="30" className="node-bg node-sqs" />
          <text x="510" y="112" className="node-title">SQS</text>
          <text x="510" y="128" className="node-sub">events</text>
        </g>

        <g className={`node ${eventFlow ? 'node-active' : ''}`}>
          <rect x="660" y="10" width="130" height="70" rx="10" className="node-bg" />
          <text x="725" y="38" className="node-title">inventory-service</text>
          <text x="725" y="54" className="node-sub">Spring Boot · :8082</text>
        </g>

        <g className={`node ${eventFlow ? 'node-active' : ''}`}>
          <rect x="660" y="150" width="130" height="70" rx="10" className="node-bg" />
          <text x="725" y="178" className="node-title">payment-service</text>
          <text x="725" y="194" className="node-sub">Spring Boot · :8083</text>
        </g>

        <g>
          <ellipse cx="435" cy="200" rx="22" ry="5" className="db-top" />
          <rect x="413" y="195" width="44" height="14" className="db-body" />
          <ellipse cx="435" cy="209" rx="22" ry="5" className="db-body" />
        </g>
      </svg>
    </div>
  )
}
