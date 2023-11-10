from django import forms
from .models import Post, Comment, Reply, Share

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'image', 'video', )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ('content',)
        
class ShareForm(forms.ModelForm):
    class Meta:
        model = Share
        fields = ('post', 'user',)


