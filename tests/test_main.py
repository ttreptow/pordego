import unittest

from pordego.main import prepare_plugin_config


class TestPordego(unittest.TestCase):
    def test_prepare_plugin_config_null_config(self):
        """Return an empty dictionary if the plugin config is None"""
        self.assertEqual({}, prepare_plugin_config(None))

    def test_prepare_plugin_config(self):
        """Return a dictionary of plugin configurations generated from the list of configs"""
        config = [{"name": "my_plugin", "key1": "value1"}]
        expected_dict = {"my_plugin": {"key1": "value1"}}
        result = prepare_plugin_config(config)
        self.assertNotIn("name", result["my_plugin"], "prepare_plugin_config should strip 'name' parameter")
        self.assertDictEqual(result, expected_dict)

    def test_prepare_plugin_config_no_name(self):
        """Raise an error if one of the plugin configs does not have a "name" parameter"""
        bad_config = [{"some": "value"}]
        self.assertRaises(Exception, prepare_plugin_config, bad_config)

