import json
import logging
import os
from typing import Any, Dict, Union

import boto3
from botocore.exceptions import ClientError

from communication.exceptions import QueueException

logger = logging.getLogger(__name__)


class MessageSizeException(Exception):
    pass


class QueueHandler:
    def __init__(self):
        self.sqs_client = boto3.client("sqs")

        self.queue_url = os.getenv("COMMUNICATION_QUEUE_URL")
        self._validate_queue_url(queue_url=self.queue_url)

    def queue(
        self, *, message_body: str, message_attributes: Dict[str, Dict[str, Any]]
    ) -> bool:
        try:
            self._validate_queue_message_size(
                message_body=message_body, message_attributes=message_attributes
            )
        except MessageSizeException:
            return False

        try:
            response = self.sqs_client.send_message(
                QueueUrl=self.queue_url,
                MessageBody=message_body,
                MessageAttributes=message_attributes,
            )
            logger.info("Queued message {0}".format(response["MessageId"]))
        except self.sqs_client.exceptions.QueueDoesNotExist:
            logger.exception(f"queue :: queue url {self.queue_url} does not exist.")
            return False
        except ClientError as e:
            if e.response["Error"]["Code"] == "AccessDenied":
                logger.exception("queue :: access denied")
            else:
                logger.exception(f"queue :: unexpected error {e}")
            return False
        except QueueException as e:
            logger.exception(f"There is an error processing queue :: {e}")
            return False

        return True

    def _validate_queue_url(self, *, queue_url: str) -> Union[None]:
        if queue_url is None:
            logging.error("_validate_queue_url :: queue url not defined")
            raise ValueError("queue url not defined")

    def _validate_queue_message_size(
        self, *, message_body: str, message_attributes: Dict[str, Dict[str, Any]]
    ) -> Union[None]:
        MESSAGE_SIZE_RESTRICTION = 262144  # This value is in bytes.

        message_size = self._calculate_queue_message_size(
            message_body=message_body, message_attributes=message_attributes
        )

        if message_size > MESSAGE_SIZE_RESTRICTION:
            logger.error(
                "_calculate_queue_message_size :: "
                "queue message size exceed the 256KB limit"
            )
            raise MessageSizeException("queue message size exceed the 256KB limit")

    def _calculate_queue_message_size(
        self, message_body: str, message_attributes: Dict[str, Dict[str, Any]]
    ) -> int:
        message_body_len = len(message_body)
        message_attributes_len = len(json.dumps(message_attributes))
        return message_body_len + message_attributes_len
