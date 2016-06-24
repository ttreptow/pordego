import logging
import sys
from argparse import ArgumentParser

from pordego.main import run_plugins
from pordego.discovery import ANALYSIS_PLUGIN_TYPE, OUTPUT_PLUGIN_TYPE, get_plugin_entry_point_names

LOG_FORMAT = " | ".join(["%(levelname)s", "%(asctime)s", "%(message)s"])


def run_analysis_plugins(args):
    run_plugins(args.config_file)


def show_plugins(args):
    print_plugins(ANALYSIS_PLUGIN_TYPE, "Analysis")
    print ""
    print_plugins(OUTPUT_PLUGIN_TYPE, "Output")


def print_plugins(plugin_type, plugin_output_name):
    print "Avaliable {} Plugins:".format(plugin_output_name)
    for plugin_name in get_plugin_entry_point_names(plugin_type):
        print plugin_name


def init_logging():
    logger = logging.getLogger()
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


def add_run_subparser(subparsers):
    parser = subparsers.add_parser("run")
    parser.add_argument("config_file")
    parser.set_defaults(func=run_analysis_plugins)


def add_show_subparser(subparsers):
    parser = subparsers.add_parser("show")
    parser.set_defaults(func=show_plugins)


def build_parser():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers()
    add_run_subparser(subparsers)
    add_show_subparser(subparsers)
    return parser


def main():
    init_logging()
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
