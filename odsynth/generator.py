from __future__ import annotations

from .core import Record
from .formatters import AbstractFormatter

PROVIDER_KEY = "provider"
PROVIDER_ARGS_KEY = "provider_args"
SUB_FIELDS_KEY = "fields"
MAX_COUNT_KEY = "max_count"
ARRAY_TYPE_MARKER = "is_array"


def convert_max_str_int(max_str: str) -> int:
    try:
        max_int = int(max_str)
        return max_int
    except ValueError:
        return 0


class DataGenerator:
    """Generates data based on a schema specification"""

    def __init__(
        self,
        object_model: Record,
        formatter: AbstractFormatter,
        num_examples: int = 10,
        batch_size: int = 5,
    ) -> None:
        """Creates a data generator

        Parameters
        -
        object_model (odsynth.core.Record):
         Object model for which data is to be generated
        num_examples (int): Number of examples to be generated
        batch_size (int): Size of batch in which data is to be generated. If the
         batch_size >= num_examples, only one batch will be created.
        formatter (AbstractFormatter): Formatter to be used to render the
         data after generation
        """
        self._num_examples = num_examples
        self._batch_size = batch_size
        self._formatter = formatter
        self._object_model = object_model

    def get_data(self):
        """Generate samples of data"""
        data_points = []
        for _ in range(self._num_examples):
            data_points.append(self._object_model.generate_data())
        if self._formatter is None:
            return data_points
        return self._formatter.format_data(data_points)

    @property
    def object_model(self):
        return self._object_model

    def yield_data(self):
        """Yield batches of data until the specified number of examples
        have all been generated."""
        num_batches, remainder = divmod(self._num_examples, self._batch_size)
        for _ in range(num_batches):
            data_points = []
            for _ in range(self._batch_size):
                data_points.append(self._object_model.generate_data())
            yield data_points
        if remainder > 0:
            data_points = []
            for _ in range(remainder):
                data_points.append(self._object_model.generate_data())
            yield data_points

    @property
    def batch_size(self) -> int:
        return self._batch_size

    @batch_size.setter
    def batch_size(self, value: int):
        self._batch_size = value

    @property
    def num_examples(self) -> int:
        return self._num_examples

    @num_examples.setter
    def num_examples(self, value: int):
        self._num_examples = value

    @property
    def formatter(self):
        return self._formatter
