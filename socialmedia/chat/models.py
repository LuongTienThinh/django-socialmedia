from django.db import models
from authentication.models import User
from django.contrib.auth import get_user_model


User = get_user_model()
class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="chat_user")
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="reciever")
    message = models.CharField(max_length=10000000000)
    image = models.ImageField(upload_to='room-messages/images/', blank=True, null=True)
    video = models.FileField(upload_to='room-messages/videos/', blank=True, null=True)
    is_read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):        
        return f"Sender: {str(self.sender)} - receiver: {str(self.receiver)}"
    
    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Personal Chat"

class ChatRoom (models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='room-messages/cover-pic/', blank=True, null=True)
    creator = models.ForeignKey(User, max_length=255, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name="group_chat_members")
    def __str__(self):        
        return f"room: {str(self.name)} "
    

class RoomMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete= models.CASCADE)    
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="group_sender")
    message = models.CharField(max_length=1000)    
    image = models.ImageField(upload_to='messages/images/', blank=True, null=True)
    video = models.FileField(upload_to='messages/videos/', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Group: {self.room.name} - Sender: {self.sender.username}"

    class Meta:
        ordering = ["-date"]
        verbose_name_plural = "Group Chats"

