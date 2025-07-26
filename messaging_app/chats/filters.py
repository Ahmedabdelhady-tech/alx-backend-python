import django_filters
from .models import Message
from django.contrib.auth import get_user_model

User = get_user_model()


class MessageFilter(django_filters.FilterSet):
    sender = django_filters.CharFilter(
        field_name="sender__username", lookup_expr="icontains"
    )
    receiver = django_filters.CharFilter(
        field_name="receiver__username", lookup_expr="icontains"
    )
    created_at = django_filters.DateTimeFromToRangeFilter(
        field_name="created_at", label="Date Range"
    )

    class Meta:
        model = Message
        fields = ["sender", "receiver", "created_at"]
