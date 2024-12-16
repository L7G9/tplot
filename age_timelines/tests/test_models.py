from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.test import TestCase

from age_timelines.models import AgeEvent, AgeTimeline


class AgeTimelineModel(TestCase):
    @classmethod
    def setUpTestData(self):
        user = User.objects.create_user(
            username="TestUser", password="TestUser01#"
        )
        age_timeline = AgeTimeline.objects.create(
            user=user,
            title="Test Age Timeline Title",
            description="Test Age Timeline Description",
            scale_unit=10,
            scale_unit_length=1,
            pdf_page_size="4",
            page_orientation="L",
            page_scale_position=0,
        )
        self.age_timeline_id = age_timeline.id

    def test_scale_unit_choices(self):
        age_timeline = AgeTimeline.objects.get(id=self.age_timeline_id)
        choices = age_timeline._meta.get_field("scale_unit").choices
        self.assertEqual(choices, AgeTimeline.SCALE_UNITS)

    def test_scale_unit_default(self):
        age_timeline = AgeTimeline.objects.get(id=self.age_timeline_id)
        default = age_timeline._meta.get_field("scale_unit").default
        self.assertEqual(default, 10)

    def test_ordering_by_title(self):
        age_timeline = AgeTimeline.objects.get(id=self.age_timeline_id)
        ordering = age_timeline._meta.ordering
        self.assertEqual(len(ordering), 1)
        self.assertEqual(ordering[0], "title")

    def test_object_name_is_title(self):
        age_timeline = AgeTimeline.objects.get(id=self.age_timeline_id)
        title = age_timeline.title
        self.assertEqual(str(age_timeline), title)

    def test_get_owner_is_user(self):
        age_timeline = AgeTimeline.objects.get(id=self.age_timeline_id)
        owner = age_timeline.user
        self.assertEqual(age_timeline.get_owner(), owner)

    def test_get_absolute_url(self):
        age_timeline = AgeTimeline.objects.get(id=self.age_timeline_id)
        url = f"/timelines/age/{age_timeline.id}/detail/"
        self.assertEqual(age_timeline.get_absolute_url(), url)


class AgeEventModel(TestCase):
    @classmethod
    def setUpTestData(self):
        user = User.objects.create_user(
            username="TestUser", password="TestUser01#"
        )
        age_timeline = AgeTimeline.objects.create(
            user=user,
            title="Test Age Timeline Title",
            description="Test Age Timeline Description",
            scale_unit=10,
            scale_unit_length=1,
            pdf_page_size="4",
            page_orientation="L",
            page_scale_position=0,
        )
        end_age_event = AgeEvent.objects.create(
            age_timeline=age_timeline,
            timeline_id=age_timeline.timeline_ptr.pk,
            title="Title",
            start_year=0,
            start_month=6,
            has_end=True,
            end_year=2,
            end_month=0,
        )
        self.end_age_event_id = end_age_event.id
        start_age_event = AgeEvent.objects.create(
            age_timeline=age_timeline,
            timeline_id=age_timeline.timeline_ptr.pk,
            title="Title",
            start_year=1,
            start_month=0,
            has_end=False,
        )
        self.start_age_event_id = start_age_event.id

    def test_start_year_default(self):
        event = AgeEvent.objects.get(id=self.start_age_event_id)
        default = event._meta.get_field("start_year").default
        self.assertEqual(default, 0)

    def test_start_month_default(self):
        event = AgeEvent.objects.get(id=self.start_age_event_id)
        default = event._meta.get_field("start_month").default
        self.assertEqual(default, 0)

    def test_start_month_max_validator(self):
        event = AgeEvent.objects.get(id=self.start_age_event_id)
        validator = event._meta.get_field("start_month").validators[0]
        self.assertEqual(validator, MaxValueValidator(11))

    def test_start_month_min_validator(self):
        event = AgeEvent.objects.get(id=self.start_age_event_id)
        validator = event._meta.get_field("start_month").validators[1]
        self.assertEqual(validator, MinValueValidator(-11))

    def test_end_year_default(self):
        event = AgeEvent.objects.get(id=self.start_age_event_id)
        default = event._meta.get_field("end_year").default
        self.assertEqual(default, 0)

    def test_end_month_default(self):
        event = AgeEvent.objects.get(id=self.start_age_event_id)
        default = event._meta.get_field("end_month").default
        self.assertEqual(default, 0)

    def test_end_month_max_validator(self):
        event = AgeEvent.objects.get(id=self.start_age_event_id)
        validator = event._meta.get_field("end_month").validators[0]
        self.assertEqual(validator, MaxValueValidator(11))

    def test_end_month_min_validator(self):
        event = AgeEvent.objects.get(id=self.start_age_event_id)
        validator = event._meta.get_field("end_month").validators[1]
        self.assertEqual(validator, MinValueValidator(-11))

    def test_ordering_by_start_year_and_start_month(self):
        event = AgeEvent.objects.get(id=self.start_age_event_id)
        ordering = event._meta.ordering
        self.assertEqual(len(ordering), 2)
        self.assertEqual(ordering[0], "start_year")
        self.assertEqual(ordering[1], "start_month")

    def test_age_string_no_months_no_years(self):
        event = AgeEvent.objects.get(id=self.start_age_event_id)
        description = event.age_string(0, 0)
        self.assertEqual(description, "0 Years")

    def test_age_string_months_no_years(self):
        event = AgeEvent.objects.get(id=self.start_age_event_id)
        description = event.age_string(0, 1)
        self.assertEqual(description, "1 Months")

    def test_age_string_years_no_months(self):
        event = AgeEvent.objects.get(id=self.start_age_event_id)
        description = event.age_string(1, 0)
        self.assertEqual(description, "1 Years")

    def test_age_string_years_and_months(self):
        event = AgeEvent.objects.get(id=self.start_age_event_id)
        description = event.age_string(1, 1)
        self.assertEqual(description, "1 Years 1 Months")

    def test_start_description(self):
        event = AgeEvent.objects.get(id=self.start_age_event_id)
        description = event.start_description()
        self.assertEqual(description, "1 Years")

    def test_start_and_description(self):
        event = AgeEvent.objects.get(id=self.end_age_event_id)
        description = event.start_end_description()
        self.assertEqual(description, "6 Months to 2 Years")

    def test_age_description(self):
        event = AgeEvent.objects.get(id=self.start_age_event_id)
        description = event.age_description()
        self.assertEqual(description, "1 Years")

    def test_age_description_has_end(self):
        event = AgeEvent.objects.get(id=self.end_age_event_id)
        description = event.age_description()
        self.assertEqual(description, "6 Months to 2 Years")

    def test_object_name_no_end(self):
        event = AgeEvent.objects.get(id=self.start_age_event_id)
        name = str(event)
        self.assertEqual(name, "1 Years : Title")

    def test_object_name_with_end(self):
        event = AgeEvent.objects.get(id=self.end_age_event_id)
        name = str(event)
        self.assertEqual(name, "6 Months to 2 Years : Title")

    def test_get_owner_is_timeline_user(self):
        event = AgeEvent.objects.get(id=self.start_age_event_id)
        expected_owner = event.age_timeline.user
        self.assertEqual(event.get_owner(), expected_owner)
