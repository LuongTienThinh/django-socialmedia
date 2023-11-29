from django.urls import path
from .views import (
    SendFriendRequestView, 
    AcceptFriendRequestView, 
    CreateGroup, 
    DeleteGroup,
    EditGroup,
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
    Like_Post,
    AddCommentView, 
    DeleteCommentView, 
    EditCommentView, 
    AddReplyView, 
    DeleteReplyView, 
    EditReplyView,
    
    
)


app_name = 'social'

urlpatterns = [
    path('send_friend_request/<int:user_id>/', SendFriendRequestView.as_view(), name='send_friend_request'),
    path('accept_friend_request/<int:pk>/', AcceptFriendRequestView.as_view(), name='accept_friend_request'),
    path('reject_friend_request/<int:pk>/', RejectFriendRequestView.as_view(), name='reject_friend_request'),
    path('cancel_friend_request/<int:pk>/', CancelFriendRequestView.as_view(), name='cancel_friend_request'),
    path('like/<int:post_id>/', Like_Post, name='like_post'),
    path('follow_user/<int:user_id>', FollowUserView.as_view(), name='follow_user'),
    path('unfollow_user/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow_user'),
    path('create_group/', CreateGroup.as_view(), name='create_group'),
    path('delete_group/<int:group_id>/', DeleteGroup.as_view(), name='delete_group'),
    path('edit_group/<int:group_id>/', EditGroup.as_view(), name='edit_group'),
    path('group/<int:group_id>/', Group_Posts, name='group_posts'),
    path('group/<int:group_id>/create-post/', CreateGroupPostView.as_view(), name='create_group_post'),
    path('groups/<int:group_id>/manage-membership/<int:user_id>/<str:action>/', ManageGroupMembershipView.as_view(), name='manage-group-membership'),
    path('groups/<int:group_id>/join/', JoinGroupView.as_view(), name='join-group'),
    path('groups/<int:group_id>/leave/<int:user_id>', LeaveGroupView.as_view(), name='leave-group'),
    path('delete_post/<int:post_id>/', DeleteGroupPost.as_view(), name='delete_group_post'),
    path('edit_post/<int:post_id>/', EditGroupPostView.as_view(), name='edit_group_post'),
    path('block_user/<int:user_id>/', block_user, name='block_user'),
    path('unblock_user/<int:user_id>/', unblock_user, name='unblock_user'),
    path('add_comment/<int:post_id>/', AddCommentView.as_view(), name='add_comment'),
    path('delete_comment/<int:comment_id>/', DeleteCommentView.as_view(), name='delete_comment'),
    path('edit_comment/<int:comment_id>/', EditCommentView.as_view(), name='edit_comment'),
    path('add_reply/<int:comment_id>/', AddReplyView.as_view(), name='add_reply'),
    path('delete_reply/<int:reply_id>/', DeleteReplyView.as_view(), name='delete_reply'),
    path('edit_reply/<int:reply_id>/', EditReplyView.as_view(), name='edit_reply'),
#     path('follow_user/', FollowUserView.as_view(), name='follow_user'),
#     path('unfollow_user/<int:pk>/', UnfollowUserView.as_view(), name='unfollow_user'),

]
