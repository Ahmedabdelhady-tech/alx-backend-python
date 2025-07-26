from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    """
    Custom pagination class for messages.
    """
    page_size = 20  # Default number of messages per page
    page_size_query_param = 'page_size'  # Allow clients to set the page size
    max_page_size = 100  # Maximum allowed page size
    last_page_strings = ('last',)  # String to indicate the last page