import random
import string
from datetime import date, datetime
from typing import Optional, Union

from django.contrib.auth.hashers import make_password
from django.utils import timezone

CUSTOMER_OBFUSCATION_CHARACTER = "*"
DEFAULT_AMOUNT_OBFUSCATE_CHARACTERS = 5


def get_datetime_now() -> datetime:
    """Get the datetime now based on the django timezone.

    Returns:
        A datetime with the django timezone.
    """

    return timezone.localtime(timezone.now())


class Obfuscate:
    @staticmethod
    def basic_obfuscate(size: Optional[int] = None) -> str:
        size = size or DEFAULT_AMOUNT_OBFUSCATE_CHARACTERS
        return "".join([CUSTOMER_OBFUSCATION_CHARACTER for _ in range(size)])

    @staticmethod
    def uniquely_obfuscate(value: str, size: int) -> str:
        random_salt = "".join(random.choice(string.ascii_letters) for _ in range(100))
        current_date = get_datetime_now()
        value_to_obfuscate = f"{value}{str(current_date)}"
        value_obfuscated = make_password(value_to_obfuscate, random_salt)
        return (
            value_obfuscated[-size:]
            if len(value_obfuscated) > size
            else value_obfuscated
        )
