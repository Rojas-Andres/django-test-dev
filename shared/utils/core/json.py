import json
from typing import Any, Dict, List, Union


def prepare_data_for_json_serialization(
    *, data: Union[List[Any], Dict[str, Any], str]
) -> None:
    """Transform unserializable objects in data to str.

    Args:
        data: A dict or list object.

    Examples:
        >>> data = {'amount': Decimal(100)}
        >>> prepare_data_for_json_serialization(data=data)
        >>> data
        {'amount': '100'}

        >>> data = {'taken_at': datetime.datetime(2020, 5, 14, 15, 16)}
        >>> prepare_data_for_json_serialization(data=data)
        >>> data
        {"taken_at": "2020-05-14 15:16:00"}

    Raises:
        AssertionError: An error occurred validating parameters.
    """

    if isinstance(data, str):
        return

    assert isinstance(data, (list, dict)), "data must be a list or dict instance."

    if isinstance(data, list):
        for index, value in enumerate(data):
            if isinstance(value, (dict, list)):
                prepare_data_for_json_serialization(data=value)

            try:
                json.dumps(value)
            except TypeError:
                data[index] = str(value)

    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict) or isinstance(value, list):
                prepare_data_for_json_serialization(data=value)

            try:
                json.dumps(value)
            except TypeError:
                data[key] = str(value)
