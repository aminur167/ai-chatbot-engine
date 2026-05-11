import re


MESSAGE_PATTERN = re.compile(
    r"\[(\d{1,2}:\d{2}),\s*(\d{1,2}/\d{1,2}/\d{2,4})\]\s*([^:\n]+):\s*([\s\S]*?)(?=\n\[\d{1,2}:\d{2},\s*\d{1,2}/\d{1,2}/\d{2,4}\]\s*[^:\n]+:|\Z)"
)


def parse_messages(chat_log):
    messages = []
    for match in MESSAGE_PATTERN.finditer(chat_log.strip()):
        messages.append(
            {
                "time": match.group(1),
                "date": match.group(2),
                "sender": match.group(3).strip(),
                "text": match.group(4).strip(),
            }
        )
    return messages


def get_last_message(chat_log):
    messages = parse_messages(chat_log)
    if not messages:
        return None
    return messages[-1]


def get_last_sender(chat_log):
    last_message = get_last_message(chat_log)
    if not last_message:
        return None
    return last_message["sender"]


def get_message_signature(message):
    if not message:
        return None
    return "|".join(
        [
            message["date"],
            message["time"],
            message["sender"],
            message["text"],
        ]
    )
