from .models import EventArea


def event_area_position_error(form, timeline, area_id=None):
    position = form.cleaned_data["page_position"]

    if area_id:
        duplicate_areas = EventArea.objects.exclude(id=area_id).filter(
            timeline=timeline, page_position=position
        )
    else:
        duplicate_areas = EventArea.objects.filter(
            timeline=timeline, page_position=position
        )

    if duplicate_areas:
        return f"Area with position { position } already exists"

    return None
