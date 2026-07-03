import base64
import logging
import os.path
import uuid
from typing import Union

logger = logging.getLogger(__name__)


class FileHandler:
    def __init__(self, *, file_path: str):
        self._validate_file_exists(file_path=file_path)

        self._file_path = file_path
        self._filename = self.get_filename()
        self._safe_filename = self.get_safe_filename()

    @property
    def file_path(self) -> str:
        return self._file_path

    @file_path.setter
    def file_path(self, value):
        pass

    @property
    def filename(self) -> str:
        return self._filename

    @filename.setter
    def filename(self, value):
        pass

    @property
    def safe_filename(self) -> str:
        return self._safe_filename

    @safe_filename.setter
    def safe_filename(self, value):
        pass

    def encode(self) -> str:
        file = open(self.file_path, "rb")
        file_read = file.read()
        file_64_encode = base64.encodebytes(file_read)

        return file_64_encode.decode()

    def get_filename(self) -> str:
        return os.path.basename(self.file_path)

    def get_safe_filename(self) -> str:
        return uuid.uuid4().hex

    def _validate_file_exists(self, *, file_path: str) -> Union[None]:
        if not os.path.isfile(file_path):
            logger.error(f"_validate_file_exists :: file not found {file_path}")
            raise FileNotFoundError(f"file not found {file_path}")
