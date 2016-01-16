import json
import os


global_config = {}


def load_configs(config_files=None):
    """
    Loads JSON configuration file(s) into the global configuration dictionary.
    :param config_files: The list of JSON configuration filenames.
    """

    for config_file in config_files:

        with open(config_file, 'r') as config:

            # Keys of the top-level dictionary are configuration filenames.
            global_config[os.path.splitext(os.path.basename(config_file))[0]] = json.load(config)


def pretty_config(name=None):
    """
    Pretty-print a configuration in the global dictionary determined by the base name.
    :param name: The base name of the configuration.
    :return: The pretty-printed string version of the configuration.
    """

    return json.dumps(global_config[name], sort_keys=True, indent=4)
