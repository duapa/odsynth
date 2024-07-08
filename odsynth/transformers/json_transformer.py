import json
from typing import Any, Dict, List

from .abstract_transformer import AbstractTransformer


class JsonTransformer(AbstractTransformer):
    """Takes data generated in odsynth.DataGenerator and
    transforms it to JSON."""

    def transform(self, data: List[Dict[str, Any]]):
        """Transforms data from odsynth.DataGenerator to JSON.

        Parameters:
        -----------
        - data (list[dict]): Generated data from odsynth.DataGenerator

        Returns:
        --------
        output (list[str]): Data transformed into a list of json strings.
        """
        list_json_str: List[str] = []
        for item in data:
            list_json_str.append(json.dumps(item))
        return list_json_str

    @classmethod
    def get_name(cls) -> str:
        return "json"
