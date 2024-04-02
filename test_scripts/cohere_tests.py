import ai_models_lib
from ai_models_lib import cohere
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.environ.get("COHERE_API_KEY")


def test_query_by_provider():
    # test for just message
    response = ai_models_lib.query(
        "cohere", API_KEY, "Should I eat ice cream or macarons? Randomly choose one."
    )
    print(response)


def test_query_simplified():
    cohere_client = cohere(API_KEY)
    response = cohere_client.query(
        details=True,
        chat_history=[
            {
                "role": "USER",
                "message": "Should I eat ice cream or macarons? Randomly choose one.",
            },
            {"role": "CHATBOT", "message": "Ice cream."},
        ],
        query="Should I eat it tonight or tomorrow morning?",
    )
    print(response.text)
    # print(response)


def test_call_cohere():
    cohere_client = cohere(API_KEY)
    response = cohere_client.client.chat(
        max_tokens=50,
        message="Should I do a quick boring assignment tonight or tomorrow. Randomly choose one.",
        model="command",
    )
    print(response.text)


def test_openai_format():
    client = cohere(API_KEY)
    response = client.Completion.create(
        engine="command",
        prompt="Should I wear brown or white tomorrow? randomly choose one.",
        max_tokens=50,
        temperature=0.7,
    )
    # print(response)
    print(response["choices"][0]["message"]["content"])


def main():
    test_query_by_provider()
    test_query_simplified()
    test_call_cohere()
    test_openai_format()


if __name__ == "__main__":
    main()
