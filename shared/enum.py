from enum import Enum


class StrEnum(str, Enum):
    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

    @classmethod
    def values(cls):
        return cls._value2member_map_.values()
