from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .populate_db import populate_db
from age_timelines.models import AgeTimeline


class AgeTimelineCreateViewTest(TestCase):
    USER_COUNT = 1
    AGE_TIMELINES_PER_USER = 0

    @classmethod
    def setUpTestData(cls):
        users = populate_db(
            cls.USER_COUNT,
            cls.AGE_TIMELINES_PER_USER,
            0,
            0,
            0
        )
        cls.user0 = User.objects.get(username=users[0]['username'])
        cls.user0_password = users[0]['password']
        cls.new_age_timeline_data = {
            'user': cls.user0,
            'title': 'New Test Age Timeline',
            'description': 'Description',
            'scale_unit': 5,
            'scale_length': 5,
            'page_size': '4',
            'page_orientation': 'L',
            'page_scale_position': 0,
        }

    def test_view_url_exists_at_desired_location(self):
        self.client.login(
            username=self.user0.username,
            password=self.user0_password
        )
        response = self.client.get("/timelines/age/add/")
        self.assertEqual(str(response.context['user']), self.user0.username)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(
            username=self.user0.username,
            password=self.user0_password
        )
        response = self.client.get(reverse("age_timelines:age-timeline-add"))
        self.assertEqual(str(response.context['user']), self.user0.username)
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        self.client.login(
            username=self.user0.username,
            password=self.user0_password
        )
        response = self.client.get(reverse("age_timelines:age-timeline-add"))
        self.assertEqual(str(response.context['user']), self.user0.username)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "age_timelines/age_timeline_add_form.html")

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("age_timelines:age-timeline-add"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_age_timeline_added(self):
        self.client.login(
            username=self.user0.username,
            password=self.user0_password
        )
        response = self.client.post(
            reverse("age_timelines:age-timeline-add"),
            data=self.new_age_timeline_data,
            follow=True
        )
        self.assertEqual(str(response.context['user']), self.user0.username)
        self.assertEquals(response.status_code, 200)

        age_timelines = AgeTimeline.objects.filter(user=self.user0)
        expected_age_timeline_count = self.AGE_TIMELINES_PER_USER + 1
        self.assertEquals(len(age_timelines), expected_age_timeline_count)

    def test_redirect_after_age_timeline_added(self):
        self.client.login(
            username=self.user0.username,
            password=self.user0_password
        )
        response = self.client.post(
            reverse("age_timelines:age-timeline-add"),
            data=self.new_age_timeline_data,
            follow=True
        )
        self.assertEqual(str(response.context['user']), self.user0.username)
        self.assertEquals(response.status_code, 200)

        age_timeline = AgeTimeline.objects.get(title=self.new_age_timeline_data['title'])
        self.assertRedirects(
            response,
            reverse(
                "age_timelines:age-timeline-detail",
                kwargs={'pk': age_timeline.id}
            ),
            status_code=302
        )
