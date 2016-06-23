import sys
from argparse import ArgumentParser

from pordego.main import run_plugins, get_plugin_entry_point_names, ALL_PLUGINS

PLUGIN_NAMES = get_plugin_entry_point_names() + [ALL_PLUGINS]


def build_parser():
    parser = ArgumentParser()
    parser.add_argument("plugins", nargs="*", choices=PLUGIN_NAMES, default=ALL_PLUGINS)
    parser.add_argument("-c", "--config", dest="config_file", required=True)
    return parser


def run_analysis_plugins(args):
    run_plugins(args.config_file, args.plugins)


def main():
    parser = build_parser()
    args = parser.parse_args()
    run_analysis_plugins(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
