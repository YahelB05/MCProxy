from dataclasses import dataclass
from typing import List, Optional
import json
from enum import Enum, auto


class HttpMethod(Enum):
    GET = auto()
    POST = auto()
    PUT = auto()

    @classmethod
    def value_of(cls, value):
        for k, v in cls.__members__.items():
            if k == value:
                return v
        else:
            raise ValueError(f"'{cls.__name__}' enum not found for '{value}'")


@dataclass
class Param:
    field: str
    type: str

    @classmethod
    def from_dict(cls, data: dict) -> 'Param':
        return cls(**data)

@dataclass
class Endpoint:
    name: str
    description: str
    url: str
    method: HttpMethod
    path_params: Optional[List[Param]] = None
    query_params: Optional[List[Param]] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'Endpoint':
        path_params = [Param.from_dict(p) for p in data.get("path_params", [])]
        query_params = [Param.from_dict(p) for p in data.get("query_params", [])]
        return cls(
            name=data["name"],
            description=data["description"],
            url=data["url"],
            method=HttpMethod.value_of(data["method"]),
            path_params=path_params,
            query_params=query_params
        )

@dataclass
class ApiConfig:
    version: str
    endpoints: List[Endpoint]

    @classmethod
    def from_json(cls, json_str: str) -> 'ApiConfig':
        try:
            data = json.loads(json_str)
            endpoints = [Endpoint.from_dict(e) for e in data["endpoints"]]
            return cls(
                version=data["version"],
                endpoints=endpoints
            )
        except (KeyError, TypeError, json.JSONDecodeError) as e:
            raise ValueError(f"Invalid API config JSON: {e}") from e
