"""Main.
"""

from argparse import Namespace
from typing import Callable

from src.api import get_county_data, get_state_data
from src.cli import create_parser, create_subparsers, parse
from src.io import load_config
from src.output import enable_coloring, print_colored_data
from src.parser import parse_county_data, parse_state_data, parse_xml

config = load_config()
resource_county = config["api"]["resources"]["vysledky_okresy_obce"]
resource_state = config["api"]["resources"]["vysledky_stat_kraje"]


def main():
    """Main func."""

    def wrapper(
        api_func: Callable,
        general_parser: Callable,
        data_specific_parser: Callable,
        printer: Callable,
        **kwargs,
    ) -> None:
        status, raw_data = api_func(**kwargs)

        if status:
            status, parsed_data = general_parser(raw_data)

            if status:
                processed_data = data_specific_parser(parsed_data, **kwargs)
                printer(processed_data)
            else:
                raise RuntimeError(f"{parsed_data}")

        else:
            raise RuntimeError(f"{raw_data}")

    enable_coloring()
    parsed: Namespace = parse(create_subparsers(create_parser()))

    if hasattr(parsed, "nuts"):
        city_name = parsed.name if parsed.name is not None else None
        wrapper(
            get_county_data,
            parse_xml,
            parse_county_data,
            print_colored_data,
            nuts=parsed.nuts,
            resource=resource_county,
            city=city_name,
        )

    if hasattr(parsed, "district"):
        district = str(parsed.district) if parsed.district is not None else None
        wrapper(
            get_state_data,
            parse_xml,
            parse_state_data,
            print_colored_data,
            resource=resource_state,
            district=district,
        )


if __name__ == "__main__":
    main()
