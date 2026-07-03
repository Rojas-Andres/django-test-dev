from __future__ import annotations

import abc
from typing import Any, Optional


class Factory:  # TODO DELETE THIS AFTER REFACTOR.
    """
    Can create from the base class the according implementation given the type.
    The base class receives the type None due to it's necessary avoid sharing
    the _registry variable among all children of Factory. Then, you can start
    define the implementations based on the base class.

    You have to define all subclasses within the same file in order to properly
    find the children classes.
    """

    _registry: dict

    def __init_subclass__(cls, type: Optional[Any] = None, **kwargs):
        super().__init_subclass__(**kwargs)
        if type:
            cls._registry[type] = cls
        else:
            cls._registry = {}

    def __new__(cls, type: Optional[Any] = None):
        if type:
            subclass = cls._registry[type]
        else:
            subclass = cls
        return super().__new__(subclass)


# Patterns for refactor
class ConfigurationFactory:
    _registry: dict

    def __init_subclass__(cls, configuration: Optional[Any] = None, **kwargs):
        super().__init_subclass__(**kwargs)
        if configuration:
            cls._registry[configuration] = cls
        else:
            cls._registry = {}

    def __new__(cls, configuration: Optional[Any] = None):
        if configuration:
            subclass = cls._registry[configuration]
        else:
            subclass = cls
        return super().__new__(subclass)


class AbstractLink(abc.ABC):
    _next_link: AbstractLink = None  # type: ignore

    def handle(self, request: Any) -> Any:
        if self._next_link:
            return self._next_link._handle(request)

        return self.get_response(request)

    @staticmethod
    @abc.abstractmethod
    def get_response(request: Any) -> Any:
        pass

    @abc.abstractmethod
    def _handle(self, request: Any) -> Any:
        pass


class Chain:
    def __init__(
        self,
        klass: type[AbstractLink],
        configurations: Optional[list[str]] = None,
    ):
        self.klass = klass
        self.configurations = configurations or []
        self.first_link = self._build()

    def run(self, request: Any) -> Any:
        # Calling the base link handle
        return self.first_link._handle(request)

    def _build(self) -> AbstractLink:
        # Adding the base link
        first_link = current_link = self.klass()
        # Adding all the configuration links that apply
        for conf in self.configurations:
            next_link = self.klass(configuration=conf)  # type: ignore
            current_link._next_link = next_link
            current_link = next_link
        return first_link
