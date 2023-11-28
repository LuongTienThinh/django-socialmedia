from django.urls import path, include
from chat import views 
from django.urls import re_path

urlpatterns = [
    path("index/", views.index, name="inbox"),
    path("inbox/<int:user_id>/", views.inbox_detail, name="inbox_detail"),
    path("inbox-room/<int:room_id>/", views.inbox_group_detail, name="inbox_room_detail"),
    path("create-room/", views.CreateChatRoom.as_view(), name="create_room"),
    path("delete-room/<int:room_id>/", views.DeleteChatRoom.as_view(), name="delete_room"),
    path("edit-room/<int:room_id>/", views.EditChatRoom.as_view(), name="edit_room"),
    path("add-member-room/<int:room_id>/<int:user_id>/", views.AddMembersRoomChat.as_view(), name="add_member_room"),
    path("delete-member-room/<int:room_id>/<int:user_id>/", views.DeleteMembersRoomChat.as_view(), name="delete_member_room"),
    path("delete-private-chat/<int:user_id>/", views.DeletePrivateChat.as_view(), name="delete_private_chat"),

]
