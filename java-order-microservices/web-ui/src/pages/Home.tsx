import { Link } from 'react-router-dom'
import { useApp } from '../store/AppContext'

export function Home() {
  const { token } = useApp()
  return (
    <>
      <section className="hero">
        <h1 className="hero-h1">
          Order processing <br />microservices
        </h1>
        <p className="hero-lead">
          Spring Boot 3 on the backend with saga orchestration and a transactional outbox.
          React + Vite frontend, deployed to ECS Fargate behind an ALB.
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
      </section>

      <section className="card">
        <p className="services-prose">
          <code>order-service</code> handles authentication and orchestrates the saga —
          reserve stock, capture payment, and compensate by releasing the reservation
          if payment fails. <code>inventory-service</code> owns stock levels,
          with pessimistic-locked reservations keyed by <code>orderId</code> so retries
          are safe. <code>payment-service</code> is a deliberately simple mock so the
          saga has something real to compensate against. Each service owns its own
          Postgres database and Flyway migrations; nothing is shared except the
          domain events flowing through SQS.
        </p>
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
          {token ? 'Dashboard' : 'Log in'}
        </Link>
      </section>
    </>
  )
}
