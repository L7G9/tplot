from django.contrib.auth.models import User
from django.test import TestCase

from scientific_timelines.models import ScientificEvent, ScientificTimeline


class ScientificTimelineModel(TestCase):
    @classmethod
    def setUpTestData(self):
        user = User.objects.create_user(
            username="TestUser", password="TestUser01#"
        )
        scientific_timeline = ScientificTimeline.objects.create(
            user=user,
            title="Test Scientific Timeline Title",
            description="Test Scientific Timeline Description",
            scale_unit=10,
            scale_unit_length=1,
            page_size="4",
            page_orientation="L",
            page_scale_position=0,
        )
        self.scientific_timeline_id = scientific_timeline.id

    def test_scale_unit_choices(self):
        scientific_timeline = ScientificTimeline.objects.get(
            id=self.scientific_timeline_id
        )
        choices = scientific_timeline._meta.get_field("scale_unit").choices
        self.assertEqual(choices, ScientificTimeline.SCALE_UNITS)

    def test_scale_unit_default(self):
        scientific_timeline = ScientificTimeline.objects.get(
            id=self.scientific_timeline_id
        )
        default = scientific_timeline._meta.get_field("scale_unit").default
        self.assertEqual(default, 1000)

    def test_ordering_by_title(self):
        scientific_timeline = ScientificTimeline.objects.get(
            id=self.scientific_timeline_id
        )
        ordering = scientific_timeline._meta.ordering
        self.assertEqual(len(ordering), 1)
        self.assertEqual(ordering[0], "title")

    def test_object_name_is_title(self):
        scientific_timeline = ScientificTimeline.objects.get(
            id=self.scientific_timeline_id
        )
        title = scientific_timeline.title
        self.assertEqual(str(scientific_timeline), title)

    def test_get_owner_is_user(self):
        scientific_timeline = ScientificTimeline.objects.get(
            id=self.scientific_timeline_id
        )
        owner = scientific_timeline.user
        self.assertEqual(scientific_timeline.get_owner(), owner)

    def test_get_absolute_url(self):
        scientific_timeline = ScientificTimeline.objects.get(
            id=self.scientific_timeline_id
        )
        url = f"/timelines/scientific/{scientific_timeline.id}/detail/"
        self.assertEqual(scientific_timeline.get_absolute_url(), url)


class ScientificEventModel(TestCase):
    @classmethod
    def setUpTestData(self):
        user = User.objects.create_user(
            username="TestUser", password="TestUser01#"
        )
        scientific_timeline = ScientificTimeline.objects.create(
            user=user,
            title="Test Scientific Timeline Title",
            description="Test Scientific Timeline Description",
            scale_unit=1000,
            scale_unit_length=10,
            page_size="4",
            page_orientation="L",
            page_scale_position=0,
        )
        self.scientific_timeline_id = scientific_timeline.id

        end_scientific_event = ScientificEvent.objects.create(
            scientific_timeline=scientific_timeline,
            timeline_id=scientific_timeline.timeline_ptr.pk,
            title="Title",
            start_year_fraction=1,
            start_multiplier=1000,
            has_end=True,
            end_year_fraction=11,
            end_multiplier=1000,
        )
        self.end_scientific_event_id = end_scientific_event.id

        start_scientific_event = ScientificEvent.objects.create(
            scientific_timeline=scientific_timeline,
            timeline_id=scientific_timeline.timeline_ptr.pk,
            title="Title",
            start_year_fraction=1,
            start_multiplier=1000,
            has_end=False,
        )
        self.start_scientific_event_id = start_scientific_event.id

    def test_start_multiplier_choices(self):
        scientific_timeline = ScientificEvent.objects.get(
            id=self.start_scientific_event_id
        )
        choices = scientific_timeline._meta.get_field(
            "start_multiplier"
        ).choices
        self.assertEqual(choices, ScientificEvent.MULTIPLIERS)

    def test_start_multiplier_default(self):
        scientific_timeline = ScientificEvent.objects.get(
            id=self.start_scientific_event_id
        )
        default = scientific_timeline._meta.get_field(
            "start_multiplier"
        ).default
        self.assertEqual(default, 1000)

    def test_end_multiplier_choices(self):
        scientific_timeline = ScientificEvent.objects.get(
            id=self.start_scientific_event_id
        )
        choices = scientific_timeline._meta.get_field("end_multiplier").choices
        self.assertEqual(choices, ScientificEvent.MULTIPLIERS)

    def test_end_multiplier_default(self):
        scientific_timeline = ScientificEvent.objects.get(
            id=self.start_scientific_event_id
        )
        default = scientific_timeline._meta.get_field("end_multiplier").default
        self.assertEqual(default, 1000)

    def test_ordering_by_start_year_and_start_month(self):
        event = ScientificEvent.objects.get(id=self.start_scientific_event_id)
        ordering = event._meta.ordering
        self.assertEqual(len(ordering), 2)
        self.assertEqual(ordering[0], "start_multiplier")
        self.assertEqual(ordering[1], "start_year_fraction")

    def test_get_owner_is_timeline_user(self):
        event = ScientificEvent.objects.get(id=self.start_scientific_event_id)
        expected_owner = event.scientific_timeline.user
        self.assertEqual(event.get_owner(), expected_owner)
