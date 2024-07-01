from typing import Any, Dict, List


class BaseTransformer:
    def transform(self, data: List[Dict[str, Any]]):
        raise NotImplementedError("Subclasses must implement serialize method")
