# friendships/forms.py
from django import forms
from .models import Friendship, Follow, Group, GroupPost, GroupComment, GroupReply

class FriendshipForm(forms.ModelForm):
    class Meta:
        model = Friendship
        fields = ['user2', 'status']

class FollowForm(forms.ModelForm):
    class Meta:
        model = Follow
        fields = ['followee']

# Group
class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control'}),           
        }

class GroupPostForm(forms.ModelForm):
    class Meta:
        model = GroupPost
        fields = ('title', 'content', 'image', 'video', )
        widgets = {
            'title': forms.Textarea(attrs={'class':'form-control'}),
            'content': forms.Textarea(attrs={'class':'form-control'}),           
        }

class GroupCommentForm(forms.ModelForm):
    class Meta:
        model = GroupComment
        fields = ('content','image',)

class GroupReplyForm(forms.ModelForm):
    class Meta:
        model = GroupReply
        fields = ('content',)
        