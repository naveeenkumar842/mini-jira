========================================================================
 MINI JIRA — a tiny working example of the "AI agent data" job
========================================================================

WHAT THIS IS
------------
A runnable, miniature version of the work described in the job:
building fake software (connectors) + realistic tasks + grading rubrics,
so AI agents can practice and be evaluated.

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
   The fake backend that exposes a real app (Jira here) as callable tools.
   Controlled + safe, but behaves faithfully like the real system.
   -> Defined in: connector.py

4. REALISTIC WORKFLOW
   A multi-step task mined from how real people actually work
   (e.g. "open a high-priority ticket, then mark it in_progress").
   These are the "long-horizon tasks" the job mentions.
   -> Defined in: task_and_rubric.py (the TASK)

5. EVALUATION / RUBRIC
   Grades the attempt as CORRECT / PARTIAL / DEFICIENT.
   KEY IDEA: it grades what the agent DID (the recorded actions),
   not what the agent SAID.
   -> Defined in: task_and_rubric.py (the grade() function)

6. CLAUDE CODE
   The AI coding agent you use to BUILD all of the above.
   (It's the tool that just created these files.)


THE FILES
---------
connector.py         The fake Jira backend. Stores tickets; every action is
                     recorded in event_log (used later for grading).
tools.py             Tool specs (what the agent sees) + a router that sends
                     tool calls to the connector.
task_and_rubric.py   The TASK (what to do) and the RUBRIC (how it's graded).
run.py               Wires it all together and runs one attempt.


THE FLOW
--------
   TASK
     |
     v
   AGENT emits tool calls
     |
     v
   CONNECTOR executes them  (records every action in event_log)
     |
     v
   RUBRIC checks event_log  ->  CORRECT / PARTIAL / DEFICIENT
     |
     v
   result becomes training / evaluation data for better agents


TRY THIS (to see grading tiers)
-------------------------------
In run.py, function fake_agent_tool_calls(), delete the second line
(the update_status call) and re-run:
    -> the rubric now prints PARTIAL ("missed the status update").
That shows WHY rubrics need correct/partial/deficient tiers: agents
often complete only PART of a long task.


HOW THE REAL JOB DIFFERS (scale, not shape)
-------------------------------------------
- Connectors faithfully mimic real Slack/Jira/Gmail APIs: exact JSON,
  error codes, auth, pagination.
- The agent is a REAL model emitting tool calls, not hand-written ones.
- Tasks are MINED from real usage and are long-horizon (10+ steps,
  often across multiple tools, e.g. Gmail -> Jira -> Slack).
- Rubrics are more detailed and reviewed in team "calibration" cycles
  so everyone grades the same way.

========================================================================
