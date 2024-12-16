from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from date_time_timelines.models import DateTimeEvent, DateTimeTimeline
from date_time_timelines.pdf.date_time import DateTime
from date_time_timelines.pdf.seconds_scale_description import (
    SecondsScaleDescription
)
from timelines.pdf.round import Round


class SecondsScaleDescriptionTest(TestCase):
    @classmethod
    def setUpTestData(self):
        user = User.objects.create_user(
            username="TestUser", password="TestUser01#"
        )

        date_time_timeline = DateTimeTimeline.objects.create(
            user=user,
            title="Test Timeline Title",
            description="Test Timeline Description",
            scale_unit=600,
            scale_unit_length=1,
            pdf_page_size="4",
            page_orientation="L",
            page_scale_position=0,
        )
        DateTimeEvent.objects.create(
            date_time_timeline=date_time_timeline,
            timeline_id=date_time_timeline.timeline_ptr.pk,
            title="Title",
            start_date_time=datetime(
                year=2000, month=1, day=1,
                hour=1, minute=14, second=27
            ),
            has_end=False,
            end_date_time=datetime(
                year=2000, month=12, day=1,
                hour=0, minute=0, second=0
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
        self.scale_description = SecondsScaleDescription(
            date_time_timeline
        )

        date_time_timeline_no_events = DateTimeTimeline.objects.create(
            user=user,
            title="Test Timeline Title",
            description="Test Timeline Description",
            scale_unit=600,
            scale_unit_length=1,
            pdf_page_size="4",
            page_orientation="L",
            page_scale_position=0,
        )
        self.scale_description_no_events = (
            SecondsScaleDescription(
                date_time_timeline_no_events
            )
        )

    def test_start_date_time(self):
        result = self.scale_description.start_date_time.date_time
        expected = datetime(
            year=2000, month=1, day=1, hour=1, minute=10, second=0
        )
        self.assertEqual(result, expected)

    def test_end_date_time(self):
        result = self.scale_description.end_date_time.date_time
        expected = datetime(
            year=2000, month=1, day=1, hour=3, minute=30, second=0
        )
        self.assertEqual(result, expected)

    def test_get_scale_units(self):
        result = self.scale_description.get_scale_units()
        self.assertEqual(result, 14)

    def test_get_scale_units_no_events(self):
        result = self.scale_description_no_events.get_scale_units()
        self.assertEqual(result, 1)

    def test_get_scale_unit_length(self):
        result = self.scale_description.get_scale_unit_length()
        self.assertEqual(result, 140)

    def test_get_scale_label(self):
        result = self.scale_description.get_scale_label(1)
        self.assertEqual(result, "2000-01-01 01:20:00")

    def test_plot_2000_01_01_01_10_00(self):
        result = self.scale_description.plot(
            DateTime(
                datetime(
                    year=2000, month=1, day=1, hour=1, minute=10, second=0
                )
            )
        )
        self.assertEqual(result, 0.0)

    def test_plot_2000_01_01_02_00_00(self):
        result = self.scale_description.plot(
            DateTime(
                datetime(
                    year=2000, month=1, day=1, hour=2, minute=0, second=0
                )
            )
        )
        self.assertEqual(result, 50.0)

    def test_plot_2000_01_01_03_10_00(self):
        result = self.scale_description.plot(
            DateTime(
                datetime(
                    year=2000, month=1, day=1, hour=3, minute=10, second=0
                )
            )
        )
        self.assertEqual(result, 120.0)

    def test_round_datetime_seconds(self):
        in_datetime = datetime(
            year=2003, month=2, day=3, hour=4, minute=23, second=44
        )
        result = self.scale_description.round_datetime(
            in_datetime, 60, Round.DOWN
        )
        expected = datetime(
            year=2003, month=2, day=3, hour=4, minute=23, second=0
        )
        self.assertEqual(result, expected)
