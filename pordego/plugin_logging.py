import logging

import sys


def setup_logging():
    _logger = logging.getLogger()
    _logger.propagate = True
    logging.captureWarnings(True)
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s"))
    _logger.addHandler(handler)
    _logger.setLevel(logging.INFO)
    return _logger
