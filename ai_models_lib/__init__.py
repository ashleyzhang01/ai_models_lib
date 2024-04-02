from .models.openai_model import OpenAIModel as openai
from .models.anthropic_model import AnthropicModel as anthropic
from .models.together_model import TogetherModel as together
from .models.replicate_model import ReplicateModel as replicate
from .models.ai21_model import AI21Model as ai21
from .models.cohere_model import CohereModel as cohere


def query(provider_name, api_key, message):
    if "openai" in provider_name.lower() or "open ai" in provider_name.lower():
        client = openai(api_key)
        return client.query(message)
    elif "anthropic" in provider_name.lower():
        client = anthropic(api_key)
        return client.query(message)
    elif "together" in provider_name.lower():
        client = together(api_key)
        return client.query(message)
    elif "replicate" in provider_name.lower():
        client = replicate(api_key)
        return client.query(message)
    elif "ai21" in provider_name.lower() or "ai 21" in provider_name.lower():
        client = ai21(api_key)
        return client.query(message)
    elif "cohere" in provider_name.lower():
        client = cohere(api_key)
        return client.query(message)
    else:
        raise ValueError("Unsupported provider")
