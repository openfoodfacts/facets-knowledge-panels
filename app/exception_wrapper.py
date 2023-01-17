import functools
import logging


def no_exception():
    """
    Exception wrapper function,
    if an exception was raised during computation
    but we don't want to sacrifice whole result for a single failure
    as most panels depends on external resources that may not be available

    """

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception:
                issue = "exception in " + func.__name__ + "\n"
                logging.exception(issue)

        return wrapper

    return decorator
