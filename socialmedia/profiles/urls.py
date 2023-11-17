# profiles/urls.py
from django.urls import path
from .views import ProfileDetailView, ProfileCreateView, ProfileUpdateView, DeletePost, EditPostView, AddPostView

app_name = 'profiles'

urlpatterns = [
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile'),
    path('profile/create/', ProfileCreateView.as_view(), name='profile_create'),
    path('profile/update/<int:pk>/', ProfileUpdateView.as_view(), name='profile_update'),
    path('delete-post/<int:post_id>/', DeletePost.as_view(), name='delete_post'),
    path('edit-post/<int:post_id>/', EditPostView.as_view(), name='edit_post'),
    path('upload_post/', AddPostView.as_view(), name='upload_post'),
]
