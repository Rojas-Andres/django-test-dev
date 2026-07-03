from rest_framework import exceptions as rest_exceptions
from rest_framework.status import HTTP_429_TOO_MANY_REQUESTS


class Throttled(rest_exceptions.ValidationError):
    status_code = HTTP_429_TOO_MANY_REQUESTS
    default_detail = "Request was throttled."
    default_code = "throttled"
