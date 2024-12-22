import json
import re

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import FileResponse, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView, DeleteView, FormView, UpdateView,
)

from timelines.ai_assist.chat_gpt_request import chat_gpt_request
from timelines.ai_assist.request_text import role_text
from timelines.ai_assist.event_choice import get_event_choices
from timelines.forms import (
    AIRequestForm, AIResultsForm, NEW_CHOICE, NewCollaboratorForm
)
from timelines.mixins import RolePermissionMixin, RoleContextMixin
from timelines.models import (
    Tag,
    EventArea,
    Collaborator,
    ROLE_VIEWER,
    ROLE_EVENT_EDITOR,
    ROLE_TIMELINE_EDITOR,
    ROLE_OWNER
)
from timelines.pdf.get_filename import get_filename
from timelines.view_errors import event_area_position_error

from .ai_assist.request_text import age_request_text
from .models import AgeEvent, AgeTimeline
from .pdf.pdf_age_timeline import PDFAgeTimeline
from .view_data.age_timeline_data import AgeTimelineData


AGE_TIMELINE_FIELD_ORDER = [
    "title",
    "description",
    "scale_unit",
    "scale_length",
    "page_orientation",
    "page_scale_position",
    "page_size",
]


class AgeTimelineDetailView(
    LoginRequiredMixin, RolePermissionMixin, DetailView
):
    model = AgeTimeline
    template_name = "age_timelines/age_timeline_detail.html"
    required_role = ROLE_VIEWER

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        timeline = self.get_object().get_timeline()
        user_role = timeline.get_role(self.request.user)
        context["user_role"] = user_role
        return context


class AgeTimelineCreateView(LoginRequiredMixin, CreateView):
    model = AgeTimeline
    fields = AGE_TIMELINE_FIELD_ORDER
    template_name = "age_timelines/age_timeline_add_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class AgeTimelineUpdateView(
    LoginRequiredMixin, RolePermissionMixin, RoleContextMixin, UpdateView
):
    model = AgeTimeline
    fields = AGE_TIMELINE_FIELD_ORDER
    template_name = "age_timelines/age_timeline_edit_form.html"
    required_role = ROLE_TIMELINE_EDITOR


class AgeTimelineDeleteView(
    LoginRequiredMixin, RolePermissionMixin, DeleteView
):
    model = AgeTimeline
    template_name = "age_timelines/age_timeline_confirm_delete.html"
    success_url = reverse_lazy("timelines:user-timelines")
    required_role = ROLE_OWNER


class AgeTimelineRoleMixin(object):
    def dispatch(self, request, *args, **kwargs):
        age_timeline = AgeTimeline.objects.get(
            pk=self.kwargs["age_timeline_id"]
        )
        user_role = (
            age_timeline.get_role(self.request.user)
        )
        if user_role < self.required_role:
            return HttpResponseForbidden()
        return super(AgeTimelineRoleMixin, self).dispatch(
            request, *args, **kwargs
        )


# return age timeline detail
class SuccessMixim(object):
    def get_success_url(self) -> str:
        return reverse_lazy(
            "age_timelines:age-timeline-detail",
            kwargs={"pk": self.kwargs["age_timeline_id"]},
        )


class AgeTimelineContextMixim:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["age_timeline"] = AgeTimeline.objects.get(
            pk=self.kwargs["age_timeline_id"]
        )
        return context


AGE_EVENT_FIELD_ORDER = [
    "event_area",
    "start_year",
    "start_month",
    "has_end",
    "end_year",
    "end_month",
    "title",
    "description",
    "image",
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
    return age_timeline.timeline_ptr


class AgeEventCreateView(
    LoginRequiredMixin,
    AgeTimelineRoleMixin,
    AgeTimelineContextMixim,
    AgeEventValidateMixim,
    SuccessMixim,
    CreateView,
):
    model = AgeEvent
    fields = AGE_EVENT_FIELD_ORDER
    template_name = "age_timelines/age_event_add_form.html"
    required_role = ROLE_EVENT_EDITOR

    def get_form_class(self):
        modelform = super().get_form_class()
        timeline_id = get_timeline_from_age_timeline(self).pk
        modelform.base_fields["tags"].limit_choices_to = {
            "timeline": timeline_id
        }
        modelform.base_fields["event_area"].limit_choices_to = {
            "timeline": timeline_id
        }

        return modelform


class AgeEventUpdateView(
    LoginRequiredMixin,
    RolePermissionMixin,
    AgeTimelineRoleMixin,
    AgeEventValidateMixim,
    SuccessMixim,
    UpdateView,
):
    model = AgeEvent
    fields = AGE_EVENT_FIELD_ORDER
    template_name = "age_timelines/age_event_edit_form.html"
    required_role = ROLE_EVENT_EDITOR

    def get_form_class(self):
        modelform = super().get_form_class()
        timeline_id = get_timeline_from_age_timeline(self).pk
        modelform.base_fields["tags"].limit_choices_to = {
            "timeline": timeline_id
        }
        modelform.base_fields["event_area"].limit_choices_to = {
            "timeline": timeline_id
        }
        return modelform


class AgeEventDeleteView(
    LoginRequiredMixin,
    RolePermissionMixin,
    AgeTimelineRoleMixin,
    SuccessMixim,
    DeleteView,
):
    model = AgeEvent
    template_name = "age_timelines/age_event_confirm_delete.html"
    required_role = ROLE_EVENT_EDITOR


class TagValidateMixim(object):
    def form_valid(self, form):
        form.instance.timeline_id = get_timeline_from_age_timeline(self).pk

        return super().form_valid(form)


class TagCreateView(
    LoginRequiredMixin,
    AgeTimelineRoleMixin,
    AgeTimelineContextMixim,
    TagValidateMixim,
    SuccessMixim,
    CreateView,
):
    model = Tag
    fields = ["name", "description", "display"]
    template_name = "age_timelines/tag_add_form.html"
    required_role = ROLE_TIMELINE_EDITOR


class TagUpdateView(
    LoginRequiredMixin,
    RolePermissionMixin,
    AgeTimelineRoleMixin,
    TagValidateMixim,
    SuccessMixim,
    UpdateView,
):
    model = Tag
    fields = ["name", "description", "display"]
    template_name = "age_timelines/tag_edit_form.html"
    required_role = ROLE_TIMELINE_EDITOR


class TagDeleteView(
    LoginRequiredMixin,
    RolePermissionMixin,
    AgeTimelineRoleMixin,
    SuccessMixim,
    DeleteView,
):
    model = Tag
    template_name = "age_timelines/tag_confirm_delete.html"
    required_role = ROLE_TIMELINE_EDITOR


class EventAreaValidateMixim(object):
    def form_valid(self, form):
        timeline_ptr = get_timeline_from_age_timeline(self)
        form.instance.timeline_id = timeline_ptr.pk

        # TODO: find a more elegant solution
        area_id = None
        if "pk" in self.kwargs:
            area_id = self.get_object().id

        position_error = event_area_position_error(
            form,
            timeline_ptr,
            area_id,
        )
        if position_error is not None:
            form.add_error("page_position", position_error)

        if form.errors:
            return self.form_invalid(form)
        else:
            return super().form_valid(form)


EVENT_AREA_FIELD_ORDER = [
    "name",
    "page_position",
    "display_event_time",
    "display_event_description",
    "display_event_image",
    "display_event_tags",
    "display_event_to_scale_line",
    "weight",
]


class EventAreaCreateView(
    LoginRequiredMixin,
    AgeTimelineRoleMixin,
    AgeTimelineContextMixim,
    EventAreaValidateMixim,
    SuccessMixim,
    CreateView,
):
    model = EventArea
    fields = EVENT_AREA_FIELD_ORDER
    template_name = "age_timelines/event_area_add_form.html"
    required_role = ROLE_TIMELINE_EDITOR


class EventAreaUpdateView(
    LoginRequiredMixin,
    RolePermissionMixin,
    AgeTimelineRoleMixin,
    EventAreaValidateMixim,
    SuccessMixim,
    UpdateView,
):
    model = EventArea
    fields = EVENT_AREA_FIELD_ORDER
    template_name = "age_timelines/event_area_edit_form.html"
    required_role = ROLE_TIMELINE_EDITOR


class EventAreaDeleteView(
    LoginRequiredMixin,
    RolePermissionMixin,
    AgeTimelineRoleMixin,
    SuccessMixim,
    DeleteView,
):
    model = EventArea
    template_name = "age_timelines/event_area_confirm_delete.html"
    required_role = ROLE_TIMELINE_EDITOR


class CollaboratorsView(
    LoginRequiredMixin,
    RolePermissionMixin,
    DetailView,
):
    model = AgeTimeline
    template_name = "age_timelines/collaborators.html"
    required_role = ROLE_OWNER


class CollaboratorSuccessMixin(object):
    def get_success_url(self) -> str:
        return reverse_lazy(
            "age_timelines:collaborators",
            kwargs={"pk": self.kwargs["age_timeline_id"]},
        )


class CollaboratorCreateView(
    LoginRequiredMixin,
    AgeTimelineRoleMixin,
    AgeTimelineContextMixim,
    CollaboratorSuccessMixin,
    FormView,
):
    form_class = NewCollaboratorForm
    template_name = "age_timelines/collaborator_add.html"
    required_role = ROLE_OWNER

    def form_valid(self, form):
        timeline = get_timeline_from_age_timeline(self)

        user_name = form.cleaned_data.get("user_name")

        try:
            user = User.objects.get(username=user_name)
        except User.DoesNotExist:
            form.add_error("user_name", "User not found.")
            return self.form_invalid(form)

        try:
            collaborator = Collaborator.objects.get(
                timeline=timeline, user=user
            )
        except Collaborator.DoesNotExist:
            collaborator = None

        if collaborator is not None:
            form.add_error(
                "user_name",
                "User already collaborating on this timeline."
            )
            return self.form_invalid(form)
        else:
            if user == self.request.user:
                form.add_error(
                    "user_name",
                    "Cannot add yourself as a collaborator."
                )
                return self.form_invalid(form)

            role = form.cleaned_data.get("role_choice")

            Collaborator.objects.create(
                timeline=timeline,
                user=user,
                role=role,
            )

            return super().form_valid(form)


class CollaboratorUpdateView(
    LoginRequiredMixin,
    RolePermissionMixin,
    AgeTimelineRoleMixin,
    AgeTimelineContextMixim,
    CollaboratorSuccessMixin,
    UpdateView,
):
    model = Collaborator
    fields = ["role"]
    template_name = "age_timelines/collaborator_edit.html"
    required_role = ROLE_OWNER


class CollaboratorDeleteView(
    LoginRequiredMixin,
    RolePermissionMixin,
    AgeTimelineRoleMixin,
    AgeTimelineContextMixim,
    CollaboratorSuccessMixin,
    DeleteView,
):
    model = Collaborator
    template_name = "age_timelines/collaborator_delete.html"
    required_role = ROLE_OWNER


class LandscapeTimelineView(
    LoginRequiredMixin, RolePermissionMixin, DetailView
):
    model = AgeTimeline
    template_name = "age_timelines/landscape_timeline.html"
    required_role = ROLE_VIEWER

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        timeline = self.get_object().get_timeline()
        user_role = timeline.get_role(self.request.user)
        context["user_role"] = user_role
        context["timeline"] = AgeTimelineData(self.get_object())

        return context


class PortraitTimelineView(
    LoginRequiredMixin, RolePermissionMixin, DetailView
):
    model = AgeTimeline
    template_name = "age_timelines/portrait_timeline.html"
    required_role = ROLE_VIEWER

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        timeline = self.get_object().get_timeline()
        user_role = timeline.get_role(self.request.user)
        context["user_role"] = user_role
        context["timeline"] = AgeTimelineData(self.get_object())

        return context


def pdf_view(request, age_timeline_id):
    age_timeline: AgeTimeline = AgeTimeline.objects.get(id=age_timeline_id)

    user_role = age_timeline.get_role(request.user)
    if user_role < ROLE_VIEWER:
        return HttpResponseForbidden()

    timeline_pdf = PDFAgeTimeline(age_timeline)

    return FileResponse(
        timeline_pdf.buffer,
        as_attachment=True,
        filename=get_filename(age_timeline.title),
    )


class AIRequestView(
    LoginRequiredMixin,
    AgeTimelineRoleMixin,
    FormView,
):
    form_class = AIRequestForm
    template_name = "age_timelines/ai_request.html"
    required_role = ROLE_OWNER

    def get(self, request, *args, **kwargs):
        form = self.form_class()

        age_timeline = AgeTimeline.objects.get(
            pk=self.kwargs["age_timeline_id"]
        )

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "view": self,
                "age_timeline": age_timeline,
            }
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
    LoginRequiredMixin,
    AgeTimelineRoleMixin,
    SuccessMixim,
    FormView,
):
    form_class = AIResultsForm
    template_name = "age_timelines/ai_result.html"
    required_role = ROLE_OWNER

    def get_form_kwargs(self):
        kwargs = super(AIResultView, self).get_form_kwargs()
        kwargs["timeline_id"] = get_timeline_from_age_timeline(self).pk
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
        context["age_timeline"] = AgeTimeline.objects.get(
            pk=self.kwargs["age_timeline_id"]
        )

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
