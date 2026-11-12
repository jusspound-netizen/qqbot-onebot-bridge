from bridge.events import parse_event


def test_group_message_parses():
    payload = {
        "post_type": "message",
        "message_type": "group",
        "group_id": 123,
        "user_id": 456,
        "raw_message": "hello",
    }
    ev = parse_event(payload)
    assert ev is not None
    assert ev.is_group
    assert not ev.is_private
    assert ev.group_id == 123
    assert ev.user_id == 456
    assert ev.raw_message == "hello"


def test_private_message_parses():
    payload = {
        "post_type": "message",
        "message_type": "private",
        "user_id": 456,
        "raw_message": "hi",
    }
    ev = parse_event(payload)
    assert ev is not None
    assert ev.is_private
    assert not ev.is_group


def test_non_message_event_returns_none():
    payload = {"post_type": "notice", "notice_type": "group_upload"}
    assert parse_event(payload) is None


def test_heartbeat_returns_none():
    payload = {"post_type": "meta_event", "meta_event_type": "heartbeat"}
    assert parse_event(payload) is None
