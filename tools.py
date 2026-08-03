"""
TOOL SCHEMAS: how the connector's functions are described to an AI agent.

An agent doesn't read your Python. It reads a list of tool *specifications*
(name, what it does, what inputs it takes) and then emits a "tool call" —
a name + arguments — which you route to the connector.
"""

TOOL_SPECS = [
    {
        "name": "create_ticket",
        "description": "Create a new Jira ticket.",
        "input_schema": {
            "title": "string (required)",
            "priority": "one of: low | medium | high",
        },
    },
    {
        "name": "update_status",
        "description": "Change a ticket's status, e.g. to 'in_progress' or 'done'.",
        "input_schema": {
            "ticket_id": "integer (required)",
            "status": "string (required)",
        },
    },
    {
        "name": "search",
        "description": "Find tickets whose title contains the query text.",
        "input_schema": {"query": "string (required)"},
    },
]


def route_tool_call(connector, name, arguments):
    """Dispatch a tool call from the agent to the real connector function."""
    fn = getattr(connector, name)
    return fn(**arguments)
