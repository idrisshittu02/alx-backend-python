"""Views for the chat messaging application using DRF ViewSets."""
from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError
from .models import User, Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer
from .permissions import IsOwner
from django.shortcuts import get_object_or_404
from .filters import MessageFilter

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__username']

    def get_queryset(self):
        # Only return conversations where the logged-in user is a participant
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        # Automatically add the user creating the conversation as a participant
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    filter_backends = [filters.SearchFilter]
    search_fields = ['conversation__id']

    def get_queryset(self):
        # Only return messages in conversations where the user is a participant
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.validated_data.get('conversation')
        if not serializer.validated_data.get('conversation'):
            raise ValidationError("Conversation is required")
        serializer.save(sender=self.request.user)


def update(self, request, *args, **kwargs):
    message = self.get_object()
    conversation_id = message.conversation.id
    if request.user not in message.conversation.participants.all():
        return Response(
            {"detail": "You are not a participant in this conversation."},
            status=status.HTTP_403_FORBIDDEN
        )
    return super().update(request, *args, **kwargs)

def destroy(self, request, *args, **kwargs):
    message = self.get_object()
    conversation_id = message.conversation.id
    if request.user not in message.conversation.participants.all():
        return Response(
            {"detail": "You are not a participant in this conversation."},
            status=status.HTTP_403_FORBIDDEN
        )
    return super().destroy(request, *args, **kwargs)