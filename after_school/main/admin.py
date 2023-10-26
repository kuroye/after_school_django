from django.contrib import admin

from .models import Character, Event, EventGroup
# Register your models here.

admin.site.register(Character)
admin.site.register(Event)
admin.site.register(EventGroup)