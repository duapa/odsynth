from typing import Any, Dict
from ..core.object_model import Field
from faker import Faker


class FakerGeneratorException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class FakerField(Field):
    @classmethod
    def get_name(cls) -> str:
        return "faker"
    
    def __init__(self, **kwargs):
        self._faker_locales = kwargs.get("locales", None)
        self._faker_command = self.validate_inputs(kwargs)
        self._faker_kwargs = {k:v for k,v in kwargs.items() if k not in ["locales", "faker_type"]}

    def validate_inputs(self, inputs: Dict[str, Any]):
        if "faker_type" not in inputs:
            raise FakerGeneratorException(
                "Expected a 'faker_type' for generating data using Faker"
            )
        try:
            if self._faker_locales:
                self._faker = Faker(self._faker_locales)
            else:
                self._faker = Faker()
        except Exception as exc:
            msg = f"Could not create Faker using given locales: {self._faker_locales} "
            raise FakerGeneratorException(f"{msg}. Details: {str(exc)}")
        try:
            faker_type = inputs.get('faker_type')
            return getattr(self._faker, faker_type)
        except AttributeError:
            raise FakerGeneratorException(
                f"Faker does not expose a generator for  '{faker_type}'"
            )
    
    def generate_data(self) -> Any:
        return self._faker_command(**self._faker_kwargs)