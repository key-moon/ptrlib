from logging import Logger

def severe_error(msg: str, logger: Logger, raise_error: bool):
    if raise_error: raise Exception(msg)
    else: logger.warning("Extract failed")
