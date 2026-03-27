"""
backend/utils/llm.py
Groq client wrapper with tool-calling support.
"""

import json
import os
from typing import List, Dict, Any, Optional, Callable
from groq import Groq

_client: Optional[Groq] = None


def get_client() -> Groq:
    global _client
    if _client is None:
        _client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    return _client


MODEL = os.getenv("GROQ_MODEL", "llama3-70b-8192")


def run_llm(
    prompt: str,
    tools: Optional[List[Dict]] = None,
    tool_functions: Optional[Dict[str, Callable]] = None,
) -> str:
    """
    Run an LLM request with optional tool calling.

    Args:
        prompt: System prompt to send.
        tools: OpenAI tool schema list (optional).
        tool_functions: Map of tool name → Python callable (optional).

    Returns:
        Final text response from the model.
    """
    client = get_client()
 
    api_params = {
        "model": MODEL,
        "messages": [{"role": "system", "content": prompt}],
    }
    
    # ONLY add tools and tool_choice if tools exist
    if tools:
        api_params["tools"] = tools
        api_params["tool_choice"] = "auto"  # String value, not None

    response = client.chat.completions.create(**api_params)
    message = response.choices[0].message

    # No tool calls — return text directly
    if not getattr(message, "tool_calls", None):
        return message.content or ""

    if not tool_functions:
        return message.content or ""

    # Execute tool calls
    tool_messages = []
    for tc in message.tool_calls:
        func_name = tc.function.name
        args = json.loads(tc.function.arguments or "{}")
        tool_fn = tool_functions.get(func_name)
        try:
            result = tool_fn(**args) if tool_fn else {"error": f"Tool '{func_name}' not found."}
        except Exception as e:
            result = {"error": str(e)}
        tool_messages.append({
            "role": "tool",
            "tool_call_id": tc.id,
            "content": json.dumps(result, default=str),
        })

    # Second pass with tool results
    followup = [
        {"role": "system", "content": prompt},
        {
            "role": "assistant",
            "content": message.content,
            "tool_calls": [
                {"id": tc.id, "type": tc.type, "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
                for tc in message.tool_calls
            ],
        },
        *tool_messages,
    ]

    final = client.chat.completions.create(model=MODEL, messages=followup)
    return final.choices[0].message.content or ""
