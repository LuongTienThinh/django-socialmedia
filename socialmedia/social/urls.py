from django.urls import path
from .views import (
    SendFriendRequestView, 
    AcceptFriendRequestView, 
    CreateGroup, 
    CreateGroupPostView, 
    Group_Posts, 
    JoinGroupView, 
    LeaveGroupView, 
    ManageGroupMembershipView,
    FollowUserView, 
    UnfollowUserView, 
    RejectFriendRequestView,
    EditGroupPostView,
    DeleteGroupPost,
    CancelFriendRequestView,
    block_user,
    unblock_user,
    
)


app_name = 'social'

urlpatterns = [
    path('send_friend_request/<int:user_id>/', SendFriendRequestView.as_view(), name='send_friend_request'),
    path('accept_friend_request/<int:pk>/', AcceptFriendRequestView.as_view(), name='accept_friend_request'),
    path('reject_friend_request/<int:pk>/', RejectFriendRequestView.as_view(), name='reject_friend_request'),
    path('cancel_friend_request/<int:pk>/', CancelFriendRequestView.as_view(), name='cancel_friend_request'),
    path('follow_user/<int:user_id>', FollowUserView.as_view(), name='follow_user'),
    path('unfollow_user/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow_user'),
    path('create_group/', CreateGroup.as_view(), name='create_group'),
    path('group/<int:group_id>/', Group_Posts, name='group_posts'),
    path('group/<int:group_id>/create-post/', CreateGroupPostView.as_view(), name='create_group_post'),
    path('groups/<int:group_id>/manage-membership/<int:user_id>/<str:action>/', ManageGroupMembershipView.as_view(), name='manage-group-membership'),
    path('groups/<int:group_id>/join/', JoinGroupView.as_view(), name='join-group'),
    path('groups/<int:group_id>/leave/', LeaveGroupView.as_view(), name='leave-group'),
    path('delete_post/<int:post_id>/', DeleteGroupPost.as_view(), name='delete_group_post'),
    path('edit_post/<int:post_id>/', EditGroupPostView.as_view(), name='edit_group_post'),
    path('block_user/<int:user_id>/', block_user, name='block_user'),
    path('unblock_user/<int:user_id>/', unblock_user, name='unblock_user'),
#     path('follow_user/', FollowUserView.as_view(), name='follow_user'),
#     path('unfollow_user/<int:pk>/', UnfollowUserView.as_view(), name='unfollow_user'),

]
