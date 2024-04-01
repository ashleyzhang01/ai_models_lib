import ai_models_lib
from ai_models_lib import openai
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.environ.get("OPENAI_API_KEY")


def test_query_by_provider():
    # test for just message
    response = ai_models_lib.query(
        "OpenAI", API_KEY, "What is the capital of Germany?"
    )
    print(response)
    response = ai_models_lib.query(
        "open ai", API_KEY, "What is the color of fire?"
    )
    print(response)


def test_query_simplified():
    openai_client = openai(API_KEY)
    response = openai_client.query("What is the capital of Pennsylvania?")
    print(response)
    response = openai_client.query(
        "Who founded the University of Pennsylvania?", details=True
    )
    print(response.choices[0].message.content)
    print(response)
    # TODO: test with kwargs
    # TODO: test model vs engine for deprecation


def test_call_client_deprecated():
    client = openai(API_KEY)
    response = client.Completion.create(
        engine="gpt-3.5-turbo",
        prompt="What is the capital of France?",
        max_tokens=50,
        temperature=0.7,
        top_p=1,
    )
    print(response.choices[0].message.content)


def test_call_openai():
    # chat completions
    openai_client = openai(API_KEY)
    response = openai_client.client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "What is 1 plus 2?"},
            {"role": "system", "content": "Treat plus as minus."},
        ],
    )
    print(response.choices[0].message.content)
    # TODO: test with kwargs
    # images
    image = openai_client.client.images.generate(
        model="dall-e-3",
        prompt="A cute baby sea otter",
        n=1,
        size="1024x1024"
    )
    print(image)
    print(image.data[0].url)


def main():
    test_query_by_provider()
    test_query_simplified()
    test_call_client_deprecated()
    # test_call_openai()


if __name__ == "__main__":
    main()
