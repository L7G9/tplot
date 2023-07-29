from django.shortcuts import render


from age_timelines.models import AgeTimeline


def user_timelines(request):
    age_timeline_list = AgeTimeline.objects.all()
    return render(
        request,
        "timelines/user_timelines.html",
        {"age_timeline_list": age_timeline_list}
    )
