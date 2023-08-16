from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .populate_db import populate_db
from age_timelines.models import AgeEvent


class AgeEventCreateViewTest(TestCase):
    USER_COUNT = 2
    AGE_TIMELINES_PER_USER = 1
    EVENTS_PER_TIMELINE = 0

    @classmethod
    def setUpTestData(cls):
        users = populate_db(
            cls.USER_COUNT,
            cls.AGE_TIMELINES_PER_USER,
            cls.EVENTS_PER_TIMELINE,
            0,
            0
        )
        cls.user0 = User.objects.get(username=users[0]['username'])
        cls.user0_password = users[0]['password']
        cls.user0_age_timeline_id = users[0]['age_timelines'][0]['id']
        cls.user1_age_timeline_id = users[1]['age_timelines'][0]['id']

        cls.new_age_event_data = {
            'age_timeline': cls.user0_age_timeline_id,
            'title': 'New Test Age Event',
            'description': 'Description',
            'start_year': 1,
            'start_month': 0,
            'has_end': False,
            'end_year': 2,
            'end_month': 0
        }

    def test_view_url_exists_at_desired_location(self):
        self.client.login(
            username=self.user0.username,
            password=self.user0_password
        )
        response = self.client.get(
            f"/timelines/age/{self.user0_age_timeline_id}/event/add/"
        )
        self.assertEqual(str(response.context['user']), self.user0.username)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(
            username=self.user0.username,
            password=self.user0_password
        )
        response = self.client.get(
            reverse(
                "age_timelines:age-event-add",
                kwargs={'age_timeline_id': self.user0_age_timeline_id}
            )
        )
        self.assertEqual(str(response.context['user']), self.user0.username)
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        self.client.login(
            username=self.user0.username,
            password=self.user0_password
        )
        response = self.client.get(
            reverse(
                "age_timelines:age-event-add",
                kwargs={'age_timeline_id': self.user0_age_timeline_id}
            )
        )
        self.assertEqual(str(response.context['user']), self.user0.username)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "age_timelines/age_event_add_form.html"
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse(
                "age_timelines:age-event-add",
                kwargs={'age_timeline_id': self.user0_age_timeline_id}
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_forbidden_if_age_timeline_not_owned_by_logged_in_user(self):
        self.client.login(
            username=self.user0.username,
            password=self.user0_password
        )
        response = self.client.get(
            reverse(
                "age_timelines:age-event-add",
                kwargs={'age_timeline_id': self.user1_age_timeline_id}
            )
        )
        self.assertEqual(response.status_code, 403)

    def test_age_event_added(self):
        self.client.login(
            username=self.user0.username,
            password=self.user0_password
        )
        response = self.client.post(
            reverse(
                "age_timelines:age-event-add",
                kwargs={'age_timeline_id': self.user0_age_timeline_id}
            ),
            data=self.new_age_event_data,
            follow=True
        )
        self.assertEqual(str(response.context['user']), self.user0.username)
        self.assertEqual(response.status_code, 200)

        age_events = AgeEvent.objects.filter(
            age_timeline=self.user0_age_timeline_id
        )
        expected_age_event_count = self.EVENTS_PER_TIMELINE + 1
        self.assertEquals(len(age_events), expected_age_event_count)

    def test_redirect_after_age_event_added(self):
        self.client.login(
            username=self.user0.username,
            password=self.user0_password
        )
        response = self.client.post(
            reverse(
                "age_timelines:age-event-add",
                kwargs={'age_timeline_id': self.user0_age_timeline_id}
            ),
            data=self.new_age_event_data,
            follow=True
        )
        self.assertEqual(str(response.context['user']), self.user0.username)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            reverse(
                "age_timelines:age-timeline-detail",
                kwargs={'pk': self.user0_age_timeline_id}
            ),
            status_code=302
        )
