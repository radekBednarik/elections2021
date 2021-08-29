# pylint: disable=missing-class-docstring, invalid-name, no-self-use, missing-function-docstring
'''Testing parser functions.
'''

from src.api import get_county_data
from src.parser import parse


class TestParser:
    def test_parser_returns_true(self):
        api_status, raw_data = get_county_data("CZ0100")
        parse_status, _ = parse(raw_data)
        assert api_status is True
        assert parse_status is True
