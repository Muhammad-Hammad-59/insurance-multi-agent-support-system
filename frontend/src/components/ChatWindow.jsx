// frontend/src/components/ChatWindow.jsx
import React, { useState, useRef, useEffect } from 'react'
import { useChat } from '../hooks/useChat.js'
import MessageBubble from './MessageBubble.jsx'

// ── Icon components (Lucide-style SVGs) ───────────────────────────────────

const ShieldIcon = () => (
  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
  </svg>
)

const SendIcon = () => (
  <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
    <line x1="22" y1="2" x2="11" y2="13" />
    <polygon points="22 2 15 22 11 13 2 9 22 2" />
  </svg>
)

const PlusIcon = () => (
  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
    <line x1="12" y1="5" x2="12" y2="19" />
    <line x1="5" y1="12" x2="19" y2="12" />
  </svg>
)

const BookOpenIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z" />
    <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z" />
  </svg>
)

const DollarSignIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="12" y1="1" x2="12" y2="23" />
    <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
  </svg>
)

const SearchIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="11" cy="11" r="8" />
    <line x1="21" y1="21" x2="16.65" y2="16.65" />
  </svg>
)

const UserIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
    <circle cx="12" cy="7" r="4" />
  </svg>
)

const SUGGESTED_QUERIES = [
  { icon: BookOpenIcon, text: 'What does life insurance cover?' },
  { icon: DollarSignIcon, text: 'Premium for policy POL000004' },
  { icon: SearchIcon, text: 'Claim CLM000001 status' },
  { icon: UserIcon, text: 'Talk to a human agent' },
]

export default function ChatWindow() {
  const { messages, loading, sendUserMessage, resetChat } = useChat()
  const [input, setInput] = useState('')
  const [inputFocused, setInputFocused] = useState(false)
  const bottomRef = useRef(null)
  const inputRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  const handleSend = async () => {
    const text = input.trim()
    if (!text || loading) return
    setInput('')
    await sendUserMessage(text)
    inputRef.current?.focus()
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const canSend = !loading && input.trim().length > 0

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      height: '100%',
      background: '#ffffff',
      fontFamily: "'Inter', sans-serif",
    }}>

      {/* ── Header ─────────────────────────────────────────────── */}
      <div style={{
        padding: '0 24px',
        height: '64px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        borderBottom: '1px solid #f1f5f9',
        flexShrink: 0,
        background: '#ffffff',
      }}>
        {/* Brand */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{
            width: '36px', height: '36px',
            borderRadius: '10px',
            background: 'linear-gradient(135deg, #6366f1, #7c3aed)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            boxShadow: '0 2px 8px rgba(99,102,241,0.3)',
          }}>
            <ShieldIcon />
          </div>
          <div>
            <div style={{
              fontWeight: 600,
              fontSize: '15px',
              color: '#0f172a',
              letterSpacing: '-0.01em',
            }}>
              Insurance AI
            </div>
            <div style={{
              fontSize: '11.5px',
              color: '#94a3b8',
              display: 'flex',
              alignItems: 'center',
              gap: '5px',
              marginTop: '1px',
            }}>
              <span style={{
                width: '6px', height: '6px',
                borderRadius: '50%',
                background: '#22c55e',
                display: 'inline-block',
              }} />
              Multi-agent system · Online
            </div>
          </div>
        </div>

        {/* New chat button */}
        <button
          onClick={resetChat}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            background: 'transparent',
            border: '1px solid #e2e8f0',
            borderRadius: '8px',
            color: '#64748b',
            padding: '6px 12px',
            cursor: 'pointer',
            fontSize: '12.5px',
            fontWeight: 500,
            fontFamily: 'inherit',
            transition: 'all 0.15s',
          }}
          onMouseEnter={e => {
            e.currentTarget.style.background = '#f8fafc'
            e.currentTarget.style.borderColor = '#cbd5e1'
            e.currentTarget.style.color = '#334155'
          }}
          onMouseLeave={e => {
            e.currentTarget.style.background = 'transparent'
            e.currentTarget.style.borderColor = '#e2e8f0'
            e.currentTarget.style.color = '#64748b'
          }}
        >
          <PlusIcon />
          New chat
        </button>
      </div>

      {/* ── Messages area ───────────────────────────────────────── */}
      <div style={{
        flex: 1,
        overflowY: 'auto',
        padding: '24px 28px',
        display: 'flex',
        flexDirection: 'column',
      }}>
        {messages.map((msg, i) => (
          <MessageBubble key={i} message={msg} />
        ))}

        {/* Typing indicator */}
        {loading && (
          <div style={{
            display: 'flex',
            alignItems: 'flex-start',
            gap: '10px',
            marginBottom: '20px',
          }}>
            <div style={{
              width: '30px', height: '30px',
              borderRadius: '50%',
              background: '#f1f5f9',
              border: '1px solid #e2e8f0',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              flexShrink: 0,
            }}>
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z" />
                <path d="M12 6v6l4 2" />
              </svg>
            </div>
            <div style={{
              background: '#f8fafc',
              border: '1px solid #e2e8f0',
              borderRadius: '4px 16px 16px 16px',
              padding: '13px 18px',
              boxShadow: '0 1px 4px rgba(0,0,0,0.04)',
              display: 'flex',
              alignItems: 'center',
              gap: '5px',
            }}>
              {[0, 180, 360].map(delay => (
                <span key={delay} style={{
                  width: '6px', height: '6px',
                  borderRadius: '50%',
                  background: '#a5b4fc',
                  display: 'inline-block',
                  animation: `typingDot 1.2s ${delay}ms ease-in-out infinite`,
                }} />
              ))}
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* ── Suggested queries (first message only) ──────────────── */}
      {messages.length === 1 && (
        <div style={{
          padding: '0 28px 16px',
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: '8px',
        }}>
          {SUGGESTED_QUERIES.map((q) => {
            const IconComp = q.icon
            return (
              <button
                key={q.text}
                onClick={() => sendUserMessage(q.text)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  background: '#fafafa',
                  border: '1px solid #e2e8f0',
                  borderRadius: '10px',
                  padding: '9px 12px',
                  fontSize: '12.5px',
                  color: '#475569',
                  cursor: 'pointer',
                  fontWeight: 400,
                  fontFamily: 'inherit',
                  textAlign: 'left',
                  transition: 'all 0.15s',
                }}
                onMouseEnter={e => {
                  e.currentTarget.style.background = '#f0f4ff'
                  e.currentTarget.style.borderColor = '#a5b4fc'
                  e.currentTarget.style.color = '#3730a3'
                }}
                onMouseLeave={e => {
                  e.currentTarget.style.background = '#fafafa'
                  e.currentTarget.style.borderColor = '#e2e8f0'
                  e.currentTarget.style.color = '#475569'
                }}
              >
                <span style={{ color: '#6366f1', flexShrink: 0 }}><IconComp /></span>
                {q.text}
              </button>
            )
          })}
        </div>
      )}

      {/* ── Input bar ───────────────────────────────────────────── */}
      <div style={{
        padding: '14px 24px 18px',
        background: '#ffffff',
        borderTop: '1px solid #f1f5f9',
        flexShrink: 0,
      }}>
        <div style={{
          display: 'flex',
          alignItems: 'flex-end',
          gap: '10px',
          background: inputFocused ? '#ffffff' : '#fafafa',
          border: `1.5px solid ${inputFocused ? '#818cf8' : '#e2e8f0'}`,
          borderRadius: '14px',
          padding: '10px 10px 10px 16px',
          transition: 'border-color 0.15s, background 0.15s',
          boxShadow: inputFocused ? '0 0 0 3px rgba(129,140,248,0.12)' : 'none',
        }}>
          <textarea
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            onFocus={() => setInputFocused(true)}
            onBlur={() => setInputFocused(false)}
            placeholder="Ask about your policy, billing, or claims…"
            rows={1}
            style={{
              flex: 1,
              border: 'none',
              outline: 'none',
              fontSize: '14px',
              lineHeight: '1.6',
              resize: 'none',
              fontFamily: 'inherit',
              background: 'transparent',
              color: '#0f172a',
              maxHeight: '120px',
              overflowY: 'auto',
            }}
          />
          <button
            onClick={handleSend}
            disabled={!canSend}
            style={{
              width: '36px',
              height: '36px',
              borderRadius: '10px',
              border: 'none',
              background: canSend
                ? 'linear-gradient(135deg, #6366f1, #7c3aed)'
                : '#e2e8f0',
              color: canSend ? '#ffffff' : '#94a3b8',
              cursor: canSend ? 'pointer' : 'not-allowed',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              flexShrink: 0,
              transition: 'all 0.15s',
              boxShadow: canSend ? '0 2px 8px rgba(99,102,241,0.35)' : 'none',
            }}
          >
            <SendIcon disabled={!canSend} />
          </button>
        </div>

        {/* Hint line */}
        <p style={{
          textAlign: 'center',
          fontSize: '11px',
          color: '#cbd5e1',
          marginTop: '8px',
          letterSpacing: '0.01em',
        }}>
          Press Enter to send · Shift + Enter for new line
        </p>
      </div>

      <style>{`
        @keyframes typingDot {
          0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
          30% { transform: translateY(-5px); opacity: 1; }
        }
      `}</style>
    </div>
  )
}
