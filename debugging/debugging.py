#!/usr/bin/env python
import logging
import traceback
from datetime import datetime

logging.basicConfig(filename=f"debuggingLog.log", level=logging.DEBUG,
                    format=" %(asctime)s - %(levelname)s - %(message)s")

"""Exception examples"""


def _exception_write_example():
    # Example of writing raised error to file
    logging.debug("START _exception_write_example")
    try:
        raise IndexError("This is an example Index Error")
    except IndexError:
        error_file = open(f"errorInfo_"
                          f"{_get_formatted_timestamp(datetime.now())}"
                          f".txt", "w")
        error_file.write(traceback.format_exc())
        print(f"Exception raised, please refer to {error_file.name}")
        error_file.close()
    logging.info("END _exception_write_example")


def _assert_example():
    # Simple assertion examples, if unmet, AssertionError is raised
    logging.debug("START _assert_example")
    ages = [12, 43, 32, 67, 54, 21, 54, 65, 21, 11]
    ages.sort()
    ages_reversed = ages[::-1]

    assert ages[0] < ages[-1]
    assert ages_reversed[0] > ages_reversed[-1]
    logging.info("END _assert_example")


"""Helpers"""


def _get_formatted_timestamp(time_now):
    # Return ISO8601-formatted timestamp for filenames
    logging.debug("START _get_formatted_timestamp(%s%%)" % time_now)
    time_stamp = time_now.isoformat()
    time_stamp = time_stamp.replace(":", "")
    time_stamp = time_stamp[:time_stamp.index(".")]
    logging.info("END _get_formatted_timestamp(%s%%)" % time_stamp)

    return time_stamp


"""Main"""


def main():
    """Demonstrate debugging and error-handling fundamentals"""
    logging.debug("START main")
    _assert_example()
    # _exception_write_example()
    logging.info("END main\n\n")


main()
