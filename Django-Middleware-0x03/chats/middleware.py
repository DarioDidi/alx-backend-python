from datetime import datetime, time
import logging
from django.http import HttpResponseForbidden

logging.basicConfig(
    filename="requests.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)

logger = logging.getLogger("requests.log")
logger.setLevel(logging.INFO)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    # One-time configuration and initialization.

    def __call__(self, request):
        response = self.get_response(request)
        user = request.user
        logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")

        # Code to be executed for each request/response after
        # the view is called.

        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.deadline = time(21)
        self.start = time(18)

    def __call__(self, request):
        now = datetime.datetime.now()
        user = request.user
        response = self.get_response(request)

        if not self.in_between(now):
            response = HttpResponseForbidden("Time out of service time")

        return response

    def in_between(self, check_time):
        return self.start <= check_time <= self.deadline


def OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ...

