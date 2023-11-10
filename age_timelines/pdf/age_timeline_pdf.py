import io

from reportlab.lib.colors import black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph

from .age import Age
from .age_timeline_scale_description import AgeTimelineScaleDescription
from ..models import AgeTimeline, AgeEvent

from timelines.pdf.timeline_layout import TimelineLayout
from timelines.pdf.pdf_event import PDFEvent
from timelines.pdf.pdf_scale import PDFScale


class AgeTimelinePDF:
    def __init__(self, age_timeline: AgeTimeline):
        self.age_timeline = age_timeline
        self.layout = TimelineLayout(age_timeline)
        self.scale_description = AgeTimelineScaleDescription(age_timeline)

        self.buffer = io.BytesIO()

        self.canvas = Canvas(
            self.buffer,
            pagesize=(
                self.layout.page_area.width,
                self.layout.page_area.height,
            ),
        )

        self.canvas.setStrokeColorRGB(0, 0, 0)

        self.title_style = self.get_title_style()
        self.basic_text_style = self.get_basic_style()

        self.scale = PDFScale(
            self.scale_description, self.canvas, self.basic_text_style
        )

        if age_timeline.page_orientation == "L":
            self.title_paragraph = self.create_paragraph(
                age_timeline.title,
                self.title_style,
                self.scale.width,
            )
            self.description_paragraph = self.create_paragraph(
                age_timeline.description,
                self.basic_text_style,
                self.scale.width,
            )
        else:
            self.title_paragraph = self.create_paragraph(
                age_timeline.title,
                self.title_style,
                self.layout.drawable_area.width,
            )
            self.description_paragraph = self.create_paragraph(
                age_timeline.description,
                self.basic_text_style,
                self.layout.drawable_area.width,
            )

        self.layout.create_layout(
            self.title_paragraph.height,
            self.description_paragraph.height,
            self.scale.width,
            self.scale.height,
        )

        self.scale.move(self.layout.scale_area.x, self.layout.scale_area.y)

        for pdf_event_area in self.layout.event_areas:
            event_area = pdf_event_area.object
            events = AgeEvent.objects.filter(timeline_area=event_area.id)
            print(f"event area {event_area.name} contains...")
            for event in events:
                print(f"{event.title}")
                # create event at start of event area
                age = Age(event.start_year, event.start_month)
                pdf_event = PDFEvent(
                    str(age),
                    event.title,
                    event.description,
                    self.canvas,
                    self.basic_text_style,
                    self.basic_text_style,
                    self.basic_text_style,
                    pdf_event_area.width,
                    pdf_event_area.height
                )
                pdf_event_area.children.append(pdf_event)

                # display in correct position in event area
                # display checking for overlaps with other events in event area


        self.canvas.setPageSize(
            (self.layout.page_area.width, self.layout.page_area.height)
        )

        # draw outlines - used for debugging
        self.canvas.rect(
            self.layout.drawable_area.x,
            self.layout.drawable_area.y,
            self.layout.drawable_area.width,
            self.layout.drawable_area.height,
        )

        self.canvas.rect(
            self.layout.title_area.x,
            self.layout.title_area.y,
            self.layout.title_area.width,
            self.layout.title_area.height,
        )

        self.canvas.rect(
            self.layout.description_area.x,
            self.layout.description_area.y,
            self.layout.description_area.width,
            self.layout.description_area.height,
        )

        self.canvas.rect(
            self.layout.scale_area.x,
            self.layout.scale_area.y,
            self.layout.scale_area.width,
            self.layout.scale_area.height,
        )

        for event_area in self.layout.event_areas:
            self.canvas.rect(
                event_area.x,
                event_area.y,
                event_area.width,
                event_area.height,
            )

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

    def draw(self):
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

            for pdf_event in pdf_event_area.children:
                pdf_event.draw()

            self.canvas.restoreState()
