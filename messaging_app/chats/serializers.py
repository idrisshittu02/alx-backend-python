from rest_framework import serializers
from .models import User, Message, Conversation


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = User
        fields = [
            'user_id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'role',
            'created_at',
            'full_name'
        ]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    message_body = serializers.CharField()

    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender',
            'message_body',
            'sent_at',
        ]

    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty or whitespace.")
        return value


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    message_set = MessageSerializer(many=True, read_only=True, source='message_set')
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'created_at',
            'message_set'
        ]

    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d %H:%M:%S")
