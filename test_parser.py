from chat_parser import get_last_message, get_last_sender, parse_messages


SAMPLE_CHAT = """[15:17, 11/05/2026] Aminur Islam: Bap er nam ki
[15:17, 11/05/2026] Aminur Islam: ?
[15:18, 11/05/2026] Bon: soiful
eta multiline message"""


def test_parser():
    messages = parse_messages(SAMPLE_CHAT)
    assert len(messages) == 3
    assert get_last_sender(SAMPLE_CHAT) == "Bon"

    last_message = get_last_message(SAMPLE_CHAT)
    assert last_message["time"] == "15:18"
    assert last_message["date"] == "11/05/2026"
    assert last_message["sender"] == "Bon"
    assert last_message["text"] == "soiful\neta multiline message"


if __name__ == "__main__":
    test_parser()
    print("parser tests passed")
