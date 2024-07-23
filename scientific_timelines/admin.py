from django.contrib import admin

from .models import ScientificEvent, ScientificTimeline


admin.site.register(ScientificTimeline)
admin.site.register(ScientificEvent)
