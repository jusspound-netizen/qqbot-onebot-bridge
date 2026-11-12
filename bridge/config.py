"""Config loader for the OneBot bridge."""
import os
from dataclasses import dataclass


@dataclass
class BridgeConfig:
    ws_url: str
    reconnect_delay: float = 3.0

    @classmethod
    def from_env(cls) -> "BridgeConfig":
        url = os.environ.get("ONEBOT_WS_URL", "ws://127.0.0.1:3001")
        delay = float(os.environ.get("ONEBOT_RECONNECT_DELAY", "3.0"))
        return cls(ws_url=url, reconnect_delay=delay)
