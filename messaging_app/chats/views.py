# views.py
from rest_framework import generics
from .models import Conversation
from .serializers import ConversationSerializer
from .serializers import MessageCreateSerializer


class ConversationDetailView(generics.RetrieveAPIView):
    queryset = Conversation.objects.prefetch_related("participants", "messages__sender")
    serializer_class = ConversationSerializer
    lookup_field = "conversation_id"


class MessageCreateView(generics.CreateAPIView):
    serializer_class = MessageCreateSerializer

    def perform_create(self, serializer):
        # Sender is automatically set in serializer
        serializer.save()
