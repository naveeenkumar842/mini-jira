"""
TOOL SCHEMAS: how the connectors' functions are described to an AI agent.

An agent doesn't read your Python. It reads a list of tool *specifications*
(name, what it does, what inputs it takes) and then emits a "tool call" —
a name + arguments — which you route to the right connector.

With multiple tools (Jira + Slack), each tool spec also records which
connector owns it, so the router knows where to send the call.
"""

TOOL_SPECS = [
    # --- Jira tools ---
    {
        "name": "create_ticket",
        "owner": "jira",
        "description": "Create a new Jira ticket.",
        "input_schema": {
            "title": "string (required)",
            "priority": "one of: low | medium | high",
        },
    },
    {
        "name": "update_status",
        "owner": "jira",
        "description": "Change a ticket's status, e.g. to 'in_progress' or 'done'.",
        "input_schema": {
            "ticket_id": "integer (required)",
            "status": "string (required)",
        },
    },
    {
        "name": "search",
        "owner": "jira",
        "description": "Find tickets whose title contains the query text.",
        "input_schema": {"query": "string (required)"},
    },
    # --- Slack tools ---
    {
        "name": "post_message",
        "owner": "slack",
        "description": "Post a message to a Slack channel.",
        "input_schema": {
            "channel": "string (required) e.g. 'engineering'",
            "text": "string (required)",
        },
    },
    {
        "name": "list_channels",
        "owner": "slack",
        "description": "List available Slack channels.",
        "input_schema": {},
    },
    {
        "name": "read_channel",
        "owner": "slack",
        "description": "Read all messages in a Slack channel.",
        "input_schema": {"channel": "string (required)"},
    },
]

# Quick lookup: tool name -> which connector owns it.
_OWNER = {spec["name"]: spec["owner"] for spec in TOOL_SPECS}


def route_tool_call(connectors, name, arguments):
    """
    Dispatch a tool call to the correct connector.

    `connectors` is a dict like {"jira": MiniJira(), "slack": MiniSlack()}.
    We look up which connector owns the tool, then call the method on it.
    """
    owner = _OWNER.get(name)
    if owner is None:
        raise ValueError(f"unknown tool: {name}")
    connector = connectors[owner]
    fn = getattr(connector, name)
    return fn(**arguments)
