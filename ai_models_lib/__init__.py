from .models.openai_model import OpenAIModel as openai
from .models.anthropic_model import AnthropicModel as anthropic
from .models.together_model import TogetherModel as together


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
    else:
        raise ValueError("Unsupported provider")
