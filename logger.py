import logging

logging.basicConfig(level=logging.INFO)


def get_logger(module: str):
    return logging.getLogger(module)
