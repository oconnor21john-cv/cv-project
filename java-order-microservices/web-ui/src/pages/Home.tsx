import { Link } from 'react-router-dom'
import { useApp } from '../store/AppContext'

const techTags = [
  'Java 25',
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
    title: 'Three independent services',
    body: 'order-service, inventory-service and payment-service each own their Postgres schema and communicate through events.',
  },
  {
    title: 'JWT-authenticated API',
    body: 'Spring Security 6 resource server with HMAC-signed tokens. Customer and admin roles gate the /orders endpoints.',
  },
  {
    title: 'Event-driven with SQS',
    body: 'Domain events flow through AWS SQS so the services stay loosely coupled — no service knows how many listeners it has.',
  },
  {
    title: 'Infrastructure as code',
    body: 'The entire stack (VPC, RDS, ECR, ECS, ALB, SQS, IAM) is provisioned by Terraform. One command, reproducible environment.',
  },
]

export function Home() {
  const { token } = useApp()
  return (
    <>
      <section className="hero">
        <div className="hero-eyebrow">
          <span className="eyebrow-dot" />
          Live portfolio demo
        </div>
        <h1 className="hero-h1">
          Java microservices, <br />
          <span className="gradient-text">live on AWS.</span>
        </h1>
        <p className="hero-lead">
          Three Spring Boot services behind an Application Load Balancer, talking over SQS,
          backed by RDS Postgres. Place a real order end-to-end and watch the flow in real time.
        </p>

        <div className="hero-cta">
          {token ? (
            <Link to="/dashboard" className="btn-primary btn-lg">
              Open dashboard →
            </Link>
          ) : (
            <Link to="/login" className="btn-primary btn-lg">
              Try the demo →
            </Link>
          )}
          <Link to="/architecture" className="btn-ghost btn-lg">
            See the architecture
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
            <div className="feature-dot" />
            <h3>{f.title}</h3>
            <p>{f.body}</p>
          </div>
        ))}
      </section>

      <section className="card home-cta">
        <div>
          <div className="card-label">Ready to try it?</div>
          <h2 className="home-cta-h">Log in with demo credentials and place an order.</h2>
          <p className="home-cta-sub">
            Use <code>customer / password</code> or <code>admin / password</code>. No signup, no email.
          </p>
        </div>
        <Link to={token ? '/dashboard' : '/login'} className="btn-primary btn-lg">
          {token ? 'Dashboard' : 'Log in'} →
        </Link>
      </section>
    </>
  )
}
