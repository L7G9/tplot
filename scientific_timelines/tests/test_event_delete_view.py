from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .populate_db import populate_db
from scientific_timelines.models import ScientificEvent


class ScientificEventDeleteViewTest(TestCase):
    USER_COUNT = 2
    AGE_TIMELINES_PER_USER = 1
    EVENTS_PER_TIMELINE = 1

    @classmethod
    def setUpTestData(cls):
        users = populate_db(
            cls.USER_COUNT,
            cls.AGE_TIMELINES_PER_USER,
            cls.EVENTS_PER_TIMELINE,
            0,
            0,
        )
        cls.user0 = User.objects.get(username=users[0]["username"])
        cls.user0_password = users[0]["password"]
        cls.user0_scientific_timeline_id = users[0]["scientific_timelines"][0][
            "id"
        ]
        cls.user0_scientific_event_id = users[0]["scientific_timelines"][0][
            "scientific_event_ids"
        ][0]
        cls.user1_scientific_timeline_id = users[1]["scientific_timelines"][0][
            "id"
        ]
        cls.user1_scientific_event_id = users[1]["scientific_timelines"][0][
            "scientific_event_ids"
        ][0]

    def test_view_url_exists_at_desired_location(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        timeline_id = self.user0_scientific_timeline_id
        event_id = self.user0_scientific_event_id
        response = self.client.get(
            f"/timelines/scientific/{timeline_id}/event/{event_id}/delete/"
        )
        self.assertEqual(str(response.context["user"]), self.user0.username)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.get(
            reverse(
                "scientific_timelines:event-delete",
                kwargs={
                    "scientific_timeline_id":
                    self.user0_scientific_timeline_id,
                    "pk": self.user0_scientific_event_id,
                },
            )
        )
        self.assertEqual(str(response.context["user"]), self.user0.username)
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.get(
            reverse(
                "scientific_timelines:event-delete",
                kwargs={
                    "scientific_timeline_id":
                    self.user0_scientific_timeline_id,
                    "pk": self.user0_scientific_event_id,
                },
            )
        )
        self.assertEqual(str(response.context["user"]), self.user0.username)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "scientific_timelines/event_delete.html"
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse(
                "scientific_timelines:event-delete",
                kwargs={
                    "scientific_timeline_id":
                    self.user0_scientific_timeline_id,
                    "pk": self.user0_scientific_event_id,
                },
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/accounts/login/"))

    def test_forbidden_if_scientific_timeline_not_owned_by_logged_in_user(
        self,
    ):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.get(
            reverse(
                "scientific_timelines:event-delete",
                kwargs={
                    "scientific_timeline_id":
                    self.user1_scientific_timeline_id,
                    "pk": self.user0_scientific_event_id,
                },
            )
        )
        self.assertEqual(response.status_code, 403)

    def test_forbidden_if_scientific_event_not_owned_by_logged_in_user(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.get(
            reverse(
                "scientific_timelines:event-delete",
                kwargs={
                    "scientific_timeline_id":
                    self.user0_scientific_timeline_id,
                    "pk": self.user1_scientific_event_id,
                },
            )
        )
        self.assertEqual(response.status_code, 403)

    def test_scientific_event_deleted(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.post(
            reverse(
                "scientific_timelines:event-delete",
                kwargs={
                    "scientific_timeline_id":
                    self.user0_scientific_timeline_id,
                    "pk": self.user0_scientific_event_id,
                },
            ),
            follow=True,
        )
        self.assertEqual(str(response.context["user"]), self.user0.username)
        self.assertEqual(response.status_code, 200)

        scientific_events = ScientificEvent.objects.filter(
            scientific_timeline=self.user0_scientific_timeline_id
        )
        expected_scientific_event_count = self.EVENTS_PER_TIMELINE - 1
        self.assertEqual(
            len(scientific_events), expected_scientific_event_count
        )

    def test_redirect_after_scientific_event_deleted(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.post(
            reverse(
                "scientific_timelines:event-delete",
                kwargs={
                    "scientific_timeline_id":
                    self.user0_scientific_timeline_id,
                    "pk": self.user0_scientific_event_id,
                },
            ),
            follow=True,
        )

        self.assertEqual(str(response.context["user"]), self.user0.username)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            reverse(
                "scientific_timelines:timeline-detail",
                kwargs={"pk": self.user0_scientific_timeline_id},
            ),
            status_code=302,
        )
