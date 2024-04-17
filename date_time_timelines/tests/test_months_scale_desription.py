from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase

from date_time_timelines.models import (
    DateTimeEvent,
    DateTimeTimeline,
    MONTH_6,
)
from date_time_timelines.pdf.date_time import DateTime
from date_time_timelines.pdf.months_scale_description import (
    MonthsScaleDescription,
)
from timelines.pdf.round import Round


class MonthsScaleDescriptionTest(TestCase):
    @classmethod
    def setUpTestData(self):
        user = User.objects.create_user(
            username="TestUser", password="TestUser01#"
        )

        date_time_timeline = DateTimeTimeline.objects.create(
            user=user,
            title="Test Timeline Title",
            description="Test Timeline Description",
            scale_unit=MONTH_6,
            scale_length=6,
            page_size="4",
            page_orientation="L",
            page_scale_position=0,
        )
        DateTimeEvent.objects.create(
            date_time_timeline=date_time_timeline,
            timeline_id=date_time_timeline.timeline_ptr.pk,
            title="Title",
            start_date_time=datetime(year=2000, month=2, day=24),
            has_end=False,
            end_date_time=datetime(year=2000, month=2, day=24),
        )
        DateTimeEvent.objects.create(
            date_time_timeline=date_time_timeline,
            timeline_id=date_time_timeline.timeline_ptr.pk,
            title="Title",
            start_date_time=datetime(year=2000, month=2, day=24),
            has_end=True,
            end_date_time=datetime(year=2001, month=7, day=17),
        )
        self.scale_description = MonthsScaleDescription(
            date_time_timeline
        )

        date_time_timeline_no_events = DateTimeTimeline.objects.create(
            user=user,
            title="Test Timeline Title",
            description="Test Timeline Description",
            scale_unit=MONTH_6,
            scale_length=6,
            page_size="4",
            page_orientation="L",
            page_scale_position=0,
        )
        self.scale_description_no_events = (
            MonthsScaleDescription(
                date_time_timeline_no_events
            )
        )

    def test_start_date_time(self):
        result = self.scale_description.start_date_time.date_time
        expected = datetime(year=2000, month=1, day=1)
        self.assertEqual(result, expected)

    def test_end_date_time(self):
        result = self.scale_description.end_date_time.date_time
        expected = datetime(year=2002, month=1, day=1)
        self.assertEqual(result, expected)

    def test_get_scale_units(self):
        result = self.scale_description.get_scale_units()
        self.assertEqual(result, 4)

    def test_get_scale_units_no_events(self):
        result = self.scale_description_no_events.get_scale_units()
        self.assertEqual(result, 1)

    def test_get_scale_length(self):
        result = self.scale_description.get_scale_length()
        self.assertEqual(result, 240)

    def test_get_scale_label(self):
        result = self.scale_description.get_scale_label(1)
        self.assertEqual(result, "2000-07-01 00:00:00")

    def test_plot_2000_01_01(self):
        result = self.scale_description.plot(
            DateTime(datetime(year=2000, month=1, day=1))
        )
        self.assertEqual(result, 0.0)

    def test_plot_2000_04_01(self):
        result = self.scale_description.plot(
            DateTime(datetime(year=2000, month=4, day=1))
        )
        self.assertEqual(result, 30.0)

    def test_plot_2000_04_16(self):
        result = self.scale_description.plot(
            DateTime(datetime(year=2000, month=4, day=16))
        )
        self.assertEqual(result, 35.0)

    def test_plot_2000_07_01(self):
        result = self.scale_description.plot(
            DateTime(datetime(year=2000, month=7, day=1))
        )
        self.assertEqual(result, 60.0)

    def test_plot_2001_01_11(self):
        result = self.scale_description.plot(
            DateTime(datetime(year=2001, month=1, day=1))
        )
        self.assertEqual(result, 120.0)

    def test_round_datetime_months(self):
        in_datetime = datetime(
            year=2003, month=2, day=5, hour=4, minute=23, second=44
        )
        result = self.scale_description.round_datetime(
            in_datetime, MONTH_6, Round.DOWN
        )
        expected = datetime(
            year=2003, month=1, day=1, hour=0, minute=0, second=0
        )
        self.assertEqual(result, expected)
