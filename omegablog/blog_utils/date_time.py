from django.utils import timezone


def now():
    """
    Gets the current timezone aware time. This function is here for easy mocking.

    :return: The current timezone aware time
    """
    return timezone.now()

