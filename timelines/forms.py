from django import forms


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
    event_count_choice = forms.ChoiceField(
        widget=forms.RadioSelect,
        label="Number of Events",
        help_text="Choose if you or AI defines how many events to find.",
        choices=AI_USER_DEFINED_CHOICES,
        initial=AI_CHOICE,
    )
    event_count_text = forms.CharField(
        help_text="Define how many events to find, e.g. 20, at least 10 or about 30.",
        max_length=100,
        required=False,
    )
    start_end_choice = forms.ChoiceField(
        widget=forms.RadioSelect,
        label="Event Start & End time unit",
        help_text="Create events with a start time unit only or with start and end time units if that information can be found.",
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
        help_text="Define what information each event's title contains.",
        max_length=100,
        required=False,
    )
    description_choice = forms.ChoiceField(
        widget=forms.RadioSelect,
        label="Description Contents",
        help_text="Choose if you or AI defines each event's description contents.",
        choices=AI_USER_DEFINED_CHOICES,
        initial=AI_CHOICE,
    )
    description_text = forms.CharField(
        help_text="Define what information each event's description contains.",
        max_length=100,
        required=False,
    )
