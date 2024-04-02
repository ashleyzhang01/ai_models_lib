import ai_models_lib
from ai_models_lib import together
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.environ.get("TOGETHER_API_KEY")


def test_query_by_provider():
    # test for just message
    response = ai_models_lib.query(
        "together", API_KEY, "What is the capital of Germany?"
    )
    print(response)


def test_query_simplified():
    together_client = together(API_KEY)
    response = together_client.query("What is the capital of Pennsylvania?")
    print(response)
    response = together_client.query(
        "Who founded the University of Pennsylvania?", details=True
    )
    print(response["output"]["choices"][0]["text"])
    print(response)


def test_openai_format():
    together_client = together(API_KEY)
    response = together_client.Completion.create(
        engine="mistralai/Mixtral-8x7B-Instruct-v0.1",
        prompt="What color is water?",
        max_tokens=50,
        temperature=0.8,
    )
    print(response["choices"][0]["message"]["content"])


def main():
    # test_query_by_provider()
    # test_query_simplified()
    # TODO: test_call_together()
    test_openai_format()


if __name__ == "__main__":
    main()
