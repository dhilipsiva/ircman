from django.contrib import admin

from core.models import User, Server, UserServer, Channel, UserChannel, \
    Message, PrivateMessage, Conversation

# Register your models here.
admin.site.register(User)
admin.site.register(Server)
admin.site.register(UserServer)
admin.site.register(Channel)
admin.site.register(UserChannel)
admin.site.register(Message)
admin.site.register(Conversation)
admin.site.register(PrivateMessage)
