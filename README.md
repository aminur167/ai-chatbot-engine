# AI Chatbot Engine

Professional WhatsApp Web auto-reply bot powered by OpenAI. It copies the visible chat, detects the latest sender, generates a natural reply, and can either preview or send the response automatically.

## Features

- Guided setup for contact name and screen coordinates.
- Preview mode for safe testing without sending messages.
- Optional confirmation before each send.
- Duplicate protection to avoid replying to the same message repeatedly.
- Debug mode for inspecting copied chat text.
- Config viewer for checking saved setup values.
- Reply logging for preview/sent/skipped replies.
- Maximum reply length control.
- Blocked keywords to avoid replying to sensitive messages.
- Persistent message memory across restarts.
- Clear OpenAI API error handling.

## 5-Step Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create `.env`:

```env
OPENAI_API_KEY=sk-your-real-key
OPENAI_MODEL=gpt-4o-mini
```

3. Test OpenAI:

```bash
python 02_openai.py
```

4. Run guided WhatsApp setup:

```bash
python main.py --setup --preview --once
```

The setup asks for the exact WhatsApp sender name and saves your screen coordinates in `.bot_config.json`.

5. Preview, then run the bot:

```bash
python main.py --preview
```

When preview looks correct, enable auto-send:

```bash
python main.py
```

Use `Ctrl+C` to stop.

## Run Modes

```bash
python main.py
```

Runs continuously and sends replies automatically.

```bash
python main.py --preview
```

Generates replies without sending them. Use this for safe testing.

```bash
python main.py --once
```

Runs one scan cycle and exits.

```bash
python main.py --confirm
```

Asks before sending each generated reply.

```bash
python main.py --debug-copy --once
```

Prints copied chat text for coordinate debugging.

```bash
python main.py --show-config
```

Shows the saved `.bot_config.json` setup.

```bash
python main.py --setup
```

Re-runs guided setup and overwrites `.bot_config.json`.

## Current Status

The codebase is ready to run. OpenAI API quota and billing must be active before replies can be generated. If quota is unavailable, the scripts will show a readable OpenAI API error.

Quick validation:

```bash
python 02_openai.py
```

If the test returns a reply, run the bot on WhatsApp Web:

```bash
python main.py --preview
```

## Configuration

The guided setup stores local settings in `.bot_config.json`:

```json
{
  "target_sender": "Bon",
  "app_click": [960, 540],
  "chat_select_start": [650, 180],
  "chat_select_end": [1850, 900],
  "input_click": [960, 1000],
  "loop_delay_seconds": 5,
  "model": "gpt-4o-mini",
  "confirm_before_send": false,
  "max_reply_words": 35,
  "reply_log_enabled": true,
  "blocked_keywords": ["otp", "password", "pin", "card", "bkash", "nagad"]
}
```

This file is ignored by git because it contains machine-specific screen coordinates.

The bot also stores restart memory in `.bot_state.json`, so it does not reply to the same latest message again after restarting.

Use `.bot_config.example.json` as a safe sample for documentation or handoff.

## Reply Logs

When `reply_log_enabled` is `true`, bot activity is saved locally in:

```text
logs/replies-YYYY-MM-DD.jsonl
```

Each log line includes the latest detected message, generated reply, timestamp, and status:

- `preview`
- `sent`
- `skipped`
- `blocked`

The `logs/` folder is ignored by git because it can contain private chat data.

## Troubleshooting

- `insufficient_quota`: Add API billing/credit in the OpenAI Platform account.
- `Detected last sender: No sender found`: Re-run `python main.py --setup` and select the chat area more accurately.
- `Detected last sender` shows a different name: Re-run setup and enter the exact WhatsApp display name.
- Reply is generated but not sent: Re-run setup and select the message input box carefully.
- Need safe testing: use `python main.py --preview --once`.
- Need to inspect copied chat text: use `python main.py --debug-copy --once`.
- Bot keeps waiting after replying once: duplicate protection is active and waiting for a new incoming message.
- Reply is too long: lower `max_reply_words` inside `.bot_config.json`.
- Sensitive message was skipped: check `blocked_keywords` inside `.bot_config.json`.

## Tests

Run the parser test without touching WhatsApp or OpenAI:

```bash
python test_parser.py
```

## Architecture

```text
main.py / 03_bot.py
  -> bot_cli.py
  -> bot_runner.py
  -> chat_parser.py
  -> ai_reply.py
  -> whatsapp_automation.py
  -> reply_logger.py
  -> chatbot_config.py
```

The entry files stay small, while the real logic lives in focused modules.

## Files

- `01_get_cursor.py`: prints mouse coordinates for manual debugging.
- `02_openai.py`: tests OpenAI API access.
- `03_bot.py`: backward-compatible command-line entry point.
- `main.py`: standard command-line entry point.
- `bot_cli.py`: CLI argument parsing and top-level error handling.
- `ai_reply.py`: OpenAI client and reply generation.
- `bot_runner.py`: main bot loop and reply decision flow.
- `chat_parser.py`: WhatsApp chat parsing and sender detection.
- `chatbot_config.py`: `.env`, guided setup, and config loading.
- `reply_logger.py`: local JSONL reply logs.
- `whatsapp_automation.py`: mouse, clipboard, and WhatsApp send automation.
- `.bot_config.example.json`: safe sample config for handoff.
- `.env.example`: example environment variables.
- `test_parser.py`: parser smoke test.
- `requirements.txt`: Python dependencies.

## Safety

- `.env`, `.bot_config.json`, `.bot_state.json`, and `logs/` are ignored by git.
- Do not share API keys.
- Use preview mode before enabling auto-send.
- ChatGPT Plus is separate from OpenAI API billing.
