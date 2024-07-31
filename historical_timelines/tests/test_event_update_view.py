from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .populate_db import populate_db
from historical_timelines.models import HistoricalEvent


class HistoricalEventUpdateViewTest(TestCase):
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
        cls.user0_hist_timeline_id = users[0]["historical_timelines"][0][
            "id"
        ]
        cls.user0_historical_event_id = users[0]["historical_timelines"][0][
            "historical_event_ids"
        ][0]
        cls.user1_hist_timeline_id = users[1]["historical_timelines"][0][
            "id"
        ]
        cls.user1_historical_event_id = users[1]["historical_timelines"][0][
            "historical_event_ids"
        ][0]
        cls.updated_historical_event_data = {
            "historical_timeline": cls.user0_hist_timeline_id,
            "title": "Updated Test Historical Event",
            "description": "Description",
            "start_bc_ad": 1,
            "start_year": 1,
            "has_end": False,
            "end_bc_ad": 1,
            "end_year": 1,
        }

    def test_view_url_exists_at_desired_location(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        timeline_id = self.user0_hist_timeline_id
        event_id = self.user0_historical_event_id
        response = self.client.get(
            f"/timelines/historical/{timeline_id}/event/{event_id}/update/"
        )
        self.assertEqual(str(response.context["user"]), self.user0.username)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.get(
            reverse(
                "historical_timelines:event-update",
                kwargs={
                    "historical_timeline_id": self.user0_hist_timeline_id,
                    "pk": self.user0_historical_event_id,
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
                "historical_timelines:event-update",
                kwargs={
                    "historical_timeline_id": self.user0_hist_timeline_id,
                    "pk": self.user0_historical_event_id,
                },
            )
        )
        self.assertEqual(str(response.context["user"]), self.user0.username)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "historical_timelines/event_edit.html"
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse(
                "historical_timelines:event-update",
                kwargs={
                    "historical_timeline_id": self.user0_hist_timeline_id,
                    "pk": self.user0_historical_event_id,
                },
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/accounts/login/"))

    def test_forbidden_if_historical_timeline_not_owned_by_logged_in_user(
        self,
    ):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.get(
            reverse(
                "historical_timelines:event-update",
                kwargs={
                    "historical_timeline_id": self.user1_hist_timeline_id,
                    "pk": self.user0_historical_event_id,
                },
            )
        )
        self.assertEqual(response.status_code, 403)

    def test_forbidden_if_historical_event_not_owned_by_logged_in_user(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.get(
            reverse(
                "historical_timelines:event-update",
                kwargs={
                    "historical_timeline_id": self.user0_hist_timeline_id,
                    "pk": self.user1_historical_event_id,
                },
            )
        )
        self.assertEqual(response.status_code, 403)

    def test_historical_event_updated(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.post(
            reverse(
                "historical_timelines:event-update",
                kwargs={
                    "historical_timeline_id": self.user0_hist_timeline_id,
                    "pk": self.user0_historical_event_id,
                },
            ),
            data=self.updated_historical_event_data,
            follow=True,
        )
        self.assertEqual(str(response.context["user"]), self.user0.username)
        self.assertEqual(response.status_code, 200)

        historical_event = HistoricalEvent.objects.get(
            id=self.user0_historical_event_id
        )
        expected_title = self.updated_historical_event_data["title"]
        self.assertEqual(historical_event.title, expected_title)

    def test_redirect_after_historical_event_updated(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.post(
            reverse(
                "historical_timelines:event-update",
                kwargs={
                    "historical_timeline_id": self.user0_hist_timeline_id,
                    "pk": self.user0_historical_event_id,
                },
            ),
            data=self.updated_historical_event_data,
            follow=True,
        )
        self.assertEqual(str(response.context["user"]), self.user0.username)
        self.assertEquals(response.status_code, 200)
        self.assertRedirects(
            response,
            reverse(
                "historical_timelines:timeline-detail",
                kwargs={"pk": self.user0_hist_timeline_id},
            ),
            status_code=302,
        )
