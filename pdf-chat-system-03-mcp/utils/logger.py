# utils/logger.py

import logging
import sys

def configure_logging():
    """Call once at app startup in main.py."""
    logging.basicConfig(
        stream    = sys.stdout,
        level     = logging.DEBUG,
        format    = "%(asctime)s  %(levelname)-8s  %(name)s  —  %(message)s",
        datefmt   = "%H:%M:%S",
    )