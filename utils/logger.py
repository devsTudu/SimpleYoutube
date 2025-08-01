import logging
import sys

def get_logger(name):
    """
    Returns a local log class to help logging.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    if "--reload" in sys.argv:
        ch.setLevel(logging.DEBUG)
    else:
        ch.setLevel(logging.WARNING)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    ch.setFormatter(formatter)

    logger.addHandler(ch)
    return logger