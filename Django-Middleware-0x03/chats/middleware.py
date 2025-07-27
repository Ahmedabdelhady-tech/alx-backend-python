import logging
from datetime import datetime
from datetime import time
from django.http import HttpResponseForbidden

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Configure logging
        self._setup_logger()

    def _setup_logger(self):
        """Ensure logger is properly configured"""
        if not logger.handlers:
            handler = logging.FileHandler("requests.log")
            formatter = logging.Formatter("%(asctime)s - %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
            logger.info("Logger configured")

    def __call__(self, request):
        user = request.user.username if request.user.is_authenticated else "Anonymous"
        logger.info(f"User: {user} - Path: {request.path}")
        return self.get_response(request)


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Define restricted hours (9 PM to 6 AM)
        self.restricted_start = time(21, 0)  # 9 PM
        self.restricted_end = time(6, 0)  # 6 AM

    def __call__(self, request):
        from datetime import datetime

        current_time = datetime.now().time()

        # Check if current time is within restricted hours
        if current_time >= self.restricted_start or current_time <= self.restricted_end:

            # Check if the request is for chat-related paths
            if request.path.startswith("/chat/") or request.path == "/chat":
                return HttpResponseForbidden(
                    "Chat access is restricted between 9 PM and 6 AM"
                )

        return self.get_response(request)
