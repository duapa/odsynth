from faker import Faker

from odsynth.core import Provider
from odsynth.providers import ProviderFactory


class SSN(Provider):
    @classmethod
    def get_name(cls):
        return "com.github.kbaafi.us_ssn"

    def generate_data(self):
        faker = Faker()
        return faker.ssn()


def initialize():
    ProviderFactory.register_provider(SSN)
