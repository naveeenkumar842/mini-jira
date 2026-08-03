"""
CONNECTOR: a fake Jira backend.

This replicates just enough of Jira to be "faithful" for an agent to practice on.
In the real job you'd emulate the actual Jira REST API responses; here we keep it
tiny but the shape is the same: state + a set of callable tools.
"""


class MiniJira:
    def __init__(self):
        # In-memory "database". A real connector would persist state and mimic
        # Jira's exact JSON, error codes, pagination, etc.
        self._tickets = {}
        self._next_id = 1
        self.event_log = []  # records every action, used later for grading

    # --- TOOLS: these are the functions an AI agent is allowed to "call" ---

    def create_ticket(self, title, priority="medium"):
        if priority not in ("low", "medium", "high"):
            # Faithful connectors reproduce the real system's validation/errors.
            raise ValueError(f"invalid priority: {priority}")
        ticket_id = self._next_id
        self._next_id += 1
        self._tickets[ticket_id] = {
            "id": ticket_id,
            "title": title,
            "priority": priority,
            "status": "open",
        }
        self.event_log.append(("create_ticket", ticket_id, priority))
        return {"id": ticket_id, "status": "open"}

    def update_status(self, ticket_id, status):
        if ticket_id not in self._tickets:
            raise KeyError(f"no such ticket: {ticket_id}")
        self._tickets[ticket_id]["status"] = status
        self.event_log.append(("update_status", ticket_id, status))
        return {"id": ticket_id, "status": status}

    def search(self, query):
        # Simple substring search over titles.
        return [t for t in self._tickets.values() if query.lower() in t["title"].lower()]
