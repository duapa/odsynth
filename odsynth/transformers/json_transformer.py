import json
from typing import Any, Dict, List

from .base_transformer import BaseTransformer


class JsonTransformer(BaseTransformer):
    def transform(self, data: List[Dict[str, Any]]):
        return json.dumps(data)
