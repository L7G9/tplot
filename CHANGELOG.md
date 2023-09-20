## 0.0.2 (2023-09-20)

### Feat

- **AgeEvent**: add min of -11 and max of 11 to month fields to ensure order by month and year is correct
- **age_timelines**: add title validation to age timeline views
- **age_timelines**: add title and end age validation to age event views
- **age_timelines**: add name validation to tag views
- **age_timelines**: add name validation to tag views
- **age_timelines**: add error checks for area views with empty name fields
- **timelines & age_timelines**: add ordering to tables and prevent a Timeline having Areas with same positions
- **timeline**: add Tag and Area functionality
- **views.py**: only let users who own resources access them
- **OwnerRequiredMixin**: create mixin to check object loaded by from pk in kwargs belongs to logged in user
- **user_timelines**: filter by user
- **urls.py**: add login / path
- **models.py**: add get_owner methods
- add sidebar links
- **AgeTimelineCreateView**: require login and add user to new timeline
- **accounts**: add basic register, login and logout functionality
- **views.py**: update AgeEvent view classes so get_success_url returns age-timeline-detail view
- **age_timelines**: add, update and delete AgeEvents
- add timeline and age_timeline urls
- **age_timelines**: add age_timeline_edit view
- **timelines**: add urls file containing user_timelines url
- **age_timelines**: add urls file containing age_timeline_edit url
- **age_timelines**: add age_timeline_edit template
- **timelines**: add user_timelines template
- **timelines**: add timeline_edit template
- **timelines**: add base template
- **timelines**: add blank=True to not required fields
- **age_timelines**: add description methods for __str__
- **timelines**: add __str__ methods
- **age_timelines**: add AgeTimeline and AgeEvent models
- **age_timeline**: start app
- **timelines**: start app
- **accounts**: start app
- **tplot_site**: start project

### Fix

- **main.yaml**: update database name inline with settings.py
- move .github directory to cortect location
- **views.py**: add missing mixims
- **AgeEventDeleteViewTest**: add missing follow values
- **AgeEventUpdateView**: add AgeTimelineOwnerMixim to ensure user is owner of agetimeline
- **AgeEventDeleteView**: add LoginRequiredMixin
- **AgeEventUpdateView**: add LoginRequiredMixin
- **AgeTimelineDeleteView**: add LoginRequiredMixin so view detects if not logged in and forwards to login page
- **AgeTimelineDetailView**: add LoginRequiredMixin so view detects if not logged in forwards to login page
- **agetimeline_detail.html**: error in age event url
- **age_timeline**: get timeline_id when adding age_event
- **age_timelines**: change models.model to models.Model

### Refactor

- **python_scripts**: move code using same AWS resources into same files
- split terminate_https script in delete_alias and delete_certificate scripts
- **awseb_https**: add directory structure and cli script
- file moved to awseb_https directory
- **setUpTestData**: remove unused variable
- **views.py**: remove unused imports
- **AgeEvent**: remove un-used get_absolute_url
- **timelines**: rename TimelineArea to EventArea
- add crispy forms
- update to use bootstrap 5
- **views.py**: let model validation make sure names ans titles are present
- **timelines**: add present_validation to all title and name fields
- **AreaValidateMixim**: add mixim for this functionality that can be shared by area views
- **timelines**: add common error check functions for views to own file
- **agetimelines**: switch to generic views
