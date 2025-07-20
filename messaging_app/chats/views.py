from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__first_name', 'participants__last_name', 'participants__email']

    def create(self, request, *args, **kwargs):
        user_ids = request.data.get('user_ids')
        if not user_ids or not isinstance(user_ids, list):
            return Response({"error": "user_ids must be a list of valid user UUIDs"},
                            status=status.HTTP_400_BAD_REQUEST)

        participants = User.objects.filter(user_id__in=user_ids)
        if participants.count() != len(user_ids):
            return Response({"error": "Some user IDs are invalid"}, status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        sender_id = request.data.get('sender_id')
        conversation_id = request.data.get('conversation_id')
        message_body = request.data.get('message_body')

        try:
            sender = User.objects.get(user_id=sender_id)
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except User.DoesNotExist:
            return Response({"error": "Invalid sender_id"}, status=status.HTTP_400_BAD_REQUEST)
        except Conversation.DoesNotExist:
            return Response({"error": "Invalid conversation_id"}, status=status.HTTP_400_BAD_REQUEST)

        message = Message.objects.create(
            sender=sender,
            conversation=conversation,
            message_body=message_body
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
