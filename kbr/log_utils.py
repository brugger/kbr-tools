import sys
import logging
import traceback
from logging import handlers
import colorlog


MAX_BYTES = 1024*1024  # 1M
logger = None


def set_log_level(new_level:int) -> int:
    """ Set the log level, value is forced with in the [1-5] range

    levels correspond to: DEBUG=5,  INFO=4 WARN=3, ERROR=2 and CRITICAL=1
    """
    if new_level < 1:
        new_level = 1
    elif new_level > 5:
        new_level = 5

    global logger
    if new_level   == 1:
        logger.setLevel(level=logging.CRITICAL)
    elif new_level == 2:
        logger.setLevel(level=logging.ERROR)
    elif new_level == 3:
        logger.setLevel(level=logging.WARNING)
    elif new_level == 4:
        logger.setLevel(level=logging.INFO)
    elif new_level == 5:
        logger.setLevel(level=logging.DEBUG)

    return new_level


def init(name:str, log_file:str=None, rotate_logs:bool=True, colour=False) -> None:

    global logger

    if colour:
        logger = colorlog.getLogger( name )
    else:
        logger = logging.getLogger( name )

    log_fmt = '%(asctime)s %(name)s.%(levelname)-8s %(message)s'
    datefmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(fmt=log_fmt,
                                  datefmt=datefmt)

    if log_file is not None:
        if rotate_logs:
            handler = handlers.RotatingFileHandler(log_file, mode='a', maxBytes=MAX_BYTES, backupCount=5)
        else:
            handler = logging.FileHandler(log_file, mode='a')

        handler.setFormatter(formatter)
        logger.addHandler(handler)
    else:
        if colour:
            colour_handler = colorlog.StreamHandler()
            colour_handler.setFormatter(colorlog.ColoredFormatter(fmt=f'%(log_color)s{log_fmt}',
                                                           datefmt=datefmt))
            logger.addHandler(colour_handler)
        else:
            screen_handler = logging.StreamHandler(stream=sys.stdout)
            screen_handler.setFormatter(formatter)
            logger.addHandler(screen_handler)

    set_log_level( logging.WARNING )

    return logger

def flush():
    logger.flush()


def no_logger( fun):
    def wrapper( msg ):
        if logger is None:
            print(f"  {msg}" )
        else:
            fun(msg)

    return wrapper

@no_logger
def debug(msg: str) -> None:
    logger.debug( msg )

@no_logger
def info(msg: str) -> None:
    logger.info( msg )

@no_logger
def warning(msg: str) -> None:
    logger.warning( msg )

@no_logger
def warn(msg: str) -> None:
    logger.warning( msg )

@no_logger
def error(msg: str) -> None:
    logger.error( msg )

@no_logger
def critical(msg: str) -> None:
    logger.critical( msg )

def exception(msg: str) -> None:
    if logger is not None:
        logger.exception( msg )
    else:
        print( traceback.format_exc() )


