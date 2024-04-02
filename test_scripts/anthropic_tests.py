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
        max_tokens=50,
        messages=[
            {"role": "user", "content": "What is the capital of France?"}
        ],
        model="claude-3-opus-20240229",
    )
    print(response.content[0].text)
    # TODO: test with kwargs


def test_openai_format():
    client = anthropic(API_KEY)
    response = client.Completion.create(
        engine="claude-3-opus-20240229",
        prompt="What is 100-10?",
        max_tokens=50,
        temperature=0.7,
        top_p=1,
    )
    # print(response)
    print(response["choices"][0]["message"]["content"])


def main():
    test_query_by_provider()
    test_query_simplified()
    test_call_anthropic()
    test_openai_format()


if __name__ == "__main__":
    main()
