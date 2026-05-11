import argparse

from openai import OpenAIError

from bot_runner import run_bot
from chatbot_config import load_config, show_config


def parse_args():
    parser = argparse.ArgumentParser(description="WhatsApp Web auto-reply bot powered by OpenAI.")
    parser.add_argument("--setup", action="store_true", help="Run guided setup and save coordinates.")
    parser.add_argument("--preview", action="store_true", help="Generate replies without sending them.")
    parser.add_argument("--once", action="store_true", help="Run one scan cycle and exit.")
    parser.add_argument("--confirm", action="store_true", help="Ask before sending each generated reply.")
    parser.add_argument("--debug-copy", action="store_true", help="Print copied chat text for coordinate debugging.")
    parser.add_argument("--show-config", action="store_true", help="Print saved bot configuration and exit.")
    return parser.parse_args()


def main():
    args = parse_args()
    config = load_config(force_setup=args.setup)

    if args.show_config:
        show_config(config)
        return

    run_bot(
        config,
        preview=args.preview,
        once=args.once,
        confirm=args.confirm,
        debug=args.debug_copy,
    )


def run_cli():
    try:
        main()
    except KeyboardInterrupt:
        print("\nBot stopped.")
    except OpenAIError as error:
        print("OpenAI API error:", error)
        print("Check your API key, quota, billing, and model name.")
    except Exception as error:
        print("Bot error:", error)
