import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

export function Home() {
  const [theme, setTheme] = useState<'light' | 'dark'>(() => {
    if (typeof window === 'undefined') return 'light'
    const stored = window.__themePreference
    return stored === 'dark' || stored === 'light' ? stored : 'light'
  })

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
    window.__themePreference = theme
  }, [theme])

  const nextTheme = theme === 'dark' ? 'light' : 'dark'

  return (
    <main className="lp">
      <div className="lp-wrap">
        <header className="lp-top">
          <div className="lp-mark">J. O&rsquo;CONNOR</div>
          <div className="lp-right">
            <button
              type="button"
              className="lp-toggle"
              onClick={() => setTheme(nextTheme)}
              aria-label={`Switch to ${nextTheme} mode`}
              title={`Switch to ${nextTheme} mode`}
            >
              {theme === 'dark' ? '☀' : '☾'}
            </button>
            <Link to="/login" className="lp-demo">Live demo &rarr;</Link>
          </div>
        </header>

        <section className="lp-hero">
          <h1>John<br />O&rsquo;Connor</h1>
          <p className="lp-role">
            Software engineer building Java and Kotlin services. Recently
            finished an MSc in Computer Science and looking for my first role
            in software.
          </p>
        </section>

        <section className="lp-spec">
          <div className="lp-row"><div className="lp-k">Location</div><div className="lp-v">Belfast, Northern Ireland</div></div>
          <div className="lp-row"><div className="lp-k">Discipline</div><div className="lp-v">Backend services, distributed systems</div></div>
          <div className="lp-row"><div className="lp-k">Languages</div><div className="lp-v">Java, Kotlin</div></div>
          <div className="lp-row"><div className="lp-k">Status</div><div className="lp-v"><span className="lp-dot" />Available for work</div></div>
        </section>

        <section className="lp-block">
          <h2>About</h2>
          <div>
            <p>
              I came to software the long way round, through lab science,
              where I learned the value of careful documentation, rigorous
              process, and getting the answer right the first time.
            </p>
          </div>
        </section>

        <section className="lp-block">
          <h2>Currently</h2>
          <div className="lp-stack">
            <p>
              I&rsquo;ve been building this site itself as a working project.
              The front-end you&rsquo;re looking at is paired with an
              order-processing microservices platform running on AWS.
            </p>
            <p className="lp-tags">
              <code>Spring Boot</code><code>ECS Fargate</code><code>PostgreSQL</code>
              <code>Flyway</code><code>SQS</code><code>Resilience4j</code>
              <code>GitHub Actions</code><code>Testcontainers</code><code>WireMock</code>
            </p>
            <p>
              The point isn&rsquo;t the stack, it&rsquo;s the end-to-end
              lifecycle. Requirements through to a thing running in the cloud
              that someone can actually hit.{' '}
              <Link to="/architecture" className="lp-link">Read about the architecture &rarr;</Link>
            </p>
          </div>
        </section>

        <section className="lp-block">
          <h2>Elsewhere</h2>
          <div className="lp-two">
            <div>
              <h3>Golf</h3>
              <p>
                A long, ongoing argument with my swing. The kind of game where
                you finally fix one thing and immediately break another,
                which, on reflection, is also a fair description of software.
              </p>
            </div>
            <div>
              <h3>Fishing</h3>
              <p>
                Quiet mornings, slow water, no notifications. Whatever the
                opposite of a stand-up meeting is, that&rsquo;s what I&rsquo;m after.
              </p>
            </div>
          </div>
        </section>

        <footer className="lp-foot">
          <span>&copy; {new Date().getFullYear()} John O&rsquo;Connor</span>
          <span>Belfast, NI</span>
        </footer>
      </div>

      <style>{`
        .lp {
          --bg: #ffffff;
          --ink: #0a0a0a;
          --muted: #6b6b6b;
          --faint: #ededed;
          --rule: #111111;
          --inv-bg: #0a0a0a;
          --inv-ink: #ffffff;
          --sans: 'Space Grotesk', system-ui, -apple-system, sans-serif;
          --mono: 'IBM Plex Mono', ui-monospace, monospace;
          background: var(--bg);
          color: var(--ink);
          min-height: 100vh;
          font-family: var(--sans);
          font-size: 17px;
          line-height: 1.6;
          -webkit-font-smoothing: antialiased;
        }
        [data-theme="dark"] .lp {
          --bg: #0b0b0c;
          --ink: #f3f2ef;
          --muted: #8d8d89;
          --faint: #212124;
          --rule: #f3f2ef;
          --inv-bg: #f3f2ef;
          --inv-ink: #0b0b0c;
        }

        .lp-wrap { max-width: 860px; margin: 0 auto; padding: 0 32px 120px; }

        .lp-top {
          display: flex; align-items: center; justify-content: space-between;
          padding: 22px 0; border-bottom: 1px solid var(--ink); margin-bottom: 88px;
        }
        .lp-mark { font-family: var(--mono); font-size: 13px; font-weight: 500; letter-spacing: 0.14em; }
        .lp-right { display: flex; align-items: center; gap: 10px; }
        .lp-toggle, .lp-demo {
          font-family: var(--mono); font-size: 12px; letter-spacing: 0.08em;
          border: 1px solid var(--ink); background: transparent; color: var(--ink);
          cursor: pointer; text-decoration: none;
          display: inline-flex; align-items: center; justify-content: center;
          transition: background .15s ease, color .15s ease;
        }
        .lp-toggle { width: 34px; height: 34px; font-size: 14px; padding: 0; }
        .lp-demo { height: 34px; padding: 0 16px; text-transform: uppercase; background: var(--inv-bg); color: var(--inv-ink); border-color: var(--inv-bg); }
        .lp-demo:hover { background: transparent; color: var(--ink); border-color: var(--ink); }
        .lp-toggle:hover { background: var(--ink); color: var(--bg); }

        .lp-hero { margin-bottom: 72px; }
        .lp-hero h1 {
          font-family: var(--sans); font-weight: 500;
          font-size: clamp(3.4rem, 11vw, 6.5rem); line-height: 0.92;
          letter-spacing: -0.03em; margin-bottom: 28px;
        }
        .lp-role { font-size: 1.15rem; line-height: 1.5; color: var(--ink); max-width: 30em; }

        .lp-spec { border-top: 1px solid var(--ink); margin-bottom: 84px; }
        .lp-row {
          display: grid; grid-template-columns: 160px 1fr; gap: 24px;
          padding: 14px 0; border-bottom: 1px solid var(--faint); align-items: baseline;
        }
        .lp-k { font-family: var(--mono); font-size: 11px; letter-spacing: 0.12em; text-transform: uppercase; color: var(--muted); }
        .lp-v { font-size: 0.98rem; }
        .lp-dot { display: inline-block; width: 7px; height: 7px; background: var(--ink); margin-right: 9px; vertical-align: 1px; }

        .lp-block { display: grid; grid-template-columns: 160px 1fr; gap: 24px; padding: 40px 0; border-top: 1px solid var(--faint); }
        .lp-block > h2 {
          font-family: var(--mono); font-size: 11px; font-weight: 500;
          letter-spacing: 0.12em; text-transform: uppercase; color: var(--muted); padding-top: 4px;
        }
        .lp-block p { max-width: 40em; margin-bottom: 1.1rem; }
        .lp-block p:last-child { margin-bottom: 0; }
        .lp-link { color: var(--ink); text-decoration: none; border-bottom: 1px solid var(--ink); padding-bottom: 1px; }
        .lp-link:hover { background: var(--ink); color: var(--bg); }

        .lp-tags { margin-bottom: 14px !important; }
        .lp-tags code {
          font-family: var(--mono); font-size: 0.82rem; border: 1px solid var(--faint);
          padding: 2px 7px; margin: 0 3px 6px 0; display: inline-block; color: var(--muted);
          background: transparent; border-radius: 0;
        }

        .lp-two { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; }
        .lp-two h3 { font-family: var(--sans); font-weight: 600; font-size: 1.05rem; margin-bottom: 8px; }
        .lp-two p { color: var(--muted); font-size: 0.95rem; margin: 0; max-width: none; }

        .lp-foot {
          border-top: 1px solid var(--ink); margin-top: 40px; padding-top: 20px;
          font-family: var(--mono); font-size: 11px; letter-spacing: 0.1em;
          text-transform: uppercase; color: var(--muted);
          display: flex; justify-content: space-between;
        }

        @media (max-width: 620px) {
          .lp-row, .lp-block { grid-template-columns: 1fr; gap: 6px; }
          .lp-block > h2 { padding-top: 0; }
          .lp-two { grid-template-columns: 1fr; gap: 28px; }
          .lp-wrap { padding: 0 20px 80px; }
        }
      `}</style>
    </main>
  )
}
