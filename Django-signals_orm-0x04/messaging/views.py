from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from .models import Message
from django.db.models import Prefetch

user = get_user_model


@login_required
@require_POST
def delete_user(request):
    user = request.user
    user.delete()
    return redirect("home")


@login_required
def threaded_conversations(request):
    # Fetch messages sent or received by the user
    messages = (
        Message.objects.filter(sender=request.user)
        .select_related("sender", "receiver")
        .prefetch_related(
            Prefetch(
                "replies",
                queryset=Message.objects.all().select_related("sender", "receiver"),
            )
        )
    )

    return render(request, "messaging/threaded_messages.html", {"messages": messages})


def unread_message_view(request):
    unread_message = Message.unread.for_user(request.user)
    for msg in unread_message:
        print(msg.content)
