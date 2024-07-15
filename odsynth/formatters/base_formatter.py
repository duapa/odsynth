from typing import Any, Dict, List

from ..core import DataElement
from .abstract_formatter import AbstractFormatter
from .exceptions import DataWritePreparationException, ObjectModelValidationException


class BaseFormatter(AbstractFormatter):
    def __init__(self, object_model: DataElement) -> None:
        self._object_model = object_model
        if not self.validate_object_model():
            raise ObjectModelValidationException(
                "Could not validate the object model: Check if schema is well formed"
            )

    def validate_object_model(self):
        return True if self.object_model.depth >= 2 else False

    @property
    def object_model(self):
        return self._object_model

    @classmethod
    def get_name(cls) -> str:
        return "default"

    def format_data(self, data: List[Dict[str, Any]]) -> Any:
        return data

    def prepare_for_writing(self, data: List[Dict[str, Any]]) -> List[str]:
        raise DataWritePreparationException(
            "File write operations are not supported for BaseFormatters"
        )

    @property
    def file_extension(self):
        raise DataWritePreparationException(
            "File write operations are not supported for BaseFormatters"
        )
