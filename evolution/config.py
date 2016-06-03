import json

grove_config = {}


def load_config(config_file_name=None):
    """
    Loads the JSON configuration file into the configuration dictionary.
    :param config_file_name: The JSON configuration file name.
    """

    with open(config_file_name, 'r') as config:

        global grove_config
        grove_config = json.load(config)


def pretty_config():
    """
    Pretty-print the configuration.
    :return: The pretty-printed string version of the configuration.
    """

    return json.dumps(grove_config, sort_keys=True, indent=4)
