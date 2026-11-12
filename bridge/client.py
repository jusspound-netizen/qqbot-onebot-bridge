"""OneBot 11 forward-WebSocket client.

Usage:

    from bridge import OneBotBridge, parse_event

    async def on_message(event):
        if event.is_group:
            print(event.group_id, event.user_id, event.raw_message)

    bridge = OneBotBridge("ws://127.0.0.1:3001", on_message)
    await bridge.run()
"""
import asyncio
import json
import logging

import websockets

from .events import OneBotEvent, parse_event

log = logging.getLogger(__name__)


class OneBotBridge:
    def __init__(self, ws_url: str, on_message, reconnect_delay: float = 3.0):
        self.ws_url = ws_url
        self.on_message = on_message
        self.reconnect_delay = reconnect_delay
        self._ws = None
        self._closed = False

    async def run(self):
        while not self._closed:
            try:
                async with websockets.connect(self.ws_url) as ws:
                    self._ws = ws
                    log.info("connected to %s", self.ws_url)
                    async for raw in ws:
                        await self._handle_raw(raw)
            except websockets.ConnectionClosed:
                log.warning("connection closed; retry in %.1fs", self.reconnect_delay)
                await asyncio.sleep(self.reconnect_delay)
            except OSError as exc:
                log.warning("connect failed (%s); retry in %.1fs", exc, self.reconnect_delay)
                await asyncio.sleep(self.reconnect_delay)

    async def _handle_raw(self, raw):
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            log.debug("ignoring non-JSON frame")
            return
        event = parse_event(payload)
        if event is None:
            return
        try:
            await self.on_message(event)
        except Exception:
            log.exception("on_message raised")

    async def send_group_msg(self, group_id: int, message: str) -> dict:
        return await self._call({
            "action": "send_group_msg",
            "params": {"group_id": group_id, "message": message},
        })

    async def send_private_msg(self, user_id: int, message: str) -> dict:
        return await self._call({
            "action": "send_private_msg",
            "params": {"user_id": user_id, "message": message},
        })

    async def _call(self, payload: dict) -> dict:
        if self._ws is None:
            raise RuntimeError("bridge is not connected")
        await self._ws.send(json.dumps(payload))
        return {"sent": payload}

    async def close(self):
        self._closed = True
        if self._ws is not None:
            await self._ws.close()
