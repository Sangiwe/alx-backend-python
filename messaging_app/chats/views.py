from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework import viewsets, status, filters
from django.contrib.auth import get_user_model
from rest_framework.exceptions import PermissionDenied
from .permissions import IsParticipantOfConversation
from rest_framework.response import Response
from .filters import MessageFilter
from .pagination import MessagePagination
from django_filters.rest_framework import DjangoFilterBackend


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
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = MessageFilter
    ordering_fields = ['sent_at']

    def perform_create(self, serializer):
        conversation = serializer.validated_data.get('conversation')
        user = self.request.user

        if user not in conversation.participants.all():
            return Response({'detail': 'You are not a participant of this conversation.'},
                            status=status.HTTP_403_FORBIDDEN)

        serializer.save(sender=user)

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(
            sender=user
        ) | Message.objects.filter(
            recipient=user
        )