from messaging.views import delete_user
from django.urls import path


urlpatterns = [path("delete-user/", delete_user, name="delete_user"),]
