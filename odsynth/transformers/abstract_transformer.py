from abc import ABC, abstractmethod
from typing import Any, Dict, List


class AbstractTransformer(ABC):
    """A Transformer takes generated data in odsynth.DataGenerator and
    transforms it to a desired in-memory format."""

    @abstractmethod
    def transform(self, data: List[Dict[str, Any]]) -> Any:
        """Transforms data from odsynth.DataGenerator to a desired in-memory format.

        Parameters:
        -----------
        - data (list[dict]): Generated data from odsynth.DataGenerator

        Returns:
        ---------
        - output (Any): Transformed data
        """
        raise NotImplementedError("Subclasses must implement transform method")

    @classmethod
    @abstractmethod
    def get_name(cls) -> str:
        """Gets an identifying name for the transformer. The Transformer factory
        uses this to create a 'selector' for various Transformers
        """
        raise NotImplementedError("Subclasses must implement get_name method")
