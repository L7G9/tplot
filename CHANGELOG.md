## 0.8.1 (2024-06-03)

### Fix

- remvoe unsed import
- **pdf_event.py**: remove extra blank line

## 0.8.0 (2024-06-03)

### Feat

- getting started guide added
- added reference guide

### Fix

- joining lines visible through some start end events

### Refactor

- move javascrip into own files

## 0.7.0 (2024-05-21)

### Feat

- 1st version of timeline user guide

### Fix

- add javascript to hide end time units when has end is not checked
- add default value to start date and end date
- update templates to not use pagination
- remove paging from timeline detail views

### Refactor

- add block for additional scripts
- add and use template for structure of user guides
- move trouble shooting into user guide
- remove inclusion of bootstarp 3

## 0.6.5 (2024-05-10)

### Fix

- add link to return to user's timelines or login/register
- **login.html-and-register.html**: update to use new template

## 0.6.4 (2024-05-10)

### Fix

- **event_area_add_form.html**: fix error with breadcrumb back to timeline

## 0.6.3 (2024-05-08)

### Fix

- fix static files

## 0.6.2 (2024-05-08)

### Fix

- **01_django.config**: fix wrong quote marks

## 0.6.1 (2024-05-08)

### Fix

- **01_django.config**: fix error with collectstatic command

## 0.6.0 (2024-05-07)

### Feat

- update ui to use new base template
- **user-guide**: base template created for user guide
- start user_guide app

### Fix

- **01_django.config**: update so static files will be served by ebs

### Refactor

- remove unused imports
- **DateTimeEvent**: add method to get description of event's date & time without title
- **AgeEvent**: add method to get description of event's age without title
- update for consisten order of event areas and tags

## 0.5.0 (2024-04-22)

### Feat

- pagination implemented for events listed in timeline detail templates

## 0.4.1 (2024-04-22)

### Fix

- **DateTimeLineline**: add missing ) to scale unit option

## 0.4.0 (2024-04-18)

### Feat

- added functionality for user to choose format for how datetime are displayed on events and scale

## 0.3.0 (2024-04-17)

### Feat

- date & time timelines added
- **DateTime**: added timeunit sub-class for timelines ordered by the callender date and clock time
- started date and time timeline app

### Fix

- **age_timeline_conform_delete.html**: add missing home link

## 0.2.1 (2024-03-22)

### Fix

- **UI**: updates to make hyperlinks more user friendly

## 0.2.0 (2024-03-22)

### Feat

- **PDFTimeline-&-PDFEvent**: update to use PDFJoiningLines
- **PDFJoiningLines**: add class to draw lines joining the PDFEvents and PDFScale in a PDFTimeline

### Fix

- **PDFAgeTimeline**: fix error where filtering AgeEvent by timeline_area instead of event_area

## 0.1.1 (2024-03-19)

### Fix

- **AgeEventCreateView-&-AgeEventUpdateView**: only display tags and event areas from current timeline

### Refactor

- renamed uses of area & timeline area to event area for consistency

## 0.1.0 (2024-03-19)

### Feat

- **PDFScale**: add plot method
- **pdf_event.py**: add class for event with a start and end
- **PDFEvent**: add orientation
- **AgeTimelinePDF**: use PDFEvent to display events in event areas
- **PDFEvent**: class to display Event on pdf
- timeline scale added generated pdf
- **pfd_view.py**: view that creates a pdf containing graphical representation of timeline
- **layout.py**: class describing pdf timeline layout
- **urls.py**: add url to download timeline pdf
- **age_timeline_detail.html**: add pdf option

### Fix

- **AgeEventCreateView-&-AgeEventUpdateView**: only display tags and event areas from current timeline
- **PDFStartEndEvent**: fix bug where width_increment is set to 0
- **PDFEvent**: fix draw method error
- **PDFEvent**: fix error with max_width not taking into account border_size
- **PDFStartEndEvent**: fix references to _get_dimensions
- **AgeTimelinePDF**: handle case when events run off end of a portrait timeline pdf
- Fix issue where there is not enough room on the pdf's canvas to display events near the end of the timeline

### Refactor

- renamed uses of area & timeline area to event area for consistency
- update to use PDFAgeTimeline
- reworked so can make pdf_timeline for any type of timeline
- increase range of tests Area class can perform
- reworked classes to draw timeline's events
- reworked ScaleDescription
- reworked drawing of timeline scale
- remove unused file
- add class for timeline's unit
- remove unused files
- **TimelineLayout**: update all measurements from mm to canvas units
- breaking into smaller classes

## 0.0.3 (2023-10-05)

### Fix

- use crispy forms

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
- move .github directory to correct location
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
