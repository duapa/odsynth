import json
from typing import Any, Dict, List

from .base_formatter import BaseFormatter


class JsonFormatter(BaseFormatter):
    """Takes data generated in odsynth.DataGenerator and
    transforms it to JSON."""

    def format_data(self, data: List[Dict[str, Any]]):
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

    def prepare_for_writing(self, data: List[Dict[str, Any]]) -> List[str]:
        return self.format_data(data=data)

    @property
    def file_extension(self):
        return __class__.get_name()
