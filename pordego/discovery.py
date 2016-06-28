from pkg_resources import iter_entry_points

ANALYSIS_PLUGIN_TYPE = "analysis"
OUTPUT_PLUGIN_TYPE = "output"


def get_plugin_entry_points(plugin_type):
    return {ep.name: ep for ep in iter_entry_points("pordego.{}".format(plugin_type))}


def get_plugin_entry_point_names(plugin_type):
    return sorted([ep.name for ep in get_plugin_entry_points(plugin_type).values()])
