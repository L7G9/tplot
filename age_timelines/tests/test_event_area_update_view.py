from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .populate_db import populate_db
from age_timelines.models import AgeTimeline
from timelines.models import EventArea


class EventAreaUpdateViewTest(TestCase):
    USER_COUNT = 2
    AGE_TIMELINES_PER_USER = 1
    EVENT_AREAS_PER_TIMELINE = 1

    @classmethod
    def setUpTestData(cls):
        users = populate_db(
            cls.USER_COUNT,
            cls.AGE_TIMELINES_PER_USER,
            0,
            0,
            cls.EVENT_AREAS_PER_TIMELINE,
        )
        cls.user0 = User.objects.get(username=users[0]["username"])
        cls.user0_password = users[0]["password"]
        cls.user0_age_timeline_id = users[0]["age_timelines"][0]["id"]
        age_timeline = AgeTimeline.objects.get(id=cls.user0_age_timeline_id)
        cls.user0_timeline_id = age_timeline.timeline_ptr.pk
        cls.user0_event_area_id = users[0]["age_timelines"][0][
            "event_area_ids"
        ][0]
        cls.user1_age_timeline_id = users[1]["age_timelines"][0]["id"]
        cls.user1_event_area_id = users[1]["age_timelines"][0][
            "event_area_ids"
        ][0]
        cls.area_event_update_data = {
            "timeline": cls.user0_timeline_id,
            "name": "Updated Test Event Area",
            "page_position": 1,
            "weight": 1,
        }

    def test_view_url_exists_at_desired_location(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        timeline_id = self.user0_age_timeline_id
        event_id = self.user0_event_area_id
        response = self.client.get(
            f"/timelines/age/{timeline_id}/event_area/{event_id}/update/"
        )
        self.assertEqual(str(response.context["user"]), self.user0.username)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.get(
            reverse(
                "age_timelines:event-area-update",
                kwargs={
                    "age_timeline_id": self.user0_age_timeline_id,
                    "pk": self.user0_event_area_id,
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
                "age_timelines:event-area-update",
                kwargs={
                    "age_timeline_id": self.user0_age_timeline_id,
                    "pk": self.user0_event_area_id,
                },
            )
        )
        self.assertEqual(str(response.context["user"]), self.user0.username)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "age_timelines/event_area_edit_form.html"
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse(
                "age_timelines:event-area-update",
                kwargs={
                    "age_timeline_id": self.user0_age_timeline_id,
                    "pk": self.user0_event_area_id,
                },
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/accounts/login/"))

    def test_forbidden_if_age_timeline_not_owned_by_logged_in_user(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.get(
            reverse(
                "age_timelines:event-area-update",
                kwargs={
                    "age_timeline_id": self.user1_age_timeline_id,
                    "pk": self.user0_event_area_id,
                },
            )
        )
        self.assertEqual(response.status_code, 403)

    def test_forbidden_if_event_area_not_owned_by_logged_in_user(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.get(
            reverse(
                "age_timelines:event-area-update",
                kwargs={
                    "age_timeline_id": self.user0_age_timeline_id,
                    "pk": self.user1_event_area_id,
                },
            )
        )
        self.assertEqual(response.status_code, 403)

    def test_event_area_updated(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.post(
            reverse(
                "age_timelines:event-area-update",
                kwargs={
                    "age_timeline_id": self.user0_age_timeline_id,
                    "pk": self.user0_event_area_id,
                },
            ),
            data=self.area_event_update_data,
            follow=True,
        )
        self.assertEqual(str(response.context["user"]), self.user0.username)
        self.assertEqual(response.status_code, 200)

        event_area = EventArea.objects.get(id=self.user0_event_area_id)
        self.assertEqual(event_area.name, self.area_event_update_data["name"])

    def test_redirect_after_event_area_updated(self):
        self.client.login(
            username=self.user0.username, password=self.user0_password
        )
        response = self.client.post(
            reverse(
                "age_timelines:event-area-update",
                kwargs={
                    "age_timeline_id": self.user0_age_timeline_id,
                    "pk": self.user0_event_area_id,
                },
            ),
            data=self.area_event_update_data,
            follow=True,
        )
        self.assertEqual(str(response.context["user"]), self.user0.username)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            reverse(
                "age_timelines:age-timeline-detail",
                kwargs={"pk": self.user0_age_timeline_id},
            ),
            status_code=302,
        )
