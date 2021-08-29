# pylint: disable= c-extension-no-member, broad-except

'''Handles the parsing of the XML data.
'''

from typing import Any, Optional

from lxml import etree


def parse(xml_string_data: str, encoding: str = "utf-8") -> tuple[bool, Optional[Any]]:
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
