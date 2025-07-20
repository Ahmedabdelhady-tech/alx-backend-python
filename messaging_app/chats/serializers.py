from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_id", "first_name", "last_name", "email", "role", "created_at"]
        extra_kwargs = {"password": {"write_only": True}}  # Hide password in responses


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)  # Nested sender representation

    class Meta:
        model = Message
        fields = ["message_id", "sender", "message_body", "sent_at"]
        read_only_fields = ["message_id", "sent_at", "sender"]


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)  # Nested messages

    class Meta:
        model = Conversation
        fields = ["conversation_id", "participants", "messages", "created_at"]
        read_only_fields = ["conversation_id", "created_at"]


class ConversationCreateSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(), write_only=True
    )

    class Meta:
        model = Conversation
        fields = ["participants"]

    def create(self, validated_data):
        participants = validated_data.pop("participants")
        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        return conversation


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["message_body", "conversation"]
        extra_kwargs = {"conversation": {"write_only": True}}

    def create(self, validated_data):
        # Automatically set sender to current user
        validated_data["sender"] = self.context["request"].user
        return super().create(validated_data)
