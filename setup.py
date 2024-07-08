import toml
from setuptools import find_packages, setup


def load_toml(file_location: str):
    with open(file_location, "r") as file:
        data = toml.load(file)
        return data


config = load_toml("./setup_config.toml")

setup(
    name=config["package"]["name"],
    version=config["package"]["version"],
    description=config["package"]["description"],
    long_description=open("./README.md").read(),
    long_description_content_type="text/markdown",
    author=config["author"]["name"],
    author_email=config["author"]["email"],
    url=config["package"]["url"],
    packages=find_packages(),
    install_requires=config["install_dependencies"]["deps"],
    entry_points={"console_scripts": config["entry_points"]["scripts"]},
)
