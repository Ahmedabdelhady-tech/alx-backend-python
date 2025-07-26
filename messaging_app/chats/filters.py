import django_filters
from .models import Message
from django.contrib.auth import get_user_model

User = get_user_model()


class MessageFilter(django_filters.FilterSet):

    sender = django_filters.ModelChoiceFilter(queryset=User.objects.all())
    created_at = django_filters.DateTimeFromToRangeFilter(
        field_name="created_at", label="Date Range"
    )

    class Meta:
        model = Message
        fields = ["sender", "created_at"]
        order_by = ["-created_at"]
