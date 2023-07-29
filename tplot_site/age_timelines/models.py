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
    scale_unit = models.PositiveSmallIntegerField(
        choices=SCALE_UNITS,
        default=10
    )

    def __str__(self):
        return self.title


class AgeEvent(timelines.Event):
    age_timeline = models.ForeignKey(AgeTimeline, on_delete=models.CASCADE)
    start_year = models.SmallIntegerField(default=0)
    start_month = models.SmallIntegerField(default=0)
    end_year = models.SmallIntegerField(default=0)
    end_month = models.SmallIntegerField(default=0)

    def age_description(self, years, months):
        if months == 0:
            return f"{years} Years"
        elif years == 0:
            return f"{months} Months"
        else:
            return f"{years} Years {months} Months"

    def start_description(self):
        return f"{self.age_description(self.start_year, self.start_month)}"

    def start_end_description(self):
        start = self.age_description(self.start_year, self.start_month)
        end = self.age_description(self.end_year, self.end_month)
        return f"{start} to {end}"

    def __str__(self):
        if self.has_end:
            return f"{self.start_end_description()} : {self.title}"
        else:
            return f"{self.start_description()} : {self.title}"
