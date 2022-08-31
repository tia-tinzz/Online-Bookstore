from django.contrib import admin

# Register your models here.
from chat.models import Room, Message

admin.site.register(Room)
admin.site.register(Message)