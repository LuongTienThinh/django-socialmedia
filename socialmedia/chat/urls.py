from django.urls import path, include
from chat import views 
from django.urls import re_path

urlpatterns = [
    re_path(r'^inbox$', views.inbox, name="inbox"),
    path("inbox/<username>/", views.inbox_detail, name="inbox_detail"),
    path("inbox-room/<roomname>/", views.inbox_group_detail, name="inbox_room_detail"),

]
