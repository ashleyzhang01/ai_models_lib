from ai21 import AI21Client

from ..base_model import BaseModel


class AI21Model(BaseModel):
    def __init__(self, api_key):
        super().__init__(api_key)
        self._api_key = api_key
        self.client = AI21Client(api_key=self._api_key)
        self.Completion = self.Completion(self)

    def set_api_key(self, key):
        super().set_api_key(key)
        self.client = AI21Client(api_key=self._api_key)

    def query(self, query, model="j2-mid", details=False, **kwargs):
        if self._api_key is None:
            raise ValueError("API key not set.")
        client = self.client
        if kmodel := kwargs.pop("model", None) or kwargs.pop("engine", None):
            model = kmodel
        max_tokens = kwargs.pop("max_tokens", 100)
        response = client.completion.create(
            model=model, max_tokens=max_tokens, prompt=query, **kwargs
        )
        return response if details else response.completions[0].data.text

    class Completion:
        def __init__(self, parent):
            self.parent = parent

        def create(self, engine, prompt, **kwargs):
            if engine:
                kwargs["model"] = engine
            response = self.parent.query(prompt, details=True, **kwargs)
            transformed_response = {
                "id": response.id,
                "object": "completions",
                "model": kwargs.get("model", "j2-mid"),
                "choices": [
                    {
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": response.completions[0].data.text,
                        },
                        "finish_reason": response.completions[0].finish_reason.reason,
                    }
                ],
            }

            return transformed_response
