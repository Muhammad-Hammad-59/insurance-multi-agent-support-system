// frontend/src/pages/App.jsx
import React from 'react'
import ChatWindow from '../components/ChatWindow.jsx'

const SparkleIcon = () => (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#a5b4fc" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 2L9.5 9.5 2 12l7.5 2.5L12 22l2.5-7.5L22 12l-7.5-2.5z" />
  </svg>
)

export default function App() {
  return (
    <div style={{
      height: '100%',
      display: 'flex',
      flexDirection: 'column',
      background: '#0f0f1a',
      overflow: 'hidden',
      fontFamily: "'Inter', sans-serif",
    }}>

      {/* Background mesh gradient */}
      <div style={{
        position: 'fixed', inset: 0, pointerEvents: 'none', zIndex: 0,
        background: `
          radial-gradient(ellipse 80% 50% at 20% -10%, rgba(99,102,241,0.18) 0%, transparent 60%),
          radial-gradient(ellipse 60% 40% at 80% 80%, rgba(139,92,246,0.14) 0%, transparent 60%)
        `,
      }} />

      {/* Hero title */}
      <div style={{
        position: 'relative', zIndex: 10,
        textAlign: 'center',
        padding: '28px 24px 16px',
        flexShrink: 0,
      }}>
        <div style={{
          display: 'inline-flex', alignItems: 'center', gap: '6px',
          background: 'rgba(99,102,241,0.12)',
          border: '1px solid rgba(99,102,241,0.3)',
          borderRadius: '20px',
          padding: '4px 12px',
          marginBottom: '12px',
        }}>
          <SparkleIcon />
          <span style={{ fontSize: '11px', color: '#a5b4fc', fontWeight: 600, letterSpacing: '0.05em' }}>
            MULTI-AGENT AI SYSTEM
          </span>
        </div>

        <h1 style={{
          fontSize: 'clamp(24px, 4vw, 40px)',
          fontWeight: 800,
          letterSpacing: '-0.03em',
          lineHeight: 1.1,
          margin: '0 0 8px',
          background: 'linear-gradient(135deg, #f1f5f9 30%, #a5b4fc 80%, #c4b5fd 100%)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundClip: 'text',
        }}>
          Insurance Support,<br />Instantly Resolved
        </h1>

        <p style={{
          fontSize: '13.5px',
          color: 'rgba(255,255,255,0.38)',
          margin: 0,
        }}>
          Ask about policies, billing, claims, or request a human agent — 24/7
        </p>
      </div>

      {/* Chat card — fills remaining space */}
      <div style={{
        position: 'relative', zIndex: 10,
        flex: 1,
        minHeight: 0,
        padding: '0 24px 24px',
        display: 'flex',
        justifyContent: 'center',
      }}>
        <div style={{
          width: '100%',
          maxWidth: '860px',
          height: '100%',
          borderRadius: '18px',
          overflow: 'hidden',
          border: '1px solid rgba(255,255,255,0.09)',
          boxShadow: `
            0 0 0 1px rgba(99,102,241,0.15),
            0 24px 80px rgba(0,0,0,0.45),
            0 2px 8px rgba(0,0,0,0.3),
            inset 0 1px 0 rgba(255,255,255,0.06)
          `,
          background: '#ffffff',
        }}>
          <ChatWindow />
        </div>
      </div>

    </div>
  )
}
