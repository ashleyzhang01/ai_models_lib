import together

from ..base_model import BaseModel


class TogetherModel(BaseModel):

    def __init__(self, api_key):
        super().__init__(api_key)
        self._api_key = api_key
        together.api_key = api_key
        self.Completion = self.Completion(self)

    def set_api(self, key):
        super().set_api_key(key)
        self.client = together(api_key=self._api_key)

    def query(self, query, details=False, **kwargs):
        if self._api_key is None:
            raise ValueError("API key not set.")
        together.api_key = self._api_key
        model = (kwargs.pop("model", None) or
                 kwargs.pop("engine", "mistralai/Mixtral-8x7B-Instruct-v0.1"))
        response = together.Complete.create(
            prompt=f"[INST] {query} [/INST]",
            model=model,
            **kwargs
        )
        return response if details else response['output']['choices'][0]['text']

    class Completion:
        def __init__(self, parent):
            self.parent = parent

        def create(self, engine, prompt, **kwargs):
            response = self.parent.query(prompt, engine, **kwargs)

            transformed_response = {
                "id": response["id"],
                "object": "chat.completion",
                "model": response["model"],
                "choices": [{
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": response["output"]["choices"][0]["text"]
                    },
                    "finish_reason": response["output"]["choices"][0]["finish_reason"]
                }],
                "usage": response["output"]["usage"]
            }

            return transformed_response
