from helloworld import time_message


def hello_world():
    """Print hello world with greeting based on current time."""
    _print_time_based_hello_world()


# Print good morning/afternoon/evening and hello world.
def _print_time_based_hello_world():
    print(f"{time_message.get_time_based_greeting()}, and hello, world!")
