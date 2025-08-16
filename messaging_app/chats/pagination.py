from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class MessagePagination(PageNumberPagination):
    """
    Custom pagination class for messages.
    """

    page_size = 20  # Default number of messages per page
    page_size_query_param = "page_size"  # Allow clients to set the page size
    max_page_size = 100  # Maximum allowed page size

    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )
