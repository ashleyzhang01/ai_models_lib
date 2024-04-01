class BaseModel:
    def __init__(self, api_key):
        self._api_key = api_key

    def set_api_key(self, api_key):
        self._api_key = api_key

    def query(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement this method.")
