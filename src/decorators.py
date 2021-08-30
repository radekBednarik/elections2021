'''Decorator funcs are here.
'''

from src.io import process_cache


def cache(**kwargs):
    """Caches the api call.

    Args:
        time_delta: (int, Optional) how long to cache and thus return cached data. Defaults to `60`.
        location: (str, Optional) location of the cache file. Defaults to `cache.tmp`
        resource_template: (str, Optional) string template to be replaced from the resource URL
        by the actual value. Defaults to `{{nuts}}`
    """

    def inner(
        func,
        time_delta: int = kwargs["time_delta"],
        location: str = kwargs["location"],
        resource_template: str = kwargs["resource_template"],
    ):
        def wrapper(*args, **kwargs):
            return process_cache(
                time_delta, location, func, resource_template, *args, **kwargs
            )

        return wrapper

    return inner
