from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import FileResponse, HttpResponseForbidden
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView, DeleteView, FormView, UpdateView,
)

from timelines.forms import NewCollaboratorForm
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

from .models import ScientificEvent, ScientificTimeline
from .pdf.pdf_scientific_timeline import PDFScientificTimeline
from .view_data.scientific_timeline_data import ScientificTimelineData


TIMELINE_FIELD_ORDER = [
    "title",
    "description",
    "scale_unit",
    "scale_unit_length",
    "pdf_page_size",
    "page_orientation",
    "page_scale_position",
    "pdf_page_size",
]


class TimelineDetailView(
    LoginRequiredMixin, RolePermissionMixin, RoleContextMixin, DetailView
):
    model = ScientificTimeline
    template_name = "scientific_timelines/timeline_detail.html"
    required_role = ROLE_VIEWER


class TimelineCreateView(LoginRequiredMixin, CreateView):
    model = ScientificTimeline
    fields = TIMELINE_FIELD_ORDER
    template_name = "scientific_timelines/timeline_add.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TimelineUpdateView(
    LoginRequiredMixin,
    RolePermissionMixin,
    RoleContextMixin,
    UpdateView
):
    model = ScientificTimeline
    fields = TIMELINE_FIELD_ORDER
    template_name = "scientific_timelines/timeline_edit.html"
    required_role = ROLE_TIMELINE_EDITOR


class TimelineDeleteView(
    LoginRequiredMixin,
    RolePermissionMixin,
    DeleteView
):
    model = ScientificTimeline
    template_name = "scientific_timelines/timeline_delete.html"
    success_url = reverse_lazy("timelines:user-timelines")
    required_role = ROLE_OWNER


class TimelineRoleMixin(object):
    def dispatch(self, request, *args, **kwargs):
        timeline = ScientificTimeline.objects.get(
            pk=self.kwargs["scientific_timeline_id"]
        )
        user_role = (
            timeline.get_role(self.request.user)
        )
        if user_role < self.required_role:
            return HttpResponseForbidden()
        return super(TimelineRoleMixin, self).dispatch(
            request, *args, **kwargs
        )


# return scientific timeline detail
class SuccessMixim(object):
    def get_success_url(self) -> str:
        return reverse_lazy(
            "scientific_timelines:timeline-detail",
            kwargs={"pk": self.kwargs["scientific_timeline_id"]},
        )


class ScientificTimelineContextMixim:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["scientific_timeline"] = ScientificTimeline.objects.get(
            pk=self.kwargs["scientific_timeline_id"]
        )
        return context


EVENT_FIELD_ORDER = [
    "event_area",
    "start_year_fraction",
    "start_multiplier",
    "has_end",
    "end_year_fraction",
    "end_multiplier",
    "title",
    "description",
    "image",
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
    return scientific_timeline.timeline_ptr


class EventCreateView(
    LoginRequiredMixin,
    TimelineRoleMixin,
    ScientificTimelineContextMixim,
    EventValidateMixim,
    SuccessMixim,
    CreateView,
):
    model = ScientificEvent
    fields = EVENT_FIELD_ORDER
    template_name = "scientific_timelines/event_add.html"
    required_role = ROLE_EVENT_EDITOR

    def get_form_class(self):
        modelform = super().get_form_class()
        timeline_id = get_timeline_from_scientific_timeline(self).pk
        modelform.base_fields["tags"].limit_choices_to = {
            "timeline": timeline_id
        }
        modelform.base_fields["event_area"].limit_choices_to = {
            "timeline": timeline_id
        }
        return modelform


class EventUpdateView(
    LoginRequiredMixin,
    RolePermissionMixin,
    TimelineRoleMixin,
    EventValidateMixim,
    SuccessMixim,
    UpdateView,
):
    model = ScientificEvent
    fields = EVENT_FIELD_ORDER
    template_name = "scientific_timelines/event_edit.html"
    required_role = ROLE_EVENT_EDITOR

    def get_form_class(self):
        modelform = super().get_form_class()
        timeline_id = get_timeline_from_scientific_timeline(self).pk
        modelform.base_fields["tags"].limit_choices_to = {
            "timeline": timeline_id
        }
        modelform.base_fields["event_area"].limit_choices_to = {
            "timeline": timeline_id
        }
        return modelform


class EventDeleteView(
    LoginRequiredMixin,
    RolePermissionMixin,
    TimelineRoleMixin,
    SuccessMixim,
    DeleteView,
):
    model = ScientificEvent
    template_name = "scientific_timelines/event_delete.html"
    required_role = ROLE_EVENT_EDITOR


class TagValidateMixim(object):
    def form_valid(self, form):
        form.instance.timeline_id = (
            get_timeline_from_scientific_timeline(self).pk
        )
        return super().form_valid(form)


class TagCreateView(
    LoginRequiredMixin,
    TimelineRoleMixin,
    ScientificTimelineContextMixim,
    TagValidateMixim,
    SuccessMixim,
    CreateView,
):
    model = Tag
    fields = ["name", "description", "display"]
    template_name = "scientific_timelines/tag_add.html"
    required_role = ROLE_TIMELINE_EDITOR


class TagUpdateView(
    LoginRequiredMixin,
    RolePermissionMixin,
    TimelineRoleMixin,
    TagValidateMixim,
    SuccessMixim,
    UpdateView,
):
    model = Tag
    fields = ["name", "description", "display"]
    template_name = "scientific_timelines/tag_edit.html"
    required_role = ROLE_TIMELINE_EDITOR


class TagDeleteView(
    LoginRequiredMixin,
    RolePermissionMixin,
    TimelineRoleMixin,
    SuccessMixim,
    DeleteView,
):
    model = Tag
    template_name = "scientific_timelines/tag_delete.html"
    required_role = ROLE_TIMELINE_EDITOR


class EventAreaValidateMixim(object):
    def form_valid(self, form):
        timeline_ptr = get_timeline_from_scientific_timeline(self)
        form.instance.timeline_id = timeline_ptr.pk

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


class EventAreaCreateView(
    LoginRequiredMixin,
    TimelineRoleMixin,
    ScientificTimelineContextMixim,
    EventAreaValidateMixim,
    SuccessMixim,
    CreateView,
):
    model = EventArea
    fields = ["name", "page_position", "weight"]
    template_name = "scientific_timelines/event_area_add.html"
    required_role = ROLE_TIMELINE_EDITOR


class EventAreaUpdateView(
    LoginRequiredMixin,
    RolePermissionMixin,
    TimelineRoleMixin,
    EventAreaValidateMixim,
    SuccessMixim,
    UpdateView,
):
    model = EventArea
    fields = ["name", "page_position", "weight"]
    template_name = "scientific_timelines/event_area_edit.html"
    required_role = ROLE_TIMELINE_EDITOR


class EventAreaDeleteView(
    LoginRequiredMixin,
    RolePermissionMixin,
    TimelineRoleMixin,
    SuccessMixim,
    DeleteView,
):
    model = EventArea
    template_name = "scientific_timelines/event_area_delete.html"
    required_role = ROLE_TIMELINE_EDITOR


class CollaboratorsView(
    LoginRequiredMixin,
    RolePermissionMixin,
    DetailView,
):
    model = ScientificTimeline
    template_name = "scientific_timelines/collaborators.html"
    required_role = ROLE_OWNER


class CollaboratorSuccessMixin(object):
    def get_success_url(self) -> str:
        return reverse_lazy(
            "scientific_timelines:collaborators",
            kwargs={"pk": self.kwargs["scientific_timeline_id"]},
        )


class CollaboratorCreateView(
    LoginRequiredMixin,
    TimelineRoleMixin,
    ScientificTimelineContextMixim,
    CollaboratorSuccessMixin,
    FormView,
):
    form_class = NewCollaboratorForm
    template_name = "scientific_timelines/collaborator_add.html"
    required_role = ROLE_OWNER

    def form_valid(self, form):
        timeline = get_timeline_from_scientific_timeline(self)

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
    TimelineRoleMixin,
    ScientificTimelineContextMixim,
    CollaboratorSuccessMixin,
    UpdateView,
):
    model = Collaborator
    fields = ["role"]
    template_name = "scientific_timelines/collaborator_edit.html"
    required_role = ROLE_OWNER


class CollaboratorDeleteView(
    LoginRequiredMixin,
    RolePermissionMixin,
    TimelineRoleMixin,
    ScientificTimelineContextMixim,
    CollaboratorSuccessMixin,
    DeleteView,
):
    model = Collaborator
    template_name = "scientific_timelines/collaborator_delete.html"
    required_role = ROLE_OWNER


class LandscapeTimelineView(
    LoginRequiredMixin, RolePermissionMixin, DetailView
):
    model = ScientificTimeline
    template_name = "scientific_timelines/landscape_timeline.html"
    required_role = ROLE_VIEWER

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        timeline = self.get_object().get_timeline()
        user_role = timeline.get_role(self.request.user)
        context["user_role"] = user_role
        context["timeline"] = ScientificTimelineData(self.get_object())

        return context


class PortraitTimelineView(
    LoginRequiredMixin, RolePermissionMixin, DetailView
):
    model = ScientificTimeline
    template_name = "scientific_timelines/portrait_timeline.html"
    required_role = ROLE_VIEWER

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        timeline = self.get_object().get_timeline()
        user_role = timeline.get_role(self.request.user)
        context["user_role"] = user_role
        context["timeline"] = ScientificTimelineData(self.get_object())

        return context


def pdf_view(request, scientific_timeline_id):
    scientific_timeline: ScientificTimeline = ScientificTimeline.objects.get(
        id=scientific_timeline_id
    )

    user_role = scientific_timeline.get_role(request.user)
    if user_role < ROLE_VIEWER:
        return HttpResponseForbidden()

    timeline_pdf = PDFScientificTimeline(scientific_timeline)

    return FileResponse(
        timeline_pdf.buffer,
        as_attachment=True,
        filename=get_filename(scientific_timeline.title),
    )
