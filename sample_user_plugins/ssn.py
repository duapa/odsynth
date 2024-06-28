from faker import Faker

import data_generator.factory as factory
from data_generator.core import Primitive


class SSN(Primitive):
    @classmethod
    def get_provider_name(cls):
        return "com.github.kbaafi.us_ssn"

    def generate_data(self):
        faker = Faker()
        return faker.ssn()


def initialize():
    factory.register_provider(SSN.get_provider_name(), SSN())
