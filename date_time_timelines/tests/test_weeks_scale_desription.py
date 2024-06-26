from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from date_time_timelines.models import DateTimeEvent, DateTimeTimeline, WEEK_1
from date_time_timelines.pdf.date_time import DateTime
from date_time_timelines.pdf.weeks_scale_description import (
    WeeksScaleDescription,
)
from timelines.pdf.round import Round


class WeeksScaleDescriptionTest(TestCase):
    @classmethod
    def setUpTestData(self):
        user = User.objects.create_user(
            username="TestUser", password="TestUser01#"
        )

        date_time_timeline = DateTimeTimeline.objects.create(
            user=user,
            title="Test Timeline Title",
            description="Test Timeline Description",
            scale_unit=WEEK_1,
            scale_length=7,
            page_size="4",
            page_orientation="L",
            page_scale_position=0,
        )
        DateTimeEvent.objects.create(
            date_time_timeline=date_time_timeline,
            timeline_id=date_time_timeline.timeline_ptr.pk,
            title="Title",
            start_date_time=datetime(
                year=2000, month=1, day=1, hour=1, minute=14, second=27
            ),
            has_end=False,
            end_date_time=datetime(
                year=2000, month=12, day=1, hour=0, minute=0, second=0
            ),
        )
        DateTimeEvent.objects.create(
            date_time_timeline=date_time_timeline,
            timeline_id=date_time_timeline.timeline_ptr.pk,
            title="Title",
            start_date_time=datetime(
                year=2000, month=1, day=1, hour=2, minute=0, second=0
            ),
            has_end=True,
            end_date_time=datetime(
                year=2000, month=1, day=1, hour=3, minute=23, second=44
            ),
        )
        self.scale_description = WeeksScaleDescription(
            date_time_timeline
        )

        date_time_timeline_no_events = DateTimeTimeline.objects.create(
            user=user,
            title="Test Timeline Title",
            description="Test Timeline Description",
            scale_unit=WEEK_1,
            scale_length=7,
            page_size="4",
            page_orientation="L",
            page_scale_position=0,
        )
        self.scale_description_no_events = (
            WeeksScaleDescription(date_time_timeline_no_events)
        )

    def test_start_date_time(self):
        result = self.scale_description.start_date_time.date_time
        expected = datetime(year=1999, month=12, day=27)
        self.assertEqual(result, expected)

    def test_end_date_time(self):
        result = self.scale_description.end_date_time.date_time
        expected = datetime(year=2000, month=1, day=3)
        self.assertEqual(result, expected)

    def test_get_scale_units(self):
        result = self.scale_description.get_scale_units()
        self.assertEqual(result, 1)

    def test_get_scale_units_no_events(self):
        result = self.scale_description_no_events.get_scale_units()
        self.assertEqual(result, 1)

    def test_get_scale_length(self):
        result = self.scale_description.get_scale_length()
        self.assertEqual(result, 70)

    def test_get_scale_label(self):
        result = self.scale_description.get_scale_label(1)
        self.assertEqual(result, "2000-01-03 00:00:00")

    def test_plot_1999_12_27(self):
        result = self.scale_description.plot(
            DateTime(datetime(year=1999, month=12, day=27))
        )
        self.assertEqual(result, 0.0)

    def test_plot_1999_12_30_12_00_00(self):
        result = self.scale_description.plot(
            DateTime(
                datetime(
                    year=1999, month=12, day=30, hour=12, minute=0, second=0
                )
            )
        )
        self.assertEqual(result, 35.0)

    def test_plot_2000_01_03(self):
        result = self.scale_description.plot(
            DateTime(
                datetime(year=2000, month=1, day=3))
        )
        self.assertEqual(result, 70.0)

    def test_round_datetime_weeks(self):
        in_datetime = datetime(
            year=2003, month=2, day=5, hour=4, minute=23, second=44
        )
        result = self.scale_description.round_datetime(
            in_datetime, WEEK_1, Round.DOWN
        )
        expected = datetime(
            year=2003, month=2, day=3, hour=0, minute=0, second=0
        )
        self.assertEqual(result, expected)
