# pylint: disable=expression-not-assigned

"""Handles output of data in the console.
"""
from subprocess import CompletedProcess, run
from sys import platform
from typing import Any, Optional, Union

from colorama import Fore, Style, init


def clear_screen() -> Optional[CompletedProcess]:
    """Clears the console."""
    if platform.startswith("linux"):
        return run("clear", shell=True, check=True)

    if platform.startswith("win32"):
        return run("cls", shell=False, check=True)

    return None


def enable_coloring() -> None:
    """Starts the coloring using Colorama.

    Should be called at the beginning of the `main()`.

    See https://github.com/tartley/colorama#initialisation
    """
    init()


def color_green(string: str) -> str:
    """Colors the string GREEN.

    Args:
        string (str): string to be colored green.

    Returns:
        str: colored string
    """
    return f"{Fore.GREEN}{string}{Style.RESET_ALL}"


def color_blue(string: str) -> str:
    """Colors the string BLUE.

    Args:
        string (str): string to be colored

    Returns:
        str: colored string
    """
    return f"{Fore.BLUE}{string}{Style.RESET_ALL}"


def color_cyan(string: str) -> str:
    """Colors the string CYAN.

    Args:
        string (str): string to be colored

    Returns:
        str: colored string
    """
    return f"{Fore.CYAN}{string}{Style.RESET_ALL}"


def print_colored_data(data: Union[dict[str, Any], list[Any]]) -> None:
    """Stdout colored `data` dict.

    Args:
        data (Union[dict[str, Any], list[Any]]): data dict to be recursively
        stdout to console.
    """
    if isinstance(data, dict):
        items = list(data.items())

        for key, value in items:
            if not isinstance(value, (dict, list)):
                print(color_cyan(key), "::", color_green(value))

            print_colored_data(value)

    if isinstance(data, list):
        for item in data:
            print_colored_data(item)
            print("-------------")
