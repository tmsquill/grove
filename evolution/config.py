__author__ = 'Troy Squillaci'

import json
import os


global_config = {}


def load_configs(config_files=None):

    for config_file in config_files:

        with open(config_file, 'r') as config:
            global_config[os.path.splitext(os.path.basename(config_file))[0]] = json.load(config)


def pretty_config(name=None):

    return json.dumps(global_config[name], sort_keys=True, indent=4)