import logging

from VBPatcher.appglobals.globals import log_fh


class _LogGenerator():
    """Wrapper for application logging.

    - Uses built-in Python `logging` module.

    ---

    - Contains the following logging methods:

        - :func:`debug(self, msg) -> None`
            - Logs a message with level `DEBUG`.

        - :func:`info(self, msg) -> None`
            - Logs a message with level `INFO`.

        - :func:`warning(self, msg) -> None`
            - Logs a message with level `WARNING`.

        - :func:`error(self, msg) -> None`
            - Logs a message with level `ERROR`.
            - Can optionally include exception information in log message.

        - :func:`critical(self, msg) -> None`
            - Logs a message with level `CRITICAL`.
    """

    CRITICAL = 50
    FATAL = CRITICAL
    ERROR = 40
    WARNING = 30
    WARN = WARNING
    INFO = 20
    DEBUG = 10
    NOTSET = 0

    def __init__(
            self,
            log_file: str,
            log_name: str = __name__,
            log_format: str = '[ %(asctime)s - %(levelname)s ] : %(message)s',
            datefmt: str = "%Y-%m-%d %H:%M:%S",
            level: int = INFO,
            stream: bool = False):
        """Initialize logger instance.

        - For the :param:`log_lvl` parameter, the level of logging can be any of the following:
            - CRITICAL = 50
            - FATAL = CRITICAL
            - ERROR = 40
            - WARNING = 30
            - WARN = WARNING
            - INFO = 20
            - DEBUG = 10
            - NOTSET = 0

        ---

        :param log_name: Name of logger
        :type log_name: :class:`str`
        :param log_file: file to write log entries
        :type log_file: :class:`str`
        :param log_fmt: Initialize the formatter either with the specified format string, or a default as described above, defaults to '[%(asctime)s - %(levelname)s] : %(message)s'
        :type log_fmt: :class:`str`, optional
        :param date_fmt: set date formatting, defaults to "%Y-%m-%d %H:%M:%S"
        :type date_fmt: :class:`str`, optional
        :param level: Set the logging level of this logger. Level must be an int or a str, defaults to `INFO`
        :type level: :class:`int`, optional
        :param stream: If True, toggle streaming to stdout
        :type stream: :class:`bool`, optional
        :return: new logging class instance
        :rtype: `None`
        """

        self.log_name: str = log_name
        self.logger: logging.Logger = logging.getLogger(log_name)
        self.log_format: str = log_format
        self.datefmt: str = datefmt
        self.level: int = level
        self.formatter: logging.Formatter = logging.Formatter(log_format,
                                                              datefmt=datefmt)
        self.log_file: str = log_file
        self.stream: bool = stream
        self.fhandler: logging.FileHandler = logging.FileHandler(log_file)

        self.logger.addHandler(self.fhandler)
        self.fhandler.setFormatter(self.formatter)
        self.logger.setLevel(level)
        if stream:  # if stream is True, then toggle logging stream to stdout
            self.logger.addHandler(logging.StreamHandler())

    def debug(self, msg) -> None:
        """Logs a message with level `DEBUG`.

        ---
z
        :param msg: message to be logged
        :type msg: :class:`str`
        :return: creates log entry
        :rtype: `None`
        """
        return self.logger.debug(msg)

    def info(self, msg) -> None:
        """Logs a message with level `INFO`.

        ---

        :param msg: message to be logged
        :type msg: :class:`str`
        :return: creates log entry
        :rtype: `None`
        """
        return self.logger.info(msg)

    def warning(self, msg) -> None:
        """Logs a message with level `WARNING`.

        ---

        :param msg: message to be logged
        :type msg: :class:`str`
        :return: creates log entry
        :rtype: `None`
        """
        return self.logger.warning(msg)

    def error(self, msg, exc_info: bool = True) -> None:
        """Logs a message with level `ERROR`.

        - Can optionally log exception info if :param:`exc_info` is `True`.

        ---

        :param msg: message to be logged
        :type msg: :class:`str`
        :param exc_info: toggle logging of exception info, defaults to `True`
        :type exc_info: :class:`bool`, optional
        :return: creates log entry
        :rtype: `None`
        """
        return self.logger.error(msg, exc_info=exc_info)

    def critical(self, msg) -> None:
        """Logs a message with level `CRITICAL`.

        ---

        :param msg: message to be logged
        :type msg: :class:`str`
        :return: creates log entry
        :rtype: `None`
        """
        return self.logger.critical(msg)


logger: _LogGenerator = _LogGenerator(log_fh, 'MAIN')  # Main logging instance

logger_stream: _LogGenerator = _LogGenerator(
    log_fh, 'STDOUT', stream=True)  # Stdout streaming logging instance
