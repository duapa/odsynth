from abc import ABC, abstractmethod
from typing import Any, Dict, List


class AbstractWriter(ABC):
    @abstractmethod
    def write_data(self, data: List[Dict[str, Any]]):
        raise NotImplementedError("'write_data' is to be implemented by its subclasses")

    @classmethod
    @abstractmethod
    def get_name(cls) -> str:
        raise NotImplementedError("'get_name' is to be implemented by its subclasses")
