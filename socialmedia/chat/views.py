from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json

from django.db.models import OuterRef, Subquery, Q
from .models import ChatMessage, ChatRoom, RoomMessage
from authentication.models import User

 
def index(request):
  return render(request, 'chat/chat.html')

@login_required
def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'username': mark_safe(json.dumps(request.user.username)),
    })


def inbox(request):
    user_id = request.user

    chat_message = ChatMessage.objects.filter(
        id__in =  Subquery(
            User.objects.filter(
                Q(sender__receiver=user_id) |
                Q(receiver__sender=user_id)
            ).distinct().annotate(
                last_msg=Subquery(
                    ChatMessage.objects.filter(
                        Q(sender=OuterRef('id'),receiver=user_id) |
                        Q(receiver=OuterRef('id'),sender=user_id)
                    ).order_by('-id')[:1].values_list('id',flat=True) 
                )
            ).values_list('last_msg', flat=True).order_by("-id")
        )
    ).order_by("-id")
    
    context = {
        'chat_message': chat_message,
    }
    return render(request, 'chat/inbox.html', context)

@login_required
def inbox_detail(request, username):
    user_id = request.user   
    message_list = ChatMessage.objects.filter(
        Q(sender=user_id, receiver__username=username) | Q(sender__username=username, receiver=user_id)
    ).order_by("-id")[:10]

    user = request.user
    sender = request.user
    receiver = User.objects.get(username=username)
    receiver_details = User.objects.get(username=username)
    
    messages_detail = ChatMessage.objects.filter(
        Q(sender=sender, receiver=receiver) | Q(sender=receiver, receiver=sender)
    ).order_by("date")

    context = {
        'message_detail': messages_detail,     
        "receiver":receiver,
        "sender":sender,
        "receiver_details":receiver_details,
        "message_list":message_list,
    }
    return render(request, 'chat/inbox_detail.html', context)


@login_required
def inbox_group_detail(request, roomname):
    room_id = ChatRoom.objects.get(room__name = roomname)
    message_list = RoomMessage.objects.filter(
        Q(room__id = room_id.id)
    ).order_by("-id")[:10]

    sender = request.user
    
    context = {     
        "sender":sender,
        "message_list":message_list,
         
    }
    return render(request, 'chat/inbox_group.html', context)


