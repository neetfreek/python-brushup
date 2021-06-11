from _datetime import datetime


def hello_world():
    """Print hello world with greeting based on current time."""
    _print_time_based_hello_world()


# Print good morning/afternoon/evening and hello world.
def _print_time_based_hello_world():
    print(f"{_get_message_for_current_time()}, and hello, world!")


# Return a suitable message based on the current time.
def _get_message_for_current_time():
    hour_now = datetime.now().hour
    if hour_now < 12:
        return "Good morning"
    elif hour_now < 18:
        return "Good afternoon"
    else:
        return "Good evening"


hello_world()
