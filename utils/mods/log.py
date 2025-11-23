import inspect
import logging
from typed import typed, Maybe, Enum, Str, Nill
from utils.err import LogErr

LogLevel = Enum(Str, 'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG')

class log:
    def __init__(self, level: LogLevel = 'DEBUG', format: Maybe(Str) = None):
        try:
            caller_frame = inspect.stack()[1]
            module_globals = caller_frame.frame.f_globals
            module_name = module_globals.get('__name__', '__main__')

            self._logger = logging.getLogger(module_name)
            self._logger.setLevel(getattr(logging, str(level)))

            if format:
                handler = logging.StreamHandler()
                handler.setFormatter(logging.Formatter(format))
                self._logger.addHandler(handler)
        except Exception as e:
            raise LogErr(e)

    def debug(self, message: Str) -> Nill:
        try:
            self._logger.debug(message)
        except Exception as e:
            raise LogErr(e)

    def info(self, message: Str) -> Nill:
        try:
            self._logger.info(message)
        except Exception as e:
            raise LogErr(e)

    def warning(self, message: Str) -> Nill:
        try:
            self._logger.warning(message)
        except Exception as e:
            raise LogErr(e)

    def error(self, message: Str) -> Nill:
        try:
            self._logger.error(message)
        except Exception as e:
            raise LogErr(e)

    def critical(self, message: Str) -> Nill:
        try:
            self._logger.critical(message)
        except Exception as e:
            raise LogErr(e)
