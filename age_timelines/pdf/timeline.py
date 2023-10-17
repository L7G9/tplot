import io

from reportlab.lib.colors import black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph

from ..models import AgeTimeline

from .layout import AgeTimelineLayout, SCALE_SIZE
from .scale import PDFScale
from .event import PDFEvent


class PDFTimeline():
    def __init__(self, age_timeline: AgeTimeline):
        self.age_timeline = age_timeline
        self.layout = AgeTimelineLayout(age_timeline)

        self.buffer = io.BytesIO()

        self.canvas = Canvas(
            self.buffer,
            pagesize=(
                self.layout.page_area.width * mm,
                self.layout.page_area.height * mm
            ),
        )

        self.canvas.setStrokeColorRGB(0, 0, 0)

        # draw outlines - used for debugging
        self.canvas.rect(
            self.layout.drawable_area.x * mm,
            self.layout.drawable_area.y * mm,
            self.layout.drawable_area.width * mm,
            self.layout.drawable_area.height * mm,
        )

        # init paragraph styles
        self.title_style = self.get_title_style()
        self.basic_text_style = self.get_basic_style()

        # init timeline title
        self.title_paragraph = self.create_paragraph(
            age_timeline.title,
            self.title_style,
            self.layout.drawable_area.width * mm
        )
        self.layout.define_title_area(self.title_paragraph.height / mm)

        # init timeline description
        self.description_paragraph = self.create_paragraph(
            age_timeline.description,
            self.basic_text_style,
            self.layout.drawable_area.width * mm
        )
        self.layout.define_description_area(self.description_paragraph.height / mm)

        # calculate areas for timeline scale and events
        # get event areas in order of position
        event_areas = age_timeline.eventarea_set.all().order_by("page_position")
        self.init_timeline_area(event_areas)

        self.scale = PDFScale(self.layout, self.canvas)

        self.draw()

        # Close the PDF object cleanly, and we're done.
        self.canvas.showPage()
        self.canvas.save()

        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.
        self.buffer.seek(0)

    def get_title_style(self):
        return ParagraphStyle(
            "Title ParagraphStyle",
            fontName="Times-Roman",
            fontSize=16,
            borderColor=black,
            borderWidth=1,
            leading=22,
        )

    def get_basic_style(self):
        return ParagraphStyle(
            "Basic Text ParagraphStyle",
            fontName="Times-Roman",
            fontSize=10,
            borderColor=black,
            borderWidth=1,
            leading=14,
        )

    def create_paragraph(self, text, style, width) -> Paragraph:
        paragraph = Paragraph(text, style)
        paragraph.wrapOn(self.canvas, width, 0)
        return paragraph

    def get_total_weight(self, event_areas):
        total_weight = 0
        for event_area in event_areas:
            total_weight += event_area.weight
        return total_weight

    def init_timeline_area(self, event_areas):
        # find area available for scale and events
        self.layout.define_timeline_area()

        # calculate available space for events
        total_event_area_height = self.layout.timeline_area.height - SCALE_SIZE

        # get total weight of all event areas
        total_weight = self.get_total_weight(event_areas)

        # calculate height per unit weight
        height_per_weight = total_event_area_height / total_weight

        scale_position_calculated = False
        next_y = self.layout.timeline_area.y

        # calculate areas for scale and event areas
        for event_area in event_areas:
            if (scale_position_calculated is False) and (self.age_timeline.page_scale_position < event_area.page_position):
                self.layout.define_landscape_scale_area(next_y, SCALE_SIZE)
                next_y += SCALE_SIZE
                scale_position_calculated = True

            event_area_height = event_area.weight * height_per_weight
            self.layout.define_landscape_event_area(
                next_y,
                event_area_height,
                event_area
            )
            next_y += event_area_height

        if scale_position_calculated is False:
            self.layout.define_landscape_scale_area(next_y, SCALE_SIZE)

        # draw outlines - used for debugging
        self.canvas.rect(
            self.layout.scale_area.x * mm,
            self.layout.scale_area.y * mm,
            self.layout.scale_area.width * mm,
            self.layout.scale_area.height * mm,
        )

        for event_area in self.layout.event_areas:
            self.canvas.rect(
                event_area.x * mm,
                event_area.y * mm,
                event_area.width * mm,
                event_area.height * mm,
            )

    def draw(self):
        self.title_paragraph.drawOn(
            self.canvas,
            self.layout.title_area.x * mm,
            self.layout.title_area.y * mm
        )

        self.description_paragraph.drawOn(
            self.canvas,
            self.layout.description_area.x * mm,
            self.layout.description_area.y * mm
        )

        self.scale.draw()

    def draw_events(self):
        for area in self.layout.event_areas:
            event_area = area.object
            events = self.age_timeline.ageevent_set.filter(timeline_area=event_area.id)
            for event in events:
                pass
