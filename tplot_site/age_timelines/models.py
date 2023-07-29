from django.db import models
from timelines import models as timelines


class AgeTimeline(timelines.Timeline):
    SCALE_UNITS = [
        (1, "1 Year"),
        (5, "5 Years"),
        (10, "10 Years"),
        (20, "20 Years"),
        (25, "25 Years"),
        (50, "50 Years"),
        (100, "100 Years"),
    ]
    scale_unit = models.PositiveSmallIntegerField(choices=SCALE_UNITS, default=3)


class AgeEvent(timelines.Event):
    age_timeline = models.ForeignKey(AgeTimeline, on_delete=models.CASCADE)
    start_year = models.SmallIntegerField(default=0)
    start_month = models.SmallIntegerField(default=0)
    end_year = models.SmallIntegerField(default=0)
    end_month = models.SmallIntegerField(default=0)
