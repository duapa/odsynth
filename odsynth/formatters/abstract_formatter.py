from abc import ABC, abstractmethod
from typing import Any, Dict, List


class AbstractFormatter(ABC):
    """A Formatter takes generated data in odsynth.DataGenerator and
    transforms it to a desired in-memory format."""

    @abstractmethod
    def format_data(self, data: List[Dict[str, Any]]) -> Any:
        """Transforms data from odsynth.DataGenerator to a desired in-memory format.

        Parameters:
        -----------
        - data (list[dict]): Generated data from odsynth.DataGenerator

        Returns:
        ---------
        - output (Any): Formatted data
        """
        raise NotImplementedError("Subclasses must implement 'format_data' method")

    @classmethod
    @abstractmethod
    def get_name(cls) -> str:
        """Gets an identifying name for the formatter. The Formatter factory
        uses this to create a 'selector' for various Formatters
        """
        raise NotImplementedError("Subclasses must implement 'get_name' method")

    @abstractmethod
    def prepare_for_writing(self, data: List[Dict[str, Any]]) -> List[str]:
        """Prepares data from odsynth.DataGenerator for writing to a medium
        Parameters:
        -----------
        - data (list[dict]): Generated data from odsynth.DataGenerator

        Returns:
        ---------
        - output (list[str]): Prepared data
        """
        raise NotImplementedError(
            "Subclasses must implement 'prepare_for_writing' method"
        )
