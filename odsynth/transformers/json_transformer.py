import json
from typing import Any, Dict, List

from .abstract_transformer import AbstractTransformer


class JsonTransformer(AbstractTransformer):
    def transform(self, data: List[Dict[str, Any]]):
        list_json_str: List[str] = []
        for item in data:
            list_json_str.append(json.dumps(item))
        return list_json_str

    @classmethod
    def get_name(cls) -> str:
        return "json"
