from .models import TimelineArea

def area_position_error(form, timeline, area_id=None):
    position = form.cleaned_data['page_position']

    if area_id:
        duplicate_areas = TimelineArea.objects.exclude(id=area_id).filter(
            timeline=timeline,
            page_position=position
        )
    else:
        duplicate_areas = TimelineArea.objects.filter(
            timeline=timeline,
            page_position=position
        )

    if duplicate_areas:
        return f"Area with position { position } already exists"

    return None


def field_empty_error(form, field_name):
    entered_text = form.cleaned_data[field_name]

    if entered_text is None:
        return f"Field { field_name } cannot be empty"

    return None
