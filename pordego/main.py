from logging import getLogger

from pkg_resources import iter_entry_points
import yaml

logger = getLogger(__name__)


def run_plugins(config_file_path):
    config = load_config(config_file_path)
    plugin_eps = get_plugin_entry_points()
    execute_plugins(plugin_eps, config.get("plugins"))


def get_plugin_entry_points():
    return {ep.name: ep for ep in iter_entry_points("pordego.analysis")}


def get_plugin_entry_point_names():
    return [ep.name for ep in iter_entry_points("pordego.analysis")]


def load_config(config_file):
    if config_file is None:
        return {}
    with open(config_file, "rt") as f:
        return yaml.load(f)


def prepare_plugin_config(plugin_config_list):
    """
    Converts a list of plugin configuration dicts into a dictionary of plugin configs and checks for
    the existance of the "name" attribute

    :param plugin_config_list: List of plugin configuration dictionaries
    :return: dictionary of plugin name to plugin config dict
    """
    plugin_config_dict = {}
    if plugin_config_list:
        try:
            plugin_config_dict = {plugin_config.pop("name"): plugin_config for plugin_config in plugin_config_list}
        except KeyError:
            raise Exception("Plugin configuration is missing mandatory 'name' field")
    return plugin_config_dict


def execute_plugins(plugin_entry_points, plugin_config_list):
    """
    Executes the analysis plugins

    :param plugin_entry_points: a dictionary of plugin name to pkg_resources.EntryPoint
    :param plugin_config_list: list of plugin configurations
    """
    if plugin_config_list is None:
        raise Exception("No plugin configuration specified!")
    for plugin_config in plugin_config_list:
        try:
            plugin_name = plugin_config.pop("name")
        except KeyError:
            raise Exception("Plugin configuration is missing mandatory 'name' field")
        if plugin_name not in plugin_entry_points:
            raise Exception("Invalid plugin specified: {}".format(plugin_name))
        plugin_func = plugin_entry_points[plugin_name].load()
        logger.info("Executing plugin %s", plugin_name)
        try:
            plugin_func(plugin_config)
        except AssertionError as e:
            logger.error("Plugin %s assertion error:\n%s", plugin_name, e)
            raise
