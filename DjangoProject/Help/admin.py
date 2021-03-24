from django.contrib import admin

from .models import *
# Register your models here.
admin.site.register(UserModel)
admin.site.register(LoginHistory)
admin.site.register(TicketModel)
admin.site.register(TicketReply)