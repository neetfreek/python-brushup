from _datetime import datetime


def get_time_based_greeting():
    """Return appropriate greeting for the current time."""
    return _get_message_for_current_time()


# Return a suitable message based on the current time.
def _get_message_for_current_time():
    hour_now = datetime.now().hour
    if hour_now < 12:
        return "Good morning"
    elif hour_now < 18:
        return "Good afternoon"
    else:
        return "Good evening"
