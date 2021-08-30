'''Handles IO operations.
'''
import pickle
from csv import reader
from datetime import datetime, timedelta
from os.path import isfile
from typing import Any, Callable

from pytomlpp import loads

from src.utils import replace_substring


def load_config(filepath: str = "config.toml") -> dict[str, Any]:
    """Loads configuration file.

    Args:
        filepath (str, optional): filepath to configuration file. Defaults to "config.toml".

    Returns:
        dict[str, Any]: parsed .toml configuration file content
    """
    with open(filepath, mode="r", encoding="utf-8") as toml_file:
        return loads(toml_file.read())


def read_csv(filepath: str) -> list[list[str]]:
    """Reads csv file and return the content.

    Args:
        filepath (str): filepath to .csv file

    Returns:
        list[list[str]]: parsed content
    """
    content: list[list[str]] = []
    with open(filepath, mode="r", encoding="utf-8") as csv_file:
        csv_reader = reader(csv_file)

        for row in csv_reader:
            content.append(row)

    return content


def read_nuts(
    filepath: str = "src/classifiers/nuts.csv", header: bool = True
) -> dict[str, str]:
    """Reads NUTS.csv classifiers file and returns parsed content.

    Args:
        filepath (str, optional): filepath to nuts.csv file. Defaults to "src/classifiers/nuts.csv".
        header (bool, optional): whether data in .csv file have header row. Defaults to "True".

    Returns:
        dict[str, str]: parsed content of the nuts.csv file
    """
    content: list[list[str]] = read_csv(filepath)
    output: dict[str, str] = {}

    if header:
        content = content[1:]

    for pair in content:
        assert len(pair) == 2
        nuts, county = pair
        if hasattr(output, nuts):
            raise KeyError(
                f"Record with {nuts} NUTS key was already found before. This value must be unique!."
            )
        output[nuts] = county

    return output


def process_cache(
    time_delta: int,
    cache_location: str,
    func: Callable,
    resource_template: str,
    *args,
    **kwargs,
):

    resource_url: str = replace_substring(
        kwargs["resource"], kwargs["nuts"], resource_template
    )
    cache: dict[str, Any] = {}

    if not isfile(cache_location):
        cache[resource_url] = {}
        cache[resource_url]["timestamp"] = datetime.now()
        cache[resource_url]["returned"] = func(*args, **kwargs)
        with open(cache_location, mode="wb") as write_handle:
            pickle.dump(cache, write_handle)
            return cache[resource_url]["returned"]

    with open(cache_location, mode="rb") as read_handle:
        cache = pickle.load(read_handle)

    if resource_url not in list(cache.keys()):
        cache[resource_url] = {}
        cache[resource_url]["timestamp"] = datetime.now()
        cache[resource_url]["returned"] = func(*args, **kwargs)
        with open(cache_location, mode="wb") as write_handle:
            pickle.dump(cache, write_handle)
            return cache[resource_url]["returned"]

    now_: datetime = datetime.now()

    if now_ > (cache[resource_url]["timestamp"] + timedelta(seconds=time_delta)):
        cache[resource_url]["timestamp"] = datetime.now()
        cache[resource_url]["returned"] = func(*args, **kwargs)
        with open(cache_location, mode="wb") as write_handle:
            pickle.dump(cache, write_handle)
            return cache[resource_url]["returned"]

    return cache[resource_url]["returned"]
