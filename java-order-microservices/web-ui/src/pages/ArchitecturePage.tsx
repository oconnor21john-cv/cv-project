import { Architecture } from '../components/Architecture'
import { useApp } from '../store/AppContext'

const flowSteps = [
  {
    num: '01',
    title: 'Browser authenticates',
    body: 'POST /auth/token on order-service returns a short-lived JWT. The browser stores it in memory and attaches it as a Bearer token on subsequent calls.',
  },
  {
    num: '02',
    title: 'Order is created',
    body: 'POST /orders persists a PENDING order row in the order-service Postgres database. Only the service owning the data writes to it.',
  },
  {
    num: '03',
    title: 'Confirm fans out via HTTP + SQS',
    body: 'order-service calls inventory-service to reserve stock, then payment-service to take payment. Domain events are published to SQS for downstream consumers.',
  },
  {
    num: '04',
    title: 'Cancel releases the reservation',
    body: 'Cancelling a confirmed order triggers an inventory release. If the order was only PENDING, nothing else has to happen.',
  },
]

const infraPoints = [
  ['VPC + public subnets', 'Two AZs for ALB + Fargate redundancy.'],
  ['Application Load Balancer', 'Routes /auth, /orders and /actuator to order-service.'],
  ['ECS Fargate', 'Three services, each with its own task definition, IAM role and log group.'],
  ['RDS Postgres', 'One db.t3.micro per service — data boundaries stay strict.'],
  ['Secrets Manager', 'DB passwords and JWT secret injected as ECS secrets.'],
  ['SQS', 'One queue per service for asynchronous domain events.'],
]

export function ArchitecturePage() {
  const { activeStage, order } = useApp()

  return (
    <>
      <section className="page-head">
        <div className="page-head-eyebrow">System design</div>
        <h1 className="page-head-h">Architecture</h1>
        <p className="page-head-sub">
          Everything runs in eu-west-2, provisioned by the Terraform stack in <code>infra/terraform</code>.
        </p>
      </section>

      <section className="card arch-card">
        <div className="card-label">Request flow</div>
        <Architecture activeStage={activeStage} hasOrder={!!order} />
      </section>

      <section className="flow-grid">
        {flowSteps.map((s) => (
          <div key={s.num} className="flow-step">
            <div className="flow-step-num">{s.num}</div>
            <h3>{s.title}</h3>
            <p>{s.body}</p>
          </div>
        ))}
      </section>

      <section className="card">
        <div className="card-label">AWS footprint</div>
        <dl className="infra-list">
          {infraPoints.map(([k, v]) => (
            <div key={k} className="infra-row">
              <dt>{k}</dt>
              <dd>{v}</dd>
            </div>
          ))}
        </dl>
      </section>
    </>
  )
}
