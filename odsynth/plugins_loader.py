from __future__ import annotations

import importlib
import os
import types
from typing import List

USER_PLUGINS_NAMESPACE = "user_providers"


class DirectoryNotFoundException(Exception):
    def __init__(self, *args: object) -> types.NoneType:
        super().__init__(*args)


def get_plugin_files(plugin_folder_name: str = None) -> List[str]:
    plugins: List[str] = []
    if plugin_folder_name and os.path.exists(plugin_folder_name) and os.path.isdir(plugin_folder_name):
        for _, _, file_names in os.walk(plugin_folder_name):
            for file_name in file_names:
                if file_name.endswith(".py") and file_name != "__init__.py":
                    plugins.append(f"{plugin_folder_name}/{file_name}")
    else:
        raise DirectoryNotFoundException(
            f"An error occured while trying to read user provided plugins. Plugin folder: {plugin_folder_name} not found."
        )
    return plugins


def load_plugins(plugin_folder_name: str) -> None:
    """Load the plugins defined in the plugin list"""

    plugins = get_plugin_files(plugin_folder_name)

    for plugin in plugins:

        module_name = plugin.split("/")[-1].replace(".py", "")
        module_name = f"{USER_PLUGINS_NAMESPACE}.{module_name}"

        loader = importlib.machinery.SourceFileLoader(module_name, plugin)
        spec = importlib.util.spec_from_loader(name=loader.name, loader=loader)

        module = importlib.util.module_from_spec(spec)
        loader.exec_module(module)
        module.initialize()
