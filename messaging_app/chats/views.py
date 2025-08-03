from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework import viewsets, status, filters
from django.contrib.auth import get_user_model
from rest_framework.exceptions import PermissionDenied
from .permissions import IsParticipantOfConversation

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]  # Optional if auth is used
    filter_backends = [filters.SearchFilter]  # ✅ using filters
    search_fields = ['participants__email']

    def perform_create(self, serializer):
        # When creating a conversation, add the current user automatically
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
        conversation.save()


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['sent_at']

    def get_queryset(self):
        conversation_id = self.request.query_params.get('conversation_id')
        user = self.request.user

        if not conversation_id:
            return Message.objects.none()

        return Message.objects.filter(
            conversation__id=conversation_id,
            conversation__participants=user
        )

    def perform_create(self, serializer):
        conversation = serializer.validated_data.get('conversation')
        user = self.request.user

        if user not in conversation.participants.all():
            raise PermissionDenied("You are not a participant of this conversation.")

        serializer.save(sender=user)
