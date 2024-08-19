import datetime

class Logger:
    """
    A logger to log messages with timestamps to the console.
    """

    def log(self, message: str) -> None:
        """
        Logs a message with a timestamp to the console.

        Args:
            message (str): The message to log.
        """
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("[{}] [LOG]: {}".format(timestamp, message))

    def log_error(self, error_message: str) -> None:
        """
        Logs an error message with a timestamp to the console.

        Args:
            error_message (str): The error message to log.
        """
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("[{}] [ERROR]: {}".format(timestamp, error_message))