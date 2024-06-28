from setuptools import find_packages, setup

from setup_utils import load_toml

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
)
