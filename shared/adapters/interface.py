# Standard Library
from datetime import datetime
from typing import Any

# Libraries
from shared.utils.core.json import prepare_data_for_json_serialization
from requests.models import Response

# Internal
from shared.utils.core.logging.models import EgressAPILog


class ConnectorLogger:
    @staticmethod
    def egress_log(
        *,
        http_method: str,
        request_data: dict[str, Any],
        service_name: str,
        status_code: int,
        response_data: dict[str, Any],
        error: str,
    ) -> None:
        timestamp = datetime.utcnow()
        integration_log = EgressAPILog(
            http_method=http_method,
            service_name=service_name,
            timestamp=timestamp,
            request_data=prepare_data_for_json_serialization(data=request_data),
            response_data=prepare_data_for_json_serialization(data=response_data),
            status_code=status_code,
            error=error,
        )
        integration_log.save()


class ExtractResponseData:
    @staticmethod
    def response_data(response: Response) -> dict[str, Any]:
        return response.json() if response.status_code < 400 else {}

    @staticmethod
    def error_message(response: Response) -> str:
        return "" if response.status_code < 400 else response.text
