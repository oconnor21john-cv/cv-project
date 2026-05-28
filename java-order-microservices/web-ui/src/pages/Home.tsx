import { Link } from 'react-router-dom'
import { useApp } from '../store/AppContext'

const techTags = [
  'Java 21',
  'Spring Boot 3',
  'PostgreSQL',
  'AWS SQS',
  'ECS Fargate',
  'Application Load Balancer',
  'Terraform',
  'GitHub Actions',
  'React · Vite',
  'Vercel',
]

const features = [
  {
    title: 'order-service',
    body: 'Accepts and persists orders, coordinates inventory reservation and payment processing. Publishes domain events to SQS. Owns the orders schema in PostgreSQL.',
  },
  {
    title: 'inventory-service',
    body: 'Manages stock levels per SKU. Exposes reserve and release endpoints called by order-service during the confirm/cancel flow.',
  },
  {
    title: 'payment-service',
    body: 'Processes payments against order totals. Returns success or failure to order-service, which compensates inventory if payment is declined.',
  },
]

export function Home() {
  const { token } = useApp()
  return (
    <>
      <section className="hero">
        <div className="hero-eyebrow">
          <span className="eyebrow-dot" />
          Live on AWS
        </div>
        <h1 className="hero-h1">
          Order processing <br />
          <span className="gradient-text">microservices</span>
        </h1>
        <p className="hero-lead">
          Three Spring Boot services running on ECS Fargate behind an ALB.
          Orders are persisted to RDS PostgreSQL, stock is reserved via REST,
          and domain events are published to SQS. The infrastructure is defined in Terraform
          and deployed through GitHub Actions.
        </p>

        <div className="hero-cta">
          {token ? (
            <Link to="/dashboard" className="btn-primary btn-lg">
              Open dashboard →
            </Link>
          ) : (
            <Link to="/login" className="btn-primary btn-lg">
              Try the live demo →
            </Link>
          )}
          <Link to="/architecture" className="btn-ghost btn-lg">
            Architecture
          </Link>
        </div>

        <div className="tech-tags">
          {techTags.map((t) => (
            <span key={t}>{t}</span>
          ))}
        </div>
      </section>

      <section className="feature-grid">
        {features.map((f) => (
          <div key={f.title} className="feature">
            <h3>{f.title}</h3>
            <p>{f.body}</p>
          </div>
        ))}
      </section>

      <section className="card home-cta">
        <div>
          <div className="card-label">Demo</div>
          <h2 className="home-cta-h">Place an order against the running services.</h2>
          <p className="home-cta-sub">
            Credentials: <code>customer / password</code>
          </p>
        </div>
        <Link to={token ? '/dashboard' : '/login'} className="btn-primary btn-lg">
          {token ? 'Dashboard' : 'Log in'} →
        </Link>
      </section>
    </>
  )
}
