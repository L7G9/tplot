from django.contrib import admin

from .models import AgeTimeline, AgeEvent


admin.site.register(AgeTimeline)
admin.site.register(AgeEvent)
