from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from age_timelines.models import AgeTimeline
from date_time_timelines.models import DateTimeTimeline
from historical_timelines.models import HistoricalTimeline
from scientific_timelines.models import ScientificTimeline


@login_required(login_url="/accounts/login/")
def user_timelines(request):
    age_timeline_list = AgeTimeline.objects.all().filter(user=request.user)
    date_time_timeline_list = DateTimeTimeline.objects.all().filter(
        user=request.user
    )
    historical_timeline_list = HistoricalTimeline.objects.all().filter(
        user=request.user
    )
    scientific_timeline_list = ScientificTimeline.objects.all().filter(
        user=request.user
    )
    return render(
        request,
        "timelines/user_timelines.html",
        {
            "age_timeline_list": age_timeline_list,
            "date_time_timeline_list": date_time_timeline_list,
            "historical_timeline_list": historical_timeline_list,
            "scientific_timeline_list": scientific_timeline_list,
        },
    )
