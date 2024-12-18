import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
import os

class Logger:
    """
    A custom logger class with rotating file handler.

    This logger writes logs to a file and automatically rotates the log file
    when it reaches a specified size. The log file is named with today's date.

    Attributes:
        name (str): The name of the logger.
        log_dir (str): The directory where logs will be saved.
        level (int): The logging level (default is logging.DEBUG).
        max_bytes (int): The maximum file size in bytes before rotating (default is 10000).
        backup_count (int): The number of backup files to keep (default is 3).
    """

    def __init__(
        self,
        name: str,
        log_dir: str = "logs",
        level: int = logging.DEBUG,
        max_bytes: int = 10000,
        backup_count: int = 3
    ) -> None:
        """
        Initialize the Logger with a rotating file handler and today's date in the filename.

        Args:
            name (str): The name of the logger.
            log_dir (str): The directory where logs will be saved.
            level (int): The logging level (default is logging.DEBUG).
            max_bytes (int): The maximum file size in bytes before rotating (default is 10000).
            backup_count (int): The number of backup log files to keep (default is 3).
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Ensure the log directory exists
        os.makedirs(log_dir, exist_ok=True)

        # Create a log filename with today's date
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = os.path.join(log_dir, f"log_{today}.log")

        try:
            # Create handler with rotating file
            file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
            file_handler.setLevel(level)

            # Create formatter
            formatter = logging.Formatter("%(lineno)s - %(levelname)s: %(message)s (%(asctime)s)")
            file_handler.setFormatter(formatter)

            # Avoid adding multiple handlers to the logger
            if not self.logger.handlers:
                self.logger.addHandler(file_handler)

        except Exception as e:
            print(f"Error initializing logger: {e}")

    def get_logger(self) -> logging.Logger:
        """
        Get the configured logger instance.

        Returns:
            logging.Logger: The configured logger instance.
        """
        return self.logger