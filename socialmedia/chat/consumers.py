# chat/consumers.py
import json
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import ChatMessage, RoomMessage
from profiles.models import Profile


User = get_user_model()

class ChatMessageConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

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

        try:
            sender = User.objects.get(username=sender_username)
            profile = Profile.objects.get(user=sender)
            profile_image = profile.profile_pic.url
        except User.DoesNotExist:
            profile_image = ''

        receiver = User.objects.get(username=data['receiver'])
        chat_message = ChatMessage(
            user = sender,
            sender=sender,
            receiver=receiver,
            message=message,
        )
        chat_message.save()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender_username,
                'profile_image': profile_image,
                'receiver': receiver.username,
            }
        )

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))

class ChatRoomConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['group_id']
        self.room_group_name = 'chat_%s' % self.room_name

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
        sender = data.get('sender')
        room = data.get('room')

        try:
            sender = User.objects.get(id=sender.id)
            profile = Profile.objects.get(user=sender)
            profile_image = profile.profile_pic.url
        except User.DoesNotExist:
            profile_image = ''

        chat_message = RoomMessage(
            sender=sender,
            room = room,
            message=message,
        )
        chat_message.save()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
                'profile_image': profile_image,
                'room': room,
            }
        )

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))