from django.contrib.auth.models import User
from django.test import TestCase

from age_timelines.models import AgeEvent, AgeTimeline
from age_timelines.pdf.age import Age
from age_timelines.pdf.age_timeline_scale_description import AgeTimelineScaleDescription


class AgeTimelineScaleDescriptionTest(TestCase):
    @classmethod
    def setUpTestData(self):
        user = User.objects.create_user(
            username="TestUser", password="TestUser01#"
        )

        age_timeline = AgeTimeline.objects.create(
            user=user,
            title="Test Age Timeline Title",
            description="Test Age Timeline Description",
            scale_unit=5,
            scale_length=1,
            page_size="4",
            page_orientation="L",
            page_scale_position=0,
        )
        AgeEvent.objects.create(
            age_timeline=age_timeline,
            timeline_id=age_timeline.timeline_ptr.pk,
            title="Title",
            start_year=5,
            start_month=6,
            has_end=False,
        )
        AgeEvent.objects.create(
            age_timeline=age_timeline,
            timeline_id=age_timeline.timeline_ptr.pk,
            title="Title",
            start_year=7,
            start_month=0,
            has_end=True,
            end_year=22,
            end_month=0,
        )
        self.scale_description = AgeTimelineScaleDescription(age_timeline)

        age_timeline_no_events = AgeTimeline.objects.create(
            user=user,
            title="Test Age Timeline Title",
            description="Test Age Timeline Description",
            scale_unit=5,
            scale_length=1,
            page_size="4",
            page_orientation="L",
            page_scale_position=0,
        )
        self.scale_description_no_events = AgeTimelineScaleDescription(age_timeline_no_events)

    def test_start_age(self):
        years = self.scale_description.start_age.years
        self.assertEqual(years, 5)

    def test_end_age(self):
        years = self.scale_description.end_age.years
        self.assertEqual(years, 25)

    def test_get_scale_units(self):
        scale_units = self.scale_description.get_scale_units()
        self.assertEqual(scale_units, 4)

    def test_get_scale_units_no_events(self):
        scale_units = self.scale_description_no_events.get_scale_units()
        self.assertEqual(scale_units, 1)

    def test_get_scale_length(self):
        scale_length = self.scale_description.get_scale_length()
        self.assertEqual(scale_length, 40)

    def test_get_scale_label(self):
        scale_label = self.scale_description.get_scale_label(1)
        self.assertEqual(scale_label, "10")

    def test_plot_age_5_years(self):
        offset = self.scale_description.plot(Age(5, 0))
        self.assertEqual(offset, 0.0)

    def test_plot_age_10_years(self):
        offset = self.scale_description.plot(Age(10, 0))
        self.assertEqual(offset, 10.0)

    def test_plot_age_15_years_6_months(self):
        offset = self.scale_description.plot(Age(15, 6))
        self.assertEqual(offset, 21.0)
