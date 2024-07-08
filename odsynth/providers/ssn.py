from faker import Faker

from ..core import Field


class SSN(Field):
    """Generates Social Security Numbers using Faker's `ssn` module"""

    @classmethod
    def get_name(cls):
        return "ssn"

    def generate_data(self):
        """Generate Social Security Number

        Returns
        -
        output (str): Generated Social Security Number
        """

        faker = Faker()
        return faker.ssn()
