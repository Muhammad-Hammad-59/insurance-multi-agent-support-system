"""
backend/utils/tracing.py
Optional OpenTelemetry tracing via Arize Phoenix.
Set PHOENIX_COLLECTOR_ENDPOINT in .env to enable.
If not configured, all decorators are no-ops.
"""

import os
import time
from functools import wraps

PHOENIX_ENDPOINT = os.getenv("PHOENIX_COLLECTOR_ENDPOINT", "")

tracer = None

if PHOENIX_ENDPOINT:
    try:
        from phoenix.otel import register
        from opentelemetry.trace.status import Status, StatusCode

        tracer_provider = register(
            project_name="insurance-support-ai",
            endpoint=PHOENIX_ENDPOINT,
            auto_instrument=True,
        )
        tracer = tracer_provider.get_tracer(__name__)
        print(f"✅ Phoenix tracing enabled: {PHOENIX_ENDPOINT}")
    except ImportError:
        print("⚠️  Phoenix not installed. Install arize-phoenix[otel] to enable tracing.")


def trace_agent(func):
    """Decorator to wrap agent functions in a Phoenix span if tracing is enabled."""
    if tracer is None:
        return func  # No-op if tracing is not set up

    @wraps(func)
    def wrapper(*args, **kwargs):
        from opentelemetry.trace.status import Status, StatusCode

        state = args[0] if args else {}
        agent_name = func.__name__

        with tracer.start_as_current_span(agent_name) as span:
            span.set_attribute("agent.name", agent_name)
            span.set_attribute("user.id", state.get("customer_id", "unknown"))
            span.set_attribute("policy.number", state.get("policy_number", "unknown"))
            span.set_attribute("claim.id", state.get("claim_id", "unknown"))
            span.set_attribute("task", state.get("task", "none"))

            start = time.time()
            try:
                result = func(*args, **kwargs)
                span.set_attribute("execution.duration_sec", time.time() - start)
                span.set_status(Status(StatusCode.OK))
                return result
            except Exception as e:
                span.record_exception(e)
                span.set_status(Status(StatusCode.ERROR, str(e)))
                raise

    return wrapper
