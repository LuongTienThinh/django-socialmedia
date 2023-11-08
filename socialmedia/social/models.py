from django.db import models
from authentication.models import User
from posts.models import Post

class Friendship(models.Model):
    user1 = models.ForeignKey(User, related_name='friendships1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='friendships2', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('friends', 'Friends'), ('pending', 'Pending')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')

# class Follow(models.Model):
#     follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
#     followee = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('follower', 'followee')

class Group(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255,blank=True)
    image = models.ImageField(upload_to='group_pic/images/', blank=True, null=True)
    members = models.ManyToManyField(User, related_name='custom_groups', through='GroupMembership')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups', null=True, blank=True )

    def __str__(self):
        return f"{self.name}"

class GroupMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('requested', 'Requested'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='requested')
    is_creator = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} | {self.group}"



class GroupPost(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    title = models.TextField(blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='group_posts/images/', blank=True, null=True)
    video = models.FileField(upload_to='group_posts/videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    likes = models.ManyToManyField(User,related_name='group_posts_likes')

    def __str__(self):
        return f"{self.author} - {self.group}"
    
class MessageGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE) 
    message = models.TextField()
    status = models.CharField(max_length=20, choices=[('requested', 'Requested'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='requested')
    post = models.ForeignKey(
    GroupPost, 
    on_delete=models.CASCADE,
    null=True,
    blank=True
  )

class JoinRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Request from {self.user} to join {self.group}"
    
