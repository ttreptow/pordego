from logging import getLogger

from pkg_resources import iter_entry_points
import yaml

logger = getLogger(__name__)


ALL_PLUGINS = "all"


def run_plugins(config_file_path, plugins_to_run=None):
    config = load_config(config_file_path)
    plugin_config_dict = prepare_plugin_config(config.get("plugins"))
    plugin_eps = get_plugin_entry_points()
    execute_plugins(plugin_eps, plugin_config_dict, plugins_to_run)


def get_plugin_entry_points():
    return {ep.name: ep for ep in iter_entry_points("pordego.analysis")}


def get_plugin_entry_point_names():
    return [ep.name for ep in iter_entry_points("pordego.analysis")]


def load_config(config_file):
    with open(config_file) as f:
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
            plugin_config_dict = {plugin_config["name"]: plugin_config for plugin_config in plugin_config_list["plugins"]}
        except KeyError:
            raise Exception("Plugin configuration is missing mandatory 'name' field")
    return plugin_config_dict


def execute_plugins(prepared_plugins, plugin_config_dict, plugins_to_run=None):
    """
    Executes the analysis plugins

    :param prepared_plugins:
    :param plugin_config_dict:
    :param plugins_to_run: If specified, only plugins in this list are executed in order, otherwise all plugins are executed
    :return:
    """
    if plugins_to_run is None or ALL_PLUGINS in plugins_to_run:
        plugins_to_run = prepared_plugins.keys()
    for plugin_name in plugins_to_run:
        if plugin_name not in prepared_plugins:
            raise Exception("Invalid plugin specified: {}".format(plugin_name))
        plugin_func = prepared_plugins[plugin_name].ep.load()
        logger.info("Executing plugin %s", plugin_name)
        plugin_func(plugin_config_dict.get(plugin_name))
