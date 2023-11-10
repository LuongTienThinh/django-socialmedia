from django.contrib import admin
from .models import Post, Comment, Reply, Share
 
# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Share)