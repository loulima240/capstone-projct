
import anthropic
import config


def main():
    # Create the Anthropic client
    client = anthropic.Anthropic(api_key=config.API_KEY)

    # Send a test message to Claude
    message = client.messages.create(
        model=config.MODEL,
        max_tokens=config.MAX_TOKENS,
        messages=[
            {
                "role": "user",
                "content": "Hello! Introduce yourself and explain how you can help me develop PadelBudy."
            }
        ]
    )

    # Display Claude's response
    for block in message.content:
        if block.type == "text":
            print(block.text)


if __name__ == "__main__":
    main()
