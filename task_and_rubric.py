"""
TASK + RUBRIC: a realistic CROSS-TOOL workflow and how we grade it.

This is closer to the real job: a long-horizon task that spans two systems
(Jira + Slack), graded step-by-step as CORRECT / PARTIAL / DEFICIENT.
"""

# --- A realistic multi-tool, long-horizon task ---
TASK = {
    "id": "task-002",
    "prompt": (
        "A user reported that login is broken.\n"
        "1. Open a HIGH priority Jira ticket titled 'Login bug'.\n"
        "2. Mark that ticket as in_progress (you've started work).\n"
        "3. Post a message in the 'engineering' Slack channel telling the team "
        "you're on it (the message must mention the login bug)."
    ),
}


# --- RUBRIC: three required steps checked across BOTH connectors' logs ---
def grade(jira_log, slack_log):
    """
    Each step is a boolean check against what actually happened.
    Grade tiers come from how many of the required steps were completed.
    """
    steps = {
        "created high-priority ticket": any(
            e[0] == "create_ticket" and e[2] == "high" for e in jira_log
        ),
        "marked ticket in_progress": any(
            e[0] == "update_status" and e[2] == "in_progress" for e in jira_log
        ),
        "posted to #engineering about login": any(
            e[0] == "post_message"
            and e[1] == "engineering"
            and "login" in e[2].lower()
            for e in slack_log
        ),
    }

    done = sum(steps.values())
    total = len(steps)

    if done == total:
        label = "CORRECT"
    elif done == 0:
        label = "DEFICIENT"
    else:
        label = "PARTIAL"

    return label, steps, done, total
