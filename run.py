"""
Puts every piece together and simulates an agent attempting the task.

Flow:  Task  ->  Agent emits tool calls  ->  Connector executes them
       ->  Rubric grades the result.

We hand-write the agent's tool calls here so the example runs with no API key.
In production the tool calls come from a real model (e.g. via Claude Code).
"""

from connector import MiniJira
from tools import TOOL_SPECS, route_tool_call
from task_and_rubric import TASK, grade


def fake_agent_tool_calls():
    """
    A stand-in for the AI agent's decisions. Given TASK, a good agent would
    emit these two tool calls. Swap this out for a real model to see how it does.
    """
    return [
        ("create_ticket", {"title": "Login bug", "priority": "high"}),
        ("update_status", {"ticket_id": 1, "status": "in_progress"}),
    ]


def main():
    jira = MiniJira()

    print("=== TOOLS the agent can call ===")
    for spec in TOOL_SPECS:
        print(f"  - {spec['name']}: {spec['description']}")

    print(f"\n=== TASK ===\n  {TASK['prompt']}\n")

    print("=== Agent takes actions (tool calls) ===")
    for name, args in fake_agent_tool_calls():
        result = route_tool_call(jira, name, args)
        print(f"  {name}({args}) -> {result}")

    grade_label, reason = grade(jira.event_log)
    print(f"\n=== RUBRIC GRADE: {grade_label} ===\n  {reason}")


if __name__ == "__main__":
    main()
