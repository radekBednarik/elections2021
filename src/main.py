"""Main.
"""

from argparse import Namespace
from src.api import get_county_data
from src.cli import create_parser, create_subparsers, parse
from src.io import load_config
from src.parser import parse_county_data, parse_xml
from src.output import enable_coloring, print_colored_data

config = load_config()
resource_county = config["api"]["resources"]["vysledky_okresy_obce"]


def main():
    """Main func."""

    enable_coloring()
    parsed: Namespace = parse(
        create_subparsers(create_parser()), ["county", "CZ0100", "--name=Praha 1"]
    )

    if parsed.nuts:
        city_name = parsed.name if parsed.name is not None else None
        # this API call is cached!
        status, raw_data = get_county_data(nuts=parsed.nuts, resource=resource_county)

        if status:
            status, parsed_data = parse_xml(raw_data)

            if status:
                county_data = parse_county_data(parsed_data, city=city_name)
                print_colored_data(county_data)


if __name__ == "__main__":
    main()
