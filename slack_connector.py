"""
CONNECTOR: a fake Slack backend.

Same idea as the Jira connector: state + callable tools, every action logged.
A faithful connector would mimic Slack's real API (channels, threads, JSON,
rate limits, errors). Here we keep it minimal but the shape matches.
"""


class MiniSlack:
    def __init__(self):
        # Pre-seed a few channels, like a real workspace would have.
        self._channels = {"engineering": [], "general": [], "support": []}
        self.event_log = []  # every action recorded, for grading

    # --- TOOLS the agent can call ---

    def post_message(self, channel, text):
        if channel not in self._channels:
            # Faithful connectors reproduce the real system's errors.
            raise KeyError(f"no such channel: {channel}")
        msg = {"channel": channel, "text": text}
        self._channels[channel].append(msg)
        self.event_log.append(("post_message", channel, text))
        return {"ok": True, "channel": channel}

    def list_channels(self):
        return list(self._channels.keys())

    def read_channel(self, channel):
        if channel not in self._channels:
            raise KeyError(f"no such channel: {channel}")
        return list(self._channels[channel])
