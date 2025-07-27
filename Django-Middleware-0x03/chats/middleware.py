import logging
from datetime import datetime

# Configure logger at module level
logger = logging.getLogger(__name__)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Configure logging only once when middleware is initialized
        self._configure_logging()

    def _configure_logging(self):
        """Configure logging settings"""
        if not logger.handlers:  # Avoid adding multiple handlers
            file_handler = logging.FileHandler("requests.log")
            formatter = logging.Formatter("%(asctime)s - %(message)s")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            logger.setLevel(logging.INFO)

    def __call__(self, request):
        user = request.user.username if request.user.is_authenticated else "Anonymous"
        path = request.path
        logger.info(f"User: {user} - Path: {path}")
        return self.get_response(request)
