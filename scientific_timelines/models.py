from django.db import models
from django.urls import reverse

from timelines import models as timelines

from .scientific_year import ScientificYear


class ScientificTimeline(timelines.Timeline):
    SCALE_UNITS = [
        (100, "0.1 Thousand Years"),
        (500, "0.5 Thousand Years"),
        (1000, "1.0 Thousand Years"),
        (100000, "0.1 Million Years"),
        (500000, "0.5 Million Years"),
        (1000000, "1.0 Million Years"),
        (100000000, "0.1 Billion Years"),
        (500000000, "0.5 Billion Years"),
        (1000000000, "1.0 Billion Years"),
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
            "scientific_timelines:timeline-detail",
            kwargs={"pk": self.pk}
        )


class ScientificEvent(timelines.Event):
    scientific_timeline = models.ForeignKey(
        ScientificTimeline,
        on_delete=models.CASCADE
    )

    MULTIPLIERS = [
        (1000, "Thousand years"),
        (1000000, "Million years"),
        (1000000000, "Billion years"),
    ]
    start_year_fraction = models.FloatField(default=1.0)
    start_multiplier = models.IntegerField(
        choices=MULTIPLIERS, default=1000
    )
    end_year_fraction = models.FloatField(default=1.0)
    end_multiplier = models.IntegerField(
        choices=MULTIPLIERS, default=1000
    )

    class Meta:
        ordering = ["start_multiplier", "start_year_fraction"]

    def start_description(self):
        return str(
            ScientificYear(self.start_year_fraction, self.start_multiplier)
        )

    def start_end_description(self):
        start = ScientificYear(self.start_year_fraction, self.start_multiplier)
        end = ScientificYear(self.end_year_fraction, self.start_multiplier)
        return start.start_end_string(end)

    def time_unit_description(self):
        if self.has_end:
            return self.start_end_description()
        else:
            return self.start_description()

    def __str__(self):
        return f"{self.time_unit_description()} : {self.title}"
