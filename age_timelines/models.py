from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse

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
        choices=SCALE_UNITS, default=10
    )

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "age_timelines:age-timeline-detail", kwargs={"pk": self.pk}
        )


class AgeEvent(timelines.Event):
    age_timeline = models.ForeignKey(AgeTimeline, on_delete=models.CASCADE)
    start_year = models.SmallIntegerField(default=0)
    start_month = models.SmallIntegerField(
        default=0, validators=[MaxValueValidator(11), MinValueValidator(-11)]
    )
    end_year = models.SmallIntegerField(default=0)
    end_month = models.SmallIntegerField(
        default=0, validators=[MaxValueValidator(11), MinValueValidator(-11)]
    )

    class Meta:
        ordering = ["start_year", "start_month"]

    def age_string(self, years, months):
        if months == 0:
            return f"{years} Years"
        elif years == 0:
            return f"{months} Months"
        else:
            return f"{years} Years {months} Months"

    def start_description(self):
        return f"{self.age_string(self.start_year, self.start_month)}"

    def start_end_description(self):
        start = self.age_string(self.start_year, self.start_month)
        end = self.age_string(self.end_year, self.end_month)
        return f"{start} to {end}"

    def time_unit_description(self):
        if self.has_end:
            return self.start_end_description()
        else:
            return self.start_description()

    def __str__(self):
        return f"{self.time_unit_description()} : {self.title}"
