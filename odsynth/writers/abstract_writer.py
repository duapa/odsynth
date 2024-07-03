from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from ..transformers import AbstractTransformer


class AbstractWriter(ABC):
    @abstractmethod
    def write_data(self, data: List[Dict[str, Any]]):
        raise NotImplementedError("'write_data' is to be implemented by its subclasses")
