import os

DOM_ROOT_KEY = "odsynth__record"
XML_DOC_ROOT = "odsynth__xml__doc"
HOME = os.environ.get("ODSYNTH_HOME", None)
PROVIDERS_HOME = "providers"
FORMATTERS_HOME = "formatters"
WRITERS_HOME = "writers"
DEFAULT_OUTPUT_SUBDIR = "odsynth__output"
SCHEMA_PROVIDER_KEY = "provider"
SCHEMA_SUB_FIELDS_KEY = "fields"
SCHEMA_PROVIDER_ARGS_KEY = "provider_args"
SCHEMA_MAX_COUNT_KEY = "max_count"
SCHEMA_ARRAY_TYPE_MARKER = "is_array"


def get_user_plugin_folder(plugins_folder: str):
    if HOME is None:
        return None
    return f"{HOME}/{plugins_folder}"


def get_formatters_home():
    return get_user_plugin_folder(FORMATTERS_HOME)


def get_writers_home():
    return get_user_plugin_folder(WRITERS_HOME)


def get_providers_home():
    return get_user_plugin_folder(PROVIDERS_HOME)
