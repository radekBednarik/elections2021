'''Utilities.
'''


def retrieve_error_message(data: str, start_tag: str = "<CHYBA>") -> str:
    """Retrieves error message from the data str body.

    Args:
        data (str): data body
        start_tag (str, optional): XML tag marking the beginning of the error message.
        Defaults to "<CHYBA>".

    Raises:
        IndexError: if Error message is corrupted, e.g not properly encoded via expected
        tags, function will throw an IndexError.

    Returns:
        str: error message
    """
    end_tag: str = "".join([start_tag[0], "/", start_tag[1:]])

    start_index: int = data.find(start_tag)
    end_index: int = data.find(end_tag)

    if start_index == -1 or end_index == -1:
        raise IndexError("Error message from data could not be retrieved.")

    return data[start_index : end_index + len(end_tag)]
