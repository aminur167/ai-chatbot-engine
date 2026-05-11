import json
import os
from pathlib import Path

import pyautogui


DEFAULT_MODEL = "gpt-4o-mini"
CONFIG_FILE = Path(".bot_config.json")
STATE_FILE = Path(".bot_state.json")


def load_env_file(path=".env"):
    env_path = Path(path)
    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def capture_position(label):
    input(f"Move your mouse to {label}, then press Enter...")
    position = pyautogui.position()
    print(f"Saved {label}: ({position.x}, {position.y})")
    return [position.x, position.y]


def create_config():
    print("Guided setup started. Keep WhatsApp Web open on the target chat.")
    sender_name = input("Exact WhatsApp sender name to reply to: ").strip()
    if not sender_name:
        raise RuntimeError("Sender name is required.")

    config = {
        "target_sender": sender_name,
        "app_click": capture_position("a safe point inside WhatsApp Web"),
        "chat_select_start": capture_position("the top-left area of visible chat messages"),
        "chat_select_end": capture_position("the bottom-right area of visible chat messages"),
        "input_click": capture_position("the WhatsApp message input box"),
        "loop_delay_seconds": 5,
        "model": os.getenv("OPENAI_MODEL", DEFAULT_MODEL),
        "confirm_before_send": False,
        "max_reply_words": 35,
        "reply_log_enabled": True,
        "blocked_keywords": ["otp", "password", "pin", "card", "bkash", "nagad"],
    }

    save_config(config)
    print(f"Setup saved to {CONFIG_FILE}")
    return config


def save_config(config):
    CONFIG_FILE.write_text(json.dumps(config, indent=2), encoding="utf-8")


def load_config(force_setup=False):
    if force_setup or not CONFIG_FILE.exists():
        return create_config()

    with CONFIG_FILE.open("r", encoding="utf-8") as file:
        config = json.load(file)

    required_keys = {
        "target_sender",
        "app_click",
        "chat_select_start",
        "chat_select_end",
        "input_click",
        "loop_delay_seconds",
        "model",
    }
    missing_keys = required_keys - set(config)
    if missing_keys:
        print("Config is missing values:", ", ".join(sorted(missing_keys)))
        return create_config()

    config.setdefault("confirm_before_send", False)
    config.setdefault("max_reply_words", 35)
    config.setdefault("reply_log_enabled", True)
    config.setdefault("blocked_keywords", ["otp", "password", "pin", "card", "bkash", "nagad"])
    save_config(config)
    return config


def show_config(config):
    print(json.dumps(config, indent=2))


def point(config, key):
    return tuple(config[key])


def load_state():
    if not STATE_FILE.exists():
        return {}

    with STATE_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")
