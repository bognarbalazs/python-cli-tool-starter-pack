import json
import logging
from logging import Formatter

import logzero

LOG_LEVELS = {
    "DEBUG": logzero.DEBUG,
    "INFO": logzero.INFO,
    "WARN": logzero.WARN,
    "ERROR": logzero.ERROR,
    "CRITICAL": logzero.CRITICAL,
}


class CustomJsonFormatter(Formatter):
    """
    A custom JSON formatter for Python logging that formats log records as JSON objects.

    Attributes:
      datefmt (str): The format string for formatting the timestamp in log records.

    Methods:
      format(record):
        Formats a log record into a JSON string containing the timestamp, log level,
        module name, function name, line number, and log message.

    Args:
      datefmt (str, optional): The format for the timestamp in the log records.
        Defaults to "%Y-%m-%dT%H:%M:%S".
    """
    def __init__(self, datefmt="%Y-%m-%dT%H:%M:%S"):
        super().__init__(datefmt=datefmt)

    def format(self, record):
        message = record.getMessage()
        log_record = {
            "time": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        try:
            json_data = json.loads(message)
            log_record["json_message"] = json_data
                
        except (json.JSONDecodeError, TypeError):
            log_record["message"] = message
            
        
        self._add_extra_fields(record, log_record)
        
        return json.dumps(log_record)

    def _add_extra_fields(self, record, log_record):
        """
        Add extra fields to log record.
        """
        for key, value in record.__dict__.items():
            if key not in ('args', 'asctime', 'created', 'exc_info', 'exc_text', 
                          'filename', 'funcName', 'id', 'levelname', 'levelno', 
                          'lineno', 'module', 'msecs', 'message', 'msg', 'name', 
                          'pathname', 'process', 'processName', 'relativeCreated', 
                          'stack_info','taskName', 'thread', 'threadName'):
                
                if key not in log_record:
                    # try to convert to JSON 
                    try:
                        json.dumps({key: value})
                        log_record[key] = value
                    except (TypeError, OverflowError):
                        # If not JSON seriazable, use as string
                        log_record[key] = str(value)

def setup_logging(log_level_name: str, log_to_file: bool, log_file_path: str) -> logging.Logger:
    """
    Sets up logging for the application using the logzero library.

    Args:
      log_level_name (str): The name of the logging level (e.g., "DEBUG", "INFO").
                  Must be a valid key in the LOG_LEVELS dictionary.
      log_to_file (bool): Whether to log messages to a file. If True, a valid
                log_file_path must be provided.
      log_file_path (str): The file path where logs should be written if log_to_file
                 is True. Ignored if log_to_file is False.

    Returns:
      logging.Logger: The configured logger instance.

    Raises:
      Exception: If an error occurs during the logging setup, an error message
             is printed with valid log levels.

    Notes:
      - The log file will have a maximum size of 10 MB, and up to 3 backup copies
        will be kept.
      - The log format is customized using the CustomJsonFormatter.
      - Existing handlers on the root logger are removed to avoid duplicate logs.
    """
    try:
        log_level = LOG_LEVELS.get(log_level_name)

        logzero.loglevel(log_level)
        logzero.formatter(CustomJsonFormatter(datefmt="%Y-%m-%d T%H:%M:%S%"))

        # Set up file logging if log file is specified
        if log_to_file == True and log_file_path != "":
            logzero.logfile(
                log_file_path,
                maxBytes=10**7,  # 10 MB
                backupCount=3,  # Keep 3 backup copies
                encoding="utf-8",
            )

        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)

        return logzero.logger
    except Exception as e:
        print(
            f"Error setting up logging: {e}, valid log levels are {LOG_LEVELS.keys()}"
        )