import { Link } from 'react-router-dom'

export function NotFound() {
  return (
    <section className="narrow">
      <div className="card" style={{ textAlign: 'center' }}>
        <div className="card-label">404</div>
        <h2 className="simple-h">Nothing to see here.</h2>
        <p className="panel-desc">That page doesn't exist.</p>
        <Link to="/" className="btn-primary">
          Back home →
        </Link>
      </div>
    </section>
  )
}
