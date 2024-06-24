from django import forms
from django.core.validators import MinValueValidator

from .models import EventArea
from timelines.ai_assist.request_text import StartEndOption

AI_CHOICE = "1"
USER_CHOICE = "2"
AI_USER_DEFINED_CHOICES = (
    (AI_CHOICE, "AI defined"),
    (USER_CHOICE, "User defined"),
)

START_ONLY_CHOICE = "1"
START_END_CHOICE = "2"
START_END_CHOICES = (
    (START_ONLY_CHOICE, "Start only"),
    (START_END_CHOICE, "Start and end if available"),
)

NEW_CHOICE = "1"
EXISTING_CHOICE = "2"
NEW_EXISTING_CHOICES = (
    (NEW_CHOICE, "New"),
    (EXISTING_CHOICE, "Existing"),
)


class AIRequestForm(forms.Form):
    topic = forms.CharField(
        label="Topic",
        help_text="Define the topic for the events to add to your timeline.",
        max_length=100,
    )
    source_choice = forms.ChoiceField(
        widget=forms.RadioSelect,
        label="Source",
        help_text="Choose if you or AI defines the source of the events.",
        choices=AI_USER_DEFINED_CHOICES,
        initial=AI_CHOICE,
    )
    source_text = forms.CharField(
        label="",
        help_text=(
            "Define source URLs using commas to separate multiple URLs."
        ),
        max_length=250,
        required=False,
    )
    event_count_choice = forms.ChoiceField(
        widget=forms.RadioSelect,
        label="Number of Events",
        help_text="Choose if you or AI defines how many events to find.",
        choices=AI_USER_DEFINED_CHOICES,
        initial=AI_CHOICE,
    )
    event_count_text = forms.CharField(
        label="",
        help_text=(
            "Define how many events to find, e.g. 20, at least 10 or about 30."
        ),
        max_length=100,
        required=False,
    )
    start_end_choice = forms.ChoiceField(
        widget=forms.RadioSelect,
        label="Event Start & End time unit",
        help_text=(
            "Create events with a start time unit only or with start and end"
            " time units if that information can be found."
        ),
        choices=START_END_CHOICES,
        initial=START_ONLY_CHOICE,
    )
    title_choice = forms.ChoiceField(
        widget=forms.RadioSelect,
        label="Title Contents",
        help_text="Choose if you or AI defines each event's title contents.",
        choices=AI_USER_DEFINED_CHOICES,
        initial=AI_CHOICE,
    )
    title_text = forms.CharField(
        label="",
        help_text="Define what information each event's title contains.",
        max_length=100,
        required=False,
    )
    description_choice = forms.ChoiceField(
        widget=forms.RadioSelect,
        label="Description Contents",
        help_text=(
            "Choose if you or AI defines each event's description contents."
        ),
        choices=AI_USER_DEFINED_CHOICES,
        initial=AI_CHOICE,
    )
    description_text = forms.CharField(
        label="",
        help_text="Define what information each event's description contains.",
        max_length=100,
        required=False,
    )

    def clean(self):
        cleaned_data = super().clean()

        source_choice = cleaned_data.get("source_choice")
        source_text = cleaned_data.get("source_text")
        if source_choice == USER_CHOICE and source_text == "":
            msg = (
                "When defining the source of the events, this must have a"
                " value."
            )
            self.add_error("source_text", msg)

        event_count_choice = cleaned_data.get("event_count_choice")
        event_count_text = cleaned_data.get("event_count_text")
        if event_count_choice == USER_CHOICE and event_count_text == "":
            msg = (
                "When defining how many events to find, this must have a"
                " value."
            )
            self.add_error("event_count_text", msg)

        title_choice = cleaned_data.get("title_choice")
        title_text = cleaned_data.get("title_text")
        if title_choice == USER_CHOICE and title_text == "":
            msg = (
                "When defining what information each event's title contains,"
                " this must have a value."
            )
            self.add_error("title_text", msg)

        description_choice = cleaned_data.get("description_choice")
        description_text = cleaned_data.get("description_text")
        if description_choice == USER_CHOICE and description_text == "":
            msg = (
                "When defining what information each event's title contains,"
                " this must have a value."
            )
            self.add_error("description_text", msg)

    def get_request_values(self):
        topic = self.cleaned_data["topic"]

        if self.cleaned_data["source_choice"] == USER_CHOICE:
            sources = self.cleaned_data["source_text"]
        else:
            sources = ""

        if self.cleaned_data["event_count_choice"] == USER_CHOICE:
            count_description = self.cleaned_data["event_count_text"]
        else:
            count_description = ""

        if self.cleaned_data["start_end_choice"] == START_ONLY_CHOICE:
            start_end_option = StartEndOption.USE_START_ONLY
        else:
            start_end_option = StartEndOption.USE_END_IF_AVAILABLE

        if self.cleaned_data["title_choice"] == USER_CHOICE:
            title_info = self.cleaned_data["title_text"]
        else:
            title_info = ""

        if self.cleaned_data["description_choice"] == USER_CHOICE:
            description_info = self.cleaned_data["description_text"]
        else:
            description_info = ""

        return (
            topic,
            sources,
            count_description,
            start_end_option,
            title_info,
            description_info,
        )


class AIResultsForm(forms.Form):
    """"""

    event_choice = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        label="Events",
        required=False,
        choices=[],
    )
    select_all_choice = forms.BooleanField(
        label="Select All",
        required=False,
    )
    event_area_choice = forms.ChoiceField(
        widget=forms.RadioSelect,
        label="Event Area",
        help_text="Create a new or use an existing event area.",
        choices=NEW_EXISTING_CHOICES,
        initial=NEW_CHOICE,
    )
    new_event_area_name = forms.CharField(
        label="New Event Area Name",
        max_length=25,
        required=False,
    )
    new_event_area_position = forms.IntegerField(
        label="Page Position",
        initial=0,
        required=False,
        validators=[MinValueValidator(0)],
    )
    new_event_area_weight = forms.IntegerField(
        label="Weight",
        initial=1,
        required=False,
        validators=[MinValueValidator(0)],
    )
    existing_event_area_choice = forms.ModelChoiceField(
        label="Existing Event Area",
        required=False,
        queryset=EventArea.objects.none(),
    )

    def __init__(self, *args, **kwargs):
        self.timeline_id = kwargs.pop("timeline_id")
        events = kwargs.pop("events")
        super(AIResultsForm, self).__init__(*args, **kwargs)

        if self.timeline_id:
            self.fields["existing_event_area_choice"].queryset = (
                EventArea.objects.filter(timeline=self.timeline_id)
            )

        if events:
            self.fields["event_choice"].choices = events

    def clean(self):
        cleaned_data = super().clean()

        selected_events = cleaned_data.get("event_choice")
        if len(selected_events) == 0:
            msg = "At least one event must be selected to add the timeline."
            self.add_error("event_choice", msg)

        event_area_choice = cleaned_data.get("event_area_choice")
        new_event_area_name = cleaned_data.get("new_event_area_name")
        if event_area_choice == NEW_CHOICE and new_event_area_name == "":
            msg = "The new event area must have a name."
            self.add_error("new_event_area_name", msg)

        if event_area_choice == NEW_CHOICE:
            position = int(cleaned_data.get("new_event_area_position"))
            event_areas = EventArea.objects.filter(
                timeline=self.timeline_id,
                page_position=position,
            )
            if event_areas.count() != 0:
                msg = "An event area with this position already exits."
                self.add_error("new_event_area_position", msg)

        existing_event_area_name = cleaned_data.get(
            "existing_event_area_choice"
        )
        if (
            event_area_choice == EXISTING_CHOICE
            and existing_event_area_name is None
        ):
            msg = "An event area must be selected."
            self.add_error("existing_event_area_choice", msg)
