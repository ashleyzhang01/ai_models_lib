from .models.openai_model import OpenAIModel
from .models.anthropic_model import AnthropicModel


# use later to make an easier interface for calling models

class ModelFactory:
    @staticmethod
    def get_model(provider: str, api_key: str):
        if provider.lower() == "openai":
            return OpenAIModel(api_key=api_key)
        elif provider.lower() == "anthropic":
            return AnthropicModel(api_key=api_key)
        else:
            raise ValueError(f"Unsupported provider: {provider}")
