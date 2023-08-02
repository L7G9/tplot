from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from timelines.models import Event, Timeline
from .models import AgeEvent, AgeTimeline


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


AGE_EVENT_FIELD_ORDER = [
    'title',
    'description',
    'start_year',
    'start_month',
    'has_end',
    'end_year',
    'end_month',
    'tags',
    'timeline_area',
]


class AgeEventCreateView(CreateView):
    model = AgeEvent
    fields = AGE_EVENT_FIELD_ORDER

    def form_valid(self, form):
        form.instance.age_timeline = AgeTimeline.objects.get(
            pk=self.kwargs['age_timeline_id']
        )
        form.instance.timeline_id = form.instance.age_timeline.timeline_ptr.pk

        return super().form_valid(form)


class AgeEventUpdateView(UpdateView):
    model = AgeEvent
    fields = AGE_EVENT_FIELD_ORDER


class AgeEventDeleteView(DeleteView):
    model = AgeEvent

    def get_success_url(self):
        return reverse_lazy(
            "age_timelines:age-timeline-detail",
            kwargs={"pk": self.object.age_timeline.id}
        )
