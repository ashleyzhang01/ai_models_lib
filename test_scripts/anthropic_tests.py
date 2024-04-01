import ai_models_lib
from ai_models_lib import anthropic
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.environ.get("ANTHROPIC_API_KEY")


def test_query_by_provider():
    # test for just message
    response = ai_models_lib.query(
        "anthropic", API_KEY, "What is the capital of Germany?"
    )
    print(response)


def test_query_simplified():
    anthropic_client = anthropic(API_KEY)
    response = anthropic_client.query("What is the capital of Pennsylvania?")
    print(response)
    response = anthropic_client.query(
        "Who founded the University of Pennsylvania?", details=True
    )
    print(response.content[0].text)
    print(response)
    # TODO: test with kwargs
    # TODO: test model vs engine


def test_call_anthropic():
    anthropic_client = anthropic(API_KEY)
    response = anthropic_client.client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": "What is the capital of France?"}
        ],
    )
    print(response.content[0].text)
    # TODO: test with kwargs


def main():
    test_query_by_provider()
    test_query_simplified()
    test_call_anthropic()


if __name__ == "__main__":
    main()
