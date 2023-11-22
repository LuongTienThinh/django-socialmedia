from django.db import models
from authentication.models import User


class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="chat_user")
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="reciever")
    message = models.CharField(max_length=10000000000)
    is_read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.user)
    
    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Personal Chat"

class ChatRoom (models.Model):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(User, max_length=255, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name="group_chat_members")
    

class RoomMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete= models.CASCADE)    
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="group_sender")
    message = models.CharField(max_length=1000)    
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Group: {self.groupname} - Sender: {self.sender.username}"

    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Group Chats"

