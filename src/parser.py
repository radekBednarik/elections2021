# pylint: disable= c-extension-no-member, broad-except

'''Handles the parsing of the XML data.
'''

from typing import Any, Optional

from lxml import etree


def parse_xml(
    xml_string_data: str, encoding: str = "utf-8"
) -> tuple[bool, Optional[Any]]:
    """Parses the XML formatted raw string data and returns representation
    as `root` node.

    Parser is `lxml`.

    String is encoded before parsing to `utf-8`, since XML has this encoding
    declaration, and `lxml` would throw otherwise. Encoding can be changed.

    Args:
        xml_string_data (str): XML data to be parsed.
        encoding (str, optional): Into which encoding the raw data string should be encoded into.
        Defaults to "utf-8".

    Returns:
        tuple[bool, Optional[Any]]: Parsed data.
    """
    try:
        parsed = etree.fromstring(xml_string_data.encode(encoding))
        return (True, parsed)
    except Exception as exc:
        print(str(exc))
        return (False, None)


def parse_county_data(parsed_data: Any, city: Optional[str] = None):
    output: dict[str, Any] = {}
    authorities_data_level: list[Any] = list(parsed_data)

    for authority_data in authorities_data_level:
        attrs: dict[str, Any] = authority_data.attrib
        print(attrs)

        # for level_2 in list(level_1):
        #     attrs_level_2: dict[str, Any] = level_2.attrib
        #     print(attrs_level_2)

        #     for level_3 in list(level_2):
        #         attrs_level_3: dict[str, Any] = level_3.attrib
        #         print(attrs_level_3)
