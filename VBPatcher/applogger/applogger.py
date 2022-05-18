import logging

class _LogGenerator():
    """Wrapper for application logging.

    - Uses built-in Python `logging` module.
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
            log_file: str = __name__,
            log_format: str = '[%(asctime)s - %(levelname)s] : %(message)s',
            date_fmt: str = "%Y-%m-%d %H:%M:%S",
            log_lvl=INFO):
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

        :param log_file: assign specific name to logger, defaults to `__name__`.
        :type log_file: str, optional
        :param log_format: Initialize the formatter either with the specified format string, or a default as described above, defaults to '[%(asctime)s - %(levelname)s] : %(message)s'
        :type log_format: str, optional
        :param date_fmt: set date formatting, defaults to "%Y-%m-%d %H:%M:%S"
        :type date_fmt: str, optional
        :param log_lvl: Set the logging level of this logger. Level must be an int or a str, defaults to `INFO`.
        :type log_lvl: int, optional
        """
        self.logger = logging.getLogger(log_file)
        self.log_format = log_format
        self.datefmt = date_fmt
        self.log_lvl = log_lvl
        self.formatter = logging.Formatter(log_format, datefmt=date_fmt)
        self.log_file = log_file
        self.fhandler = logging.FileHandler(log_file)
        self.logger.addHandler(self.fhandler)
        self.fhandler.setFormatter(self.formatter)
        self.logger.setLevel(log_lvl)

    def debug(self, msg):
        return self.logger.debug(msg)

    def info(self, msg):
        return self.logger.info(msg)

    def warning(self, msg):
        return self.logger.warning(msg)

    def error(self, msg):
        return self.logger.error(msg)

    def critical(self, msg):
        return self.logger.critical(msg)
