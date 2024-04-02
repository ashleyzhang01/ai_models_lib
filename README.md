# ai_models_lib

`ai_models_lib` is a Python library designed to simplify interfacing with various AI models and model providers. This library allows users to seamlessly query different providers with a unified API, currently supporting OpenAI, Anthropic, Together, Replicate, AI21, and Cohere.

## Installation

You can install `ai_models_lib` locally using pip. Navigate to the library's root directory and run one of the following commands:

- To install the package:
``` pip install . ```

- To install the package in editable mode:
``` pip install -e . ```


## Usage

### Simple Queries

To perform simple queries with `ai_models_lib`, import the library and query a provider using the following syntax:

```python
import ai_models_lib

response = ai_models_lib.query(provider, api_key, query)

```
Where `provider` should be a string representing the model provider (e.g., "openai", "anthropic"), `api_key` is your API key for the provider, and `query` is your question or prompt. The currently supported providers are: `openai`, `anthropic`, `together`, `replicate`, `ai21`, and `cohere`.
However, under this query format, you can't choose which engine/model under the provider it uses--it uses a default. 

### Less Simple Queries:
Each provider model has a `query` function that allows you to easily make queries to that provider with different models/engines and other arguments. 
Import a specific model with `from ai_models_lib import <provider>` (or you can do `ai_models_lib.<provider>` for each call for the same functionality). Then, `provider_client = <provider>(API_KEY)` initializes the provider's model with your api key. There's a default model/engine provided for each provider, but you can set a model yourself, along with others arguments such as tokens. This also depends on the original provider and what they can take in. `details` is defaulted to `False`, and that will just return the response message text, but if you set `details` to `True`, it'll return the whole response from the call to the provider. 

Here are some examples: 

__OpenAI:__
```python
openai_client = openai(API_KEY)
response = openai_client.query("What is the capital of Pennsylvania?")
print(response)
```

__Cohere:__
```python
cohere_client = cohere(API_KEY)
response = cohere_client.query(
    details=True,
    chat_history=[
        {"role": "USER", "message": "Should I eat ice cream or macarons? Randomly choose one."},
        {"role": "CHATBOT", "message": "Ice cream."}
    ],
    query="Should I eat it tonight or tomorrow morning?"
)
print(response.text)
```

### Calling the Provider
You can also make calls directly to the provider, which is currently working for all providers except Together. You can directly call the provider using `.client` after initializing the provider client. This allows you to use methods specific to the provider. For instance, with Replicate, using their .run function:
```python
replicate_client = replicate(API_KEY)
response = replicate_client.client.run(
    "meta/llama-2-70b-chat",
    input={
        "system_prompt": "Pinocchio is the Disney character whose nose grows when he lies.",
        "prompt": "What would happen if Pinocchio said 'my nose will now grow'?",
    },
)
print(response)
```

This allows you to access all the methods a provider has. For example, generating images with OpenAI:
```python
openai_client = openai(API_KEY)
image = openai_client.client.images.generate(
    model="dall-e-3", prompt="A cute baby sea otter", n=1, size="1024x1024"
)
```

### Call with the OpenAI format:

All models can be called using the deprecated OpenAI Completion call format. After initializing whichever provider, you can call `.Completion.create(...)` with arguments in the OpenAI format. All other providers' responses will be converted to the response format of that deprecated OpenAI Completion call format. However, some of the arguments for OpenAI's calls won't work for other providers if they don't accommodate it in their default model, such as top_p doesn't work for Cohere.

Here's an example for OpenAI:
```python
client = openai(API_KEY)
response = client.Completion.create(
    engine="gpt-3.5-turbo",
    prompt="What is the capital of France?",
    max_tokens=50,
    temperature=0.7,
    top_p=1,
)
print(response.choices[0].message.content)
```

Here's an example for Anthropic:
```python
client = anthropic(API_KEY)
response = client.Completion.create(
    engine="claude-3-opus-20240229",
    prompt="What is 100-10?",
    max_tokens=50,
    temperature=0.7,
    top_p=1,
)
print(response["choices"][0]["message"]["content"])
```

## Adding New Models
1. In `__init__.py`, setup your provider import:
    ```python
    from .models.<provider_model>.py import <Provider> as provider
    ```
    And add a condition to return the client query:
    ```python
    elif "<provider>" in provider_name.lower():
        client = <provider>(api_key)
        return client.query(message)
    ```

2. Create a new provider model file in `models/.<provider>_model.py`:
    ```python
    import provider
    from ..base_model import BaseModel

    class ProviderModel(BaseModel):
        def __init__(self, api_key):
            super().__init__(api_key)
            self._api_key = api_key
            self.client = <Provider>(api_key=self._api_key)  # Initialize provider with API key
            self.Completion = self.Completion(self)  # For OpenAI format of calling

        def set_api(self, key):
            super().set_api_key(key)
            self.client = <Provider>(api_key=self._api_key)  # Reinitialize provider

        # Create a query method
        def query(self, query, details=False, **kwargs):
            ...
            return response if details else response.message.content

        # Class to follow the OpenAI deprecated format
        class Completion:
            def __init__(self, parent):
                self.parent = parent

            def create(self, engine, prompt, **kwargs):
                response = self.parent.query(...)
                # Convert response to OpenAI format and return
    ```
    This structure allows for easy extension and integration of additional AI models and providers into `ai_models_lib`.
