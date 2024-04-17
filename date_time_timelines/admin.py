from django.contrib import admin

from .models import DateTimeTimeline, DateTimeEvent


admin.site.register(DateTimeTimeline)
admin.site.register(DateTimeEvent)
