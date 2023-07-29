from django.contrib import admin

from .models import Timeline, TimelineArea, Tag, Event

admin.site.register(Timeline)
admin.site.register(TimelineArea)
admin.site.register(Tag)
admin.site.register(Event)
