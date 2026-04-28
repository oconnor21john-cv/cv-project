import { useState, type FormEvent } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { postJson, type TokenResponse } from '../lib/api'
import { useApp } from '../store/AppContext'

type LocationState = { from?: string } | null

export function Login() {
  const { baseUrl, token, setToken, addLog, busy, setBusy, setActiveStage } = useApp()
  const navigate = useNavigate()
  const location = useLocation()
  const from = (location.state as LocationState)?.from || '/dashboard'

  const [username, setUsername] = useState('customer')
  const [password, setPassword] = useState('password')
  const [error, setError] = useState('')

  async function onSubmit(e: FormEvent) {
    e.preventDefault()
    setError('')
    setBusy('auth')
    setActiveStage('auth')
    addLog('info', `POST /auth/token — requesting JWT for ${username}`)
    try {
      const resp = await postJson<TokenResponse>(`${baseUrl}/auth/token`, { username, password })
      setToken(resp.accessToken)
      addLog('success', `JWT issued for ${username} (${resp.accessToken.slice(0, 14)}…)`)
      navigate(from, { replace: true })
    } catch (e) {
      const msg = e instanceof Error ? e.message : String(e)
      setError(msg)
      addLog('error', msg)
    } finally {
      setBusy('idle')
      setActiveStage('idle')
    }
  }

  if (token) {
    return (
      <section className="narrow">
        <div className="card">
          <div className="card-label">Already signed in</div>
          <h2 className="simple-h">You're already logged in.</h2>
          <p className="panel-desc">Head to the dashboard to create an order.</p>
          <button className="btn-primary" onClick={() => navigate('/dashboard')}>
            Go to dashboard →
          </button>
        </div>
      </section>
    )
  }

  return (
    <section className="narrow">
      <div className="login-card">
        <div className="login-head">
          <div className="login-mark">
            <span />
            <span />
            <span />
          </div>
          <h1>Log in</h1>
          <p>Authenticate with the order-service to try the live demo.</p>
        </div>

        <form onSubmit={onSubmit} className="login-form">
          <label>
            <span>Username</span>
            <input
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              disabled={busy !== 'idle'}
              autoFocus
            />
          </label>
          <label>
            <span>Password</span>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              disabled={busy !== 'idle'}
            />
          </label>

          {error && <div className="error-box">{error}</div>}

          <button type="submit" className="btn-primary btn-block" disabled={busy !== 'idle'}>
            {busy === 'auth' ? <span className="spin" /> : null}
            {busy === 'auth' ? 'Authenticating…' : 'Get token'}
          </button>
        </form>

        <div className="login-foot">
          <div className="creds-hint">
            Demo credentials: <code>customer / password</code>
          </div>
        </div>
      </div>
    </section>
  )
}
