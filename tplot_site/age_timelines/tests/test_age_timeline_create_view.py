from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .populate_db import populate_db
from age_timelines.models import AgeTimeline


class AgeTimelineDetailViewTest(TestCase):
    USER_COUNT = 1

    @classmethod
    def setUpTestData(cls):
        populate_db(cls.USER_COUNT, 0, 0, 0, 0)
        cls.test_user_0 = User.objects.get(username="test_user_0")

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("age_timelines:age-timeline-add"))
        self.assertRedirects(response, "/accounts/login/?next=/timelines/age/add/")

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="test_user_0", password="TestUser0#")
        response = self.client.get("/timelines/age/add/")
        self.assertEqual(str(response.context['user']), "test_user_0")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username="test_user_0", password="TestUser0#")
        response = self.client.get(reverse("age_timelines:age-timeline-add"))
        self.assertEqual(str(response.context['user']), "test_user_0")
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        self.client.login(username="test_user_0", password="TestUser0#")
        response = self.client.get(reverse("age_timelines:age-timeline-add"))
        self.assertTemplateUsed(response, "age_timelines/age_timeline_add_form.html")

    def test_age_timeline_added(self):
        self.client.login(username="test_user_0", password="TestUser0#")
        data = {
            'user': self.test_user_0,
            'title': 'New Age Timeline',
            'description': 'Description',
            'scale_unit': 5,
            'scale_length': 5,
            'page_size': '4',
            'page_orientation': 'L',
            'page_scale_position': 0,
        }
        response = self.client.post(reverse("age_timelines:age-timeline-add"), data=data, follow=True)
        self.assertEquals(response.status_code, 200)
        age_timelines = AgeTimeline.objects.filter(user=self.test_user_0)
        self.assertEquals(len(age_timelines), 1)

    def test_age_redirect_to_age_timeline_detail_on_add(self):
        self.client.login(username="test_user_0", password="TestUser0#")
        data = {
            'user': self.test_user_0,
            'title': 'New Age Timeline',
            'description': 'Description',
            'scale_unit': 5,
            'scale_length': 5,
            'page_size': '4',
            'page_orientation': 'L',
            'page_scale_position': 0,
        }
        response = self.client.post(reverse("age_timelines:age-timeline-add"), data=data, follow=True)
        age_timeline = AgeTimeline.objects.get(user=self.test_user_0)
        self.assertRedirects(response, reverse("age_timelines:age-timeline-detail", kwargs={'pk': age_timeline.id}), status_code=302)
