import logging

from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger()


class ServerErrorLoggingMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception) -> None:  # noqa: ARG002
        logger.exception("Server Error:", exc_info=exception)
