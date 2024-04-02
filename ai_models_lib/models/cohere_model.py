import cohere

from ..base_model import BaseModel


class CohereModel(BaseModel):
    def __init__(self, api_key):
        super().__init__(api_key)
        self._api_key = api_key
        self.client = cohere.Client(api_key=self._api_key)
        self.Completion = self.Completion(self)

    def set_api_key(self, key):
        super().set_api_key(key)
        self.client = cohere.Client(api_key=self._api_key)

    def query(self, query, model=None, details=False, **kwargs):
        if self._api_key is None:
            raise ValueError("API key not set.")
        client = self.client
        if kmodel := kwargs.pop("model", None) or kwargs.pop("engine", None):
            model = kmodel
        response = client.chat(message=query, model=model, **kwargs)
        # return response
        return response if details else response.text

    class Completion:
        def __init__(self, parent):
            self.parent = parent

        def create(self, engine, prompt, **kwargs):
            if engine:
                kwargs["model"] = engine
            response = self.parent.query(prompt, details=True, **kwargs)
            transformed_response = {
                "id": response.generation_id,
                "model": kwargs.get("model", "command"),
                "choices": [
                    {
                        "index": 0,
                        "message": {
                            "role": "chatbot",
                            "content": response.text,
                        },
                        "logprobs": None,
                        "finish_reason": response.finish_reason,
                    }
                ],
                "usage": response.token_count,
            }

            return transformed_response
