from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from timelines.mixins import OwnerRequiredMixin

from .models import AgeEvent, AgeTimeline


AGE_TIMELINE_FIELD_ORDER = [
    'title',
    'description',
    'scale_unit',
    'scale_length',
    'page_size',
    'page_orientation',
    'page_scale_position',
]


class AgeTimelineDetailView(OwnerRequiredMixin, DetailView):
    model = AgeTimeline

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context


class AgeTimelineCreateView(LoginRequiredMixin, CreateView):
    model = AgeTimeline
    fields = AGE_TIMELINE_FIELD_ORDER

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AgeTimelineUpdateView(OwnerRequiredMixin, UpdateView):
    model = AgeTimeline
    fields = AGE_TIMELINE_FIELD_ORDER


class AgeTimelineDeleteView(OwnerRequiredMixin, DeleteView):
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


class AgeEventCreateView(LoginRequiredMixin, CreateView):
    model = AgeEvent
    fields = AGE_EVENT_FIELD_ORDER

    def form_valid(self, form):
        form.instance.age_timeline = AgeTimeline.objects.get(
            pk=self.kwargs['age_timeline_id']
        )
        form.instance.timeline_id = form.instance.age_timeline.timeline_ptr.pk

        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        age_timeline = AgeTimeline.objects.get(
            pk=kwargs['age_timeline_id']
        )
        if age_timeline.get_owner() != self.request.user:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "age_timelines:age-timeline-detail",
            kwargs={"pk": self.object.age_timeline.id}
        )


class AgeEventUpdateView(OwnerRequiredMixin, UpdateView):
    model = AgeEvent
    fields = AGE_EVENT_FIELD_ORDER

    def get_success_url(self) -> str:
        return reverse_lazy(
            "age_timelines:age-timeline-detail",
            kwargs={"pk": self.object.age_timeline.id}
        )


class AgeEventDeleteView(OwnerRequiredMixin, DeleteView):
    model = AgeEvent

    def get_success_url(self) -> str:
        return reverse_lazy(
            "age_timelines:age-timeline-detail",
            kwargs={"pk": self.object.age_timeline.id}
        )
