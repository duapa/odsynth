from abc import ABC, abstractmethod
from typing import Any, Dict, List


class AbstractTransformer(ABC):
    @abstractmethod
    def transform(self, data: List[Dict[str, Any]]):
        raise NotImplementedError("Subclasses must implement transform method")

    @classmethod
    @abstractmethod
    def get_name(cls) -> str:
        raise NotImplementedError("Subclasses must implement get_name method")
