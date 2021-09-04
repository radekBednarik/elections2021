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


def parse_county_data(parsed_data: Any, city: Optional[str] = None) -> dict[str, Any]:
    """Parses XML object to retrieve data as `dict`.

    In case the `city` name from given NUTS county is not provided,
    then data for NUTS county level are returned.

    In case the `city` name is provided, data for given city are returned.

    Args:
        parsed_data (Any): lxml Element object representing XML data
        city (Optional[str], optional): Name of the city from the county
        E.g. "Praha 1". Defaults to None.

    Returns:
        dict[str, Any]: parsed data from lxml Element object as `dict`.
    """
    output: dict[str, Any] = {}
    authorities_data_level: list[Any] = list(parsed_data)
    master_key: str = ""

    for level_1 in authorities_data_level:
        if city is None and "OKRES" in level_1.tag:
            master_key = level_1.attrib["NUTS_OKRES"]
            output[master_key] = {"descriptors": dict(level_1.attrib), "data": []}

            for level_2 in list(level_1):
                output[master_key]["data"].append(dict(level_2.attrib))

            break

        if (
            city is not None
            and "OBEC" in level_1.tag
            and city.strip() == level_1.attrib["NAZ_OBEC"]
        ):
            master_key = level_1.attrib["CIS_OBEC"]
            output[master_key] = {"descriptors": dict(level_1.attrib), "data": []}

            for level_2 in list(level_1):
                output[master_key]["data"].append(dict(level_2.attrib))

            break

    return output
