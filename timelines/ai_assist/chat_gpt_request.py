from openai import OpenAI


def chat_gpt_request(role_text: str, request_text: str) -> str:
    """Make request to ChatGPT."""
    client = OpenAI()

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": role_text},
            {"role": "user", "content": request_text},
        ],
        model="gpt-3.5-turbo",
        response_format={"type": "json_object"},
    )

    return chat_completion.choices[0].message.content
