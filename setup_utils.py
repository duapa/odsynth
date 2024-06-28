import toml


def load_toml(file_location: str):
    with open(file_location, "r") as file:
        data = toml.load(file)
        return data
