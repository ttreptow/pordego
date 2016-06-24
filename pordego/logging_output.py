import traceback


def print_output(output, output_config):
    for analysis_name, failure_message, exc_info in output:
        if failure_message:
            print("Analysis '{}' failed:\n{}".format(analysis_name, failure_message))
        elif exc_info:
            print("Analysis '{}' had an error:\n".format(analysis_name))
            traceback.print_exception(*exc_info)
        else:
            print("Analysis '{}' succeeded".format(analysis_name))
