import os

import yaml


def load_config(config_file, default=None):
    if config_file is None:
        return default
    with open(config_file, "rt") as f:
        return yaml.load(f)


def get_analysis_configs(analysis_config, path_to_config_file):
    plugin_config_list = []
    for plugin_config in analysis_config:
        if "include" in plugin_config:
            include_file_path = plugin_config["include"]
            include_file_path = os.path.abspath(os.path.join(path_to_config_file, include_file_path))
            included_configs = load_config(include_file_path, [])
            plugin_config_list.extend(get_analysis_configs(included_configs, os.path.dirname(include_file_path)))
        else:
            plugin_config_list.append(plugin_config)
    return plugin_config_list
