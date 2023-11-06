from django.urls import path
from .views import AddPostView,AddCommentView, index, Like_Post, DeleteCommentView, EditCommentView, AddReplyView, DeleteReplyView, EditReplyView

urlpatterns = [
    path('posts/<str:page>/', index, name='home'),
    path('upload_post/', AddPostView.as_view(), name='upload_post'),
    path('like/<int:post_id>/', Like_Post, name='like_post'),
    path('add_comment/<int:post_id>/', AddCommentView.as_view(), name='add_comment'),
    path('delete_comment/<int:comment_id>/', DeleteCommentView.as_view(), name='delete_comment'),
    path('edit_comment/<int:comment_id>/', EditCommentView.as_view(), name='edit_comment'),
    path('add_reply/<int:comment_id>/', AddReplyView.as_view(), name='add_reply'),
    path('delete_reply/<int:reply_id>/', DeleteReplyView.as_view(), name='delete_reply'),
    path('edit_reply/<int:reply_id>/', EditReplyView.as_view(), name='edit_reply'),
]