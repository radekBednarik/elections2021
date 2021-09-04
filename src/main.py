'''Main.
'''

from argparse import ArgumentParser, Namespace
from src.api import get_county_data
from src.cli import create_parser, create_subparsers, parse
from src.io import load_config
from src.parser import parse_county_data, parse_xml


config = load_config()
resource_county = config["api"]["resources"]["vysledky_okresy_obce"]


def main():
    """Main func."""
    parser: ArgumentParser = create_parser()
    parser = create_subparsers(parser)
    parsed: Namespace = parse(
        parser,
    )

    if parsed.nuts:
        city_name = parsed.name if parsed.name is not None else None
        status, raw_data = get_county_data(nuts=parsed.nuts, resource=resource_county)

        if status:
            status, parsed_data = parse_xml(raw_data)

            if status:
                county_data = parse_county_data(parsed_data, city=city_name)
                print(county_data)


if __name__ == "__main__":
    main()
