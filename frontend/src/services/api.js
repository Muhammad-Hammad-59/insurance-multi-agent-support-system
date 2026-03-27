// frontend/src/services/api.js
// Handles all HTTP calls to the FastAPI backend.
import config from './config';
const BASE_URL = config.API_URL

/**
 * Send a chat message and get a response.
 * @param {string} message
 * @param {string} sessionId
 * @param {object} [opts] — Optional overrides: { policy_number, customer_id, claim_id }
 */
export async function sendMessage(message, sessionId, opts = {}) {
  const res = await fetch(`${BASE_URL}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message,
      session_id: sessionId,
      ...opts,
    }),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Unknown error' }))
    throw new Error(err.detail || `HTTP ${res.status}`)
  }
  return res.json()
}

/**
 * Clear a session on the backend.
 */
export async function clearSession(sessionId) {
  await fetch(`${BASE_URL}/session/${sessionId}`, { method: 'DELETE' })
}

/**
 * Health check.
 */
export async function healthCheck() {
  const res = await fetch(`${BASE_URL}/health`)
  return res.json()
}
