from django.db import models
from django.urls import reverse

from timelines import models as timelines

WEEK_1 = 401
MONTH_PREFIX = 500
MONTH_1 = MONTH_PREFIX + 1
MONTH_2 = MONTH_PREFIX + 2
MONTH_3 = MONTH_PREFIX + 3
MONTH_6 = MONTH_PREFIX + 6
YEAR_PREFIX = 60000
YEAR_1 = YEAR_PREFIX + 1
YEAR_5 = YEAR_PREFIX + 5
YEAR_10 = YEAR_PREFIX + 10
YEAR_100 = YEAR_PREFIX + 100
YEAR_1000 = YEAR_PREFIX + 1000


class DateTimeTimeline(timelines.Timeline):
    SCALE_UNITS = [
        (1, "1 Second"),
        (5, "5 Seconds"),
        (10, "10 Seconds"),
        (15, "15 Seconds"),
        (30, "30 Seconds"),
        (60, "1 Minute"),
        (300, "5 Minutes"),
        (600, "10 Minutes"),
        (900, "15 Minutes"),
        (1800, "30 Minutes"),
        (3600, "1 Hour"),
        (10800, "3 Hours"),
        (21600, "6 Hours"),
        (43200, "12 Hours"),
        (86400, "1 Day"),
        (WEEK_1, "1 Week"),
        (MONTH_1, "1 Month"),
        (MONTH_2, "2 Months"),
        (MONTH_3, "3 Months"),
        (MONTH_6, "6 Months"),
        (YEAR_1, "1 Year"),
        (YEAR_5, "5 Years"),
        (YEAR_10, "10 Years"),
        (YEAR_100, "100 Years"),
        (YEAR_1000, "1000 Years"),
    ]

    scale_unit = models.PositiveIntegerField(
        choices=SCALE_UNITS, default=86400
    )

    # event_date_format = models.CharField(max_length=100)

    # scale_date_format = models.CharField(max_length=100)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "date_time_timelines:date-time-timeline-detail",
            kwargs={"pk": self.pk}
        )

    def is_week_scale_unit(self) -> bool:
        """Test if scale_unit refers to scale a measured in weeks."""
        return self.scale_unit == WEEK_1

    def is_month_scale_unit(self) -> bool:
        """Test if scale_unit refers to scale a measured in months."""
        return self.scale_unit >= MONTH_1 and self.scale_unit <= MONTH_6

    def get_months_in_scale_unit(self) -> int:
        """Get the number of months per scale unit."""
        return self.scale_unit - MONTH_PREFIX

    def is_year_scale_unit(self) -> bool:
        """Test if scale_unit refers to scale a measured in years."""
        return self.scale_unit >= YEAR_1 and self.scale_unit <= YEAR_1000

    def get_years_in_scale_unit(self) -> int:
        """Get the number of years per scale unit."""
        return self.scale_unit - YEAR_PREFIX


class DateTimeEvent(timelines.Event):
    date_time_timeline = models.ForeignKey(
        DateTimeTimeline,
        on_delete=models.CASCADE
    )
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()

    class Meta:
        ordering = ["start_date_time"]

    def start_description(self):
        return self.start_date_time

    def start_end_description(self):
        start = self.start_date_time
        end = self.end_date_time
        return f"{start} to {end}"

    def __str__(self):
        if self.has_end:
            return f"{self.start_end_description()} : {self.title}"
        else:
            return f"{self.start_description()} : {self.title}"
