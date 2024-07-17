from datetime import datetime

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


DISPLAY_FORMATS = [
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",
    "%Y-%m-%d",
    "%Y-%m",
    "%Y",
    "%m-%d %H:%M:%S",
    "%m-%d %H:%M",
    "%m-%d",
    "%m",
    "%d %H:%M:%S",
    "%d %H:%M",
    "%d",
    "%H:%M:%S",
    "%H:%M",
    "%H",
    "%M:%S",
    "%M",
    "%S",
    "%a %d %b %Y %H:%M:%S",
    "%a %d %b %Y %H:%M",
    "%a %d %b %Y",
    "%a %d %b",
    "%a %d",
    "%a",
    "%d %b %Y %H:%M:%S",
    "%d %b %Y %H:%M",
    "%d %b %Y",
    "%d %b",
    "%b %Y",
    "%b",
]


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

    DISPLAY_FORMAT_DESCRIPTIONS = [
        (0, "2000-04-03 13:30:15 (year-month-day hour:min:sec)"),
        (1, "2000-04-03 13:30 (year-month-day hour:min)"),
        (2, "2000-04-03 (year-month-day)"),
        (3, "2000-04 (year-month)"),
        (4, "2000 (year)"),
        (5, "04-03 13:30:15 (month-day hour:min:sec)"),
        (6, "04-03 13:30 (month-day hour:min)"),
        (7, "04-03 (month-day)"),
        (8, "04 (month)"),
        (9, "03 13:30:15 (day hour:min:sec)"),
        (10, "03 13:30 (day hour:min)"),
        (11, "03 (day)"),
        (12, "13:30:15(hour:min:sec)"),
        (13, "13:30 (hour:min)"),
        (14, "13 (hour)"),
        (15, "30:15 (min:sec)"),
        (16, "30 (min)"),
        (17, "15 (sec)"),
        (
            18,
            "Mon 03 Apr 2000 13:30:15 (day day:month:year hour:min:sec)",
        ),
        (
            19,
            "Mon 03 Apr 2000 13:30 (day day:month:year hour:min)",
        ),
        (20, "Mon 03 Apr 2000 (day day:month:year)"),
        (21, "Mon 03 Apr (day day:month)"),
        (22, "Mon 03 (day day)"),
        (23, "Mon (day)"),
        (24, "03 Apr 2000 13:30:15 (day:month:year hour:min:sec)"),
        (25, "03 Apr 2000 13:30 (day:month:year hour:min)"),
        (26, "03 Apr 2000 (day:month:year)"),
        (27, "03 Apr (day:month)"),
        (28, "Apr 2000 (month:year)"),
        (29, "Apr (month)"),
    ]

    scale_unit = models.PositiveIntegerField(
        choices=SCALE_UNITS, default=86400
    )

    event_display_format = models.PositiveSmallIntegerField(
        choices=DISPLAY_FORMAT_DESCRIPTIONS, default=0
    )

    scale_display_format = models.PositiveSmallIntegerField(
        choices=DISPLAY_FORMAT_DESCRIPTIONS, default=0
    )

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "date_time_timelines:date-time-timeline-detail",
            kwargs={"pk": self.pk},
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

    def get_event_display_format(self) -> str:
        """Get datetime format for events on timeline pdf."""
        return DISPLAY_FORMATS[self.event_display_format]

    def get_scale_display_format(self) -> str:
        """Get datetime format for scale on timeline pdf."""
        return DISPLAY_FORMATS[self.scale_display_format]


class DateTimeEvent(timelines.Event):
    date_time_timeline = models.ForeignKey(
        DateTimeTimeline, on_delete=models.CASCADE
    )
    start_date_time = models.DateTimeField(default=datetime.now)
    end_date_time = models.DateTimeField(default=datetime.now)

    class Meta:
        ordering = ["start_date_time"]

    def start_description(self):
        return self.start_date_time.strftime(
            DISPLAY_FORMATS[self.date_time_timeline.event_display_format]
        )

    def start_end_description(self):
        start = self.start_date_time.strftime(
            DISPLAY_FORMATS[self.date_time_timeline.event_display_format]
        )
        end = self.end_date_time.strftime(
            DISPLAY_FORMATS[self.date_time_timeline.event_display_format]
        )
        return f"{start} to {end}"

    def date_time_description(self):
        if self.has_end:
            return self.start_end_description()
        else:
            return self.start_description()

    def __str__(self):
        return f"{self.date_time_description()} : {self.title}"
