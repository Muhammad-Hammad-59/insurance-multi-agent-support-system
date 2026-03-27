// frontend/src/hooks/useChat.js
import { useState, useCallback, useRef } from 'react'
import { sendMessage, clearSession } from '../services/api.js'

function generateSessionId() {
  return 'session-' + Math.random().toString(36).slice(2)
}

/**
 * Custom hook that manages chat state and API communication.
 */
export function useChat() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: '👋 Hello! I\'m your insurance support assistant. How can I help you today?\n\nYou can ask me about:\n• Policy details and coverage\n• Billing and payments\n• Claim status\n• General insurance questions',
      agent: null,
    }
  ])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const sessionId = useRef(generateSessionId())

  const sendUserMessage = useCallback(async (text) => {
    if (!text.trim() || loading) return

    const userMessage = { role: 'user', content: text }
    setMessages(prev => [...prev, userMessage])
    setLoading(true)
    setError(null)

    try {
      const data = await sendMessage(text, sessionId.current)

      const assistantMessage = {
        role: 'assistant',
        content: data.response || '(No response)',
        agent: data.agent_used,
        needsClarification: data.needs_clarification,
        isEscalation: data.requires_human_escalation,
      }
      setMessages(prev => [...prev, assistantMessage])
    } catch (err) {
      setError(err.message)
      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: '⚠️ Sorry, something went wrong. Please try again.',
          agent: null,
          isError: true,
        }
      ])
    } finally {
      setLoading(false)
    }
  }, [loading])

  const resetChat = useCallback(async () => {
    await clearSession(sessionId.current)
    sessionId.current = generateSessionId()
    setMessages([
      {
        role: 'assistant',
        content: '👋 Hello! I\'m your insurance support assistant. How can I help you today?',
        agent: null,
      }
    ])
    setError(null)
  }, [])

  return { messages, loading, error, sendUserMessage, resetChat }
}
