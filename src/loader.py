from __future__ import annotations
import importlib
from typing import List
import types
import os

plugins_dirs = []


def add_plugins_dir(plugins_dir: str) -> None:
    plugins_dirs.append(plugins_dir)


def import_module(module_name: str):
    """Import the plugin module"""
    return importlib.import_module(module_name)


def get_plugins() -> List[str]:
    plugins: List[str] = []
    for folder_name in plugins_dirs:
        for _, _, file_names in (os.walk(folder_name)):
            for file_name in file_names:
                if file_name.endswith(".py") and file_name!= "__init__.py":
                    plugins.append(f"data_generator.provider_plugins.{file_name.replace('.py','')}")
    return plugins


def load_plugins() -> None:
    plugins = get_plugins()
    """Load the plugins defined in the plugin list"""
    for plugin_name in plugins:
        plugin = import_module(plugin_name)
        plugin.initialize()


