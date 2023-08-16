from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .populate_db import populate_db
from age_timelines.models import AgeTimeline


class AgeTimelineUpdateViewTest(TestCase):
    USER_COUNT = 2
    TIMELINES_PER_USER = 1

    @classmethod
    def setUpTestData(cls):
        users = populate_db(
            cls.USER_COUNT,
            cls.TIMELINES_PER_USER,
            0,
            0,
            0
        )
        cls.user0 = User.objects.get(username=users[0]['username'])
        cls.user0_password = users[0]['password']
        cls.user0_age_timeline_id = users[0]['age_timelines'][0]['id']
        cls.user1_age_timeline_id = users[1]['age_timelines'][0]['id']
        cls.updated_age_timeline_data = {
            'user': cls.user0,
            'title': 'Updated Age Timeline',
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
        response = self.client.get(
            reverse(
                "age_timelines:age-timeline-update",
                kwargs={'pk': self.user0_age_timeline_id}
            )
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
                "age_timelines:age-timeline-update",
                kwargs={'pk': self.user0_age_timeline_id}
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
                "age_timelines:age-timeline-update",
                kwargs={'pk': self.user0_age_timeline_id}
            )
        )
        self.assertEqual(str(response.context['user']), self.user0.username)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "age_timelines/age_timeline_edit_form.html"
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse(
                "age_timelines:age-timeline-update",
                kwargs={'pk': self.user0_age_timeline_id}
            )
        )
        timeline_id = self.user0_age_timeline_id
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/timelines/age/{timeline_id}/update/"
        )

    def test_forbidden_if_age_timeline_not_owned_by_logged_in_user(self):
        self.client.login(
            username=self.user0.username,
            password=self.user0_password
        )
        response = self.client.get(
            reverse(
                "age_timelines:age-timeline-update",
                kwargs={'pk': self.user1_age_timeline_id}
            )
        )
        self.assertEqual(response.status_code, 403)

    def test_age_timeline_updated(self):
        self.client.login(
            username=self.user0.username,
            password=self.user0_password
        )
        response = self.client.post(
            reverse(
                "age_timelines:age-timeline-update",
                kwargs={'pk': self.user0_age_timeline_id}
            ),
            data=self.updated_age_timeline_data,
            follow=True
        )
        self.assertEqual(str(response.context['user']), self.user0.username)
        self.assertEqual(response.status_code, 200)

        age_timeline = AgeTimeline.objects.get(id=self.user0_age_timeline_id)
        self.assertEqual(
            age_timeline.title,
            self.updated_age_timeline_data['title']
        )

    def test_redirect_after_age_timeline_updated(self):
        self.client.login(
            username=self.user0.username,
            password=self.user0_password
        )
        response = self.client.post(
            reverse(
                "age_timelines:age-timeline-update",
                kwargs={'pk': self.user0_age_timeline_id}
            ),
            data=self.updated_age_timeline_data,
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
