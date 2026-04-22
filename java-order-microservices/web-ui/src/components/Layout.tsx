import { NavLink, Outlet, useLocation, useNavigate } from 'react-router-dom'
import { useApp } from '../store/AppContext'
import { ToastContainer } from './Toast'
import { ThemeToggle } from './ThemeToggle'

export function Layout() {
  const { token, username, isAdmin, clearToken, apiHealthy } = useApp()
  const location = useLocation()
  const navigate = useNavigate()

  function onLogout() {
    clearToken()
    navigate('/login')
  }

  const isHome = location.pathname === '/'

  return (
    <div className="page">
      <div className="page-bg" aria-hidden="true" />

      <header className="topbar">
        <NavLink to="/" className="brand">
          <div className="brand-mark" aria-hidden="true">
            <span />
            <span />
            <span />
          </div>
          <div>
            <div className="brand-name">Order Microservices</div>
            <div className="brand-sub">Live AWS demo</div>
          </div>
        </NavLink>

        <nav className="topnav">
          <NavLink to="/" end className={({ isActive }) => (isActive ? 'active' : '')}>
            Home
          </NavLink>
          <NavLink to="/architecture" className={({ isActive }) => (isActive ? 'active' : '')}>
            Architecture
          </NavLink>
          {token ? (
            <>
              <NavLink to="/dashboard" className={({ isActive }) => (isActive ? 'active' : '')}>
                Dashboard
              </NavLink>
              {isAdmin && (
                <NavLink to="/admin" className={({ isActive }) => (isActive ? 'active admin-link' : 'admin-link')}>
                  Admin
                </NavLink>
              )}
            </>
          ) : (
            <NavLink to="/login" className={({ isActive }) => (isActive ? 'active' : '')}>
              Login
            </NavLink>
          )}
        </nav>

        <div className="topbar-right">
          <ThemeToggle />
          <div className={`live-tag ${apiHealthy ? 'ok' : apiHealthy === false ? 'down' : ''}`}>
            <span className="ring" />
            {apiHealthy === null ? 'Connecting…' : apiHealthy ? 'API live' : 'API unreachable'}
          </div>
          {token && username && (
            <span className="user-label">
              {isAdmin && <span className="role-badge">Admin</span>}
              {username}
            </span>
          )}
          {token && (
            <button className="btn-ghost btn-sm" onClick={onLogout}>
              Log out
            </button>
          )}
        </div>
      </header>

      <main className={`main ${isHome ? 'main-wide' : ''}`}>
        <Outlet />
      </main>

      <footer className="footer">
        <span>Built with Spring Boot, Terraform, and a lot of coffee.</span>
        <span className="footer-links">
          <NavLink to="/architecture">Architecture</NavLink>
          <NavLink to="/login">Login</NavLink>
        </span>
      </footer>

      <ToastContainer />
    </div>
  )
}
