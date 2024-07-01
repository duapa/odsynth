from faker import Faker

from ..core import Provider

faker = Faker()

MIN_KEY = "min"
MAX_KEY = "max"

DEFAULT_MIN_VALUE = 0
DEFAULT_MAX_VALUE = 999999


class RandomInt(Provider):
    @property
    def field_name(self):
        return self._field_name

    @field_name.setter
    def field_name(self, value):
        self._field_name = value

    @classmethod
    def get_provider_name(cls) -> str:
        return "random_int"

    def validate_kwargs(self):
        _max = None
        _min = None
        if MAX_KEY in self._kwargs:
            _max = self._kwargs[MAX_KEY]
            try:
                _max = int(_max)
            except ValueError as ve:
                raise ValueError(
                    f"An error occurred while trying to validate kwargs for provider {__class__.get_provider_name()}: {str(ve)}"
                )
        if MIN_KEY in self._kwargs:
            _min = self._kwargs[MIN_KEY]
            try:
                _min = int(_min)
            except ValueError as ve:
                raise ValueError(
                    f"An error occurred while trying to validate kwargs for provider {__class__.get_provider_name()}: {str(ve)}"
                )
        if _max is None:
            _max = DEFAULT_MAX_VALUE
        if _min is None:
            _min = DEFAULT_MIN_VALUE
        if _max < _min:
            raise ValueError(
                f"Min value {_min} cannot be greater than Max value {_max} in provider '{__class__.get_provider_name()}'"
            )
        self._max = _max
        self._min = _min

    def generate_data(self):
        self.validate_kwargs()
        return faker.random_int(min=self._min, max=self._max)
