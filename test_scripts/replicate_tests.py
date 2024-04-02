import ai_models_lib
from ai_models_lib import replicate
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.environ.get("REPLICATE_API_KEY")

# api = replicate(API_KEY)
# output = api.client.run(
#     "meta/llama-2-70b-chat",
#     input={"prompt": "what came first the chicken or the egg?"}
#     )
# print(output)


def test_query_by_provider():
    # test for just message
    response = ai_models_lib.query(
        "replicate", API_KEY, "What came first, the chicken or the egg?"
    )
    print(response)


def test_query_simplified():
    replicate_client = replicate(API_KEY)
    response = replicate_client.query("Is water wet?", "meta/llama-2-70b-chat")
    print(response)


def test_call_replicate():
    replicate_client = replicate(API_KEY)
    response = replicate_client.client.run(
        "meta/llama-2-70b-chat",
        input={
            "system_prompt": "Pinocchio is the Disney character whose nose grows when he lies.",
            "prompt": "In that fictional world, would happen if Pinocchio said 'my nose will now grow'?",
        },
    )
    print(response)


def test_openai_format():
    client = replicate(API_KEY)
    response = client.Completion.create(
        engine="meta/llama-2-70b-chat",
        prompt="Does the set of all those sets that do not contain themselves contain itself?",
    )
    print(response)
    print(response["choices"][0]["message"]["content"])


def main():
    test_query_by_provider()
    test_query_simplified()
    test_call_replicate()
    test_openai_format()


if __name__ == "__main__":
    main()
