"""
TASK + RUBRIC: the realistic workflow the agent must do, and how we grade it.
"""

# --- A realistic (mined-from-real-usage) long-horizon task ---
TASK = {
    "id": "task-001",
    "prompt": (
        "A user reported that login is broken. "
        "Open a HIGH priority ticket titled 'Login bug', "
        "then mark it as in_progress because you've started work."
    ),
}


# --- RUBRIC: defines correct / partial / deficient, checked against event_log ---
def grade(event_log):
    created_high = any(
        e[0] == "create_ticket" and e[2] == "high" for e in event_log
    )
    marked_progress = any(
        e[0] == "update_status" and e[2] == "in_progress" for e in event_log
    )

    if created_high and marked_progress:
        return "CORRECT", "Created a high-priority ticket AND marked it in_progress."
    if created_high or marked_progress:
        missing = "the status update" if created_high else "the high-priority ticket"
        return "PARTIAL", f"Did some of the task but missed {missing}."
    return "DEFICIENT", "Did not create the ticket or update status correctly."
