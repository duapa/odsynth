from abc import ABC, abstractmethod
from typing import Any, Dict, List


class AbstractTransformer(ABC):
    @abstractmethod
    def transform(self, data: List[Dict[str, Any]]):
        raise NotImplementedError("Subclasses must implement serialize method")
