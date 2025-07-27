from django.conf import settings
import logging
from datetime import datetime
from datetime import time
from django.http import HttpResponseForbidden
from django.core.cache import cache
import time

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


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Rate limit settings
        self.RATE_LIMIT = 5  # 5 messages
        self.TIME_WINDOW = 60  # 60 seconds (1 minute)
        self.POST_PATHS = ["/chat/send/", "/chat/message/"]  # Paths to monitor

    def __call__(self, request):
        # Only check for POST requests to specific paths
        if request.method == "POST" and any(
            request.path.startswith(path) for path in self.POST_PATHS
        ):
            ip_address = self.get_client_ip(request)
            cache_key = f"rate_limit_{ip_address}"

            # Get current request count and timestamp
            request_data = cache.get(cache_key, {"count": 0, "start_time": time.time()})

            # Reset counter if time window has passed
            if time.time() - request_data["start_time"] > self.TIME_WINDOW:
                request_data = {"count": 0, "start_time": time.time()}

            # Increment request count
            request_data["count"] += 1
            cache.set(cache_key, request_data, self.TIME_WINDOW)

            # Check if rate limit exceeded
            if request_data["count"] > self.RATE_LIMIT:
                return HttpResponseForbidden(
                    "Rate limit exceeded: Please wait before sending more messages"
                )

        return self.get_response(request)

    def get_client_ip(self, request):
        """Get the client's IP address from request"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip


class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Define protected paths and required roles
        self.PROTECTED_PATHS = {
            "/chat/delete/": ["admin", "moderator"],
            "/chat/ban/": ["admin"],
            "/chat/config/": ["admin"],
        }

    def __call__(self, request):
        current_path = request.path

        # Check if the current path requires special permissions
        for protected_path, required_roles in self.PROTECTED_PATHS.items():
            if current_path.startswith(protected_path):
                # Check if user is authenticated
                if not request.user.is_authenticated:
                    return HttpResponseForbidden("Authentication required")

                # Check user's role (compatible with different user model implementations)
                user_role = None

                # Try different ways to get the role
                if hasattr(request.user, "role"):
                    user_role = request.user.role
                elif hasattr(request.user, "profile") and hasattr(
                    request.user.profile, "role"
                ):
                    user_role = request.user.profile.role
                elif hasattr(request.user, "groups"):
                    # Fallback to Django groups
                    user_role = (
                        "admin"
                        if request.user.groups.filter(name="admin").exists()
                        else (
                            "moderator"
                            if request.user.groups.filter(name="moderator").exists()
                            else None
                        )
                    )

                if user_role not in required_roles:
                    return HttpResponseForbidden(
                        f"Access denied. Requires {', '.join(required_roles)} role"
                    )
                break

        return self.get_response(request)
