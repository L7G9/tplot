from django.contrib import admin

from .models import HistoricalEvent, HistoricalTimeline


admin.site.register(HistoricalTimeline)
admin.site.register(HistoricalEvent)
