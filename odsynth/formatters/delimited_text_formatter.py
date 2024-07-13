from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List

from odsynth.core.object_model import Record

from .base_formatter import BaseFormatter
from .exceptions import ObjectModelValidationException


def get_delimiter(enum_str):
    try:
        return DelimitedTextFormats[enum_str]
    except KeyError:
        raise ValueError(
            f"{enum_str} is not a valid member of {DelimitedTextFormats.__name__}"
        )


class DelimitedTextFormats(Enum):
    comma = (",", "csv")
    pipe = ("|", "txt")
    tab = ("\t", "tsv")


class DelimitedTextFormatter(BaseFormatter):
    def __init__(self, object_model: Record, delimiter: str = "comma") -> None:
        self._object_model = object_model
        if not self.validate_object_model():
            raise ObjectModelValidationException(
                "Expected a tabular and non-nested schema"
            )
        self._delimiter = get_delimiter(delimiter)

    def validate_object_model(self):
        if self._object_model.depth != 2:
            return False
        return True

    @classmethod
    def get_name(cls) -> str:
        return "txt"

    def format_data(self, data: List[Dict[str, Any]]) -> List[str]:
        def values_to_str(values: List[Any]):
            strings = []
            for item in values:
                strings.append(str(item))
            return strings

        list_txt_str = []
        for item in data:
            values = values_to_str(list(item.values()))
            delimiter = self._delimiter.value[0]
            txt_str = delimiter.join(values)
            list_txt_str.append(txt_str)
        return list_txt_str

    def prepare_for_writing(self, data: List[Dict[str, Any]]) -> List[str]:
        fields = []
        delimiter = self._delimiter.value[0]
        for item in self._object_model.children:
            fields.append(item.field_name)
        header = [delimiter.join(fields)]
        output = header + self.format_data(data)
        return output

    @property
    def file_extension(self):
        return self._delimiter.value[1]
