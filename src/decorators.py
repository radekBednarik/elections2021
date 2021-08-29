'''Decorator funcs are here.
'''

import pickle
from datetime import datetime, timedelta
from os.path import isfile
from typing import Any


def cache(**kwargs):
    """Caches the api call.

    Args:
        time_delta: (int, Optional) how long to cache and thus return cached data. Defaults to 60.
        location: (str, Optional) location of the cache file. Defaults to cache.tmp
    """

    def inner(
        func,
        time_delta: int = kwargs["time_delta"],
        location: str = kwargs["location"],
    ):
        def wrapper(*args, **kwargs):
            if not isfile(location):
                with open(location, mode="wb") as write_handle:
                    pickle.dump(
                        {
                            "timestamp": datetime.now(),
                            "returned": func(*args, **kwargs),
                        },
                        write_handle,
                    )
                    return location

            with open(location, mode="rb") as read_handle:
                cache_data: dict[str, Any] = pickle.load(read_handle)

            now_: datetime = datetime.now()
            if now_ > (cache_data["timestamp"] + timedelta(seconds=time_delta)):
                with open(location, mode="wb") as write_handle:
                    pickle.dump(
                        {
                            "timestamp": datetime.now(),
                            "returned": func(*args, **kwargs),
                        },
                        write_handle,
                    )
                    return location

            return location

        return wrapper

    return inner
