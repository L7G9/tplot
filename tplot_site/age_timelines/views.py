from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import AgeTimeline


def age_timeline_edit(request, age_timeline_id):
    age_timeline = get_object_or_404(AgeTimeline, pk=age_timeline_id)
    return render(
        request,
        "age_timelines/age_timeline_edit.html",
        {"timeline": age_timeline, "age_timeline": age_timeline}
    )


AGE_TIMELINE_FIELD_ORDER = [
        'title',
        'description',
        'scale_unit',
        'scale_length',
        'page_size',
        'page_orientation',
        'page_scale_position',
]


class AgeTimelineDetailView(DetailView):
    model = AgeTimeline

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context


class AgeTimelineCreateView(CreateView):
    model = AgeTimeline
    fields = AGE_TIMELINE_FIELD_ORDER


class AgeTimelineUpdateView(UpdateView):
    model = AgeTimeline
    fields = AGE_TIMELINE_FIELD_ORDER


class AgeTimelineDeleteView(DeleteView):
    model = AgeTimeline
    success_url = reverse_lazy("timelines:user-timelines")
