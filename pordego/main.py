import os
import sys
from logging import getLogger

from pordego.config_loader import load_config, get_analysis_configs
from pordego.discovery import ANALYSIS_PLUGIN_TYPE, get_plugin_entry_points, OUTPUT_PLUGIN_TYPE
from pordego.plugin_logging import setup_logging

setup_logging()
logger = getLogger(__name__)


def run_plugins(config_file_path):
    """
    Run all plugins. This is the entry point to pordego when being used programatically

    :param config_file_path: Path to the configuration file
    :return:
    """
    config = load_config(config_file_path, {})
    analysis_eps = get_plugin_entry_points(ANALYSIS_PLUGIN_TYPE)
    plugin_config_list = get_analysis_configs(config.get("analysis"), os.path.dirname(config_file_path))
    analysis_results = execute_plugins(analysis_eps, plugin_config_list, execute_analysis_function)
    output_eps = get_plugin_entry_points(OUTPUT_PLUGIN_TYPE)
    execute_plugins(output_eps, config.get("output", []), execute_output_function, analysis_results)
    return analysis_results


def execute_plugins(plugin_entry_points, plugin_config_list, execute_func, *execute_args):
    """
    Executes the analysis plugins

    :param plugin_entry_points: a dictionary of plugin name to pkg_resources.EntryPoint
    :param plugin_config_list: list of plugin configurations
    :param execute_func: Function to call with
    :param execute_args: arguments to add to execute_func
    """
    if plugin_config_list is None:
        raise Exception("No plugin configuration specified!")
    output = []
    for plugin_config in plugin_config_list:
        try:
            plugin_name = plugin_config.pop("plugin_name")
        except KeyError:
            raise Exception("Plugin configuration is missing mandatory 'plugin_name' field")
        if plugin_name not in plugin_entry_points:
            raise Exception("Invalid plugin specified: {}".format(plugin_name))
        plugin_func = plugin_entry_points[plugin_name].load()
        logger.info("Executing plugin %s", plugin_name)
        output.append(execute_func(plugin_name, plugin_func, plugin_config, *execute_args))
    return output


def execute_analysis_function(plugin_name, plugin_func, plugin_config):
    failure_message = None
    exc_info = None
    try:
        plugin_func(plugin_config)
    except AssertionError as e:
        failure_message = str(e)
    except Exception:
        exc_info = sys.exc_info()
    return plugin_config.get("name", plugin_name), failure_message, exc_info


def execute_output_function(plugin_name, plugin_func, plugin_config, analysis_results):
    try:
        plugin_func(analysis_results, plugin_config)
    except Exception:
        logger.exception("Output plugin %s failed", plugin_name)

