from datetime import date, datetime
from datetime import timezone as tz
from typing import Union

from django.utils import timezone

MONDAY = 0
TUESDAY = 1
WEDNESDAY = 2
THURSDAY = 3
FRIDAY = 4
SATURDAY = 5
SUNDAY = 6


def get_datetime_utc_now() -> datetime:
    """Get the datetime now. UTC.

    Returns:
        A datetime.
    """

    return datetime.utcnow()


def get_datetime_now() -> datetime:
    """Get the datetime now based on the django timezone.

    Returns:
        A datetime with the django timezone.
    """

    return timezone.localtime(timezone.now())


def get_datetime_utc_tz_info() -> datetime:
    """Get the datetime now. UTC.

    Returns:
        A datetime.
    """

    return datetime.utcnow().replace(tzinfo=tz.utc)
