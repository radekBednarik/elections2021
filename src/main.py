'''Main.
'''

from argparse import ArgumentParser, Namespace
from typing import Any
from src.api import get_county_data
from src.cli import create_parser, create_subparsers, parse
from src.io import load_config
from src.parser import parse_county_data, parse_xml


config = load_config()
resource_county = config["api"]["resources"]["vysledky_okresy_obce"]


def main():
    parser: ArgumentParser = create_parser()
    parser = create_subparsers(parser)
    parsed: Namespace = parse(parser)

    print(parsed)

    if parsed.nuts:
        status, raw_data = get_county_data(nuts=parsed.nuts, resource=resource_county)

        if status:
            status, parsed_data = parse_xml(raw_data)

            if status:
                print(parsed_data)


if __name__ == "__main__":
    main()
