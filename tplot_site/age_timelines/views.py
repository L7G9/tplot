from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from timelines.mixins import OwnerRequiredMixin
from timelines.view_errors import area_position_error, field_empty_error
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

class AgeEventValidateMixim(object):
    def form_valid(self, form):
        form.instance.age_timeline = AgeTimeline.objects.get(
            pk=self.kwargs['age_timeline_id']
        )
        form.instance.timeline_id = form.instance.age_timeline.timeline_ptr.pk

        name_error = field_empty_error(form, "title")
        if name_error is not None:
            form.add_error("title", name_error)

        if form.cleaned_data['has_end']:
            # TODO: move this logic somewhere useful
            start_year = form.cleaned_data['start_year']
            start_month = form.cleaned_data['start_month']
            start_total = (start_year * 12) + start_month

            end_year = form.cleaned_data['end_year']
            end_month = form.cleaned_data['end_month']
            end_total = (end_year * 12) + end_month

            if end_total <= start_total:
                form.add_error(
                    "end_year",
                    "End age must be greater than start age"
                )
                form.add_error(
                    "end_month",
                    "End age must be greater than start age"
                )

        if form.errors:
            return self.form_invalid(form)
        else:
            return super().form_valid(form)


class AgeEventCreateView(LoginRequiredMixin, AgeTimelineOwnerMixim, AgeEventValidateMixim, SuccessMixim, CreateView):
    model = AgeEvent
    fields = AGE_EVENT_FIELD_ORDER
    template_name = "age_timelines/age_event_add_form.html"


class AgeEventUpdateView(OwnerRequiredMixin, AgeEventValidateMixim, SuccessMixim, UpdateView):
    model = AgeEvent
    fields = AGE_EVENT_FIELD_ORDER
    template_name = "age_timelines/age_event_edit_form.html"


class AgeEventDeleteView(OwnerRequiredMixin, SuccessMixim, DeleteView):
    model = AgeEvent
    template_name = "age_timelines/age_event_confirm_delete.html"


class TagValidateMixim(object):
    def form_valid(self, form):
        age_timeline = AgeTimeline.objects.get(
            pk=self.kwargs['age_timeline_id']
        )
        form.instance.timeline_id = age_timeline.timeline_ptr.pk

        name_error = field_empty_error(form, "name")
        if name_error is not None:
            form.add_error("name", name_error)

        if form.errors:
            return self.form_invalid(form)
        else:
            return super().form_valid(form)


class TagCreateView(LoginRequiredMixin, AgeTimelineOwnerMixim, TagValidateMixim, SuccessMixim, CreateView):
    model = Tag
    fields = ['name']
    template_name = "age_timelines/tag_add_form.html"


class TagUpdateView(OwnerRequiredMixin, TagValidateMixim, SuccessMixim, UpdateView):
    model = Tag
    fields = ["name"]
    template_name = "age_timelines/tag_edit_form.html"


class TagDeleteView(OwnerRequiredMixin, SuccessMixim, DeleteView):
    model = Tag
    template_name = "timelines/tag_confirm_delete.html"


class AreaCreateView(LoginRequiredMixin, AgeTimelineOwnerMixim, SuccessMixim, CreateView):
    model = TimelineArea
    fields = ["name", "page_position", "weight"]
    template_name = "age_timelines/area_add_form.html"

    def form_valid(self, form):
        age_timeline = AgeTimeline.objects.get(
            pk=self.kwargs['age_timeline_id']
        )
        form.instance.timeline_id = age_timeline.timeline_ptr.pk

        name_error = field_empty_error(form, "name")
        if name_error is not None:
            form.add_error("name", name_error)

        position_error = area_position_error(
            form,
            age_timeline.timeline_ptr
        )
        if position_error is not None:
            form.add_error("page_position", position_error)

        if form.errors:
            return self.form_invalid(form)
        else:
            return super().form_valid(form)


class AreaUpdateView(OwnerRequiredMixin, SuccessMixim, UpdateView):
    model = TimelineArea
    fields = ["name", "page_position", "weight"]
    template_name = "age_timelines/area_edit_form.html"

    def form_valid(self, form):
        age_timeline = AgeTimeline.objects.get(
            pk=self.kwargs['age_timeline_id']
        )
        form.instance.timeline_id = age_timeline.timeline_ptr.pk

        name_error = field_empty_error(form, "name")
        if name_error is not None:
            form.add_error("name", name_error)

        position_error = area_position_error(
            form,
            age_timeline.timeline_ptr,
            self.get_object().id
        )
        if position_error is not None:
            form.add_error("page_position", position_error)

        if form.errors:
            return self.form_invalid(form)
        else:
            return super().form_valid(form)


class AreaDeleteView(OwnerRequiredMixin, SuccessMixim, DeleteView):
    model = TimelineArea
    template_name = "timelines/area_confirm_delete.html"
