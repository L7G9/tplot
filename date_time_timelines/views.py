from datetime import datetime
import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from timelines.ai_assist.chat_gpt_request import chat_gpt_request
from timelines.ai_assist.event_choice import get_event_choices
from timelines.ai_assist.request_text import role_text
from timelines.forms import AIRequestForm, AIResultsForm, NEW_CHOICE
from timelines.mixins import OwnerRequiredMixin
from timelines.models import EventArea, Tag
from timelines.pdf.get_filename import get_filename
from timelines.view_errors import event_area_position_error

from .ai_assist.request_text import date_time_request_text
from .models import DateTimeEvent, DateTimeTimeline
from .pdf.pdf_date_time_timeline import PDFDateTimeTimeline


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


class AgeTimelineContextMixim:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["date_time_timeline"] = DateTimeTimeline.objects.get(
            pk=self.kwargs["date_time_timeline_id"]
        )
        return context


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
    AgeTimelineContextMixim,
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
    AgeTimelineContextMixim,
    TagValidateMixim,
    SuccessMixim,
    CreateView,
):
    model = Tag
    fields = ["name", "description", "display"]
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
    fields = ["name", "description", "display"]
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
    AgeTimelineContextMixim,
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


class TimelineView(
    LoginRequiredMixin, OwnerRequiredMixin, DetailView
):
    model = DateTimeTimeline
    template_name = "date_time_timelines/timeline.html"


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
        filename=get_filename(timeline.title),
    )


class AIRequestView(
    LoginRequiredMixin,
    DateTimeTimelineOwnerMixim,
    FormView
):
    form_class = AIRequestForm
    template_name = "date_time_timelines/ai_request.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()

        date_time_timeline = DateTimeTimeline.objects.get(
            pk=self.kwargs["date_time_timeline_id"]
        )

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "view": self,
                "date_time_timeline": date_time_timeline
            }
        )

    def form_valid(self, form):
        self.request.session['ai_role'] = role_text()
        request_values = form.get_request_values()
        self.request.session['ai_request'] = date_time_request_text(
            topic=request_values[0],
            sources=request_values[1],
            count_description=request_values[2],
            start_end_option=request_values[3],
            title_info=request_values[4],
            description_info=request_values[5],
        )
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "date_time_timelines:date-time-timeline-ai-result",
            kwargs={
                "date_time_timeline_id": self.kwargs["date_time_timeline_id"],
            },
        )


class AIResultView(
    LoginRequiredMixin,
    DateTimeTimelineOwnerMixim,
    SuccessMixim,
    FormView
):
    form_class = AIResultsForm
    template_name = "date_time_timelines/ai_result.html"

    def get_form_kwargs(self):
        kwargs = super(AIResultView, self).get_form_kwargs()
        kwargs['timeline_id'] = get_timeline_from_date_time_timeline(self)
        kwargs['events'] = get_event_choices(self.request.session['ai_result'])

        return kwargs

    def get(self, request, *args, **kwargs):
        role_text = self.request.session['ai_role']
        request_text = self.request.session['ai_request']
        result_text = chat_gpt_request(role_text, request_text)
        self.request.session['ai_result'] = json.loads(result_text)

        form = self.form_class(**self.get_form_kwargs())
        context = self.get_context_data()
        context['form'] = form
        context['view'] = self
        context["date_time_timeline"] = DateTimeTimeline.objects.get(
            pk=self.kwargs["date_time_timeline_id"]
        )

        return render(
            request,
            self.template_name,
            context,
        )

    def __new_event_area(self, form, timeline):
        new_name = form.cleaned_data['new_event_area_name']
        new_position = form.cleaned_data['new_event_area_position']
        new_weight = form.cleaned_data['new_event_area_weight']

        return EventArea.objects.create(
            timeline=timeline,
            name=new_name,
            page_position=new_position,
            weight=new_weight,
        )

    def __new_event(
            self,
            json_event,
            date_time_timeline,
            timeline,
            event_area
    ):
        datetime_format = "%Y-%m-%d %H:%M:%S"
        start = datetime.strptime(json_event["start"], datetime_format)
        has_end = json_event['end'] != ""
        if has_end:
            end = datetime.strptime(json_event["end"], datetime_format)
        else:
            end = datetime.strptime(json_event["start"], datetime_format)
        title = json_event['title']
        description = json_event['description']

        return DateTimeEvent.objects.create(
            date_time_timeline=date_time_timeline,
            timeline=timeline,
            start_date_time=start,
            has_end=has_end,
            end_date_time=end,
            title=title,
            description=description,
            event_area=event_area,
        )

    def form_valid(self, form):
        date_time_timeline = DateTimeTimeline.objects.get(
            pk=self.kwargs["date_time_timeline_id"]
        )
        timeline = date_time_timeline.timeline_ptr

        if form.cleaned_data['event_area_choice'] == NEW_CHOICE:
            event_area = self.__new_event_area(form, timeline)
        else:
            event_area = form.cleaned_data['existing_event_area_choice']

        json_events = self.request.session['ai_result']
        for event_index in form.cleaned_data['event_choice']:
            self.__new_event(
                json_events['events'][int(event_index)],
                date_time_timeline,
                timeline,
                event_area
            )

        return super().form_valid(form)
