from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsParticipantOfConversation(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in ["PUT", "PATCH", "DELETE"]:

            if request.user not in obj.participants.all():
                raise PermissionDenied("You are not a participant in this conversation.")
                return False
        return request.user in obj.participants.all()
