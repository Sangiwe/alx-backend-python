from rest_framework import permissions
from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.sender == request.user or obj.receiver == request.user

class IsParticipantOfConversation(BasePermission):
    """
    Allows access only to participants of the conversation.
    """

    def has_object_permission(self, request, view, obj):
        # Ensure the user is either the sender or recipient of the message/conversation
        user = request.user
        return user == obj.sender or user == obj.recipient
