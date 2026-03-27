// frontend/src/components/MessageBubble.jsx
import React, { useState } from 'react'
import ReactMarkdown from 'react-markdown'

// ── Inline SVG icons ─────────────────────────────────────────────────
const FileTextIcon = ({color='currentColor'}) => (
  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
    <polyline points="14 2 14 8 20 8" />
    <line x1="16" y1="13" x2="8" y2="13" />
    <line x1="16" y1="17" x2="8" y2="17" />
    <polyline points="10 9 9 9 8 9" />
  </svg>
)

const CreditCardIcon = ({color='currentColor'}) => (
  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
    <rect x="1" y="4" width="22" height="16" rx="2" ry="2" />
    <line x1="1" y1="10" x2="23" y2="10" />
  </svg>
)

const ClipboardListIcon = ({color='currentColor'}) => (
  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
    <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2" />
    <rect x="8" y="2" width="8" height="4" rx="1" ry="1" />
    <line x1="9" y1="12" x2="15" y2="12" />
    <line x1="9" y1="16" x2="13" y2="16" />
  </svg>
)

const HelpCircleIcon = ({color='currentColor'}) => (
  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="12" r="10" />
    <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3" />
    <line x1="12" y1="17" x2="12.01" y2="17" />
  </svg>
)

const PhoneCallIcon = ({color='currentColor'}) => (
  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
    <path d="M15.05 5A5 5 0 0 1 19 8.95M15.05 1A9 9 0 0 1 23 8.94m-1 7.98v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 3.14 9.13 19.79 19.79 0 0 1 .07 .5a2 2 0 0 1 1.99-2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 6.82A16 16 0 0 0 14 12.74l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 13.92z" />
  </svg>
)

const CpuIcon = ({color='currentColor'}) => (
  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
    <rect x="4" y="4" width="16" height="16" rx="2" />
    <rect x="9" y="9" width="6" height="6" />
    <line x1="9" y1="1" x2="9" y2="4" />
    <line x1="15" y1="1" x2="15" y2="4" />
    <line x1="9" y1="20" x2="9" y2="23" />
    <line x1="15" y1="20" x2="15" y2="23" />
    <line x1="20" y1="9" x2="23" y2="9" />
    <line x1="20" y1="14" x2="23" y2="14" />
    <line x1="1" y1="9" x2="4" y2="9" />
    <line x1="1" y1="14" x2="4" y2="14" />
  </svg>
)

// Bot icon for AI avatar
const BotIcon = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#6366f1" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="3" y="11" width="18" height="10" rx="2" />
    <circle cx="12" cy="5" r="2" />
    <path d="M12 7v4" />
    <line x1="8" y1="16" x2="8" y2="16" strokeWidth="3" />
    <line x1="16" y1="16" x2="16" y2="16" strokeWidth="3" />
  </svg>
)

// User icon for user avatar
const UserAvatarIcon = () => (
  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
    <circle cx="12" cy="7" r="4" />
  </svg>
)

const AGENT_META = {
  policy_agent:           { label: 'Policy',       color: '#6366f1', bg: '#eef2ff', Icon: FileTextIcon },
  billing_agent:          { label: 'Billing',       color: '#0891b2', bg: '#ecfeff', Icon: CreditCardIcon },
  claims_agent:           { label: 'Claims',        color: '#059669', bg: '#ecfdf5', Icon: ClipboardListIcon },
  general_help_agent:     { label: 'General Help',  color: '#7c3aed', bg: '#f5f3ff', Icon: HelpCircleIcon },
  human_escalation_agent: { label: 'Human Support', color: '#d97706', bg: '#fffbeb', Icon: PhoneCallIcon },
  supervisor_agent:       { label: 'Supervisor',    color: '#64748b', bg: '#f8fafc', Icon: CpuIcon },
}

function extractContent(content) {
  const thinkMatch = content.match(/<think>([\s\S]*?)<\/think>/)
  const thinking = thinkMatch ? thinkMatch[1].trim() : null
  const mainContent = content.replace(/<think>[\s\S]*?<\/think>/g, '').trim()
  return { thinking, mainContent }
}

function Avatar({ isUser }) {
  return (
    <div style={{
      width: '30px',
      height: '30px',
      borderRadius: '50%',
      flexShrink: 0,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: isUser
        ? 'linear-gradient(135deg, #6366f1, #7c3aed)'
        : '#f0f0fa',
      border: isUser ? 'none' : '1px solid #e0e5f5',
      marginTop: '2px',
    }}>
      {isUser ? <UserAvatarIcon /> : <BotIcon />}
    </div>
  )
}

export default function MessageBubble({ message }) {
  const isUser = message.role === 'user'
  const meta = message.agent ? AGENT_META[message.agent] : null
  const { thinking, mainContent } = extractContent(message.content || '')
  const [showThinking, setShowThinking] = useState(false)

  return (
    <div style={{
      display: 'flex',
      flexDirection: isUser ? 'row-reverse' : 'row',
      alignItems: 'flex-start',
      gap: '10px',
      marginBottom: '20px',
      maxWidth: '100%',
    }}>
      <Avatar isUser={isUser} />

      <div style={{ maxWidth: '72%', minWidth: 0 }}>
        {/* Agent pill badge */}
        {!isUser && meta && (
          <div style={{ marginBottom: '5px' }}>
            <span style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '4px',
              background: meta.bg,
              color: meta.color,
              fontSize: '10.5px',
              fontWeight: 600,
              padding: '2px 7px 2px 5px',
              borderRadius: '20px',
              letterSpacing: '0.03em',
              textTransform: 'uppercase',
            }}>
              <meta.Icon color={meta.color} />
              {meta.label}
            </span>
          </div>
        )}

        {/* AI thinking toggle */}
        {!isUser && thinking && (
          <button
            onClick={() => setShowThinking(v => !v)}
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '5px',
              background: 'none',
              border: 'none',
              cursor: 'pointer',
              fontSize: '11.5px',
              color: '#94a3b8',
              fontWeight: 500,
              padding: '2px 0 6px',
              fontFamily: 'inherit',
              transition: 'color 0.15s',
            }}
            onMouseEnter={e => e.currentTarget.style.color = '#64748b'}
            onMouseLeave={e => e.currentTarget.style.color = '#94a3b8'}
          >
            <span style={{ fontSize: '9px' }}>{showThinking ? '▼' : '▶'}</span>
            Reasoning
          </button>
        )}

        {/* Thinking panel */}
        {!isUser && thinking && showThinking && (
          <div style={{
            background: '#fafafa',
            border: '1px solid #e2e8f0',
            borderRadius: '10px',
            padding: '10px 14px',
            marginBottom: '8px',
            fontSize: '12.5px',
            color: '#64748b',
            whiteSpace: 'pre-wrap',
            wordBreak: 'break-word',
            lineHeight: '1.6',
            fontStyle: 'italic',
          }}>
            {thinking}
          </div>
        )}

        {/* Main bubble */}
        <div style={{
          padding: '11px 15px',
          borderRadius: isUser
            ? '16px 16px 4px 16px'
            : '4px 16px 16px 16px',
          background: isUser
            ? 'linear-gradient(135deg, #6366f1, #7c3aed)'
            : message.isError
            ? '#fef7f7'
            : message.isEscalation
            ? '#fffbeb'
            : '#f8fafc',
          color: isUser ? '#ffffff' : '#1e293b',
          border: isUser
            ? 'none'
            : message.isError
            ? '1px solid #fecdd3'
            : message.isEscalation
            ? '1px solid #fde68a'
            : '1px solid #e2e8f0',
          lineHeight: '1.65',
          fontSize: '14px',
          wordBreak: 'break-word',
          boxShadow: isUser
            ? '0 2px 12px rgba(99,102,241,0.25)'
            : '0 1px 4px rgba(0,0,0,0.04)',
        }}>
          <ReactMarkdown
            components={{
              p: ({ children }) => (
                <p style={{ margin: '0 0 6px 0' }}>{children}</p>
              ),
              strong: ({ children }) => (
                <strong style={{ fontWeight: 600 }}>{children}</strong>
              ),
              em: ({ children }) => (
                <em style={{ fontStyle: 'italic', opacity: 0.85 }}>{children}</em>
              ),
              ul: ({ children }) => (
                <ul style={{ margin: '6px 0', paddingLeft: '18px' }}>{children}</ul>
              ),
              ol: ({ children }) => (
                <ol style={{ margin: '6px 0', paddingLeft: '18px' }}>{children}</ol>
              ),
              li: ({ children }) => (
                <li style={{ marginBottom: '3px' }}>{children}</li>
              ),
              code: ({ children }) => (
                <code style={{
                  background: isUser ? 'rgba(255,255,255,0.18)' : '#e2e8f0',
                  padding: '1px 5px',
                  borderRadius: '4px',
                  fontFamily: 'ui-monospace, SFMono-Regular, monospace',
                  fontSize: '12.5px',
                  color: isUser ? '#fff' : '#1e293b',
                }}>
                  {children}
                </code>
              ),
              a: ({ children, href }) => (
                <a href={href}
                  style={{
                    color: isUser ? 'rgba(255,255,255,0.9)' : '#6366f1',
                    textDecoration: 'underline',
                    textUnderlineOffset: '2px',
                  }}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {children}
                </a>
              ),
            }}
          >
            {mainContent || message.content}
          </ReactMarkdown>
        </div>
      </div>
    </div>
  )
}
