from django.db import models
from authentication.models import User

class Post(models.Model):
    title = models.TextField(blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='posts/images/', blank=True, null=True)
    video = models.FileField(upload_to='posts/videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    likes = models.ManyToManyField(User,related_name='posts_likes')

    def total_likes(self):
        return self.likes.count()

    def __str__(self) :
        return f'{self.title} | {self.user}'
    
    def total_comment(self):
        return Comment.objects.filter(post=self).count() + Reply.objects.filter(comment__post=self).count()
    
    def share_count(self):
        return Share.objects.filter(post=self).count()

class Comment(models.Model):
    content = models.TextField(blank=True)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='comments/images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self) :
        return f'{self.user} | {self.content}'
    
class Reply(models.Model):
    content = models.TextField()
    comment = models.ForeignKey(Comment, related_name='replies', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return f'{self.comment} | {self.comment.post}'
    

class Share(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    shared_at = models.DateTimeField(auto_now_add=True)
    def __str__(self) :
       return f'{self.post.title} | {self.user}'