import time

from ai_reply import generate_reply, get_client
from chat_parser import get_last_message, get_message_signature
from chatbot_config import load_state, save_state
from reply_logger import write_reply_log
from whatsapp_automation import copy_visible_chat, focus_chat_window, send_reply


def should_send_reply(config, reply, confirm=False):
    if not confirm and not config.get("confirm_before_send", False):
        return True

    print("Reply preview:", reply)
    answer = input("Send this reply? [y/N]: ").strip().lower()
    return answer in {"y", "yes"}


def has_blocked_keyword(config, message):
    if not message:
        return False

    text = message["text"].lower()
    blocked_keywords = [word.lower() for word in config.get("blocked_keywords", [])]
    return any(keyword in text for keyword in blocked_keywords)


def run_bot(config, preview=False, once=False, confirm=False, debug=False):
    client = get_client()
    focus_chat_window(config)
    state = load_state()
    last_replied_signature = state.get("last_replied_signature")

    print("Bot started. Press Ctrl+C to stop.")
    print("Target sender:", config["target_sender"])
    print("Mode:", "preview" if preview else "auto-send")

    while True:
        time.sleep(config.get("loop_delay_seconds", 5))
        chat_history = copy_visible_chat(config)
        last_message = get_last_message(chat_history)
        last_sender = last_message["sender"] if last_message else None
        current_signature = get_message_signature(last_message)

        if debug:
            print("Copied chat preview:")
            print(chat_history[-1000:] if chat_history else "[empty clipboard]")

        print("Detected last sender:", last_sender or "No sender found")
        if last_sender != config["target_sender"]:
            print("Waiting for target sender...")
            if once:
                break
            continue

        if current_signature == last_replied_signature:
            print("Already replied to this message. Waiting for a new message...")
            if once:
                break
            continue

        if has_blocked_keyword(config, last_message):
            print("Blocked keyword detected. Reply skipped for safety.")
            write_reply_log(config, last_message, "", "blocked")
            last_replied_signature = current_signature
            state["last_replied_signature"] = current_signature
            save_state(state)
            if once:
                break
            continue

        print("Generating reply...")
        reply = generate_reply(client, config, chat_history)

        if preview:
            print("Preview reply:", reply)
            write_reply_log(config, last_message, reply, "preview")
            last_replied_signature = current_signature
            state["last_replied_signature"] = current_signature
            save_state(state)
        elif should_send_reply(config, reply, confirm=confirm):
            send_reply(config, reply)
            write_reply_log(config, last_message, reply, "sent")
            last_replied_signature = current_signature
            state["last_replied_signature"] = current_signature
            save_state(state)
            print("Reply sent.")
        else:
            write_reply_log(config, last_message, reply, "skipped")
            last_replied_signature = current_signature
            state["last_replied_signature"] = current_signature
            save_state(state)
            print("Reply skipped.")

        if once:
            break
