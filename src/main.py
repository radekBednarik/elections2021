"""Main.
"""

from argparse import Namespace
from src.api import get_county_data, get_state_data
from src.cli import create_parser, create_subparsers, parse
from src.io import load_config
from src.parser import parse_county_data, parse_state_data, parse_xml
from src.output import enable_coloring, print_colored_data

config = load_config()
resource_county = config["api"]["resources"]["vysledky_okresy_obce"]
resource_state = config["api"]["resources"]["vysledky_stat_kraje"]


def main():
    """Main func."""

    enable_coloring()
    parsed: Namespace = parse(create_subparsers(create_parser()))

    if hasattr(parsed, "nuts"):
        city_name = parsed.name if parsed.name is not None else None
        # this API call is cached!
        status, raw_data = get_county_data(nuts=parsed.nuts, resource=resource_county)

        if status:
            status, parsed_data = parse_xml(raw_data)

            if status:
                county_data = parse_county_data(parsed_data, city=city_name)
                print_colored_data(county_data)

    if hasattr(parsed, "district"):
        status, raw_data = get_state_data(resource=resource_state)

        if status:
            status, parsed_data = parse_xml(raw_data)

            if status:
                state_data = parse_state_data(parsed_data)
                print_colored_data(state_data)


if __name__ == "__main__":
    main()
