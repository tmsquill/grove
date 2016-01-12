import json
import os


global_config = {}

nodes = ['10.0.0.30', '10.0.0.31', '10.0.0.32', '10.0.0.33', '10.0.0.34', '10.0.0.35', '10.0.0.36']

def load_configs(config_files=None):
    """
    Loads a JSON configuration file into a dictionary.
    :param config_files: The filename containing a JSON configuration.
    """

    for config_file in config_files:

        with open(config_file, 'r') as config:
            global_config[os.path.splitext(os.path.basename(config_file))[0]] = json.load(config)


def pretty_config(name=None):
    """
    Pretty-print a configuration in the global dictionary determined by the base name.
    :param name: The base name of the configuration.
    :return: The pretty-printed string version of the configuration.
    """

    return json.dumps(global_config[name], sort_keys=True, indent=4)
