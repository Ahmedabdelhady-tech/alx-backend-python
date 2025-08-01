from messaging.views import delete_user, threaded_conversations
from django.urls import path


urlpatterns = [
    path("delete-user/", delete_user, name="delete_user"),
    path(
        "threaded_conversations/", threaded_conversations, name="threaded_conversations"
    ),
]
