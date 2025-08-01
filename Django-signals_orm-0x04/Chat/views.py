from django.shortcuts import render
from messaging.models import Message
from django.views.decorators.cache import cache_page


@cache_page(60)
def conversation_view(request, conversation_id):
    messages = Message.objects.filter(conversation_id=conversation_id).select_related(
        "sender", "receiver"
    )
    return render(request, "messaging/conversation.html", {"message": messages})
