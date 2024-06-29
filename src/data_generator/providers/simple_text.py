from faker import Faker

from ..core import Primitive

DEFAULT_TEXT_MAX_NB_CHARS = 20

faker = Faker()


def str_to_int(int_str: str) -> int:
    try:
        int_repr = int(int_str)
        return int_repr
    except ValueError:
        return 0


class Text(Primitive):
    @classmethod
    def get_provider_name(cls) -> str:
        return "text"

    def validate_kwargs(self):
        if (
            "max_nb_chars" in self.provider_kwargs
            and str_to_int(self.provider_kwargs["max_nb_chars"]) > 0
        ):
            self._max_nb_chars = str_to_int(self.provider_kwargs["max_nb_chars"])
        else:
            self._max_nb_chars = DEFAULT_TEXT_MAX_NB_CHARS

    def generate_data(self):
        self.validate_kwargs()
        return faker.text(max_nb_chars=self._max_nb_chars)


class FirstName(Primitive):
    @classmethod
    def get_provider_name(cls) -> str:
        return "first_name"

    def generate_data(self):
        return faker.first_name()


class LastName(Primitive):
    @classmethod
    def get_provider_name(cls) -> str:
        return "last_name"

    def generate_data(self):
        return faker.last_name()
