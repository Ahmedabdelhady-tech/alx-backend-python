import logging
from datetime import datetime

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
