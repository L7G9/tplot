from django.shortcuts import get_object_or_404, render

from .models import AgeTimeline


def age_timeline_edit(request, age_timeline_id):
    age_timeline = get_object_or_404(AgeTimeline, pk=age_timeline_id)
    return render(
        request,
        "age_timelines/age_timeline_edit.html",
        {"timeline": age_timeline, "age_timeline": age_timeline}
    )
