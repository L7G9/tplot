from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .populate_db import populate_db
from scientific_timelines.models import ScientificEvent


class ScientificEventUpdateViewTest(TestCase):
    USER_COUNT = 2
    TIMELINES_PER_USER = 1
    EVENTS_PER_TIMELINE = 1

    @classmethod
    def setUpTestData(cls):
        users = populate_db(
            cls.USER_COUNT,
            cls.TIMELINES_PER_USER,
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
        cls.updated_scientific_event_data = {
            "scientific_timeline": cls.user0_scientific_timeline_id,
            "title": "Updated Test Scientific Event",
            "description": "Description",
            "start_year_fraction": 1,
            "start_multiplier": 1000,
            "has_end": False,
            "end_year_fraction": 1,
            "end_multiplier": 1000,
        }

    def test_view_url_exists_at_desired_location(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        timeline_id = self.user0_scientific_timeline_id
        event_id = self.user0_scientific_event_id
        response = self.client.get(
            f"/timelines/scientific/{timeline_id}/event/{event_id}/update/"
        )
        self.assertEqual(str(response.context["user"]), self.user0.username)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.get(
            reverse(
                "scientific_timelines:event-update",
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
                "scientific_timelines:event-update",
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
            response, "scientific_timelines/event_edit.html"
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse(
                "scientific_timelines:event-update",
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
                "scientific_timelines:event-update",
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
                "scientific_timelines:event-update",
                kwargs={
                    "scientific_timeline_id":
                    self.user0_scientific_timeline_id,
                    "pk": self.user1_scientific_event_id,
                },
            )
        )
        self.assertEqual(response.status_code, 403)

    def test_scientific_event_updated(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.post(
            reverse(
                "scientific_timelines:event-update",
                kwargs={
                    "scientific_timeline_id":
                    self.user0_scientific_timeline_id,
                    "pk": self.user0_scientific_event_id,
                },
            ),
            data=self.updated_scientific_event_data,
            follow=True,
        )
        self.assertEqual(str(response.context["user"]), self.user0.username)
        self.assertEqual(response.status_code, 200)

        scientific_event = ScientificEvent.objects.get(
            id=self.user0_scientific_event_id
        )
        expected_title = self.updated_scientific_event_data["title"]
        self.assertEqual(scientific_event.title, expected_title)

    def test_redirect_after_scientific_event_updated(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.post(
            reverse(
                "scientific_timelines:event-update",
                kwargs={
                    "scientific_timeline_id":
                    self.user0_scientific_timeline_id,
                    "pk": self.user0_scientific_event_id,
                },
            ),
            data=self.updated_scientific_event_data,
            follow=True,
        )
        self.assertEqual(str(response.context["user"]), self.user0.username)
        self.assertEquals(response.status_code, 200)
        self.assertRedirects(
            response,
            reverse(
                "scientific_timelines:timeline-detail",
                kwargs={"pk": self.user0_scientific_timeline_id},
            ),
            status_code=302,
        )
