from faker import Faker

from ..core import Field

faker = Faker()

MIN_KEY = "min"
MAX_KEY = "max"

DEFAULT_MIN_VALUE = 0
DEFAULT_MAX_VALUE = 999999


class RandomInt(Field):
    """Generates an random integer"""

    @property
    def field_name(self):
        return self._field_name

    @field_name.setter
    def field_name(self, value):
        self._field_name = value

    @classmethod
    def get_name(cls) -> str:
        return "random_int"

    def validate_kwargs(self):
        _max = None
        _min = None
        if MAX_KEY in self._kwargs:
            _max = self._kwargs[MAX_KEY]
            try:
                _max = int(_max)
            except ValueError as ve:
                err_msg = (
                    "An error occurred while trying to validate kwargs for provider"
                )
                err_msg += f" {__class__.get_provider_name()}"
                err_msg += f": {str(ve)}"

                raise ValueError(err_msg)
        if MIN_KEY in self._kwargs:
            _min = self._kwargs[MIN_KEY]
            try:
                _min = int(_min)
            except ValueError as ve:
                err_msg = (
                    "An error occurred while trying to validate kwargs for provider"
                )
                err_msg += f" {__class__.get_provider_name()}"
                err_msg += f": {str(ve)}"
                raise ValueError(err_msg)
        if _max is None:
            _max = DEFAULT_MAX_VALUE
        if _min is None:
            _min = DEFAULT_MIN_VALUE
        if _max < _min:
            err_msg = (
                f"Min value {_min} cannot be greater than Max value {_max} in provider "
            )
            err_msg += __class__.get_provider_name()
            raise ValueError(err_msg)
        self._max = _max
        self._min = _min

    def generate_data(self) -> int:
        """Use Faker.random_int to generate a random integer"""
        self.validate_kwargs()
        return faker.random_int(min=self._min, max=self._max)
