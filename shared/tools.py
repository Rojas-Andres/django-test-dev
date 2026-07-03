import sys
from datetime import datetime
from enum import Enum
from importlib import import_module
from typing import Any, Callable, Iterable, TypeVar
from uuid import UUID

from shared.exceptions import ValidationError

_M = TypeVar("_M")


def import_string(dotted_path: str) -> Callable:
    """
    Functionality taken from the Django Library
    Import a dotted module path and return the attribute/class designated by
    the last name in the path. Raise ImportError if the import failed.

    Raises:
        ImportError: In case the module to import is not found or the
        class name is not in the module.
    """
    try:
        module_path, class_name = dotted_path.rsplit(".", 1)
    except ValueError as err:
        raise ImportError(f"{dotted_path} doesn't look like a module path") from err

    try:
        return _cached_import(module_path, class_name)
    except AttributeError as err:
        raise ImportError(
            f"Module {module_path} does not define a " f"{class_name} attribute/class"
        ) from err


def _cached_import(module_path: str, class_name: str) -> Callable:
    """
    Functionality taken from the Django Library
    Proxy function that helps to load an object from memory or directly from
    the source.

    Raises:
        AttributeError: In case the module to import is not found or the
        class name is not in the module.
    """
    modules = sys.modules
    if module_path not in modules or (
        # Module is not fully initialized.
        getattr(modules[module_path], "__spec__", None) is not None
        and getattr(modules[module_path].__spec__, "_initializing", False) is True
    ):
        import_module(module_path)
    return getattr(modules[module_path], class_name)


def call_domain_command(cmd: Command, publish_events: bool = True) -> Any:
    """
    Creates a bus based on the command domain an handles it.

    Args:
        cmd: The domain command to handle
        publish_events: Boolean field to indicate if the events will be handled

    Example:
        from functools import partial
        run = partial(
            call_domain_command, publish_events=False
        )
        run(cmd)
    """
    if isinstance(cmd, Command) is False:
        raise ValidationError("Entry must be a Command")

    command_module = cmd.__class__.__module__
    domain_path = command_module.replace(".domain.commands", "")
    bootstrap = import_string(f"{domain_path}.bootstrap.bootstrap")

    bus = bootstrap(publish=lambda *args: None)
    if publish_events:
        bus = bootstrap()

    [result] = bus.handle(cmd)

    return result


def enum_to_choices(obj: type[Enum]) -> list[tuple[Any, str]]:
    return [(elem.value, elem.name) for elem in iter(obj)]  # type: ignore


def flat_dict_or_list_dicts(
    object_: dict[str, Any] | list[dict[Any, Any]],
) -> dict[str, Any] | list[dict[Any, Any]]:
    """This function allow to flat an object in both cases it would be
    a dict or list of dicts
    flat an element will become a compound dicts into a single
    "key: value" object
    eg:
        dict = {
            'first_element': {'inner1': 'inner1', 'inner2': 'inner2},
            'second_element: [
                {
                    'inner1': 'inner1',
                    'inner2': 'inner2'
                },
                {
                    'inner3': 'inner3',
                    'inner4': 'inner4'
                }
            ]
        result = flat_dict_or_list_dicts(dict)
        result = {
            'first_element.inner1': 'inner1',
            'first_element.inner2': 'inner2',
            'second_element1.inner1': 'inner1',
            'second_element1.inner2': 'inner2',
            'second_element2.inner1': 'inner1',
            'second_element2.inner2': 'inner2'
        }
    """

    def _flat(dictionary: dict[str, Any]) -> dict[str, Any]:
        dict_copy = dictionary.copy()
        for key, _ in filter(
            lambda value: type(value[1]) in [list, dict], dictionary.items()
        ):
            iterable = dict_copy.pop(key)
            match iterable:
                case list():
                    for index, inner in enumerate(iterable, start=1):
                        try:
                            dict_copy |= {
                                f"{key}{index}.{key1}": value
                                for key1, value in inner.items()
                            }
                        except AttributeError:
                            dict_copy |= {f"{key}.{index}": inner}
                case dict():
                    dict_copy |= {
                        f"{key}.{_key}": value for _key, value in iterable.items()
                    }
        return dict_copy

    if isinstance(object_, list):
        for element in object_:
            _flat(element)
        return object_
    return _flat(object_)


def batch(iterable: list[Any], n: int = 1) -> Iterable:
    """A function to batch a list

    Function to generate a batch iterable from list
    Typical usage example:

    for little_list in batch(my_list, 5):
        process little list

    """
    size = len(iterable)
    for ndx in range(0, size, n):
        yield iterable[ndx : min(ndx + n, size)]


def dict_factory(data: list[tuple[str, Any]]) -> dict[str, Any]:
    result = dict()
    for field, value in data:
        if isinstance(value, datetime):
            result.update({field: value.isoformat()})
            continue
        if isinstance(value, UUID):
            result.update({field: str(value)})
            continue
        result.update({field: value})
    return result


def as_dict(model) -> dict[str, Any]:
    data = [
        (prop, getattr(model, prop)) for prop in dir(model) if not prop.startswith("__")
    ]
    return dict_factory(data=data)


def get_property_object(obj: Any) -> dict[str, Any]:
    """
    Function to get the property's (@property) of an object
    """
    _props: dict[str, Any] = {}
    _type = type(obj)
    props_calculated = {
        name: getattr(_type, name)
        for name in dir(_type)
        if isinstance(getattr(_type, name), property)
    }
    for name, prop in props_calculated.items():
        try:
            _props[name] = prop.fget(obj)
        except (Exception,):
            pass
    return _props
