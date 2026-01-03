import logging
import traceback


class LogFormatter(logging.Formatter):
    def format(self, record):
        time = self.formatTime(record, self.datefmt)
        level = record.levelname
        name = record.name
        message = record.getMessage()
        if record.exc_info:
            exc_type, exc_value, exc_traceback = record.exc_info
            exception_details = traceback.format_exception(
                exc_type,
                exc_value,
                exc_traceback,
            )
            message += "\n" + "".join(exception_details)
        return f"[{time}] {level} {name}: {message}"
