import datetime

class Logger:
    """
    A logger to log messages with timestamps to the console.
    """
    def log(self, message):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("[{}] [LOG]: {}".format(timestamp, message))

    def log_error(self, error_message):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("[{}] [ERROR]: {}".format(timestamp, error_message))