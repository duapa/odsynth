from faker import Faker

from odsynth.core import Provider
from odsynth.provider_factory import ProviderFactory


class SSN(Provider):
    @classmethod
    def get_provider_name(cls):
        return "com.github.kbaafi.us_ssn"

    def generate_data(self):
        faker = Faker()
        return faker.ssn()


def initialize():
    ProviderFactory.register_provider(SSN.get_provider_name(), SSN())
