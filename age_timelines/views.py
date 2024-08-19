import json
import re

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from timelines.ai_assist.chat_gpt_request import chat_gpt_request
from timelines.ai_assist.request_text import role_text
from timelines.ai_assist.event_choice import get_event_choices
from timelines.forms import AIRequestForm, AIResultsForm, NEW_CHOICE
from timelines.mixins import OwnerRequiredMixin
from timelines.models import Tag, EventArea
from timelines.view_errors import event_area_position_error

from .ai_assist.request_text import age_request_text
from .models import AgeEvent, AgeTimeline
from .pdf.pdf_age_timeline import PDFAgeTimeline


AGE_TIMELINE_FIELD_ORDER = [
    "title",
    "description",
    "scale_unit",
    "scale_length",
    "page_size",
    "page_orientation",
    "page_scale_position",
]


class AgeTimelineDetailView(
    LoginRequiredMixin, OwnerRequiredMixin, DetailView
):
    model = AgeTimeline
    template_name = "age_timelines/age_timeline_detail.html"

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


class AgeTimelineUpdateView(
    LoginRequiredMixin, OwnerRequiredMixin, UpdateView
):
    model = AgeTimeline
    fields = AGE_TIMELINE_FIELD_ORDER
    template_name = "age_timelines/age_timeline_edit_form.html"


class AgeTimelineDeleteView(
    LoginRequiredMixin, OwnerRequiredMixin, DeleteView
):
    model = AgeTimeline
    template_name = "age_timelines/age_timeline_confirm_delete.html"
    success_url = reverse_lazy("timelines:user-timelines")


# check age timeline found with age_timeline_id is owned by logged in user
class AgeTimelineOwnerMixim(object):
    def dispatch(self, request, *args, **kwargs):
        age_timeline = AgeTimeline.objects.get(
            pk=self.kwargs["age_timeline_id"]
        )
        if age_timeline.get_owner() != request.user:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)


# return age timeline detail
class SuccessMixim(object):
    def get_success_url(self) -> str:
        return reverse_lazy(
            "age_timelines:age-timeline-detail",
            kwargs={"pk": self.kwargs["age_timeline_id"]},
        )


AGE_EVENT_FIELD_ORDER = [
    "start_year",
    "start_month",
    "has_end",
    "end_year",
    "end_month",
    "title",
    "description",
    "event_area",
    "tags",
]


class AgeEventValidateMixim(object):
    def form_valid(self, form):
        form.instance.age_timeline = AgeTimeline.objects.get(
            pk=self.kwargs["age_timeline_id"]
        )
        form.instance.timeline_id = form.instance.age_timeline.timeline_ptr.pk

        if form.cleaned_data["has_end"]:
            # TODO: move this logic somewhere useful
            start_year = form.cleaned_data["start_year"]
            start_month = form.cleaned_data["start_month"]
            start_total = (start_year * 12) + start_month

            end_year = form.cleaned_data["end_year"]
            end_month = form.cleaned_data["end_month"]
            end_total = (end_year * 12) + end_month

            if end_total <= start_total:
                form.add_error(
                    "end_year", "End age must be greater than start age"
                )
                form.add_error(
                    "end_month", "End age must be greater than start age"
                )

        if form.errors:
            return self.form_invalid(form)
        else:
            return super().form_valid(form)


def get_timeline_from_age_timeline(view):
    age_timeline = AgeTimeline.objects.get(pk=view.kwargs["age_timeline_id"])
    return age_timeline.timeline_ptr.pk


class AgeEventCreateView(
    LoginRequiredMixin,
    AgeTimelineOwnerMixim,
    AgeEventValidateMixim,
    SuccessMixim,
    CreateView,
):
    model = AgeEvent
    fields = AGE_EVENT_FIELD_ORDER
    template_name = "age_timelines/age_event_add_form.html"

    def get_form_class(self):
        modelform = super().get_form_class()
        timeline_id = get_timeline_from_age_timeline(self)
        modelform.base_fields["tags"].limit_choices_to = {
            "timeline": timeline_id
        }
        modelform.base_fields["event_area"].limit_choices_to = {
            "timeline": timeline_id
        }
        return modelform


class AgeEventUpdateView(
    LoginRequiredMixin,
    AgeTimelineOwnerMixim,
    OwnerRequiredMixin,
    AgeEventValidateMixim,
    SuccessMixim,
    UpdateView,
):
    model = AgeEvent
    fields = AGE_EVENT_FIELD_ORDER
    template_name = "age_timelines/age_event_edit_form.html"

    def get_form_class(self):
        modelform = super().get_form_class()
        timeline_id = get_timeline_from_age_timeline(self)
        modelform.base_fields["tags"].limit_choices_to = {
            "timeline": timeline_id
        }
        modelform.base_fields["event_area"].limit_choices_to = {
            "timeline": timeline_id
        }
        return modelform


class AgeEventDeleteView(
    LoginRequiredMixin,
    AgeTimelineOwnerMixim,
    OwnerRequiredMixin,
    SuccessMixim,
    DeleteView,
):
    model = AgeEvent
    template_name = "age_timelines/age_event_confirm_delete.html"


class TagValidateMixim(object):
    def form_valid(self, form):
        age_timeline = AgeTimeline.objects.get(
            pk=self.kwargs["age_timeline_id"]
        )
        form.instance.timeline_id = age_timeline.timeline_ptr.pk

        return super().form_valid(form)


class TagCreateView(
    LoginRequiredMixin,
    AgeTimelineOwnerMixim,
    TagValidateMixim,
    SuccessMixim,
    CreateView,
):
    model = Tag
    fields = ["name", "description", "display"]
    template_name = "age_timelines/tag_add_form.html"


class TagUpdateView(
    LoginRequiredMixin,
    AgeTimelineOwnerMixim,
    OwnerRequiredMixin,
    TagValidateMixim,
    SuccessMixim,
    UpdateView,
):
    model = Tag
    fields = ["name", "description", "display"]
    template_name = "age_timelines/tag_edit_form.html"


class TagDeleteView(
    LoginRequiredMixin,
    AgeTimelineOwnerMixim,
    OwnerRequiredMixin,
    SuccessMixim,
    DeleteView,
):
    model = Tag
    template_name = "age_timelines/tag_confirm_delete.html"


class EventAreaValidateMixim(object):
    def form_valid(self, form):
        age_timeline = AgeTimeline.objects.get(
            pk=self.kwargs["age_timeline_id"]
        )
        form.instance.timeline_id = age_timeline.timeline_ptr.pk

        # TODO: find a more elegant solution
        area_id = None
        if "pk" in self.kwargs:
            area_id = self.get_object().id

        position_error = event_area_position_error(
            form,
            age_timeline.timeline_ptr,
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
    AgeTimelineOwnerMixim,
    EventAreaValidateMixim,
    SuccessMixim,
    CreateView,
):
    model = EventArea
    fields = ["name", "page_position", "weight"]
    template_name = "age_timelines/event_area_add_form.html"


class EventAreaUpdateView(
    LoginRequiredMixin,
    AgeTimelineOwnerMixim,
    OwnerRequiredMixin,
    EventAreaValidateMixim,
    SuccessMixim,
    UpdateView,
):
    model = EventArea
    fields = ["name", "page_position", "weight"]
    template_name = "age_timelines/event_area_edit_form.html"


class EventAreaDeleteView(
    LoginRequiredMixin,
    AgeTimelineOwnerMixim,
    OwnerRequiredMixin,
    SuccessMixim,
    DeleteView,
):
    model = EventArea
    template_name = "age_timelines/event_area_confirm_delete.html"


class TimelineView(
    LoginRequiredMixin, OwnerRequiredMixin, DetailView
):
    model = AgeTimeline
    template_name = "age_timelines/timeline.html"


def pdf_view(request, age_timeline_id):
    age_timeline: AgeTimeline = AgeTimeline.objects.get(id=age_timeline_id)

    if age_timeline.get_owner() != request.user:
        return HttpResponseForbidden()

    timeline_pdf = PDFAgeTimeline(age_timeline)

    return FileResponse(
        timeline_pdf.buffer, as_attachment=True, filename="timeline.pdf"
    )


class AIRequestView(LoginRequiredMixin, AgeTimelineOwnerMixim, FormView):
    form_class = AIRequestForm
    template_name = "age_timelines/ai_request.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()

        return render(
            request, self.template_name, {"form": form, "view": self}
        )

    def form_valid(self, form):
        self.request.session["ai_role"] = role_text()
        request_values = form.get_request_values()
        self.request.session["ai_request"] = age_request_text(
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
            "age_timelines:ai-result",
            kwargs={
                "age_timeline_id": self.kwargs["age_timeline_id"],
            },
        )


class AIResultView(
    LoginRequiredMixin, AgeTimelineOwnerMixim, SuccessMixim, FormView
):
    form_class = AIResultsForm
    template_name = "age_timelines/ai_result.html"

    def get_form_kwargs(self):
        kwargs = super(AIResultView, self).get_form_kwargs()
        kwargs["timeline_id"] = get_timeline_from_age_timeline(self)
        kwargs["events"] = get_event_choices(self.request.session["ai_result"])
        return kwargs

    def get(self, request, *args, **kwargs):
        role_text = self.request.session["ai_role"]
        request_text = self.request.session["ai_request"]
        result_text = chat_gpt_request(role_text, request_text)
        self.request.session["ai_result"] = json.loads(result_text)

        form = self.form_class(**self.get_form_kwargs())
        context = self.get_context_data()
        context["form"] = form
        context["view"] = self

        return render(
            request,
            self.template_name,
            context,
        )

    def __new_event_area(self, form, timeline):
        new_name = form.cleaned_data["new_event_area_name"]
        new_position = form.cleaned_data["new_event_area_position"]
        new_weight = form.cleaned_data["new_event_area_weight"]

        return EventArea.objects.create(
            timeline=timeline,
            name=new_name,
            page_position=new_position,
            weight=new_weight,
        )

    def __get_age_unit(self, unit_name, age_string) -> int:
        match = re.search(f"(\\d+) {unit_name}", age_string)
        return int(match.group(1))

    def __new_event(self, json_event, age_timeline, timeline, event_area):
        start_year = self.__get_age_unit("Years", json_event["start"])
        start_month = self.__get_age_unit("Months", json_event["start"])
        has_end = json_event["end"] != ""
        if has_end:
            end_year = self.__get_age_unit("Years", json_event["end"])
            end_month = self.__get_age_unit("Months", json_event["end"])
        else:
            end_year = start_year
            end_month = start_month
        title = json_event["title"]
        description = json_event["description"]

        return AgeEvent.objects.create(
            age_timeline=age_timeline,
            timeline=timeline,
            start_year=start_year,
            start_month=start_month,
            has_end=has_end,
            end_year=end_year,
            end_month=end_month,
            title=title,
            description=description,
            event_area=event_area,
        )

    def form_valid(self, form):
        age_timeline = AgeTimeline.objects.get(
            pk=self.kwargs["age_timeline_id"]
        )
        timeline = age_timeline.timeline_ptr

        if form.cleaned_data["event_area_choice"] == NEW_CHOICE:
            event_area = self.__new_event_area(form, timeline)
        else:
            event_area = form.cleaned_data["existing_event_area_choice"]

        json_events = self.request.session["ai_result"]
        for event_index in form.cleaned_data["event_choice"]:
            self.__new_event(
                json_events['events'][int(event_index)],
                age_timeline,
                timeline,
                event_area,
            )

        return super().form_valid(form)
