from django.urls import path
from .views import AddPostView, search, home1, friend, group, Like_Post, DeleteSharePost, ConfirmMembershipView, AddCommentView, DeleteCommentView, EditCommentView, AddReplyView, DeleteReplyView, EditReplyView, SharePostView, DeletePost, EditPostView

urlpatterns = [
    path('', home1, name='home'),
    path('friend/', friend, name='friend'),
    path('group/', group, name='group'),
    path('upload_post/', AddPostView.as_view(), name='upload_post'),
    path('like/<int:post_id>/', Like_Post, name='like_post'),
    path('add_comment/<int:post_id>/', AddCommentView.as_view(), name='add_comment'),
    path('delete_comment/<int:comment_id>/', DeleteCommentView.as_view(), name='delete_comment'),
    path('edit_comment/<int:comment_id>/', EditCommentView.as_view(), name='edit_comment'),
    path('add_reply/<int:comment_id>/', AddReplyView.as_view(), name='add_reply'),
    path('delete_reply/<int:reply_id>/', DeleteReplyView.as_view(), name='delete_reply'),
    path('edit_reply/<int:reply_id>/', EditReplyView.as_view(), name='edit_reply'),
    path('confirm-membership/<int:user_id>/<str:action>/<int:group_id>/', ConfirmMembershipView.as_view(), name='confirm-membership'),
    path('share-post/<int:post_id>/', SharePostView.as_view(), name='share_post'),
    path('delete-share-post/<int:share_id>/', DeleteSharePost.as_view(), name='delete_share_post'),
    path('delete-post/<int:post_id>/', DeletePost.as_view(), name='delete_post'),
    path('edit-post/<int:post_id>/', EditPostView.as_view(), name='edit_post'),
    path('search/', search, name='search'),
    
]