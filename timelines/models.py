from django.contrib.auth.models import User
from django.db import models


class Timeline(models.Model):
    # basic
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank=True)

    # scale
    SCALE_LENGTHS = [
        (1, "1cm"),
        (2, "2cm"),
        (3, "3cm"),
        (4, "4cm"),
        (5, "5cm"),
        (6, "6cm"),
        (7, "7cm"),
        (8, "8cm"),
        (9, "9cm"),
        (10, "10cm"),
        (12, "12cm"),
        (15, "15cm"),
        (20, "20cm"),
        (25, "25cm"),
        (30, "30cm"),
    ]
    scale_length = models.PositiveSmallIntegerField(
        choices=SCALE_LENGTHS, default=5
    )

    # display layout
    PAGE_SIZES = [("3", "A3"), ("4", "A4"), ("5", "A5")]
    page_size = models.CharField(max_length=1, choices=PAGE_SIZES, default="4")
    PAGE_ORIENTATIONS = [
        ("L", "Landscape"),
        ("P", "Portrait"),
    ]
    page_orientation = models.CharField(
        max_length=1, choices=PAGE_ORIENTATIONS, default="L"
    )
    page_scale_position = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_owner(self):
        return self.user


class EventArea(models.Model):
    timeline = models.ForeignKey(Timeline, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    page_position = models.PositiveSmallIntegerField(default=0)
    weight = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ["name"]
        unique_together = ["timeline", "page_position"]

    def __str__(self):
        return self.name

    def get_owner(self):
        return self.timeline.user


class Tag(models.Model):
    timeline = models.ForeignKey(Timeline, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_owner(self):
        return self.timeline.user


class Event(models.Model):
    timeline = models.ForeignKey(Timeline, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    timeline_area = models.ForeignKey(
        EventArea, blank=True, null=True, on_delete=models.SET_NULL
    )
    has_end = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_owner(self):
        return self.timeline.user
