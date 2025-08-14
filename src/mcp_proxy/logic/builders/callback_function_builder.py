import requests


class EndpointHttpCaller:
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def __call__(self, **kwargs) -> str:
        url = self._build_url_with_path_params(kwargs)
        method = self.endpoint.method.name.upper()
        query_params = self._extract_query_params(kwargs)

        if method == "GET":
            response = requests.get(url, params=query_params)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        response.raise_for_status()
        return response.text

    def _build_url_with_path_params(self, kwargs: dict) -> str:
        url = self.endpoint.url
        for param in self.endpoint.path_params or []:
            key = param.field
            if key in kwargs:
                url = url.replace(f"{{{key}}}", str(kwargs[key]))
        return url

    def _extract_query_params(self, kwargs: dict) -> dict:
        query = {}
        for param in self.endpoint.query_params or []:
            key = param.field
            if key in kwargs:
                query[key] = kwargs[key]
        return query
