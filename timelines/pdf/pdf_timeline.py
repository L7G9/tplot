"""Contains class to create a PDF of a timeline.

Classes:
    PDFTimeline
"""

import io
from abc import ABC, abstractmethod
from typing import List, Union

from reportlab.lib.colors import black
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph

from timelines.models import Event, EventArea, Timeline
from timelines.pdf.inside import Inside
from timelines.pdf.pdf_event import PDFEvent
from timelines.pdf.pdf_scale import PDFScale
from timelines.pdf.pdf_start_end_event import PDFStartEndEvent
from timelines.pdf.pdf_timeline_layout import PDFTimelineLayout
from timelines.pdf.scale_description import ScaleDescription

from .pdf_event_area import PDFEventArea


class PDFTimeline(ABC):
    """An abstract Class to draw a Timeline on a PDF.

    Should be inherited by a class to draw a specific type of timeline
    such as PDFAgeTimeline for an AgeTimeline instance.  This classes
    abstract methods should be implemented for that type of timeline
    and it's events.

    Attributes:
        timeline: An instance of a sub-class of Timeline.
        layout: A PDFTimelineLayout instance describing all the graphics
        elements all the timeline to draw on the PDF.
        buffer: ???
        canvas: A Canvas instance to draw the timeline on.
        title_style: A ParagraphStyle instance to use for the title.
        basic_text_style: A ParagraphStyle instance to use for all other text
        on the timeline.
        scale_description: An instance of a sub-class of ScaleDescription.
        scale: A PDFScale instance to draw on the timeline scale.
        title_paragraph: A Paragraph instance to draw the timeline title.
        description_paragraph: A Paragraph instance to draw the timeline
        description.
    """

    def __init__(self, timeline: Timeline):
        """Initialise Instance.

        Creates an initial PDF to to measure the size of the timeline's
        graphical elements on.

        Creates graphical title, description and scale objects that given to
        the a layout instance which uses their dimensions to decide how to
        arrange all the graphical elements of the timeline on the PDF.

        Updates the size of the PDF inline with the layout and draws all the
        graphical elements of the timeline on the PDF.

        Args:
            timeline: An instance of a sub-class of Timeline.
        """
        self.timeline = timeline
        self.layout = PDFTimelineLayout(timeline)

        # create initial canvas
        self.buffer = io.BytesIO()
        self.canvas = Canvas(
            self.buffer,
            pagesize=(
                self.layout.page_area.width,
                self.layout.page_area.height,
            ),
        )
        self.canvas.setStrokeColorRGB(0, 0, 0)

        # init fonts
        self.title_style = self.__create_title_style()
        self.basic_text_style = self.__create_basic_style()

        # init scale
        self.scale_description = self._create_scale_description(timeline)
        self.scale = PDFScale(
            self.scale_description, self.canvas, self.basic_text_style
        )

        # init title & description
        self.title_paragraph = self.__create_paragraph(
            str(timeline.title), self.title_style
        )
        self.description_paragraph = self.__create_paragraph(
            str(timeline.description), self.basic_text_style
        )

        # update layout using dimensions of title, description & scale
        self.layout.set_dimensions(
            self.title_paragraph.height,
            self.description_paragraph.height,
            self.scale.width,
            self.scale.height,
        )
        self.scale.move(self.layout.scale_area.x, self.layout.scale_area.y)

        # add events to event areas
        overlap = self.__add_events()

        # update layout if any events go over the edge of their event areas
        if overlap > 0:
            self.layout.expand_event_overlap(overlap)
            self.scale.move(self.layout.scale_area.x, self.layout.scale_area.y)

        # set final page size & draw
        self.canvas.setPageSize(
            (self.layout.page_area.width, self.layout.page_area.height)
        )
        self.__draw()

        # close the PDF object
        self.canvas.showPage()
        self.canvas.save()

        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.
        self.buffer.seek(0)

    @abstractmethod
    def _create_scale_description(
        self, timeline: Timeline
    ) -> ScaleDescription:
        """Creates a ScaleDescription from a Timeline.  Returned object will be
        the subclass of ScaleDescription specific to the type of timeline, eg
        AgeTimelineScaleDescription for AgeTimeline."""
        raise NotImplementedError("Subclasses should implement this")

    @abstractmethod
    def _get_events(self, event_area_id: int) -> List[Event]:
        """Gets list of all Events in an EventArea.  Objects in list will be
        the subclass of Event specific to the type of timeline, eg AgeEvent
        for AgeTimeline."""
        raise NotImplementedError("Subclasses should implement this")

    @abstractmethod
    def _get_event_start_time(self, event: Event) -> str:
        """Gets description of Event's time when it has no end time."""
        raise NotImplementedError("Subclasses should implement this")

    @abstractmethod
    def _get_event_start_to_end_time(self, event: Event) -> str:
        """Gets description of Event's time when it has an end time."""
        raise NotImplementedError("Subclasses should implement this")

    @abstractmethod
    def _get_event_start_to_end_size(self, event: Event) -> float:
        """Gets size (length or height depending of orientation) that an
        PDFEvent should be on the pdf when it has has an end time."""
        raise NotImplementedError("Subclasses should implement this")

    @abstractmethod
    def _plot_event(self, event: Event, pdf_event: PDFEvent) -> float:
        """Gets the position (x or y coordinate depending on orientation) that
        an PDFEvent should be on the pdf relative to the start of it's
        PDFEventArea."""
        raise NotImplementedError("Subclasses should implement this")

    def __create_paragraph(
        self, text: str, style: ParagraphStyle
    ) -> Paragraph:
        """Creates a paragraph to wide enough for the title or description."""
        paragraph = Paragraph(text, style)
        paragraph.wrapOn(self.canvas, self.layout.drawable_area.width, 0)
        return paragraph

    def __create_pdf_event(
        self, event: Event, pdf_event_area: PDFEventArea
    ) -> PDFEvent:
        """Creates a PDFEvent of a size and layout suitable for it's Event,
        PDFEventArea and Timeline."""
        if event.has_end:
            return PDFStartEndEvent(
                self._get_event_start_to_end_time(event),
                str(event.title),
                str(event.description),
                str(self.timeline.page_orientation),
                self.canvas,
                self.basic_text_style,
                self.basic_text_style,
                self.basic_text_style,
                self.layout.event_border,
                self._get_event_start_to_end_size(event),
                pdf_event_area.width,
                pdf_event_area.height,
            )
        else:
            return PDFEvent(
                self._get_event_start_time(event),
                str(event.title),
                str(event.description),
                str(self.timeline.page_orientation),
                self.canvas,
                self.basic_text_style,
                self.basic_text_style,
                self.basic_text_style,
                self.layout.event_border,
                pdf_event_area.width,
                pdf_event_area.height,
            )

    def __add_events(self) -> float:
        """Creates PDFEvent objects for each Event object in a Timeline, then
        positions and adds it to it's PDFEventArea. Checks to see if any of
        PDFEvents overlap the expandable side of it's PDFEventArea and returns
        the largest overlap."""
        max_overlap = 0
        for pdf_event_area in self.layout.event_areas:
            event_area: EventArea = pdf_event_area.event_area
            events: List[Event] = self._get_events(event_area.id)

            for event in events:
                pdf_event: PDFEvent = self.__create_pdf_event(
                    event,
                    pdf_event_area
                )
                coordinates = self.__get_event_position(
                    event, pdf_event, pdf_event_area
                )
                if coordinates is not None:
                    pdf_event.x, pdf_event.y = coordinates

                # todo - handle case were coordinates is none

                pdf_event_area.events.append(pdf_event)

                # todo - handle case where event is too big to fit event area
                overlap = self.__get_event_overlap(pdf_event, pdf_event_area)
                if overlap > max_overlap:
                    max_overlap = overlap

        return max_overlap

    def __get_event_position(
        self, event: Event, pdf_event: PDFEvent, pdf_event_area: PDFEventArea
    ) -> Union[tuple[float, float], None]:
        """Get the best position for pdf_event in pdf_event_area."""
        # find preferred position of pdf_event from start of pdf_event_area
        event_position = self._plot_event(event, pdf_event)

        # place pdf_event in preferred position then get best position making
        # sure it does not overlap any other PDFEvents or any part of it's
        # PDFEventArea which cannot be expanded
        if self.timeline.page_orientation == "L":
            pdf_event.x = event_position
            return pdf_event_area.get_landscape_position(pdf_event, True, True)
        else:
            pdf_event.y = event_position
            return pdf_event_area.get_portrait_position(pdf_event, True, True)

    def __get_event_overlap(
        self, pdf_event: PDFEvent, pdf_event_area: PDFEventArea
    ) -> float:
        """Get how much pdf_event overlaps the expandable side (right for
        landscape and bottom for portrait) of pdf_event_area."""
        inside_event_area = Inside(pdf_event, pdf_event_area)
        if self.timeline.page_orientation == "L":
            if inside_event_area.test(right_inside=False):
                return abs(pdf_event.right() - pdf_event_area.width)
        else:
            if inside_event_area.test(bottom_inside=False):
                return abs(pdf_event.y)

        return 0

    def __draw(self):
        """Draw all the graphical elements of the timeline on the PDF."""
        self.title_paragraph.drawOn(
            self.canvas,
            self.layout.title_area.x,
            self.layout.title_area.y,
        )

        self.description_paragraph.drawOn(
            self.canvas,
            self.layout.description_area.x,
            self.layout.description_area.y,
        )

        self.scale.draw()

        for pdf_event_area in self.layout.event_areas:
            self.canvas.saveState()
            self.canvas.translate(pdf_event_area.x, pdf_event_area.y)

            for pdf_event in pdf_event_area.events:
                pdf_event.draw()

            self.canvas.restoreState()

    def __create_title_style(self) -> ParagraphStyle:
        """Create a paragraph style for the timeline's title."""
        return ParagraphStyle(
            "Title ParagraphStyle",
            fontName="Times-Roman",
            fontSize=16,
            borderColor=black,
            borderWidth=0,
            leading=22,
        )

    def __create_basic_style(self) -> ParagraphStyle:
        """Create a general paragraph style for the timeline's text."""
        return ParagraphStyle(
            "Basic Text ParagraphStyle",
            fontName="Times-Roman",
            fontSize=10,
            borderColor=black,
            borderWidth=0,
            leading=14,
        )
