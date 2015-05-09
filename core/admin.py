from django.contrib import admin

from core.models import User, Server, UserServer, Channel, UserChannel, \
    Message, PrivateMessage

# Register your models here.
admin.site.register(User)
admin.site.register(Server)
admin.site.register(UserServer)
admin.site.register(Channel)
admin.site.register(UserChannel)
admin.site.register(Message)
admin.site.register(PrivateMessage)
