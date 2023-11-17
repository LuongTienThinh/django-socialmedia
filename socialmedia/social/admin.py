from django.contrib import admin
from .models import Friendship, Group, GroupMembership, GroupPost, MessageGroup, Follow, Block, GroupComment, GroupReply

class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('id', 'user1', 'user2', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user1__username', 'user2__username')

# class FollowAdmin(admin.ModelAdmin):
#     list_display = ('id', 'follower', 'followee', 'created_at')
#     search_fields = ('follower__username', 'followee__username')

admin.site.register(Friendship, FriendshipAdmin)

admin.site.register(Follow)
admin.site.register(GroupMembership)
admin.site.register(GroupPost)
admin.site.register(Group)
admin.site.register(MessageGroup)
admin.site.register(Block)
admin.site.register(GroupComment)
admin.site.register(GroupReply)
