from django.contrib.auth.models import User
from age_timelines.models import AgeEvent, AgeTimeline
from timelines.models import EventArea, Tag


def populate_db(
        user_count,
        age_timelines_per_user,
        events_per_timeline,
        tags_per_timeline,
        areas_per_timeline
):
    users = []
    for user_index in range(user_count):
        user = User.objects.create_user(
            username=f"User{user_index}",
            password=f"Password{user_index}#"
        )
        user_ids = {
            'username': f"User{user_index}",
            'password': f"Password{user_index}#",
            'age_timelines': []
        }
        users.append(user_ids)
        for age_timeline_index in range(age_timelines_per_user):
            age_timeline = AgeTimeline.objects.create(
                user=user,
                title=f"AgeTimeline{age_timeline_index}"
            )
            age_timeline_ids = {
                'id': age_timeline.id,
                'age_event_ids': [],
                'tag_ids': [],
                'event_area_ids': [],
            }
            user_ids['age_timelines'].append(age_timeline_ids)

            for age_event_index in range(events_per_timeline):
                age_event = AgeEvent.objects.create(
                    age_timeline=age_timeline,
                    timeline_id=age_timeline.timeline_ptr.pk,
                    title=f"Event{age_event_index}"
                )
                age_timeline_ids['age_event_ids'].append(age_event.id)

            for tag_index in range(tags_per_timeline):
                tag = Tag.objects.create(
                    timeline=age_timeline.timeline_ptr,
                    name=f"Tag{tag_index}"
                )
                age_timeline_ids['tag_ids'].append(tag.id)

            for area_index in range(areas_per_timeline):
                event_area = EventArea.objects.create(
                    timeline=age_timeline.timeline_ptr,
                    name=f"Area{area_index}", page_position=area_index+1
                )
                age_timeline_ids['event_area_ids'].append(event_area.id)

    return users
