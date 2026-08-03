========================================================================
 MINI JIRA + SLACK — a tiny working example of the "AI agent data" job
========================================================================

WHAT THIS IS
------------
A runnable, miniature version of the work described in the job:
building fake software (connectors) + realistic tasks + grading rubrics,
so AI agents can practice and be evaluated.

This version spans TWO tools (Jira + Slack) to show a realistic
"long-horizon" workflow that crosses systems.

Run it with:
    cd mini_jira
    python run.py


THE SIX CONCEPTS (and where each lives)
---------------------------------------
1. AI AGENT
   An AI that TAKES ACTIONS to finish a goal, working in a loop:
   think -> act -> see result -> think again -> ... until done.
   -> Driven in: run.py

2. TOOL CALLING
   HOW the agent acts. It is given a list of tools (functions) and
   emits a "tool call" = a name + arguments. You route that to the code.
   Example: create_ticket(title="Login bug", priority="high")
   -> Defined in: tools.py

3. CONNECTOR
   The fake backend that exposes a real app as callable tools.
   Controlled + safe, but behaves faithfully like the real system.
   -> Defined in: connector.py (Jira)  and  slack_connector.py (Slack)

4. REALISTIC WORKFLOW
   A multi-step task mined from how real people actually work. Here it
   spans TWO tools: open a Jira ticket, update it, THEN post to Slack.
   These are the "long-horizon tasks" the job mentions.
   -> Defined in: task_and_rubric.py (the TASK)

5. EVALUATION / RUBRIC
   Grades the attempt as CORRECT / PARTIAL / DEFICIENT.
   Here it checks THREE required steps across BOTH connectors' logs.
   KEY IDEA: it grades what the agent DID (the recorded actions),
   not what the agent SAID.
   -> Defined in: task_and_rubric.py (the grade() function)

6. CLAUDE CODE
   The AI coding agent you use to BUILD all of the above.
   (It's the tool that created these files.)


THE FILES
---------
connector.py         Fake Jira backend. Every action recorded in event_log.
slack_connector.py   Fake Slack backend. Channels + messages, also logged.
tools.py             Tool specs for BOTH systems + a router that sends each
                     call to the connector that owns it.
task_and_rubric.py   The cross-tool TASK and the 3-step RUBRIC.
run.py               Wires it all together and runs one attempt.


THE FLOW
--------
   TASK (spans Jira + Slack)
     |
     v
   AGENT emits tool calls
     |
     v
   ROUTER sends each call to the right CONNECTOR
     |               (each records its actions in event_log)
     v
   RUBRIC checks all required steps -> CORRECT / PARTIAL / DEFICIENT
     |
     v
   result becomes training / evaluation data for better agents


TRY THIS (to see grading tiers)
-------------------------------
In run.py, function fake_agent_tool_calls(), delete the third line
(the post_message call) and re-run:
    -> the rubric now prints PARTIAL (2/3 steps): the Slack post FAILs.
That shows WHY rubrics need correct/partial/deficient tiers: agents
often complete only PART of a long, multi-tool task.


HOW THE REAL JOB DIFFERS (scale, not shape)
-------------------------------------------
- Connectors faithfully mimic real Slack/Jira/Gmail APIs: exact JSON,
  error codes, auth, pagination, threads, rate limits.
- The agent is a REAL model emitting tool calls, not hand-written ones.
- Tasks are MINED from real usage and are long-horizon (10+ steps,
  often across several tools, e.g. Gmail -> Jira -> Slack).
- Rubrics are more detailed and reviewed in team "calibration" cycles
  so everyone grades the same way.

========================================================================
