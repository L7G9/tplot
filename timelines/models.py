from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


class Timeline(models.Model):
    # basic
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank=True)

    # scale
    SCALE_UNIT_LENGTHS = [
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
    scale_unit_length = models.PositiveSmallIntegerField(
        choices=SCALE_UNIT_LENGTHS, default=5
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

    def get_timeline(self):
        return self

    def get_role(self, user):
        if user is None:
            return ROLE_NONE
        elif user == self.user:
            return ROLE_OWNER
        else:
            collaborators = self.collaborator_set.filter(
                user=user
            )
            if len(collaborators) != 0:
                return collaborators[0].role
            else:
                return ROLE_NONE


class EventArea(models.Model):
    timeline = models.ForeignKey(Timeline, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    page_position = models.PositiveSmallIntegerField(default=0)
    weight = models.PositiveSmallIntegerField(
        default=1, validators=[MinValueValidator(1)],
    )

    class Meta:
        ordering = ["name"]
        unique_together = ["timeline", "page_position"]

    def __str__(self):
        return self.name

    def get_owner(self):
        return self.timeline.user

    def get_timeline(self):
        return self.timeline


class Tag(models.Model):
    timeline = models.ForeignKey(Timeline, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=1000, blank=True)
    display = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_owner(self):
        return self.timeline.user

    def get_timeline(self):
        return self.timeline


class Event(models.Model):
    timeline = models.ForeignKey(Timeline, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    event_area = models.ForeignKey(
        EventArea,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    has_end = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_owner(self):
        return self.timeline.user

    def get_timeline(self):
        return self.timeline

    def tag_string(self, display_only):
        if display_only:
            tags = self.tags.filter(display=True)
        else:
            tags = self.tags.all()

        if tags.count() > 0:
            tag_string = "("
            for tag in tags:
                if tag == tags.last():
                    tag_string += f"{tag.name})"
                else:
                    tag_string += f"{tag.name}, "
            return tag_string
        else:
            return ""


ROLE_NONE = 0
ROLE_VIEWER = 1
ROLE_EVENT_EDITOR = 2
ROLE_TIMELINE_EDITOR = 3
ROLE_OWNER = 4
ROLE_DESCRIPTIONS = [
    "None",
    "Viewer",
    "Event Editor",
    "Timeline Editor",
    "Owner",
]
ROLES = [
    (ROLE_VIEWER, ROLE_DESCRIPTIONS[ROLE_VIEWER]),
    (ROLE_EVENT_EDITOR, ROLE_DESCRIPTIONS[ROLE_EVENT_EDITOR]),
    (ROLE_TIMELINE_EDITOR, ROLE_DESCRIPTIONS[ROLE_TIMELINE_EDITOR]),
]


class Collaborator(models.Model):
    timeline = models.ForeignKey(Timeline, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.PositiveSmallIntegerField(
        choices=ROLES, default=ROLE_VIEWER
    )

    class Meta:
        unique_together = ["timeline", "user"]

    def get_owner(self):
        return self.timeline.user

    def get_timeline(self):
        return self.timeline

    def role_string(self):
        return ROLE_DESCRIPTIONS[self.role]
