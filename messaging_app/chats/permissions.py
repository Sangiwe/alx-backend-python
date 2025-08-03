from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user or obj.receiver == request.user

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to only allow participants of a conversation
    to view, create, update, or delete messages.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Allow only if user is sender or recipient
        is_participant = user == obj.sender or user == obj.recipient

        # Only allow these methods for participants
        if request.method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
            return is_participant

        return False
