from django.contrib import admin

from .models import Timeline, EventArea, Tag, Event

admin.site.register(Timeline)
admin.site.register(EventArea)
admin.site.register(Tag)
admin.site.register(Event)
