from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db.models import F
from django.test import TestCase

from historical_timelines.models import HistoricalEvent, HistoricalTimeline


class HistoricalTimelineModel(TestCase):
    @classmethod
    def setUpTestData(self):
        user = User.objects.create_user(
            username="TestUser", password="TestUser01#"
        )
        historical_timeline = HistoricalTimeline.objects.create(
            user=user,
            title="Test Historical Timeline Title",
            description="Test Historical Timeline Description",
            scale_unit=10,
            scale_unit_length=1,
            pdf_page_size="4",
            page_orientation="L",
            page_scale_position=0,
        )
        self.historical_timeline_id = historical_timeline.id

    def test_scale_unit_choices(self):
        historical_timeline = HistoricalTimeline.objects.get(
            id=self.historical_timeline_id
        )
        choices = historical_timeline._meta.get_field("scale_unit").choices
        self.assertEqual(choices, HistoricalTimeline.SCALE_UNITS)

    def test_scale_unit_default(self):
        historical_timeline = HistoricalTimeline.objects.get(
            id=self.historical_timeline_id
        )
        default = historical_timeline._meta.get_field("scale_unit").default
        self.assertEqual(default, 10)

    def test_ordering_by_title(self):
        historical_timeline = HistoricalTimeline.objects.get(
            id=self.historical_timeline_id
        )
        ordering = historical_timeline._meta.ordering
        self.assertEqual(len(ordering), 1)
        self.assertEqual(ordering[0], "title")

    def test_object_name_is_title(self):
        historical_timeline = HistoricalTimeline.objects.get(
            id=self.historical_timeline_id
        )
        title = historical_timeline.title
        self.assertEqual(str(historical_timeline), title)

    def test_get_owner_is_user(self):
        historical_timeline = HistoricalTimeline.objects.get(
            id=self.historical_timeline_id
        )
        owner = historical_timeline.user
        self.assertEqual(historical_timeline.get_owner(), owner)

    def test_get_absolute_url(self):
        historical_timeline = HistoricalTimeline.objects.get(
            id=self.historical_timeline_id
        )
        url = f"/timelines/historical/{historical_timeline.id}/detail/"
        self.assertEqual(historical_timeline.get_absolute_url(), url)


class HistoricalEventModel(TestCase):
    @classmethod
    def setUpTestData(self):
        user = User.objects.create_user(
            username="TestUser", password="TestUser01#"
        )
        historical_timeline = HistoricalTimeline.objects.create(
            user=user,
            title="Test Historical Timeline Title",
            description="Test Historical Timeline Description",
            scale_unit=10,
            scale_unit_length=1,
            pdf_page_size="4",
            page_orientation="L",
            page_scale_position=0,
        )
        self.historical_timeline_id = historical_timeline.id

        end_historical_event = HistoricalEvent.objects.create(
            historical_timeline=historical_timeline,
            timeline_id=historical_timeline.timeline_ptr.pk,
            title="Title",
            start_bc_ad=1,
            start_year=1,
            has_end=True,
            end_bc_ad=2,
            end_year=0,
        )
        self.end_historical_event_id = end_historical_event.id

        start_historical_event = HistoricalEvent.objects.create(
            historical_timeline=historical_timeline,
            timeline_id=historical_timeline.timeline_ptr.pk,
            title="Title",
            start_bc_ad=1,
            start_year=12,
            has_end=False,
        )
        self.start_historical_event_id = start_historical_event.id

    def test_start_bc_ad_choices(self):
        historical_event = HistoricalEvent.objects.get(
            id=self.start_historical_event_id
        )
        choices = historical_event._meta.get_field("start_bc_ad").choices
        self.assertEqual(choices, HistoricalEvent.BC_AD)

    def test_start_bc_ad_default(self):
        event = HistoricalEvent.objects.get(id=self.start_historical_event_id)
        default = event._meta.get_field("start_bc_ad").default
        self.assertEqual(default, -1)

    def test_start_year_default(self):
        event = HistoricalEvent.objects.get(id=self.start_historical_event_id)
        default = event._meta.get_field("start_year").default
        self.assertEqual(default, 1)

    def test_start_year_min_validator(self):
        event = HistoricalEvent.objects.get(id=self.start_historical_event_id)
        validator = event._meta.get_field("start_year").validators[0]
        self.assertEqual(validator, MinValueValidator(1))

    def test_end_bc_ad_choices(self):
        event = HistoricalEvent.objects.get(id=self.start_historical_event_id)
        choices = event._meta.get_field("end_bc_ad").choices
        self.assertEqual(choices, HistoricalEvent.BC_AD)

    def test_end_bc_ad_default(self):
        event = HistoricalEvent.objects.get(id=self.start_historical_event_id)
        default = event._meta.get_field("end_bc_ad").default
        self.assertEqual(default, -1)

    def test_end_year_default(self):
        event = HistoricalEvent.objects.get(id=self.start_historical_event_id)
        default = event._meta.get_field("end_year").default
        self.assertEqual(default, 1)

    def test_end_year_min_validator(self):
        event = HistoricalEvent.objects.get(id=self.start_historical_event_id)
        validator = event._meta.get_field("end_year").validators[0]
        self.assertEqual(validator, MinValueValidator(1))

    def test_ordering_by_start_year_and_start_month(self):
        event = HistoricalEvent.objects.get(id=self.start_historical_event_id)
        ordering = event._meta.ordering
        self.assertEqual(len(ordering), 1)
        self.assertEqual(ordering[0], F("start_bc_ad") * F("start_year"))
