"""
backend/graph.py
Defines and compiles the LangGraph multi-agent workflow.
"""

from typing import TypedDict, List, Annotated, Dict, Any, Optional
from langgraph.graph import StateGraph, END, add_messages

from backend.agents import (
    supervisor_agent,
    policy_agent_node,
    billing_agent_node,
    claims_agent_node,
    general_help_agent_node,
    human_escalation_node,
    final_answer_agent,
)


class GraphState(TypedDict):
    # Core conversation
    messages: Annotated[List[Any], add_messages]
    user_input: str
    conversation_history: Optional[str]
    n_iteration: Optional[int]

    # Context
    customer_id: Optional[str]
    policy_number: Optional[str]
    claim_id: Optional[str]
    user_intent: Optional[str]

    # Routing
    next_agent: Optional[str]
    task: Optional[str]
    justification: Optional[str]
    end_conversation: Optional[bool]
    needs_clarification: Optional[bool]
    clarification_question: Optional[str]

    # Escalation
    requires_human_escalation: bool
    escalation_reason: Optional[str]

    # Extracted entities
    extracted_entities: Dict[str, Any]
    database_lookup_result: Dict[str, Any]

    # Billing
    billing_amount: Optional[float]
    payment_method: Optional[str]
    billing_frequency: Optional[str]
    invoice_date: Optional[str]

    # Metadata
    timestamp: Optional[str]
    final_answer: Optional[str]


# def decide_next_agent(state: GraphState) -> str:
#     """Conditional edge: determines which node to go to next."""
#     if state.get("needs_clarification"):
#         return "supervisor_agent"
#     if state.get("end_conversation"):
#         return "end"
#     if state.get("requires_human_escalation"):
#         return "human_escalation_agent"
#     return state.get("next_agent", "general_help_agent")

def decide_next_agent(state: GraphState) -> str:
    """Conditional edge: determines which node to go to next."""
    if state.get("needs_clarification"):
        return "ask_clarification"  # ✅ Changed this
    if state.get("end_conversation"):
        return "end"
    if state.get("requires_human_escalation"):
        return "human_escalation_agent"
    return state.get("next_agent", "general_help_agent")
# def decide_next_agent(state: GraphState) -> str:
#     """Conditional edge: determines which node to go to next."""
#     # If we need clarification, we should ask the user (end the graph for now)
#     if state.get("needs_clarification"):
#         return "ask_clarification"  # This should go to END or a special node
    
#     # If conversation should end, go to final answer
#     if state.get("end_conversation"):
#         return "final_answer"
    
#     # If human escalation is required, go there
#     if state.get("requires_human_escalation"):
#         return "human_escalation_agent"
    
#     # If we have a next agent specified, go there
#     next_agent = state.get("next_agent")
#     if next_agent:
#         # Map agent names to node names
#         agent_mapping = {
#             "policy_agent": "policy_agent",
#             "billing_agent": "billing_agent",
#             "claims_agent": "claims_agent",
#             "general_help_agent": "general_help_agent",
#             "human_escalation_agent": "human_escalation_agent",
#         }
#         return agent_mapping.get(next_agent, "general_help_agent")
    
#     # Default to general help
#     return "general_help_agent"


def build_graph():
    """Build and compile the LangGraph workflow."""
    workflow = StateGraph(GraphState)

    # Register nodes
    workflow.add_node("supervisor_agent", supervisor_agent)
    workflow.add_node("policy_agent", policy_agent_node)
    workflow.add_node("billing_agent", billing_agent_node)
    workflow.add_node("claims_agent", claims_agent_node)
    workflow.add_node("general_help_agent", general_help_agent_node)
    workflow.add_node("human_escalation_agent", human_escalation_node)
    workflow.add_node("final_answer_agent", final_answer_agent)

    # Entry point
    workflow.set_entry_point("supervisor_agent")

    # Supervisor routes to specialists or end
    # workflow.add_conditional_edges(
    #     "supervisor_agent",
    #     decide_next_agent,
    #     # {
             
    #     #     "policy_agent": "policy_agent",
    #     #     "billing_agent": "billing_agent",
    #     #     "claims_agent": "claims_agent",
    #     #     "human_escalation_agent": "human_escalation_agent",
    #     #     "general_help_agent": "general_help_agent",
    #     #     "end": "final_answer_agent",
    #     # },
    #     {
    #         "policy_agent": "policy_agent",
    #         "billing_agent": "billing_agent",
    #         "claims_agent": "claims_agent",
    #         "general_help_agent": "general_help_agent",
    #         "human_escalation_agent": "human_escalation_agent",
    #         "final_answer": "final_answer_agent",
    #         "ask_clarification": END,  # End to wait for user input
    #     },
    # )

    workflow.add_conditional_edges(
        "supervisor_agent",
        decide_next_agent,
        {
            "policy_agent": "policy_agent",
            "billing_agent": "billing_agent",
            "claims_agent": "claims_agent",
            "human_escalation_agent": "human_escalation_agent",
            "general_help_agent": "general_help_agent",
            "end": "final_answer_agent",
            "ask_clarification": END, # ✅ ADD THIS LINE!
        },
    )
    # Specialists return to supervisor
    for node in ["policy_agent", "billing_agent", "claims_agent", "general_help_agent"]:
        workflow.add_edge(node, "supervisor_agent")

    # Terminal nodes
    workflow.add_edge("final_answer_agent", END)
    workflow.add_edge("human_escalation_agent", END)

    return workflow.compile()


# Compile once at import time
app = build_graph()


# def run_query(user_message: str, session_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
#     """
#     Run a single user query through the multi-agent graph.

#     Args:
#         user_message: The user's message.
#         session_context: Optional dict with conversation_history, policy_number, etc.

#     Returns:
#         Dict with 'final_answer', 'needs_clarification', 'clarification_question', etc.
#     """
#     ctx = session_context or {}
#     initial_state = {
#         "n_iteration": 0,
#         "messages": [],
#         "user_input": user_message,
#         "user_intent": "",
#         "claim_id": ctx.get("claim_id", ""),
#         "policy_number": ctx.get("policy_number", ""),
#         "customer_id": ctx.get("customer_id", ""),
#         "next_agent": "supervisor_agent",
#         "extracted_entities": {},
#         "database_lookup_result": {},
#         "requires_human_escalation": False,
#         "escalation_reason": "",
#         "billing_amount": None,
#         "payment_method": None,
#         "billing_frequency": None,
#         "invoice_date": None,
#         "conversation_history": ctx.get("conversation_history", f"User: {user_message}"),
#         "task": "Help user with their query",
#         "final_answer": "",
#         "end_conversation": False,
#         "needs_clarification": False,
#     }

#     final_state = app.invoke(initial_state)
#     return final_state



def run_query(user_message: str, session_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Run a single user query through the multi-agent graph.
    """
    ctx = session_context or {}
    
    # Build conversation history properly
    if ctx.get("conversation_history"):
        conversation_history = ctx["conversation_history"] + f"\nUser: {user_message}"
    else:
        conversation_history = f"User: {user_message}"
    
    initial_state = {
        "n_iteration": 0,
        "messages": [],
        "user_input": user_message,
        "user_intent": "",
        "claim_id": ctx.get("claim_id", ""),
        "policy_number": ctx.get("policy_number", ""),
        "customer_id": ctx.get("customer_id", ""),
        "next_agent": None,  # Start with None, supervisor will set it
        "extracted_entities": {},
        "database_lookup_result": {},
        "requires_human_escalation": False,
        "escalation_reason": "",
        "billing_amount": None,
        "payment_method": None,
        "billing_frequency": None,
        "invoice_date": None,
        "conversation_history": conversation_history,
        "task": "Help user with their query",
        "final_answer": "",
        "end_conversation": False,
        "needs_clarification": False,
        "clarification_question": None,
    }

    final_state = app.invoke(initial_state)
    
    # Check if we need clarification
    if final_state.get("needs_clarification"):
        print("🤔 Agent needs clarification from user.")
        return {
            "final_answer": None,
            "needs_clarification": True,
            "clarification_question": final_state.get("clarification_question"),
            "conversation_history": final_state.get("conversation_history"),
            "policy_number": final_state.get("policy_number"),
            "claim_id": final_state.get("claim_id"),
        }
    print("✅ Agent provided a final answer.")
    return final_state