import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView


from timelines.mixins import OwnerRequiredMixin
from timelines.view_errors import event_area_position_error
from timelines.models import EventArea, Tag

from .models import DateTimeEvent, DateTimeTimeline
from .pdf.pdf_date_time_timeline import PDFDateTimeTimeline

from timelines.forms import AIRequestForm, AIResultsForm, USER_CHOICE

DATE_TIME_TIMELINE_FIELD_ORDER = [
    "title",
    "description",
    "scale_unit",
    "scale_length",
    "scale_display_format",
    "page_size",
    "page_orientation",
    "page_scale_position",
    "event_display_format",
]


class DateTimeTimelineDetailView(
    LoginRequiredMixin, OwnerRequiredMixin, DetailView
):
    model = DateTimeTimeline
    template_name = "date_time_timelines/timeline_detail.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()

        return context


class DateTimeTimelineCreateView(LoginRequiredMixin, CreateView):
    model = DateTimeTimeline
    fields = DATE_TIME_TIMELINE_FIELD_ORDER
    template_name = "date_time_timelines/timeline_add_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DateTimeTimelineUpdateView(
    LoginRequiredMixin, OwnerRequiredMixin, UpdateView
):
    model = DateTimeTimeline
    fields = DATE_TIME_TIMELINE_FIELD_ORDER
    template_name = "date_time_timelines/timeline_edit_form.html"


class DateTimeTimelineDeleteView(
    LoginRequiredMixin, OwnerRequiredMixin, DeleteView
):
    model = DateTimeTimeline
    template_name = "date_time_timelines/timeline_confirm_delete.html"
    success_url = reverse_lazy("timelines:user-timelines")


# check date time timeline found with date_time_timeline_id is owned by logged
# in user
class DateTimeTimelineOwnerMixim(object):
    def dispatch(self, request, *args, **kwargs):
        timeline = DateTimeTimeline.objects.get(
            pk=self.kwargs["date_time_timeline_id"]
        )
        if timeline.get_owner() != request.user:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)


# return date time timeline detail
class SuccessMixim(object):
    def get_success_url(self) -> str:
        return reverse_lazy(
            "date_time_timelines:date-time-timeline-detail",
            kwargs={"pk": self.kwargs["date_time_timeline_id"]},
        )


DATE_TIME_EVENT_FIELD_ORDER = [
    "start_date_time",
    "has_end",
    "end_date_time",
    "title",
    "description",
    "event_area",
    "tags",
]


class DateTimeEventValidateMixim(object):
    def form_valid(self, form):
        form.instance.date_time_timeline = DateTimeTimeline.objects.get(
            pk=self.kwargs["date_time_timeline_id"]
        )
        form.instance.timeline_id = (
            form.instance.date_time_timeline.timeline_ptr.pk
        )

        if form.cleaned_data["has_end"]:
            start_date = form.cleaned_data["start_date_time"]
            end_date = form.cleaned_data["end_date_time"]

            if end_date <= start_date:
                form.add_error(
                    "start_date_time",
                    "End date & time must be greater than start date & time"
                )
                form.add_error(
                    "end_date_time",
                    "End date & time must be greater than start date & time"
                )

        if form.errors:
            return self.form_invalid(form)
        else:
            return super().form_valid(form)


def get_timeline_from_date_time_timeline(view):
    timeline = DateTimeTimeline.objects.get(
            pk=view.kwargs["date_time_timeline_id"]
        )
    return timeline.timeline_ptr.pk


class DateTimeEventCreateView(
    LoginRequiredMixin,
    DateTimeTimelineOwnerMixim,
    DateTimeEventValidateMixim,
    SuccessMixim,
    CreateView,
):
    model = DateTimeEvent
    fields = DATE_TIME_EVENT_FIELD_ORDER
    template_name = "date_time_timelines/event_add_form.html"

    def get_form_class(self):
        modelform = super().get_form_class()
        timeline_id = get_timeline_from_date_time_timeline(self)
        modelform.base_fields['tags'].limit_choices_to = {
            'timeline': timeline_id
        }
        modelform.base_fields['event_area'].limit_choices_to = {
            'timeline': timeline_id
        }
        return modelform


class DateTimeEventUpdateView(
    LoginRequiredMixin,
    DateTimeTimelineOwnerMixim,
    OwnerRequiredMixin,
    DateTimeEventValidateMixim,
    SuccessMixim,
    UpdateView,
):
    model = DateTimeEvent
    fields = DATE_TIME_EVENT_FIELD_ORDER
    template_name = "date_time_timelines/event_edit_form.html"

    def get_form_class(self):
        modelform = super().get_form_class()
        timeline_id = get_timeline_from_date_time_timeline(self)
        modelform.base_fields['tags'].limit_choices_to = {
            'timeline': timeline_id
        }
        modelform.base_fields['event_area'].limit_choices_to = {
            'timeline': timeline_id
        }
        return modelform


class DateTimeEventDeleteView(
    LoginRequiredMixin,
    DateTimeTimelineOwnerMixim,
    OwnerRequiredMixin,
    SuccessMixim,
    DeleteView,
):
    model = DateTimeEvent
    template_name = "date_time_timelines/event_confirm_delete.html"


class TagValidateMixim(object):
    def form_valid(self, form):
        timeline = DateTimeTimeline.objects.get(
            pk=self.kwargs["date_time_timeline_id"]
        )
        form.instance.timeline_id = timeline.timeline_ptr.pk

        return super().form_valid(form)


class TagCreateView(
    LoginRequiredMixin,
    DateTimeTimelineOwnerMixim,
    TagValidateMixim,
    SuccessMixim,
    CreateView,
):
    model = Tag
    fields = ["name"]
    template_name = "date_time_timelines/tag_add_form.html"


class TagUpdateView(
    LoginRequiredMixin,
    DateTimeTimelineOwnerMixim,
    OwnerRequiredMixin,
    TagValidateMixim,
    SuccessMixim,
    UpdateView,
):
    model = Tag
    fields = ["name"]
    template_name = "date_time_timelines/tag_edit_form.html"


class TagDeleteView(
    LoginRequiredMixin,
    DateTimeTimelineOwnerMixim,
    OwnerRequiredMixin,
    SuccessMixim,
    DeleteView,
):
    model = Tag
    template_name = "date_time_timelines/tag_confirm_delete.html"


class EventAreaValidateMixim(object):
    def form_valid(self, form):
        timeline = DateTimeTimeline.objects.get(
            pk=self.kwargs["date_time_timeline_id"]
        )
        form.instance.timeline_id = timeline.timeline_ptr.pk

        # TODO: find a more elegant solution
        area_id = None
        if "pk" in self.kwargs:
            area_id = self.get_object().id

        position_error = event_area_position_error(
            form,
            timeline.timeline_ptr,
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
    DateTimeTimelineOwnerMixim,
    EventAreaValidateMixim,
    SuccessMixim,
    CreateView,
):
    model = EventArea
    fields = ["name", "page_position", "weight"]
    template_name = "date_time_timelines/event_area_add_form.html"


class EventAreaUpdateView(
    LoginRequiredMixin,
    DateTimeTimelineOwnerMixim,
    OwnerRequiredMixin,
    EventAreaValidateMixim,
    SuccessMixim,
    UpdateView,
):
    model = EventArea
    fields = ["name", "page_position", "weight"]
    template_name = "date_time_timelines/event_area_edit_form.html"


class EventAreaDeleteView(
    LoginRequiredMixin,
    DateTimeTimelineOwnerMixim,
    OwnerRequiredMixin,
    SuccessMixim,
    DeleteView,
):
    model = EventArea
    template_name = "date_time_timelines/event_area_confirm_delete.html"


def pdf_view(request, date_time_timeline_id):
    timeline: DateTimeTimeline = DateTimeTimeline.objects.get(
        id=date_time_timeline_id
    )

    if timeline.get_owner() != request.user:
        return HttpResponseForbidden()

    timeline_pdf = PDFDateTimeTimeline(timeline)

    return FileResponse(
        timeline_pdf.buffer,
        as_attachment=True,
        filename="timeline.pdf"
    )


class AIRequestView(
    LoginRequiredMixin,
    DateTimeTimelineOwnerMixim,
    FormView
):
    form_class = AIRequestForm
    template_name = "date_time_timelines/ai_request.html"

    def form_valid(self, form):
        if (
            (form.cleaned_data["event_count_choice"] == USER_CHOICE)
            and (form.cleaned_data["event_count_text"] == "")
        ):
            form.add_error(
                "event_count_text",
                "Event count must be defined."
            )

        if (
            (form.cleaned_data["title_choice"] == USER_CHOICE)
            and (form.cleaned_data["title_text"] == "")
        ):
            form.add_error(
                "title_text",
                "Title contents must be defined."
            )

        if (
            (form.cleaned_data["description_choice"] == USER_CHOICE)
            and (form.cleaned_data["description_text"] == "")
        ):
            form.add_error(
                "description_text",
                "Description contents must be defined."
            )

        if form.errors:
            return self.form_invalid(form)
        else:
            return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        form = self.form_class()

        return render(
            request,
            self.template_name,
            {"form": form, "view": self}
        )

    def get_success_url(self) -> str:
        return reverse_lazy(
            "date_time_timelines:date-time-timeline-ai-result",
            kwargs={"date_time_timeline_id": self.kwargs["date_time_timeline_id"]},
        )


class AIResultView(
    LoginRequiredMixin,
    DateTimeTimelineOwnerMixim,
    SuccessMixim,
    FormView
):
    form_class = AIResultsForm
    template_name = "date_time_timelines/ai_result.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events"] = json.loads("""[
            {
                "start": "1961-05-25 00:00:00",
                "end": "",
                "title": "Kennedy's Moon Landing Proposal",
                "description": "President John F. Kennedy announced the goal of sending an American to the Moon before the end of the decade."
            },
            {
                "start": "1967-01-27 00:00:00",
                "end": "",
                "title": "Apollo 1 Tragedy",
                "description": "A cabin fire during a launch rehearsal test killed astronauts Gus Grissom, Ed White, and Roger B. Chaffee."
            },
            {
                "start": "1968-12-21 00:00:00",
                "end": "",
                "title": "Launch of Apollo 8",
                "description": "Apollo 8 launched and became the first manned spacecraft to orbit the Moon and return safely to Earth."
            },
            {
                "start": "1969-07-16 13:32:00",
                "end": "",
                "title": "Launch of Apollo 11",
                "description": "Apollo 11 was launched from Kennedy Space Center, carrying astronauts Neil Armstrong, Buzz Aldrin, and Michael Collins."
            },
            {
                "start": "1969-07-20 20:17:40",
                "end": "",
                "title": "Apollo 11 Moon Landing",
                "description": "The Lunar Module Eagle landed on the Moon's surface, and Neil Armstrong became the first human to set foot on the Moon."
            },
            {
                "start": "1970-04-11 13:13:00",
                "end": "",
                "title": "Launch of Apollo 13",
                "description": "Apollo 13 was launched but suffered a critical failure en route to the Moon, resulting in a mission abort and safe return of the crew."
            },
            {
                "start": "1972-12-07 00:00:00",
                "end": "",
                "title": "Launch of Apollo 17",
                "description": "Apollo 17 was launched, marking the last manned mission to the Moon, with astronauts Eugene Cernan, Ronald Evans, and Harrison Schmitt."
            },
            {
                "start": "1972-12-19 00:00:00",
                "end": "",
                "title": "Return of Apollo 17",
                "description": "Apollo 17 safely returned to Earth, concluding the Apollo program's manned lunar missions."
            }
            ]""")

        return context

    def get_form_kwargs(self):
        print("***get_form_kwargs***")
        kwargs = super(AIResultView, self).get_form_kwargs()
        kwargs['timeline_id'] = get_timeline_from_date_time_timeline(self)
        return kwargs

    def get(self, request, *args, **kwargs):
        form = self.form_class(**self.get_form_kwargs())

        return render(
            request,
            self.template_name,
            {"form": form, "view": self}
        )
