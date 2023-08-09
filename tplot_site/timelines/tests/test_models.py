from django.contrib.auth.models import User
from django.test import TestCase

from timelines.models import EventArea, Tag, Timeline


class TimelineModel(TestCase):
    @classmethod
    def setUpTestData(self):
        user = User.objects.create_user(
            username="TestUser",
            password="TestUser01#"
        )
        timeline = Timeline.objects.create(
            user=user,
            title="Test Timeline Title",
            description="Test Timeline Description",
            scale_length=1,
            page_size="4",
            page_orientation="L",
            page_scale_position=0,
        )
        self.timeline_id = timeline.id

    def test_title_label(self):
        timeline = Timeline.objects.get(id=self.timeline_id)
        field_label = timeline._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_title_name_max_length(self):
        timeline = Timeline.objects.get(id=self.timeline_id)
        max_length = timeline._meta.get_field('title').max_length
        self.assertEqual(max_length, 100)

    def test_description_label(self):
        timeline = Timeline.objects.get(id=self.timeline_id)
        field_label = timeline._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')

    def test_description_max_length(self):
        timeline = Timeline.objects.get(id=self.timeline_id)
        max_length = timeline._meta.get_field('description').max_length
        self.assertEqual(max_length, 1000)

    def test_description_blank(self):
        timeline = Timeline.objects.get(id=self.timeline_id)
        blank = timeline._meta.get_field('description').blank
        self.assertTrue(blank)

    def test_scale_length_label(self):
        timeline = Timeline.objects.get(id=self.timeline_id)
        field_label = timeline._meta.get_field('scale_length').verbose_name
        self.assertEqual(field_label, 'scale length')

    def test_scale_choices(self):
        timeline = Timeline.objects.get(id=self.timeline_id)
        choices = timeline._meta.get_field('scale_length').choices
        self.assertEqual(choices, Timeline.SCALE_LENGTHS)

    def test_scale_default(self):
        timeline = Timeline.objects.get(id=self.timeline_id)
        default = timeline._meta.get_field('scale_length').default
        self.assertEqual(default, 5)

    def test_page_size_label(self):
        timeline = Timeline.objects.get(id=self.timeline_id)
        field_label = timeline._meta.get_field('page_size').verbose_name
        self.assertEqual(field_label, 'page size')

    def test_page_size_max_length(self):
        timeline = Timeline.objects.get(id=self.timeline_id)
        max_length = timeline._meta.get_field('page_size').max_length
        self.assertEqual(max_length, 1)

    def test_page_size_choices(self):
        timeline = Timeline.objects.get(id=self.timeline_id)
        choices = timeline._meta.get_field('page_size').choices
        self.assertEqual(choices, Timeline.PAGE_SIZES)

    def test_page_size_default(self):
        timeline = Timeline.objects.get(id=self.timeline_id)
        default = timeline._meta.get_field('page_size').default
        self.assertEqual(default, "4")

    def test_page_orientation_label(self):
        timeline = Timeline.objects.get(id=self.timeline_id)
        field_label = timeline._meta.get_field('page_orientation').verbose_name
        self.assertEqual(field_label, 'page orientation')

    def test_page_orientation_max_length(self):
        timeline = Timeline.objects.get(id=self.timeline_id)
        max_length = timeline._meta.get_field('page_orientation').max_length
        self.assertEqual(max_length, 1)

    def test_page_orientation_choices(self):
        timeline = Timeline.objects.get(id=self.timeline_id)
        choices = timeline._meta.get_field('page_orientation').choices
        self.assertEqual(choices, Timeline.PAGE_ORIENTATIONS)

    def test_page_orientation_default(self):
        timeline = Timeline.objects.get(id=self.timeline_id)
        default = timeline._meta.get_field('page_orientation').default
        self.assertEqual(default, "L")

    def test_page_scale_position_label(self):
        timeline = Timeline.objects.get(id=self.timeline_id)
        field_label = timeline._meta.get_field('page_scale_position').verbose_name
        self.assertEqual(field_label, 'page scale position')

    def test_page_scale_position_default(self):
        timeline = Timeline.objects.get(id=self.timeline_id)
        default = timeline._meta.get_field('page_scale_position').default
        self.assertEqual(default, 0)

    def test_object_name_is_title(self):
        timeline = Timeline.objects.get(id=self.timeline_id)
        expected_object_name = timeline.title
        self.assertEqual(str(timeline), expected_object_name)

    def test_get_owner_is_user(self):
        timeline = Timeline.objects.get(id=self.timeline_id)
        expected_owner = timeline.user
        self.assertEqual(timeline.get_owner(), expected_owner)


class EventAreaModel(TestCase):
    @classmethod
    def setUpTestData(self):
        user = User.objects.create_user(
            username="TestUser",
            password="TestUser01#"
        )
        timeline = Timeline.objects.create(
            user=user,
            title="Test Timeline Title",
            description="Test Timeline Description",
            scale_length=1,
            page_size="4",
            page_orientation="L",
            page_scale_position=0,
        )
        area = EventArea.objects.create(
            timeline=timeline,
            name="Test Event Area",
            page_position=1,
            weight=1,
        )
        self.area_id = area.id

    def test_name_max_length(self):
        area = EventArea.objects.get(id=self.area_id)
        max_length = area._meta.get_field('name').max_length
        self.assertEqual(max_length, 25)

    def test_page_position_default(self):
        area = EventArea.objects.get(id=self.area_id)
        default = area._meta.get_field('page_position').default
        self.assertEqual(default, 0)

    def test_weight_default(self):
        area = EventArea.objects.get(id=self.area_id)
        default = area._meta.get_field('weight').default
        self.assertEqual(default, 1)

    def test_meta_ordering_by_name(self):
        area = EventArea.objects.get(id=self.area_id)
        ordering = area._meta.ordering
        self.assertEqual(len(ordering), 1)
        self.assertEqual(ordering[0], "name")

    def test_meta_unique_together_timeline_page_position(self):
        area = EventArea.objects.get(id=self.area_id)
        unique_together = area._meta.unique_together
        self.assertEqual(len(unique_together), 1)
        self.assertEqual(unique_together[0], ("timeline", "page_position"))

    def test_object_name_is_name(self):
        area = EventArea.objects.get(id=self.area_id)
        name = area.name
        self.assertEqual(str(area), name)

    def test_get_owner_is_timeline_user(self):
        area = EventArea.objects.get(id=self.area_id)
        owner = area.timeline.user
        self.assertEqual(area.get_owner(), owner)


class TagModel(TestCase):
    @classmethod
    def setUpTestData(self):
        user = User.objects.create_user(
            username="TestUser",
            password="TestUser01#"
        )
        timeline = Timeline.objects.create(
            user=user,
            title="Test Timeline Title",
            description="Test Timeline Description",
            scale_length=1,
            page_size="4",
            page_orientation="L",
            page_scale_position=0,
        )
        tag = Tag.objects.create(timeline=timeline, name="Test Tag")
        self.tag_id = tag.id

    def test_name_max_length(self):
        tag = Tag.objects.get(id=self.tag_id)
        max_length = tag._meta.get_field("name").max_length
        self.assertEqual(max_length, 25)

    def test_meta_ordering_by_name(self):
        tag = Tag.objects.get(id=self.tag_id)
        ordering = tag._meta.ordering
        self.assertEqual(len(ordering), 1)
        self.assertEqual(ordering[0], "name")

    def test_object_name_is_title(self):
        tag = Tag.objects.get(id=self.tag_id)
        expected_object_name = tag.name
        self.assertEqual(str(tag), expected_object_name)

    def test_get_owner_is_timeline_user(self):
        tag = Tag.objects.get(id=self.tag_id)
        expected_owner = tag.timeline.user
        self.assertEqual(tag.get_owner(), expected_owner)

