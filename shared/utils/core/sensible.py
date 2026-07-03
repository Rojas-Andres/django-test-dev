from typing import Any, Dict, List, Optional, Union


def obfuscate_sensible_data(
    *,
    data: Union[List[Any], Dict[str, Any]],
    sensible_keys: List[str],
    encrypted: Optional[bool] = False,
) -> Union[None]:
    """Clean data based on sensible_keys.

    - If the data is a list, we only take care of dict values.
    - If the data is a dict, we search each key on sensible keys
      and do the filtering.

    Args:
        sensible_keys: A list of keys that are going to obfuscate.
        data: A list or dict object.

    Examples:
        >>> sensible_keys = ['password']
        >>> data = {'password': 'my-insecure-password'}
        >>> obfuscate_sensible_data(sensible_keys=sensible_keys, data=data)
        >>> data
        {'password': '[filter] -> str'}

    Raises:
        AssertionError: An error occurred validating parameters.

    """
    if not sensible_keys or not data or isinstance(data, str):
        return

    assert isinstance(
        sensible_keys, (list, tuple)
    ), "sensible_keys must be a list or tuple instance."
    assert isinstance(data, (list, dict)), "data must be a list or dict instance."

    if isinstance(data, list):
        for value in data:
            if isinstance(value, dict):
                obfuscate_sensible_data(data=value, sensible_keys=sensible_keys)
        return

    for key, value in data.items():
        if isinstance(value, dict) or isinstance(value, list):
            _encrypted = key in sensible_keys or encrypted
            obfuscate_sensible_data(
                data=value, sensible_keys=sensible_keys, encrypted=_encrypted
            )
            continue

        if key in sensible_keys or encrypted:
            data[key] = f"[filter] -> {type(value)}"
