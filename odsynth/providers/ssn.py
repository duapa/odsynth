from faker import Faker

from ..core import Provider


class SSN(Provider):
    @classmethod
    def get_provider_name(cls):
        return "ssn"

    def generate_data(self):
        faker = Faker()
        return faker.ssn()

