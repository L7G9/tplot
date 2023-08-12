from django.contrib.auth.models import User
from django.test import TestCase
from age_timelines.models import AgeEvent, AgeTimeline
from timelines.models import EventArea, Tag
from .populate_db import populate_db


class PopulateDBTest(TestCase):
    USERS = 3
    AGE_TIMELINES_PER_USER = 2
    EVENTS_PER_TIMELINE = 2
    TAGS_PER_TIMELINE = 1
    EVENT_AREAS_PER_TIMELINE = 1

    def test_populate_db_tables(self):
        populate_db(
            self.USERS,
            self.AGE_TIMELINES_PER_USER,
            self.EVENTS_PER_TIMELINE,
            self.TAGS_PER_TIMELINE,
            self.EVENT_AREAS_PER_TIMELINE
        )
        self.assertEqual(
            len(User.objects.all()),
            self.USERS
        )
        total_timelines = self.USERS * self.AGE_TIMELINES_PER_USER
        self.assertEqual(
            len(AgeTimeline.objects.all()),
            total_timelines
        )
        self.assertEqual(
            len(AgeEvent.objects.all()),
            total_timelines * self.EVENTS_PER_TIMELINE
        )
        self.assertEqual(
            len(EventArea.objects.all()),
            total_timelines * self.EVENT_AREAS_PER_TIMELINE
        )
        self.assertEqual(
            len(Tag.objects.all()),
            total_timelines * self.TAGS_PER_TIMELINE
        )

    def test_populate_db_output(self):
        users = populate_db(
            self.USERS,
            self.AGE_TIMELINES_PER_USER,
            self.EVENTS_PER_TIMELINE,
            self.TAGS_PER_TIMELINE,
            self.EVENT_AREAS_PER_TIMELINE
        )

        self.assertEqual(len(users), self.USERS)
        self.assertEqual(users[0]['username'], "User0")
        self.assertEqual(users[0]['password'], "Password0#")
        self.assertEqual(
            len(users[0]['age_timeline_ids']),
            self.AGE_TIMELINES_PER_USER
        )
        self.assertEqual(
            len(users[0]['age_timeline_ids'][0]['age_event_ids']),
            self.EVENTS_PER_TIMELINE
        )
        self.assertEqual(
            len(users[0]['age_timeline_ids'][0]['tag_ids']),
            self.TAGS_PER_TIMELINE
        )
        self.assertEqual(
            len(users[0]['age_timeline_ids'][0]['event_area_ids']),
            self.EVENT_AREAS_PER_TIMELINE
        )

    def test_populate_db_none(self):
        users = populate_db(0, 0, 0, 0, 0)

        self.assertEqual(len(User.objects.all()), 0)
        self.assertEqual(len(AgeTimeline.objects.all()), 0)
        self.assertEqual(len(AgeEvent.objects.all()), 0)
        self.assertAlmostEqual(len(EventArea.objects.all()), 0)
        self.assertEqual(len(Tag.objects.all()), 0)

        self.assertEqual(len(users), 0)
