# QQ Bot OneBot 11 Bridge

A minimal Python client for a self-hosted NapCat (or any OneBot 11) server.
Receives group and private messages, calls your async callback, replies
through the same WebSocket.

## Risk warning

**This uses the unofficial OneBot 11 protocol.** Tencent treats these clients
as unauthorized software and may freeze the account. Use a disposable
"small account" (小号), not your primary QQ account.

The code does not bypass detection. It is a client for a bridge that
Tencent can detect.

## Install

    pip install websockets

No other dependencies.

## Use

    from bridge import OneBotBridge, parse_event

    async def on_message(event):
        if event.is_group:
            print(event.group_id, event.user_id, event.raw_message)
            # await bridge.send_group_msg(event.group_id, "reply")

    bridge = OneBotBridge("ws://127.0.0.1:3001", on_message)
    await bridge.run()

## Config via env

    ONEBOT_WS_URL=ws://127.0.0.1:3001
    ONEBOT_RECONNECT_DELAY=3.0

## What it does not do

- Does not log in to QQ. NapCat does that.
- Does not handle signing. NapCat does that.
- Does not replace the official API for account safety.

## License

MIT
