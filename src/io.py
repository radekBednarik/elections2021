'''Handles IO operations.
'''
from typing import Any
from csv import reader

from pytomlpp import loads


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


if __name__ == "__main__":
    print(load_config())
