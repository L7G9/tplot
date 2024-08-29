from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse, HttpResponseForbidden
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView


from timelines.mixins import OwnerRequiredMixin
from timelines.view_errors import event_area_position_error
from timelines.pdf.get_filename import get_filename
from timelines.models import Tag, EventArea

from .models import HistoricalEvent, HistoricalTimeline
from .pdf.pdf_historical_timeline import PDFHistoricalTimeline


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
    model = HistoricalTimeline
    template_name = "historical_timelines/timeline_detail.html"


class TimelineCreateView(LoginRequiredMixin, CreateView):
    model = HistoricalTimeline
    fields = TIMELINE_FIELD_ORDER
    template_name = "historical_timelines/timeline_add.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TimelineUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = HistoricalTimeline
    fields = TIMELINE_FIELD_ORDER
    template_name = "historical_timelines/timeline_edit.html"


class TimelineDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = HistoricalTimeline
    template_name = "historical_timelines/timeline_delete.html"
    success_url = reverse_lazy("timelines:user-timelines")


class TimelineOwnerMixim(object):
    """Check historical timeline found with historical_timeline_id is owned by
    logged in user."""

    def dispatch(self, request, *args, **kwargs):
        historical_timeline = HistoricalTimeline.objects.get(
            pk=self.kwargs["historical_timeline_id"]
        )
        if historical_timeline.get_owner() != request.user:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)


class SuccessMixim(object):
    """Return historical timeline detail."""

    def get_success_url(self) -> str:
        return reverse_lazy(
            "historical_timelines:timeline-detail",
            kwargs={"pk": self.kwargs["historical_timeline_id"]},
        )


class HistoricalTimelineContextMixim:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["historical_timeline"] = HistoricalTimeline.objects.get(
            pk=self.kwargs["historical_timeline_id"]
        )
        return context


EVENT_FIELD_ORDER = [
    "start_bc_ad",
    "start_year",
    "has_end",
    "end_bc_ad",
    "end_year",
    "title",
    "description",
    "event_area",
    "tags",
]


class EventValidateMixim(object):
    def form_valid(self, form):
        form.instance.historical_timeline = HistoricalTimeline.objects.get(
            pk=self.kwargs["historical_timeline_id"]
        )
        form.instance.timeline_id = (
            form.instance.historical_timeline.timeline_ptr.pk
        )

        if form.cleaned_data["has_end"]:
            start_bc_ad = form.cleaned_data["start_bc_ad"]
            start_year = form.cleaned_data["start_year"]
            start_total = start_bc_ad * start_year

            end_bc_ad = form.cleaned_data["end_bc_ad"]
            end_year = form.cleaned_data["end_year"]
            end_total = end_bc_ad * end_year

            if end_total <= start_total:
                form.add_error("end_bc_ad", "End must be after than start")
                form.add_error("end_year", "End must be after than start")

        if form.errors:
            return self.form_invalid(form)
        else:
            return super().form_valid(form)


def get_timeline_from_historical_timeline(view):
    historical_timeline = HistoricalTimeline.objects.get(
        pk=view.kwargs["historical_timeline_id"]
    )
    return historical_timeline.timeline_ptr.pk


class EventCreateView(
    LoginRequiredMixin,
    TimelineOwnerMixim,
    HistoricalTimelineContextMixim,
    EventValidateMixim,
    SuccessMixim,
    CreateView,
):
    model = HistoricalEvent
    fields = EVENT_FIELD_ORDER
    template_name = "historical_timelines/event_add.html"

    def get_form_class(self):
        modelform = super().get_form_class()
        timeline_id = get_timeline_from_historical_timeline(self)
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
    model = HistoricalEvent
    fields = EVENT_FIELD_ORDER
    template_name = "historical_timelines/event_edit.html"

    def get_form_class(self):
        modelform = super().get_form_class()
        timeline_id = get_timeline_from_historical_timeline(self)
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
    model = HistoricalEvent
    template_name = "historical_timelines/event_delete.html"


class TagValidateMixim(object):
    def form_valid(self, form):
        historical_timeline = HistoricalTimeline.objects.get(
            pk=self.kwargs["historical_timeline_id"]
        )
        form.instance.timeline_id = historical_timeline.timeline_ptr.pk

        return super().form_valid(form)


class TagCreateView(
    LoginRequiredMixin,
    TimelineOwnerMixim,
    HistoricalTimelineContextMixim,
    TagValidateMixim,
    SuccessMixim,
    CreateView,
):
    model = Tag
    fields = ["name", "description", "display"]
    template_name = "historical_timelines/tag_add.html"


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
    template_name = "historical_timelines/tag_edit.html"


class TagDeleteView(
    LoginRequiredMixin,
    TimelineOwnerMixim,
    OwnerRequiredMixin,
    SuccessMixim,
    DeleteView,
):
    model = Tag
    template_name = "historical_timelines/tag_delete.html"


class EventAreaValidateMixim(object):
    def form_valid(self, form):
        historical_timeline = HistoricalTimeline.objects.get(
            pk=self.kwargs["historical_timeline_id"]
        )
        form.instance.timeline_id = historical_timeline.timeline_ptr.pk

        area_id = None
        if "pk" in self.kwargs:
            area_id = self.get_object().id

        position_error = event_area_position_error(
            form,
            historical_timeline.timeline_ptr,
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
    HistoricalTimelineContextMixim,
    EventAreaValidateMixim,
    SuccessMixim,
    CreateView,
):
    model = EventArea
    fields = ["name", "page_position", "weight"]
    template_name = "historical_timelines/event_area_add.html"


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
    template_name = "historical_timelines/event_area_edit.html"


class EventAreaDeleteView(
    LoginRequiredMixin,
    TimelineOwnerMixim,
    OwnerRequiredMixin,
    SuccessMixim,
    DeleteView,
):
    model = EventArea
    template_name = "historical_timelines/event_area_delete.html"


class TimelineView(LoginRequiredMixin, OwnerRequiredMixin, DetailView):
    model = HistoricalTimeline
    template_name = "historical_timelines/timeline.html"


def pdf_view(request, historical_timeline_id):
    historical_timeline: HistoricalTimeline = HistoricalTimeline.objects.get(
        id=historical_timeline_id
    )

    timeline_pdf = PDFHistoricalTimeline(historical_timeline)

    return FileResponse(
        timeline_pdf.buffer,
        as_attachment=True,
        filename=get_filename(historical_timeline.title),
    )
