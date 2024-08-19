from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse, HttpResponseForbidden
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView


from timelines.mixins import OwnerRequiredMixin
from timelines.view_errors import event_area_position_error
from timelines.models import Tag, EventArea

from .models import ScientificEvent, ScientificTimeline
from .pdf.pdf_scientific_timeline import PDFScientificTimeline


TIMELINE_FIELD_ORDER = [
    "title",
    "description",
    "scale_unit",
    "scale_length",
    "page_size",
    "page_orientation",
    "page_scale_position",
]


class TimelineDetailView(LoginRequiredMixin, OwnerRequiredMixin, DetailView):
    model = ScientificTimeline
    template_name = "scientific_timelines/timeline_detail.html"


class TimelineCreateView(LoginRequiredMixin, CreateView):
    model = ScientificTimeline
    fields = TIMELINE_FIELD_ORDER
    template_name = "scientific_timelines/timeline_add.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TimelineUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = ScientificTimeline
    fields = TIMELINE_FIELD_ORDER
    template_name = "scientific_timelines/timeline_edit.html"


class TimelineDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = ScientificTimeline
    template_name = "scientific_timelines/timeline_delete.html"
    success_url = reverse_lazy("timelines:user-timelines")


class TimelineOwnerMixim(object):
    """Check scientific timeline found with scientific_timeline_id is owned
    by logged in user."""

    def dispatch(self, request, *args, **kwargs):
        scientific_timeline = ScientificTimeline.objects.get(
            pk=self.kwargs["scientific_timeline_id"]
        )
        if scientific_timeline.get_owner() != request.user:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)


# return scientific timeline detail
class SuccessMixim(object):
    def get_success_url(self) -> str:
        return reverse_lazy(
            "scientific_timelines:timeline-detail",
            kwargs={"pk": self.kwargs["scientific_timeline_id"]},
        )


EVENT_FIELD_ORDER = [
    "start_year_fraction",
    "start_multiplier",
    "has_end",
    "end_year_fraction",
    "end_multiplier",
    "title",
    "description",
    "event_area",
    "tags",
]


class EventValidateMixim(object):
    def form_valid(self, form):
        form.instance.scientific_timeline = ScientificTimeline.objects.get(
            pk=self.kwargs["scientific_timeline_id"]
        )
        form.instance.timeline_id = (
            form.instance.scientific_timeline.timeline_ptr.pk
        )

        if form.cleaned_data["has_end"]:
            start_year_fraction = form.cleaned_data["start_year_fraction"]
            start_multiplier = form.cleaned_data["start_multiplier"]
            start_total = start_year_fraction * start_multiplier

            end_year_fraction = form.cleaned_data["end_year_fraction"]
            end_multiplier = form.cleaned_data["end_multiplier"]
            end_total = end_year_fraction * end_multiplier

            if end_total <= start_total:
                form.add_error(
                    "end_year_fraction", "End must be greater than start"
                )
                form.add_error(
                    "end_multiplier", "End must be greater than start"
                )

        if form.errors:
            return self.form_invalid(form)
        else:
            return super().form_valid(form)


def get_timeline_from_scientific_timeline(view):
    scientific_timeline = ScientificTimeline.objects.get(
        pk=view.kwargs["scientific_timeline_id"]
    )
    return scientific_timeline.timeline_ptr.pk


class EventCreateView(
    LoginRequiredMixin,
    TimelineOwnerMixim,
    EventValidateMixim,
    SuccessMixim,
    CreateView,
):
    model = ScientificEvent
    fields = EVENT_FIELD_ORDER
    template_name = "scientific_timelines/event_add.html"

    def get_form_class(self):
        modelform = super().get_form_class()
        timeline_id = get_timeline_from_scientific_timeline(self)
        modelform.base_fields["tags"].limit_choices_to = {
            "timeline": timeline_id
        }
        modelform.base_fields["event_area"].limit_choices_to = {
            "timeline": timeline_id
        }
        return modelform


class EventUpdateView(
    LoginRequiredMixin,
    TimelineOwnerMixim,
    OwnerRequiredMixin,
    EventValidateMixim,
    SuccessMixim,
    UpdateView,
):
    model = ScientificEvent
    fields = EVENT_FIELD_ORDER
    template_name = "scientific_timelines/event_edit.html"

    def get_form_class(self):
        modelform = super().get_form_class()
        timeline_id = get_timeline_from_scientific_timeline(self)
        modelform.base_fields["tags"].limit_choices_to = {
            "timeline": timeline_id
        }
        modelform.base_fields["event_area"].limit_choices_to = {
            "timeline": timeline_id
        }
        return modelform


class EventDeleteView(
    LoginRequiredMixin,
    TimelineOwnerMixim,
    OwnerRequiredMixin,
    SuccessMixim,
    DeleteView,
):
    model = ScientificEvent
    template_name = "scientific_timelines/event_delete.html"


class TagValidateMixim(object):
    def form_valid(self, form):
        scientific_timeline = ScientificTimeline.objects.get(
            pk=self.kwargs["scientific_timeline_id"]
        )
        form.instance.timeline_id = scientific_timeline.timeline_ptr.pk

        return super().form_valid(form)


class TagCreateView(
    LoginRequiredMixin,
    TimelineOwnerMixim,
    TagValidateMixim,
    SuccessMixim,
    CreateView,
):
    model = Tag
    fields = ["name", "description", "display"]
    template_name = "scientific_timelines/tag_add.html"


class TagUpdateView(
    LoginRequiredMixin,
    TimelineOwnerMixim,
    OwnerRequiredMixin,
    TagValidateMixim,
    SuccessMixim,
    UpdateView,
):
    model = Tag
    fields = ["name", "description", "display"]
    template_name = "scientific_timelines/tag_edit.html"


class TagDeleteView(
    LoginRequiredMixin,
    TimelineOwnerMixim,
    OwnerRequiredMixin,
    SuccessMixim,
    DeleteView,
):
    model = Tag
    template_name = "scientific_timelines/tag_delete.html"


class EventAreaValidateMixim(object):
    def form_valid(self, form):
        scientific_timeline = ScientificTimeline.objects.get(
            pk=self.kwargs["scientific_timeline_id"]
        )
        form.instance.timeline_id = scientific_timeline.timeline_ptr.pk

        area_id = None
        if "pk" in self.kwargs:
            area_id = self.get_object().id

        position_error = event_area_position_error(
            form,
            scientific_timeline.timeline_ptr,
            area_id,
        )
        if position_error is not None:
            form.add_error("page_position", position_error)

        if form.errors:
            return self.form_invalid(form)
        else:
            return super().form_valid(form)


class EventAreaCreateView(
    LoginRequiredMixin,
    TimelineOwnerMixim,
    EventAreaValidateMixim,
    SuccessMixim,
    CreateView,
):
    model = EventArea
    fields = ["name", "page_position", "weight"]
    template_name = "scientific_timelines/event_area_add.html"


class EventAreaUpdateView(
    LoginRequiredMixin,
    TimelineOwnerMixim,
    OwnerRequiredMixin,
    EventAreaValidateMixim,
    SuccessMixim,
    UpdateView,
):
    model = EventArea
    fields = ["name", "page_position", "weight"]
    template_name = "scientific_timelines/event_area_edit.html"


class EventAreaDeleteView(
    LoginRequiredMixin,
    TimelineOwnerMixim,
    OwnerRequiredMixin,
    SuccessMixim,
    DeleteView,
):
    model = EventArea
    template_name = "scientific_timelines/event_area_delete.html"


class TimelineView(LoginRequiredMixin, OwnerRequiredMixin, DetailView):
    model = ScientificTimeline
    template_name = "scientific_timelines/timeline.html"


def pdf_view(request, scientific_timeline_id):
    scientific_timeline: ScientificTimeline = ScientificTimeline.objects.get(
        id=scientific_timeline_id
    )

    timeline_pdf = PDFScientificTimeline(scientific_timeline)

    return FileResponse(
        timeline_pdf.buffer, as_attachment=True, filename="timeline.pdf"
    )
