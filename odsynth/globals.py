import os

DOM_ROOT_KEY = "odsynth__dom"
XML_DOC_ROOT = "odsynth__xml__doc"
HOME = os.environ.get("ODSYNTH_HOME", None)
PROVIDERS_HOME = "providers"
TRANSFORMERS_HOME = "transformers"
WRITERS_HOME = "writers"

def get_user_plugin_folder(plugins_folder: str):
    if HOME is None:
        return None
    return f"{HOME}/{plugins_folder}"

def get_transformers_home():
    return get_user_plugin_folder(TRANSFORMERS_HOME)

def get_writers_home():
    return get_user_plugin_folder(WRITERS_HOME)

def get_providers_home():
    return get_user_plugin_folder(PROVIDERS_HOME)
