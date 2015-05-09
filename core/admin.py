from django.contrib import admin

from core.models import User, Server, Account, Message, PrivateMessage

# Register your models here.
admin.site.register(User)
admin.site.register(Server)
admin.site.register(Account)
admin.site.register(Message)
admin.site.register(PrivateMessage)
