import logging
import re
from typing import Tuple

__all__ = ["ColoredFormatter", "transform_http_message"]

_HTTP_LOG_PATTERN = re.compile(
    r"^(?P<address>\S+)\s+\"(?P<method>[A-Z]+)\s+[^\"]+\s+HTTP/[0-9.]+\"\s+(?P<status>\d+)(?:\s+(?P<size>\S+))?"
)


def transform_http_message(message: str) -> Tuple[bool, str]:
    """Transform Azure SDK HTTP logs into a concise REST format."""
    match = _HTTP_LOG_PATTERN.match(message)
    if not match:
        return False, message

    address = match.group("address")
    method = match.group("method")
    status = match.group("status")
    size = match.group("size") or ""
    outcome = f"{status} {size}".strip()

    return True, f"{address} Action: {method} Outcome: {outcome}"


def _should_transform_http(record: logging.LogRecord) -> bool:
    """Return True when the log record is emitted by Azure HTTP logging."""
    if not record.name.startswith("azure.core.pipeline.policies.http_logging_policy"):
        return False
    message = record.getMessage()
    return "HTTP/" in message and message.startswith("http")


class ColoredFormatter(logging.Formatter):
    """
    Custom formatter that adds colors to log messages.
    - INFO messages: Yellow
    - DEBUG messages: White (default terminal color)
    - HTTP logs: transformed to REST format without additional coloring
    """

    YELLOW = "\033[33m"
    WHITE = "\033[37m"
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        original_levelname = record.levelname
        original_msg = record.msg
        original_args = record.args

        transformed = False
        if _should_transform_http(record):
            transformed, new_message = transform_http_message(record.getMessage())
            if transformed:
                record.levelname = "REST"
                record.msg = new_message
                record.args = ()

        formatted = super().format(record)

        if transformed:
            record.levelname = original_levelname
            record.msg = original_msg
            record.args = original_args
            return formatted

        if record.levelno == logging.INFO:
            return f"{self.YELLOW}{formatted}{self.RESET}"
        if record.levelno == logging.DEBUG:
            return f"{self.WHITE}{formatted}{self.RESET}"
        return formatted