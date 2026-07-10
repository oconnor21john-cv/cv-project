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
    <main className="page">
      <div className="grain" aria-hidden="true" />

      <header className="topbar">
        <nav className="nav">
          <button
            type="button"
            className="theme-btn"
            onClick={() => setTheme(nextTheme)}
            aria-label={`Switch to ${nextTheme} mode`}
            title={`Switch to ${nextTheme} mode`}
          >
            {theme === 'dark' ? '☀' : '☾'}
          </button>
          <Link to="/login" className="nav-cta">Click here for demo</Link>
        </nav>
      </header>

      <section className="hero">
        <p className="eyebrow">Belfast, Northern Ireland</p>
        <h1 className="headline">
          <span className="line">John</span>
          <span className="line italic">O&rsquo;Connor</span>
        </h1>
        <p className="lede">
          Software engineer building Java and Kotlin services. Recently
          finished an MSc in Computer Science and looking for my first role
          in software.
        </p>
      </section>

      <section className="block" aria-labelledby="about-h">
        <h2 id="about-h" className="block-title">
          <span className="num">01</span> About
        </h2>
        <div className="block-body">
          <p>
            I came to software the long way round, through lab science,
            where I learned the value of careful documentation, rigorous
            process, and getting the answer right the first time.
          </p>
        </div>
      </section>

      <section className="block" aria-labelledby="now-h">
        <h2 id="now-h" className="block-title">
          <span className="num">02</span> Now
        </h2>
        <div className="block-body">
          <p>
            I&rsquo;ve been building this site itself as a working project.
            The front-end you&rsquo;re looking at is paired with an
            order-processing microservices platform running on AWS. Spring
            Boot services on ECS Fargate, PostgreSQL with Flyway migrations,
            SQS for async messaging, Resilience4j circuit breakers, and a
            GitHub Actions pipeline that takes a commit through tests
            (Testcontainers, WireMock) and out to production.
          </p>
          <p>
            The point isn&rsquo;t the stack, it&rsquo;s the end-to-end
            lifecycle. Requirements through to a thing running in the cloud
            that someone can actually hit.{' '}
            <Link to="/architecture" className="inline-link">
              Read more about the architecture &rarr;
            </Link>
          </p>
        </div>
      </section>

      <section className="block" aria-labelledby="interests-h">
        <h2 id="interests-h" className="block-title">
          <span className="num">03</span> Off the clock
        </h2>
        <div className="block-body interests">
          <div className="interest">
            <h3>Golf</h3>
            <p>
              A long, ongoing argument with my swing. The kind of game where
              you finally fix one thing and immediately break another,
              which, on reflection, is also a fair description of
              software.
            </p>
          </div>
          <div className="interest">
            <h3>Fishing</h3>
            <p>
              Quiet mornings, slow water, no notifications. Whatever the
              opposite of a stand-up meeting is, that&rsquo;s what
              I&rsquo;m after.
            </p>
          </div>
        </div>
      </section>

      <footer className="foot">
        <p className="copy">&copy; {new Date().getFullYear()} John O&rsquo;Connor &middot; Belfast</p>
      </footer>

      <style>{`
        :root {
          --bg: #f4efe6;
          --ink: #1a1a1a;
          --muted: #6b6357;
          --rule: #d9d1c2;
          --accent: #a8431f;
        }

        [data-theme="dark"] {
          --bg: #1a1714;
          --ink: #f4efe6;
          --muted: #c4baa6;
          --rule: #3d342a;
          --accent: #d96838;
        }

        * { box-sizing: border-box; }

        html, body {
          margin: 0;
          padding: 0;
          background: var(--bg);
          color: var(--ink);
          font-family: 'Söhne', 'Inter', -apple-system, sans-serif;
          transition: background 0.25s ease, color 0.25s ease;
        }

        .page {
          max-width: 720px;
          margin: 0 auto;
          padding: 4rem 2rem 5rem;
          position: relative;
          font-family: 'Iowan Old Style', 'Charter', 'Georgia', serif;
          font-size: 18px;
          line-height: 1.7;
          color: var(--ink);
        }

        /* subtle paper grain */
        .grain {
          position: fixed;
          inset: 0;
          pointer-events: none;
          opacity: 0.04;
          z-index: 1;
          background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>");
        }

        .topbar {
          display: flex;
          justify-content: flex-end;
          align-items: center;
          margin-bottom: 6rem;
          font-family: 'JetBrains Mono', 'IBM Plex Mono', monospace;
          font-size: 12px;
          letter-spacing: 0.08em;
          text-transform: uppercase;
        }

        .nav { display: flex; gap: 0.75rem; align-items: center; }
        .nav a {
          color: var(--muted);
          text-decoration: none;
          transition: all 0.2s ease;
          position: relative;
        }

        .theme-btn {
          width: 36px;
          height: 36px;
          border-radius: 999px;
          border: 1px solid var(--rule);
          background: transparent;
          color: var(--ink);
          font-family: inherit;
          font-size: 14px;
          cursor: pointer;
          display: inline-flex;
          align-items: center;
          justify-content: center;
          padding: 0;
          transition: background 0.2s ease, color 0.2s ease, border-color 0.2s ease;
        }
        .theme-btn:hover {
          background: var(--accent);
          border-color: var(--accent);
          color: var(--bg);
        }

        .nav-cta {
          padding: 0.6rem 1.1rem;
          border: 1px solid var(--rule);
          border-radius: 999px;
          color: var(--ink) !important;
          background: transparent;
          font-weight: 500;
        }
        .nav-cta:hover {
          color: var(--bg) !important;
          background: var(--accent);
          border-color: var(--accent);
        }

        .hero { margin-bottom: 6rem; }

        .eyebrow {
          font-family: 'JetBrains Mono', 'IBM Plex Mono', monospace;
          font-size: 12px;
          letter-spacing: 0.1em;
          text-transform: uppercase;
          color: var(--muted);
          margin: 0 0 1.5rem;
        }

        .headline {
          font-family: 'Canela', 'Iowan Old Style', 'Charter', 'Georgia', serif;
          font-size: clamp(3.25rem, 10vw, 5.75rem);
          line-height: 0.98;
          font-weight: 400;
          letter-spacing: -0.025em;
          margin: 0 0 2rem;
        }
        .headline .line { display: block; }
        .headline .italic { font-style: italic; color: var(--accent); }

        .lede {
          font-size: 1.2rem;
          line-height: 1.55;
          color: var(--ink);
          max-width: 30em;
          margin: 0;
        }

        .block {
          padding: 3.5rem 0;
          border-top: 1px solid var(--rule);
        }
        .block:last-of-type { padding-bottom: 4rem; }

        .block-title {
          font-family: 'JetBrains Mono', 'IBM Plex Mono', monospace;
          font-size: 11px;
          font-weight: 500;
          letter-spacing: 0.12em;
          text-transform: uppercase;
          color: var(--muted);
          margin: 0 0 2rem;
          display: flex;
          align-items: baseline;
          gap: 1rem;
        }
        .num {
          color: var(--accent);
          font-weight: 600;
        }

        .block-body p {
          margin: 0 0 1.2rem;
          max-width: 36em;
        }
        .block-body p:last-child { margin-bottom: 0; }

        .inline-link {
          color: var(--accent);
          text-decoration: none;
          border-bottom: 1px solid var(--accent);
          padding-bottom: 1px;
          transition: opacity 0.2s;
        }
        .inline-link:hover { opacity: 0.65; }

        .interests {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 2.5rem 3rem;
        }
        @media (max-width: 560px) {
          .interests { grid-template-columns: 1fr; gap: 2rem; }
        }
        .interest {
          padding-left: 1rem;
          border-left: 2px solid var(--rule);
        }
        .interest h3 {
          font-family: 'Canela', 'Iowan Old Style', 'Charter', 'Georgia', serif;
          font-style: italic;
          font-weight: 400;
          font-size: 1.35rem;
          margin: 0 0 0.6rem;
          color: var(--accent);
        }
        .interest p {
          margin: 0;
          color: var(--muted);
          font-size: 0.98rem;
        }

        .foot {
          margin-top: 4rem;
          padding-top: 2rem;
          border-top: 1px solid var(--rule);
          font-family: 'JetBrains Mono', 'IBM Plex Mono', monospace;
          font-size: 11px;
          letter-spacing: 0.1em;
          text-transform: uppercase;
          color: var(--muted);
        }
        .foot .copy { margin: 0; }
      `}</style>
    </main>
  )
}
