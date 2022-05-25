import logging

from VBPatcher.appglobals.appglobals import _logFile


class _LogGenerator():
    """Wrapper for application logging.

    - Uses built-in Python `logging` module.

    - Class methods:
        - `debug(self, msg) -> None`
            - Logs a message with level `DEBUG`.

        - `info(self, msg) -> None`
            - Logs a message with level `INFO`.

        - `warning(self, msg) -> None`
            - Logs a message with level `WARNING`.

        - `error(self, msg) -> None`
            - Logs a message with level `ERROR`.

        - `critical(self, msg) -> None`
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

    def __init__(self,
                 name: str,
                 log_file: str,
                 log_fmt: str = '[%(asctime)s - %(levelname)s] : %(message)s',
                 date_fmt: str = "%Y-%m-%d %H:%M:%S",
                 level=INFO):
        """Initialize logger instance.

        - For the `log_lvl` parameter, the level of logging can be any of the following:
            - CRITICAL = 50
            - FATAL = CRITICAL
            - ERROR = 40
            - WARNING = 30
            - WARN = WARNING
            - INFO = 20
            - DEBUG = 10
            - NOTSET = 0

        ---

        :param name: Name of logger.
        :type name: str
        :param log_file: file to create log entries.
        :type log_file: str
        :param log_fmt: Initialize the formatter either with the specified format string, or a default as described above, defaults to '[%(asctime)s - %(levelname)s] : %(message)s'
        :type log_fmt: str, optional
        :param date_fmt: set date formatting, defaults to "%Y-%m-%d %H:%M:%S"
        :type date_fmt: str, optional
        :param level: Set the logging level of this logger. Level must be an int or a str, defaults to `INFO`.
        :type level: int, optional
        """

        self.name = name
        self.logger = logging.getLogger(name)
        self.log_format = log_fmt
        self.datefmt = date_fmt
        self.log_lvl = level
        self.formatter = logging.Formatter(log_fmt, datefmt=date_fmt)
        self.log_file = log_file
        self.fhandler = logging.FileHandler(log_file)
        self.logger.addHandler(self.fhandler)
        self.fhandler.setFormatter(self.formatter)
        self.logger.setLevel(level)

    def debug(self, msg) -> None:
        """Logs a message with level `DEBUG`.

        :param msg: message to be logged.
        :type msg: str
        :return: creates log entry.
        :rtype: None
        """
        return self.logger.debug(msg)

    def info(self, msg):
        """Logs a message with level `INFO`.

        :param msg: message to be logged.
        :type msg: str
        :return: creates log entry.
        :rtype: None
        """
        return self.logger.info(msg)

    def warning(self, msg):
        """Logs a message with level `WARNING`.

        :param msg: message to be logged.
        :type msg: str
        :return: creates log entry.
        :rtype: None
        """
        return self.logger.warning(msg)

    def error(self, msg):
        """Logs a message with level `ERROR`.

        :param msg: message to be logged.
        :type msg: str
        :return: creates log entry.
        :rtype: None
        """
        return self.logger.error(msg)

    def critical(self, msg):
        """Logs a message with level `CRITICAL`.

        :param msg: message to be logged.
        :type msg: str
        :return: creates log entry.
        :rtype: None
        """
        return self.logger.critical(msg)


logger = _LogGenerator(__name__, _logFile)
