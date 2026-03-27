"""
backend/api/routes.py
REST API endpoints for the insurance support chatbot.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any

router = APIRouter()

# In-memory session store (replace with Redis for production)
_sessions: Dict[str, Dict[str, Any]] = {}


class ChatRequest(BaseModel):
    message: str
    session_id: str
    policy_number: Optional[str] = None
    customer_id: Optional[str] = None
    claim_id: Optional[str] = None


class ChatResponse(BaseModel):
    session_id: str
    response: Optional[str] = None
    needs_clarification: bool = False
    clarification_question: Optional[str] = None
    agent_used: Optional[str] = None
    requires_human_escalation: bool = False


@router.get("/health")
def health_check():
    return {"status": "ok", "service": "insurance-support-ai"}


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Main chat endpoint. Supports multi-turn conversations via session_id.

    - On first message, creates a new session.
    - Subsequent messages append to existing conversation history.
    - If the agent needs clarification, returns needs_clarification=True.
    - The next request should include the user's answer as the message.
    """
    from backend.graph import run_query

    session_id = request.session_id
    session = _sessions.get(session_id, {})

    # Build conversation context
    conversation_history = session.get("conversation_history", "")
    if conversation_history:
        # Check if we're answering a clarification question
        if session.get("needs_clarification") and session.get("clarification_question"):
            conversation_history += f"\nAssistant: {session['clarification_question']}"
        conversation_history += f"\nUser: {request.message}"
    else:
        conversation_history = f"User: {request.message}"

    context = {
        "conversation_history": conversation_history,
        "policy_number": request.policy_number or session.get("policy_number", ""),
        "customer_id": request.customer_id or session.get("customer_id", ""),
        "claim_id": request.claim_id or session.get("claim_id", ""),
    }

    try:
        result = run_query(request.message, context)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")

    # Persist session state
    _sessions[session_id] = {
        "conversation_history": result.get("conversation_history", conversation_history),
        "policy_number": request.policy_number or session.get("policy_number", ""),
        "customer_id": request.customer_id or session.get("customer_id", ""),
        "claim_id": request.claim_id or session.get("claim_id", ""),
        "needs_clarification": result.get("needs_clarification", False),
        "clarification_question": result.get("clarification_question"),
    }

    return ChatResponse(
        session_id=session_id,
        response=result.get("final_answer") or result.get("clarification_question"),
        needs_clarification=result.get("needs_clarification", False),
        clarification_question=result.get("clarification_question"),
        agent_used=result.get("next_agent"),
        requires_human_escalation=result.get("requires_human_escalation", False),
    )


@router.delete("/session/{session_id}")
def clear_session(session_id: str):
    """Clear a conversation session."""
    _sessions.pop(session_id, None)
    return {"status": "cleared", "session_id": session_id}
