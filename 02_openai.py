import os

from openai import OpenAIError

from ai_reply import get_client
from chatbot_config import DEFAULT_MODEL


def main():
    client = get_client()
    model = os.getenv("OPENAI_MODEL", DEFAULT_MODEL)

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Reply with one short friendly sentence."},
            {"role": "user", "content": "OpenAI connection test successful hole bolo."},
        ],
    )

    print(completion.choices[0].message.content)


if __name__ == "__main__":
    try:
        main()
    except OpenAIError as error:
        print("OpenAI API error:", error)
        print("Check your API key, quota, billing, and model name.")
    except Exception as error:
        print("Error:", error)
