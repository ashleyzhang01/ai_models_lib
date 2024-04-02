import replicate

from ..base_model import BaseModel


class ReplicateModel(BaseModel):
    def __init__(self, api_key):
        super().__init__(api_key)
        self._api_key = api_key
        self.client = replicate.Client(api_token=self._api_key)
        self.Completion = self.Completion(self)

    def set_api_key(self, key):
        super().set_api_key(key)
        self.client = replicate.Client(api_key=self._api_key)

    def query(self, query, model="meta/llama-2-70b-chat", details=False, **kwargs):
        if self._api_key is None:
            raise ValueError("API key not set.")
        client = self.client
        if (kmodel := kwargs.pop("model", None) or kwargs.pop(
            "engine", None)):
            model = kmodel
        response = client.run(
            model,
            input={"prompt": query},
            **kwargs
        )
        return ''.join(response)
        # return response if details else response.content[0].text

    class Completion:
        def __init__(self, parent):
            self.parent = parent

        def create(self, engine, prompt, **kwargs):
            if engine:
                kwargs['model'] = engine
            response = self.parent.query(prompt, details=True, **kwargs)

            transformed_response = {
                "id": None,
                "object": "Replicate",
                "model": kwargs.get('model', 'meta/llama-2-70b-chat'),
                "choices": [{
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": response
                    },
                    "finish_reason": "finished"
                }]
            }

            return transformed_response

