from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import permissions


class IsParticipantOfConversation(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        methods = ["PUT", "PATCH", "DELETE"]

        if request.method in SAFE_METHODS:
            return True
        if request.method in methods:
            if hasattr(obj, "participants"):
                return obj.participants.filter(id=request.user.id).exists()

            if hasattr(obj, "conversation"):
                return obj.conversation.participants.filter(id=request.user.id).exists()

        return False
