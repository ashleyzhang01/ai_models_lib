import ai_models_lib
from ai_models_lib import ai21
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.environ.get("AI21_API_KEY")


def test_query_by_provider():
    # test for just message
    response = ai_models_lib.query(
        "ai21",
        API_KEY,
        "If you gradually replace all parts of a car one by one over time, until none of the original pieces remain, is it still the same car?",
    )
    print(response)


def test_query_simplified():
    ai21_client = ai21(API_KEY)
    response = ai21_client.query(
        model="j2-mid",
        query="If you drop a soap on the floor will the soap make the floor clean or will the floor make the soap dirty?",
        details=True,
    )
    print(response.completions[0].data.text)
    print(response)


def test_call_ai21():
    ai21_client = ai21(API_KEY)
    response = ai21_client.client.completion.create(
        model="j2-mid",
        max_tokens=50,
        prompt="If you try to fail and succeed, which have you done?",
    )
    print(response.completions[0].data.text)
    # TODO: test with kwargs


def test_openai_format():
    client = ai21(API_KEY)
    response = client.Completion.create(
        engine="j2-mid",
        prompt="What is 100-10?",
        max_tokens=50,
        temperature=0.7,
        top_p=1,
    )
    # print(response)
    print(response["choices"][0]["message"]["content"])


def main():
    # test_query_by_provider()
    # test_query_simplified()
    # test_call_ai21()
    test_openai_format()


if __name__ == "__main__":
    main()
