from django.db import models
from authentication.models import User
from posts.models import Post, Comment, Reply

class Friendship(models.Model):
    user1 = models.ForeignKey(User, related_name='friendships1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='friendships2', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('friends', 'Friends'), ('pending', 'Pending')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followee = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followee')

    def __str__(self):
        return f"{self.followee} dang theo doi {self.follower}"
# -- Group

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
    
    def total_likes(self):
        return self.likes.count()
    
    def total_comment(self):
        return GroupComment.objects.filter(post=self).count() + GroupReply.objects.filter(comment__post=self).count()
    


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

# block user
class Block(models.Model):
    blocker = models.ForeignKey(User, related_name='blocker', on_delete=models.CASCADE)
    blocked_user = models.ForeignKey(User, related_name='blocked_user', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('blocker', 'blocked_user')


class GroupComment(models.Model):
    content = models.TextField()
    post = models.ForeignKey(GroupPost, related_name='group_comments', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='group_comments/images/', blank=True, null=True)
    user = models.ForeignKey(User, related_name='group_comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self) :
        return f'{self.post} | {self.content}'
    
class GroupReply(models.Model):
    content = models.TextField()
    comment = models.ForeignKey(GroupComment, related_name='group_replies', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

