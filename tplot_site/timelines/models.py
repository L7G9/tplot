from django.db import models


class Timeline(models.Model):

    PAGE_SIZES = [
        ("3", "A3"),
        ("4", "A4"),
        ("5", "A5")
    ]

    PAGE_ORIENTATIONS = [
        ("L", "Landscape"),
        ("P", "Portrait"),
    ]

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

    # basic
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    # date_created = models.
    # date_updated = models.
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank=True)

    # scale
    scale_length = models.PositiveSmallIntegerField(
        choices=SCALE_LENGTHS,
        default=5
    )

    # display layout
    page_size = models.CharField(max_length=1, choices=PAGE_SIZES, default="4")
    page_orientation = models.CharField(
        max_length=1,
        choices=PAGE_ORIENTATIONS,
        default="L"
    )
    page_scale_position = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.title


class TimelineArea(models.Model):
    timeline = models.ForeignKey(Timeline, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    # page_position = models.PositiveSmallIntegerField(default=0)
    weight = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.name


class Tag(models.Model):
    timeline = models.ForeignKey(Timeline, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Event(models.Model):
    timeline = models.ForeignKey(Timeline, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    timeline_area = models.ForeignKey(
        TimelineArea,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    has_end = models.BooleanField(default=False)

    def __str__(self):
        return self.title
