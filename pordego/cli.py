import logging
import sys
from argparse import ArgumentParser

from pordego.main import run_plugins, get_plugin_entry_point_names

LOG_FORMAT = " | ".join(["%(levelname)s", "%(asctime)s", "%(message)s"])


def run_analysis_plugins(args, logger):
    try:
        run_plugins(args.config_file)
    except AssertionError:
        sys.exit(-1)
    except Exception:
        logger.exception("Plugin error")
        sys.exit(-2)


def show_plugins(args, logger):
    print "Available Plugins:"
    for plugin_name in get_plugin_entry_point_names():
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
    logger = init_logging()
    parser = build_parser()
    args = parser.parse_args()
    args.func(args, logger)
    return 0


if __name__ == "__main__":
    sys.exit(main())
