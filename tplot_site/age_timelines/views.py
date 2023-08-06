from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from timelines.mixins import OwnerRequiredMixin

from timelines.models import Tag, TimelineArea
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
    template_name = "age_timelines/age_timeline_detail.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()

        return context


class AgeTimelineCreateView(LoginRequiredMixin, CreateView):
    model = AgeTimeline
    fields = AGE_TIMELINE_FIELD_ORDER
    template_name = "age_timelines/age_timeline_add_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AgeTimelineUpdateView(OwnerRequiredMixin, UpdateView):
    model = AgeTimeline
    fields = AGE_TIMELINE_FIELD_ORDER
    template_name = "age_timelines/age_timeline_edit_form.html"


class AgeTimelineDeleteView(OwnerRequiredMixin, DeleteView):
    model = AgeTimeline
    template_name = "age_timelines/age_timeline_confirm_delete.html"
    success_url = reverse_lazy("timelines:user-timelines")


# check age timeline found with age_timeline_id is owned by logged in user
class AgeTimelineOwnerMixim(object):
    def dispatch(self, request, *args, **kwargs):
        age_timline = AgeTimeline.objects.get(
            pk=self.kwargs['age_timeline_id']
        )
        if age_timline.get_owner() != request.user:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)


# get age timeline object and id of timeline object
class AgeTimelineMixim(object):
    def form_valid(self, form):
        form.instance.age_timeline = AgeTimeline.objects.get(
            pk=self.kwargs['age_timeline_id']
        )
        form.instance.timeline_id = form.instance.age_timeline.timeline_ptr.pk

        return super().form_valid(form)


# return age timeline detail
class SuccessMixim(object):
    def get_success_url(self) -> str:
        return reverse_lazy(
            "age_timelines:age-timeline-detail",
            kwargs={"pk": self.kwargs['age_timeline_id']},
            # kwargs={"pk": self.object.age_timeline.id},
        )


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


class AgeEventCreateView(LoginRequiredMixin, AgeTimelineOwnerMixim, AgeTimelineMixim, SuccessMixim, CreateView):
    model = AgeEvent
    fields = AGE_EVENT_FIELD_ORDER
    template_name = "age_timelines/age_event_add_form.html"


class AgeEventUpdateView(OwnerRequiredMixin, SuccessMixim, UpdateView):
    model = AgeEvent
    fields = AGE_EVENT_FIELD_ORDER
    template_name = "age_timelines/age_event_edit_form.html"


class AgeEventDeleteView(OwnerRequiredMixin, SuccessMixim, DeleteView):
    model = AgeEvent
    template_name = "age_timelines/age_event_confirm_delete.html"


class TagCreateView(LoginRequiredMixin, AgeTimelineOwnerMixim, AgeTimelineMixim, SuccessMixim, CreateView):
    model = Tag
    fields = ['name']
    template_name = "age_timelines/tag_add_form.html"


class TagUpdateView(OwnerRequiredMixin, AgeTimelineMixim, SuccessMixim, UpdateView):
    model = Tag
    fields = ["name"]
    template_name = "age_timelines/tag_edit_form.html"


class TagDeleteView(OwnerRequiredMixin, SuccessMixim, DeleteView):
    model = Tag
    template_name = "timelines/tag_confirm_delete.html"


def area_form_duplicates(form, area_id=None):
    timeline = form.instance.age_timeline.timeline_ptr
    position = form.cleaned_data['page_position']

    duplicate_areas = TimelineArea.objects.filter(timeline=timeline, page_position=position)
    if area_id is not None:
        duplicate_areas.exclude(id=area_id)

    return duplicate_areas, position


class AreaCreateView(LoginRequiredMixin, AgeTimelineOwnerMixim, SuccessMixim, CreateView):
    model = TimelineArea
    fields = ["name", "page_position", "weight"]
    template_name = "age_timelines/area_add_form.html"

    def form_valid(self, form):
        form.instance.age_timeline = AgeTimeline.objects.get(
            pk=self.kwargs['age_timeline_id']
        )
        form.instance.timeline_id = form.instance.age_timeline.timeline_ptr.pk

        duplicate_areas, position = area_form_duplicates(form)

        if not duplicate_areas:
            return super().form_valid(form)
        else:
            form.add_error("page_position", f"Area with position { position } already exists")
            return self.form_invalid(form)


class AreaUpdateView(OwnerRequiredMixin, SuccessMixim, UpdateView):
    model = TimelineArea
    fields = ["name", "page_position", "weight"]
    template_name = "age_timelines/area_edit_form.html"

    def form_valid(self, form):
        form.instance.age_timeline = AgeTimeline.objects.get(
            pk=self.kwargs['age_timeline_id']
        )
        form.instance.timeline_id = form.instance.age_timeline.timeline_ptr.pk

        duplicate_areas, position = area_form_duplicates(form, self.get_object().id)

        if not duplicate_areas:
            return super().form_valid(form)
        else:
            form.add_error("page_position", f"Area with position { position } already exists")
            return self.form_invalid(form)


class AreaDeleteView(OwnerRequiredMixin, SuccessMixim, DeleteView):
    model = TimelineArea
    template_name = "timelines/area_confirm_delete.html"
