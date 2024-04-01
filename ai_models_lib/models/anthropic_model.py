from anthropic import Anthropic

from ..base_model import BaseModel


class AnthropicModel(BaseModel):
    def __init__(self, api_key):
        super().__init__(api_key)
        self._api_key = api_key
        self.client = Anthropic(api_key=self._api_key)
        self.Completion = self.Completion(self)

    def set_api_key(self, key):
        super().set_api_key(key)
        self.client = Anthropic(api_key=self._api_key)

    def query(self, query, details=False, **kwargs):
        if self._api_key is None:
            raise ValueError("API key not set.")
        client = self.client
        model = kwargs.pop("model", None) or kwargs.pop(
            "engine", "claude-3-opus-20240229"
        )
        max_tokens = kwargs.pop("max_tokens", 1000)
        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": query}],
            **kwargs
        )
        return response if details else response.content[0].text

    # class Messages:
    #     def __init__(self, parent):
    #         self.parent = parent
    #
    #     def create(self, messages, **kwargs):
    #         prompt = messages[0].get('content')
    #         return self.parent.query(prompt, **kwargs)
    class Completion:
        def __init__(self, parent):
            self.parent = parent

        def create(self, engine, prompt, **kwargs):
            if engine:
                kwargs['model'] = engine
            return self.parent.query(prompt, engine, **kwargs)

