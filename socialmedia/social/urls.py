from django.urls import path
from .views import SendFriendRequestView, AcceptFriendRequestView, CreateGroup, CreateGroupPostView, Group_Posts, JoinGroupView, ApproveJoinRequestView


# app_name = 'social'

urlpatterns = [
    path('send_friend_request/<int:user_id>/', SendFriendRequestView.as_view(), name='send_friend_request'),
    path('accept_friend_request/<int:pk>/', AcceptFriendRequestView.as_view(), name='accept_friend_request'),
    path('create_group/', CreateGroup.as_view(), name='create_group'),
    path('group/<int:group_id>/', Group_Posts, name='group_posts'),
    path('group/<int:group_id>/create-post/', CreateGroupPostView.as_view(), name='create_group_post'),
    path('groups/<int:group_id>/join/', JoinGroupView.as_view(), name='join-group'),
    path('requests/<int:request_id>/approve/', ApproveJoinRequestView.as_view(), name='approve-join-request'),
#     path('follow_user/', FollowUserView.as_view(), name='follow_user'),
#     path('unfollow_user/<int:pk>/', UnfollowUserView.as_view(), name='unfollow_user'),

]
