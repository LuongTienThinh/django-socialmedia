from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat-private/(?P<user_id>\w+)/$', consumers.ChatMessageConsumer.as_asgi()),
    re_path(r'ws/chat-room/(?P<room_id>\d+)/$', consumers.ChatRoomConsumer.as_asgi()),

]
