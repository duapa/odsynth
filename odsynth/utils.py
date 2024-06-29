import yaml


def load_yaml(file_location: str):
    with open(file_location, "r") as file:
        data = yaml.safe_load(file)
        return data
