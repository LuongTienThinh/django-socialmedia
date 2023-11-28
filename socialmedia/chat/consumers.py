# chat/consumers.py
import json
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import ChatMessage, RoomMessage, ChatRoom
from profiles.models import Profile
from django.core.serializers.json import DjangoJSONEncoder
from django.core.files.base import ContentFile
import base64

User = get_user_model()

class ChatMessageConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = 'chat-private_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        sender_username = data.get('sender')
        receiver_name = data.get('receiver')
        fileData = data.get('fileData')
        fileType = data.get('fileType')
        image = ""
        video = ""  
        if fileData and fileType:
            if fileType.startswith('image'):  # Kiểm tra nếu file là hình ảnh
                image_data = fileData.split(';base64,')[1]  # Loại bỏ phần đầu chuỗi Base64
                image = ContentFile(base64.b64decode(image_data), name='image.png')

                # Xử lý hình ảnh ở đây, ví dụ: lưu vào cơ sở dữ liệu, thực hiện các thao tác khác...
            elif fileType.startswith('video'):  # Kiểm tra nếu file là video
                video_data = fileData.split(';base64,')[1]  # Loại bỏ phần đầu chuỗi Base64
                video = ContentFile(base64.b64decode(video_data), name='video.mp4')
                # Xử lý video ở đây, ví dụ: lưu vào cơ sở dữ liệu, thực hiện các thao tác khác...

            else:
                image = ""
                video = ""  
        

        try:
            sender = User.objects.get(username=sender_username)
            receiver = User.objects.get(username=receiver_name)
            profile = Profile.objects.get(user=sender)
            profile_image = profile.profile_pic.url
        except User.DoesNotExist:
            profile_image = ''

        chat_message = ChatMessage(
            user=sender,
            sender=sender,
            receiver=receiver,
            message=message,
            image=image,
            video=video,
        )
        chat_message.save()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.username,
                'profile_image': profile_image,
                'receiver': receiver.username,
                'image': chat_message.image.url if chat_message.image else '',
                'video': chat_message.video.url if chat_message.video else '',
            }
        )

    def chat_message(self, event):
        self.send(text_data=json.dumps(event, cls=DjangoJSONEncoder))


class ChatRoomConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'chat-room_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        sender_name = data.get('sender')
        room = data.get('room')
        current_room = ChatRoom.objects.get(name=room)
        fileData = data.get('fileData')
        fileType = data.get('fileType')
        image = ""
        video = "" 

        if fileData and fileType:
            if fileType.startswith('image'):  # Kiểm tra nếu file là hình ảnh
                image_data = fileData.split(';base64,')[1]  # Loại bỏ phần đầu chuỗi Base64
                image = ContentFile(base64.b64decode(image_data), name='image.png')

                # Xử lý hình ảnh ở đây, ví dụ: lưu vào cơ sở dữ liệu, thực hiện các thao tác khác...
            elif fileType.startswith('video'):  # Kiểm tra nếu file là video
                video_data = fileData.split(';base64,')[1]  # Loại bỏ phần đầu chuỗi Base64
                video = ContentFile(base64.b64decode(video_data), name='video.mp4')
                # Xử lý video ở đây, ví dụ: lưu vào cơ sở dữ liệu, thực hiện các thao tác khác...

            else:
                image = ""
                video = ""  


        try:
            sender = User.objects.get(username=sender_name)
            profile = Profile.objects.get(user=sender)
            profile_image = profile.profile_pic.url
        except User.DoesNotExist:
            profile_image = ''

        chat_message = RoomMessage(
            sender=sender,
            room=current_room,
            message=message,
            image=image,
            video=video,
        )
        chat_message.save()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.username,
                'profile_image': profile_image,
                'room': current_room.name,
                'image': chat_message.image.url if chat_message.image else '',
                'video': chat_message.video.url if chat_message.video else '',
            }
        )

    def chat_message(self, event):
        self.send(text_data=json.dumps(event, cls=DjangoJSONEncoder))