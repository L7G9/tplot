from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from age_timelines.models import AgeTimeline

from .models import Tag, Timeline

@login_required(login_url="/accounts/login/")
def user_timelines(request):
    age_timeline_list = AgeTimeline.objects.all().filter(user=request.user)
    return render(
        request,
        "timelines/user_timelines.html",
        {"age_timeline_list": age_timeline_list}
    )
