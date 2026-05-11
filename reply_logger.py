from datetime import datetime
import json
from pathlib import Path


LOG_DIR = Path("logs")


def write_reply_log(config, last_message, reply, status):
    if not config.get("reply_log_enabled", True):
        return

    LOG_DIR.mkdir(exist_ok=True)
    log_path = LOG_DIR / f"replies-{datetime.now().strftime('%Y-%m-%d')}.jsonl"
    entry = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "target_sender": config["target_sender"],
        "last_message": last_message,
        "reply": reply,
        "status": status,
    }

    with log_path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(entry, ensure_ascii=False) + "\n")
