"""OneBot 11 event parsing.

OneBot 11 delivers JSON frames. The relevant shape for a bridge:

    {
        "post_type": "message",
        "message_type": "group" | "private",
        "group_id": 123,          # present when message_type == "group"
        "user_id": 456,           # sender
        "raw_message": "text",    # plaintext representation
        "message": [ ... ],       # structured segments (CQ codes / arrays)
        "time": 1700000000,
        "self_id": 789
    }

This module normalizes that into a dataclass so callbacks don't have
to guard against missing keys.
"""
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class OneBotEvent:
    post_type: str
    message_type: Optional[str] = None
    group_id: Optional[int] = None
    user_id: Optional[int] = None
    raw_message: str = ""
    message: Any = None
    self_id: Optional[int] = None
    time: Optional[int] = None

    @property
    def is_group(self) -> bool:
        return self.message_type == "group"

    @property
    def is_private(self) -> bool:
        return self.message_type == "private"


def parse_event(payload: dict) -> Optional[OneBotEvent]:
    """Convert a raw OneBot 11 dict to an OneBotEvent.

    Returns None for non-message events (heartbeats, lifecycle, etc.).
    """
    if not isinstance(payload, dict):
        return None
    if payload.get("post_type") != "message":
        return None
    return OneBotEvent(
        post_type=payload.get("post_type", ""),
        message_type=payload.get("message_type"),
        group_id=payload.get("group_id"),
        user_id=payload.get("user_id"),
        raw_message=payload.get("raw_message", ""),
        message=payload.get("message"),
        self_id=payload.get("self_id"),
        time=payload.get("time"),
    )
