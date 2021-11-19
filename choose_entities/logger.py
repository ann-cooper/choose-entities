"""Reference: https://docs.python-guide.org/writing/logging/
"""
import logging
import os
import sys


def get_logger(name: str, level: int = logging.DEBUG):
    """Sets up a logger.

    Parameters
    ----------
    name: str
        The module name
    level: int, optional
        The logging level, by default logging.DEBUG
    """
    logger = logging.getLogger(name)
    logger.setLevel(level=level)

    log_handler = logging.StreamHandler()
    log_formatter = logging.Formatter(
                "%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)"
            )
    log_handler.setFormatter(log_formatter)
    logger.addHandler(log_handler)
    logger.propagate = False

    return logger
