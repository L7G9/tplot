from django.contrib.auth.models import User
from scientific_timelines.models import ScientificEvent, ScientificTimeline
from timelines.models import EventArea, Tag


def populate_db(
    user_count,
    timelines_per_user,
    events_per_timeline,
    tags_per_timeline,
    areas_per_timeline,
):
    users = []
    for user_index in range(user_count):
        user = User.objects.create_user(
            username=f"User{user_index}", password=f"Password{user_index}#"
        )
        user_ids = {
            "username": f"User{user_index}",
            "password": f"Password{user_index}#",
            "scientific_timelines": [],
        }
        users.append(user_ids)
        for timeline_index in range(timelines_per_user):
            timeline = ScientificTimeline.objects.create(
                user=user, title=f"ScientificTimeline{timeline_index}"
            )
            scientific_timeline_ids = {
                "id": timeline.id,
                "scientific_event_ids": [],
                "tag_ids": [],
                "event_area_ids": [],
            }
            user_ids["scientific_timelines"].append(scientific_timeline_ids)

            for event_index in range(events_per_timeline):
                event = ScientificEvent.objects.create(
                    scientific_timeline=timeline,
                    timeline_id=timeline.timeline_ptr.pk,
                    title=f"Event{event_index}",
                )
                scientific_timeline_ids["scientific_event_ids"].append(
                    event.id
                )

            for tag_index in range(tags_per_timeline):
                tag = Tag.objects.create(
                    timeline=timeline.timeline_ptr, name=f"Tag{tag_index}"
                )
                scientific_timeline_ids["tag_ids"].append(tag.id)

            for area_index in range(areas_per_timeline):
                event_area = EventArea.objects.create(
                    timeline=timeline.timeline_ptr,
                    name=f"Area{area_index}",
                    page_position=area_index + 1,
                )
                scientific_timeline_ids["event_area_ids"].append(event_area.id)

    return users
