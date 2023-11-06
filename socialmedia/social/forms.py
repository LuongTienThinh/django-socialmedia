# friendships/forms.py
from django import forms
from .models import Friendship, Group, GroupPost

class FriendshipForm(forms.ModelForm):
    class Meta:
        model = Friendship
        fields = ['user2', 'status']

# class FollowForm(forms.ModelForm):
#     class Meta:
#         model = Follow
#         fields = ['followee']

# Group
class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description', 'image']

class GroupPostForm(forms.ModelForm):
    class Meta:
        model = GroupPost
        fields = ('title', 'content', 'image', 'video', )
