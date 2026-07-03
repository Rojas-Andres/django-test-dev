# Standard Library
from typing import Any

# Libraries
from requests.models import Response


class ExtractResponseData:
    @staticmethod
    def response_data(response: Response) -> dict[str, Any]:
        return response.json() if response.status_code < 400 else {}

    @staticmethod
    def error_message(response: Response) -> str:
        return "" if response.status_code < 400 else response.text
