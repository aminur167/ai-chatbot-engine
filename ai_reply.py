import os

from openai import OpenAI

from chatbot_config import DEFAULT_MODEL, load_env_file


def get_client():
    load_env_file()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is missing. Add it to .env or set it in your environment.")

    return OpenAI(api_key=api_key)


def trim_reply(reply, max_words):
    words = reply.split()
    if len(words) <= max_words:
        return reply
    return " ".join(words[:max_words]).rstrip(".,!?") + "..."


def generate_reply(client, config, chat_history):
    max_words = config.get("max_reply_words", 35)
    completion = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", config.get("model", DEFAULT_MODEL)),
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Naruto, a friendly coder who speaks naturally in Bangla, Hindi, "
                    "and English when appropriate. Reply like a normal WhatsApp message."
                ),
            },
            {
                "role": "system",
                "content": (
                    "Return only the message body. Do not include timestamps, sender names, "
                    f"or prefixes. Keep the reply within {max_words} words."
                ),
            },
            {"role": "user", "content": chat_history},
        ],
    )
    reply = completion.choices[0].message.content.strip()
    return trim_reply(reply, max_words)
