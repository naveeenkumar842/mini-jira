"""
Puts every piece together and simulates an agent attempting a CROSS-TOOL task.

Flow:  Task  ->  Agent emits tool calls (across Jira AND Slack)
       ->  Router sends each call to the right connector
       ->  Rubric grades every required step.

We hand-write the agent's tool calls here so the example runs with no API key.
In production the tool calls come from a real model (e.g. via Claude Code).
"""

from connector import MiniJira
from slack_connector import MiniSlack
from tools import TOOL_SPECS, route_tool_call
from task_and_rubric import TASK, grade


def fake_agent_tool_calls():
    """
    Stand-in for the AI agent's decisions. A good agent, given TASK, would
    emit these calls across two different tools. Swap for a real model to
    see whether it completes all three steps.
    """
    return [
        ("create_ticket", {"title": "Login bug", "priority": "high"}),
        ("update_status", {"ticket_id": 1, "status": "in_progress"}),
        ("post_message", {"channel": "engineering",
                          "text": "Heads up: investigating the login bug now."}),
    ]


def main():
    # Both connectors live in one registry the router can dispatch to.
    connectors = {"jira": MiniJira(), "slack": MiniSlack()}

    print("=== TOOLS the agent can call (across 2 systems) ===")
    for spec in TOOL_SPECS:
        print(f"  - [{spec['owner']:5}] {spec['name']}: {spec['description']}")

    print(f"\n=== TASK ===\n{TASK['prompt']}\n")

    print("=== Agent takes actions (tool calls) ===")
    for name, args in fake_agent_tool_calls():
        result = route_tool_call(connectors, name, args)
        print(f"  {name}({args}) -> {result}")

    label, steps, done, total = grade(
        connectors["jira"].event_log,
        connectors["slack"].event_log,
    )

    print(f"\n=== RUBRIC GRADE: {label}  ({done}/{total} steps) ===")
    for step, ok in steps.items():
        mark = "PASS" if ok else "FAIL"
        print(f"  [{mark}] {step}")


if __name__ == "__main__":
    main()
