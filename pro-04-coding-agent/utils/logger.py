import logging
import sys


def configure_logging() -> None:
    """
    Configure Python logging to stdout.
    Call once at app startup in main.py.
    Format: timestamp  LEVEL  logger_name: message
    """
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.DEBUG,
        format="%(asctime)s  %(levelname)-8s  %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )
