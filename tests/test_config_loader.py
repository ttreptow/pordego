import os
import unittest

from pordego.config_loader import get_analysis_configs, load_config

PATH_TO_DATA_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data")


class TestConfigLoader(unittest.TestCase):
    def test_include_config(self):
        """Include files and recursively included files should resolve correctly"""
        analysis_config = load_config(os.path.join(PATH_TO_DATA_DIR, "test_config_include.yml"))["analysis"]
        configs = get_analysis_configs(analysis_config, PATH_TO_DATA_DIR)
        self.assertEqual([{'config_val': 1, 'plugin_name': 'sub_test'},
                          {'sub_sub_config1': 2, 'plugin_name': 'sub_sub_test'}], configs)
