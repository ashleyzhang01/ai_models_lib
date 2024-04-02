from openai import OpenAI

from ..base_model import BaseModel


class OpenAIModel(BaseModel):

    def __init__(self, api_key):
        super().__init__(api_key)
        self._api_key = api_key
        self.client = OpenAI(api_key=self._api_key)
        self.Completion = self.Completion(self)

    def set_api(self, key):
        super().set_api_key(key)
        self.client = OpenAI(api_key=self._api_key)

    def query(self, query, details=False, **kwargs):
        if self._api_key is None:
            raise ValueError("API key not set.")
        client = OpenAI(api_key=self._api_key)
        model = (kwargs.pop("model", None) or
                 kwargs.pop("engine", "gpt-3.5-turbo"))
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": query}],
            **kwargs
        )
        return response if details else response.choices[0].message.content

    class Completion:
        def __init__(self, parent):
            self.parent = parent

        def create(self, engine, prompt, **kwargs):
            if engine:
                kwargs['engine'] = engine
            return self.parent.query(prompt, details=True, **kwargs)
