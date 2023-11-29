from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect

from django.views.generic import CreateView, View
from django.db.models import OuterRef, Subquery, Q
from .forms import ChatRoomForm
from .models import ChatMessage, ChatRoom, RoomMessage
from authentication.models import User
from profiles.models import Profile
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@login_required(login_url='/auth/login/')
def index(request):
    all_profiles = Profile.objects.all()

    chat_users = ChatMessage.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
    list_user = list(set([chat.sender if chat.sender != request.user else chat.receiver for chat in chat_users]))
    list_room = ChatRoom.objects.filter(Q(members=request.user)| Q(creator=request.user)).distinct()
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

@login_required(login_url='/auth/login/')
def inbox_detail(request, user_id):

    sender = request.user
    receiver_user = User.objects.get(id =user_id)
    message_list = ChatMessage.objects.filter(
        Q(sender=sender, receiver=receiver_user) | Q(sender=receiver_user, receiver=sender)
    ).order_by("date")

    messages_detail = ChatMessage.objects.filter(
        Q(sender=sender, receiver=receiver_user) | Q(sender=receiver_user, receiver=sender)
    ).order_by("date")

    chat_users = ChatMessage.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
    list_user = list(set([chat.sender if chat.sender != request.user else chat.receiver for chat in chat_users]))

    list_room = ChatRoom.objects.filter(Q(members=request.user)| Q(creator=request.user)).distinct()
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
        receiver = User.objects.get(id =user_id)

    context = {
        "receiver":receiver,
        "receiver_user":receiver_user,
        "sender":sender,
        "message_list":message_list,
        "combined_list":combined_list,    
        "profiles":all_profiles,
    }
    return render(request, 'chat/inbox_detail.html', context)


@login_required(login_url='/auth/login/')
def inbox_group_detail(request, room_id):
    room_name = ChatRoom.objects.get(id = room_id)
    message_list = RoomMessage.objects.filter(
        Q(room__id = room_name.id)
    ).order_by("date")
    reversed_list = list(reversed(message_list))

    sender = request.user
   
    all_profiles = Profile.objects.all()

    chat_users = ChatMessage.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
    list_user = list(set([chat.sender if chat.sender != request.user else chat.receiver for chat in chat_users]))
    list_room = ChatRoom.objects.filter(Q(members=request.user)| Q(creator=request.user)).distinct()
    combined_list = []

    # Thêm các người dùng vào danh sách kết hợp và đánh dấu chúng là người dùng
    for user in list_user:
        combined_list.append({'object': user, 'type': 'user'})

    # Thêm các phòng chat vào danh sách kết hợp và đánh dấu chúng là phòng chat
    for room in list_room:
        combined_list.append({'object': room, 'type': 'room'})

    friends = User.objects.filter(
                Q(friendships1__user2=request.user, friendships1__status='friends') |
                Q(friendships2__user1=request.user, friendships2__status='friends')
            ).distinct()

    # danh sách thành viên nhóm chat
    room_members = room_name.members.all().exclude(id = room_name.creator.id )
    # danh sách bạn bè chưa tham gia nhóm chat
    not_joined_friends = friends.exclude(id__in=[member.id for member in room_members])

    form = ChatRoomForm(request.GET, request.FILES, instance=room_name)

    context = {     
        "sender":sender,
        "message_list":message_list,
        "room": room_name,    
        "list_user":list_user,
        "list_room":list_room,
        "profiles":all_profiles,     
        "combined_list":combined_list,     
        "friends":friends,     
        "room_members":room_members,     
        "not_joined_friends":not_joined_friends,     
        "form":form,     
    }    
    return render(request, 'chat/inbox_group.html', context)


@method_decorator(login_required(login_url='/auth/login/'), name='dispatch')
class CreateChatRoom(CreateView):
    template_name = 'chat/inbox.html'
    def get(self, request):
        form = ChatRoomForm(request.POST, request.FILES)  # Tạo một mẫu trống để hiển thị
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ChatRoomForm(request.POST, request.FILES)  # Truyền dữ liệu từ POST và FILES vào mẫu
        if form.is_valid():
            chatroom = form.save(commit=False)  # Lưu nhóm vào cơ sở dữ liệu
            chatroom.creator = self.request.user
            chatroom.save()
            return redirect('inbox_room_detail', room_id=chatroom.id)  # Chuyển hướng đến trang bài viết của nhóm vừa tạo

        return redirect('inbox_room_detail', room_id=chatroom.id)
    

@method_decorator(login_required(login_url='/auth/login/'), name='dispatch')
class DeleteChatRoom(View):
    def post(self, request, room_id):
        room = get_object_or_404(ChatRoom, id=room_id)
        if request.user.id == room.creator.id:
            room.delete()
        return redirect('inbox')  # Điều hướng sau khi xóa

    def get(self, request, room_id):
        room = get_object_or_404(ChatRoom, id=room_id)
        if request.user.id == room.creator.id:
            room.delete()
        return redirect('inbox')
    
@method_decorator(login_required(login_url='/auth/login/'), name='dispatch')
class EditChatRoom(View):
    template_name = 'chat/inbox_group.html'

    def post(self, request, room_id):
        room = get_object_or_404(ChatRoom, id=room_id)
        print(1111)
        print(room.name)
        form = ChatRoomForm(request.POST, request.FILES, instance=room)
        if request.user == room.creator:
            if form.is_valid():
                form.save()
            return redirect('inbox_room_detail',room_id=room_id)  # Điều hướng sau khi xóa
    
        return render(request, self.template_name, {'form': form, 'room_id': room_id})

@method_decorator(login_required(login_url='/auth/login/'), name='dispatch')
class AddMembersRoomChat(CreateView):
    def post(self, request, user_id, room_id):
        room = get_object_or_404(ChatRoom, id=room_id)
        if request.user.id == room.creator.id:
            user = get_object_or_404(User, id = user_id)
            if not user in room.members.all():
                room.members.add(user)
            return redirect('inbox_room_detail', room_id=room_id)
        return redirect('inbox_room_detail', room_id=room_id)
        

@method_decorator(login_required(login_url='/auth/login/'), name='dispatch')
class DeleteMembersRoomChat(View):
    def post(self, request, user_id, room_id):
        room = get_object_or_404(ChatMessage, id=room_id)
        user = get_object_or_404(User,id=user_id)
        if request.user.id == room.creator.id :        
            if user in room.members.all():
                room.members.remove(user)
            return redirect('inbox_room_detail', room_id=room_id)
        if request.user == user:
            if user in room.members.all():
                room.members.remove(user)
            return redirect('inbox')
        return redirect('inbox_room_detail', room_id=room_id)
    
@method_decorator(login_required(login_url='/auth/login/'), name='dispatch')
class DeletePrivateChat(View):
    def post(self, request, user_id):
        receiver = get_object_or_404(User,id=user_id)
        sender = request.user  # Thay bằng người gửi cụ thể

        # Lấy tất cả các tin nhắn liên quan đến người gửi và người nhận
        messages_to_delete = ChatMessage.objects.filter(sender=sender, receiver=receiver) | ChatMessage.objects.filter(sender=receiver, receiver=sender)

        # Kiểm tra xem có tin nhắn nào để xóa hay không
        if messages_to_delete.exists():
            # Xóa tất cả các tin nhắn
            messages_to_delete.delete()
            # Tin nhắn đã được xóa thành công
            return redirect('inbox')
        else:
            messages_to_delete.delete()
            # Không có tin nhắn nào để xóa
            # Thực hiện logic hoặc trả về thông báo tùy thuộc vào yêu cầu của bạn
            return redirect('inbox')
        