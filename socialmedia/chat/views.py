from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json

from django.db.models import OuterRef, Subquery, Q
from .models import ChatMessage, ChatRoom, RoomMessage
from authentication.models import User
from profiles.models import Profile
 
def index(request):
    all_profiles = Profile.objects.all()

    chat_users = ChatMessage.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
    list_user = list(set([chat.sender if chat.sender != request.user else chat.receiver for chat in chat_users]))
    list_room = ChatRoom.objects.filter(members=request.user)
    combined_list = []

    # Thêm các người dùng vào danh sách kết hợp và đánh dấu chúng là người dùng
    for user in list_user:
        combined_list.append({'object': user, 'type': 'user'})

    # Thêm các phòng chat vào danh sách kết hợp và đánh dấu chúng là phòng chat
    for room in list_room:
        combined_list.append({'object': room, 'type': 'room'})
    context = {            
            "combined_list":combined_list,
            "profiles":all_profiles,
        }
    return render(request, 'chat/inbox.html', context)

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

    sender = request.user
    receiver = User.objects.get(username=username)
    message_list = ChatMessage.objects.filter(
        Q(sender=sender, receiver=receiver) | Q(sender=receiver, receiver=sender)
    ).order_by("date")

    messages_detail = ChatMessage.objects.filter(
        Q(sender=sender, receiver=receiver) | Q(sender=receiver, receiver=sender)
    ).order_by("date")

    chat_users = ChatMessage.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
    list_user = list(set([chat.sender if chat.sender != request.user else chat.receiver for chat in chat_users]))

    list_room = ChatRoom.objects.filter(members=request.user)
    combined_list = []

    # Thêm các người dùng vào danh sách kết hợp và đánh dấu chúng là người dùng
    for user in list_user:
        combined_list.append({'object': user, 'type': 'user'})

    # Thêm các phòng chat vào danh sách kết hợp và đánh dấu chúng là phòng chat
    for room in list_room:
        combined_list.append({'object': room, 'type': 'room'})


    all_profiles = Profile.objects.all()

    if messages_detail:
        r = messages_detail.first()
        receiver = User.objects.get(username=r.receiver)
    else:
        receiver = User.objects.get(username=username)

    context = {
        "receiver":receiver,
        "sender":sender,
        "message_list":message_list,
        "combined_list":combined_list,    
        "profiles":all_profiles,
    }
    return render(request, 'chat/inbox_detail.html', context)


@login_required
def inbox_group_detail(request, roomname):
    room = ChatRoom.objects.get(name = roomname)
    message_list = RoomMessage.objects.filter(
        Q(room__id = room.id)
    ).order_by("-date").values()[:10]
    print(message_list.count())

    sender = request.user
   
    all_profiles = Profile.objects.all()

    chat_users = ChatMessage.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
    list_user = list(set([chat.sender if chat.sender != request.user else chat.receiver for chat in chat_users]))
    list_room = ChatRoom.objects.filter(members=request.user)
    combined_list = []

    # Thêm các người dùng vào danh sách kết hợp và đánh dấu chúng là người dùng
    for user in list_user:
        combined_list.append({'object': user, 'type': 'user'})

    # Thêm các phòng chat vào danh sách kết hợp và đánh dấu chúng là phòng chat
    for room in list_room:
        combined_list.append({'object': room, 'type': 'room'})

    
    context = {     
        "sender":sender,
        "message_list":message_list,
        "room": room,    
        "list_user":list_user,
        "list_room":list_room,
        "profiles":all_profiles,     
        "combined_list":combined_list,     
    }    
    return render(request, 'chat/inbox_group.html', context)


