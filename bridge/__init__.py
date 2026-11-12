"""OneBot 11 WebSocket bridge for self-hosted QQ agents.

The client requires websockets. The event parser does not, so the
package can be imported without the dependency installed.
"""
from .events import OneBotEvent, parse_event

__all__ = ["OneBotBridge", "OneBotEvent", "parse_event"]


def __getattr__(name):
    # Lazy import so rom bridge import parse_event works without
    # websockets installed.
    if name == "OneBotBridge":
        from .client import OneBotBridge
        return OneBotBridge
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
