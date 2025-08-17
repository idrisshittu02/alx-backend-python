from rest_framework import serializers
from .models import CustomUser, Conversation, Message

class CustomUserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    class Meta:
        model = CustomUser
        fields = ['user_id', 'email','first_name', 'last_name', 'full_name', 'phone_number']

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'sender_name', 'message_body', 'sent_at', 'is_read']
        
    def get_sender_name(self, obj):
        return f"{obj.sender.get_full_name()} ({obj.sender.email})"
class ConversationSerializer(serializers.ModelSerializer):
    participants = CustomUserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']

    def validate(self, data):
        if 'participants' not in data or len(data['participants']) < 2:
            raise serializers.ValidationError("A conversation must have at least two participants.")
        return data