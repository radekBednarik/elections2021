# pylint: disable= c-extension-no-member, broad-except

"""Handles the parsing of the XML data.
"""

from typing import Any, Optional

from lxml import etree
from src.decorators import add_party_name


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


@add_party_name
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


@add_party_name
def parse_state_data(
    parsed_data: Any, district: Optional[str] = None
) -> dict[str, Any]:
    """Parses XML object to retrieve data as `dict`.

    If `district` is not provided, returns state level data (CR - tagged
    element). Otherwise returns district level of data.

    `district` value must be in <1, 14> range inclusive.

    Args:
        parsed_data (Any): lxml Element object representing XML data
        district (Optional[int], optional): Number of district. Defaults to None.

    Returns:
        dict[str, Any]: parsed data as `dict`.
    """
    output: dict[str, Any] = {}
    top_level_data: list[Any] = list(parsed_data)
    master_key: str = ""

    for level_1 in top_level_data:
        if district is None and "CR" in level_1.tag:
            master_key = level_1.tag
            output[master_key] = {"data": []}

            for level_2 in list(level_1):
                output[master_key]["data"].append(dict(level_2.attrib))

                for level_3 in list(level_2):
                    output[master_key]["data"].append(dict(level_3.attrib))

                    for level_4 in list(level_3):
                        output[master_key]["data"].append(dict(level_4.attrib))

        if district is not None:
            # check if district value is in <1, 14>
            if (int(district)) not in list(range(1, 15)):
                raise IndexError(
                    f"{district} value is out of bounds.\
                    Must be in integer interval <1, 14> inclusive."
                )
            items: list[tuple[str, str]] = list(level_1.attrib.items())

            for key, value in items:
                if key == "CIS_KRAJ" and value == district:
                    output[master_key] = {
                        "descriptors": dict(level_1.attrib),
                        "data": [],
                    }

                    for level_2 in list(level_1):
                        output[master_key]["data"].append(dict(level_2.attrib))

                        for level_3 in list(level_2):
                            output[master_key]["data"].append(dict(level_3.attrib))

    return output
