from django.urls import path
from .views import SendFriendRequestView, AcceptFriendRequestView, FollowUserView, UnfollowUserView, RejectFriendRequestView

app_name = 'social'

urlpatterns = [
    path('send_friend_request/<int:user_id>/', SendFriendRequestView.as_view(), name='send_friend_request'),
    path('accept_friend_request/<int:pk>/', AcceptFriendRequestView.as_view(), name='accept_friend_request'),
    path('reject_friend_request/<int:pk>/', RejectFriendRequestView.as_view(), name='reject_friend_request'),
    path('follow_user/<int:user_id>', FollowUserView.as_view(), name='follow_user'),
    path('unfollow_user/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow_user'),
]
