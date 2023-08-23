from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from age_timelines.models import AgeTimeline


@login_required(login_url="/accounts/login/")
def user_timelines(request):
    age_timeline_list = AgeTimeline.objects.all().filter(user=request.user)
    return render(
        request,
        "timelines/user_timelines.html",
        {"age_timeline_list": age_timeline_list},
    )
