import logging

logging.basicConfig()

def get_logger(module: str):
    return logging.getLogger(module)
