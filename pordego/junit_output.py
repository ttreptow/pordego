import traceback

from junit_xml import TestSuite, TestCase


def write_output_file(output, output_config):
    config = JunitOutputConfig(output_config)
    test_cases = build_test_cases(output)
    write_xml(test_cases, config)


def build_test_cases(output):
    test_cases = []
    for test_name, failure_message, exc_info in output:
        test_case = TestCase(test_name)
        if failure_message:
            test_case.add_failure_info(output=failure_message)
        elif exc_info:
            test_case.add_error_info(output="".join(traceback.format_exception(*exc_info)))
        test_cases.append(test_case)
    return test_cases


def write_xml(test_cases, config):
    ts = TestSuite(config.suite_name, test_cases)
    with open(config.output_path, 'w') as f:
        TestSuite.to_file(f, [ts], prettyprint=False)


class JunitOutputConfig(object):
    def __init__(self, output_path=None, suite_name=None):
        self.output_path = output_path or "static_analysis.xml"
        self.suite_name = suite_name or "Static Analysis"
