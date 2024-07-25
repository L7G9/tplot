from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F
from django.urls import reverse

from timelines import models as timelines

from .historical_year import HistoricalYear


class HistoricalTimeline(timelines.Timeline):
    SCALE_UNITS = [
        (1, "1 Years"),
        (5, "5 Years"),
        (10, "10 Years"),
        (25, "25 Years"),
        (50, "50 Years"),
        (100, "100 Years"),
        (500, "500 Years"),
        (1000, "1000 Years"),
    ]
    scale_unit = models.IntegerField(
        choices=SCALE_UNITS, default=10
    )

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "historical_timelines:timeline-detail", kwargs={"pk": self.pk}
        )


class HistoricalEvent(timelines.Event):
    historical_timeline = models.ForeignKey(
        HistoricalTimeline,
        on_delete=models.CASCADE
    )

    BC_AD = [
        (-1, "BC"),
        (1, "AD"),
    ]

    start_bc_ad = models.SmallIntegerField(choices=BC_AD, default=-1)
    start_year = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
    )
    end_bc_ad = models.SmallIntegerField(choices=BC_AD, default=-1)
    end_year = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
    )

    class Meta:
        ordering = [F("start_bc_ad") * F("start_year")]

    def start_description(self):
        return str(HistoricalYear(self.start_bc_ad * self.start_year))

    def start_end_description(self):
        start = HistoricalYear(self.start_bc_ad * self.start_year)
        end = HistoricalYear(self.end_bc_ad * self.end_year)
        return start.start_end_string(end)

    def time_unit_description(self):
        if self.has_end:
            return self.start_end_description()
        else:
            return self.start_description()

    def __str__(self):
        return f"{self.time_unit_description()} : {self.title}"

    def get_start(self) -> int:
        return self.start_bc_ad * self.start_year

    def get_end(self) -> int:
        return self.end_bc_ad * self.end_year
