import json
import time
from typing import Any, Dict, List

from odsynth.transformers import JsonTransformer

from .abstract_writer import AbstractWriter


class JsonToDiscWriter(AbstractWriter):
    def __init__(self, base_dir):
        self._base_dir = base_dir
        self._transformer = JsonTransformer()

    def write_data(self, data: List[Dict[str, Any]]):
        timestamp = int(time.time() * 1e6)
        filename = f"{self._base_dir}/odsynth_{timestamp}.json"
        with open(filename, "w") as file:
            for item in self._transformer.transform(data):
                file.write(item)
                file.write("\n")
