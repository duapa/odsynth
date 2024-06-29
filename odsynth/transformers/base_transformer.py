from typing import List, Dict, Any

class BaseTransformer:
    def transform(self, data:List[Dict[str, Any]]):
        raise NotImplementedError("Subclasses must implement serialize method")