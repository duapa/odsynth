from ..core import Primitive
from faker import Faker

faker = Faker()


class Text(Primitive):
    @classmethod
    def get_provider_name(cls) -> str:
        return "str"

    def generate_data(self):
        return faker.text(max_nb_chars=20)
    

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