import io

from reportlab.lib.colors import black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph

from .age_timeline_scale_description import AgeTimelineScaleDescription
from ..models import AgeTimeline
from timelines.pdf.timeline_layout import TimelineLayout
from timelines.pdf.scale_drawer import ScaleDrawer

from timelines.pdf.pdf_scale import PDFScale

class AgeTimelinePDF():
    def __init__(self, age_timeline: AgeTimeline):
        self.age_timeline = age_timeline
        self.layout = TimelineLayout(
            age_timeline,
            AgeTimelineScaleDescription(age_timeline)
        )

        self.buffer = io.BytesIO()

        self.canvas = Canvas(
            self.buffer,
            pagesize=(
                self.layout.page_area.width * mm,
                self.layout.page_area.height * mm
            ),
        )

        self.canvas.setStrokeColorRGB(0, 0, 0)

        # init paragraph styles
        self.title_style = self.get_title_style()
        self.basic_text_style = self.get_basic_style()

        # init timeline title
        self.title_paragraph = self.create_paragraph(
            age_timeline.title,
            self.title_style,
            self.layout.drawable_area.width * mm
        )

        # init timeline description
        self.description_paragraph = self.create_paragraph(
            age_timeline.description,
            self.basic_text_style,
            self.layout.drawable_area.width * mm
        )

        self.layout.create_layout(
            self.title_paragraph.height / mm,
            self.description_paragraph.height / mm,
        )

        self.canvas.setPageSize(
            (
                self.layout.page_area.width * mm,
                self.layout.page_area.height * mm
            )
        )

        # draw outlines - used for debugging
        """
        self.canvas.rect(
            self.layout.drawable_area.x * mm,
            self.layout.drawable_area.y * mm,
            self.layout.drawable_area.width * mm,
            self.layout.drawable_area.height * mm,
        )

        self.canvas.rect(
            self.layout.title_area.x * mm,
            self.layout.title_area.y * mm,
            self.layout.title_area.width * mm,
            self.layout.title_area.height * mm,
        )

        self.canvas.rect(
            self.layout.description_area.x * mm,
            self.layout.description_area.y * mm,
            self.layout.description_area.width * mm,
            self.layout.description_area.height * mm,
        )

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
        """

        # scale_drawer = ScaleDrawer(self.layout, self.canvas)
        # scale_drawer.draw()

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
            self.layout.title_area.x * mm,
            self.layout.title_area.y * mm
        )

        self.description_paragraph.drawOn(
            self.canvas,
            self.layout.description_area.x * mm,
            self.layout.description_area.y * mm
        )

        scale = PDFScale(self.layout.scale_description, self.canvas, self.basic_text_style)
        scale.move(0, 100)
        print(f"page ({self.layout.page_area.width * mm,}, {self.layout.page_area.height * mm}, )")
        print(f"scale ({scale.x}, {scale.y}, {scale.width}, {scale.height})")
        print(f"units ({scale.units.x}, {scale.units.y}, {scale.units.width}, {scale.units.height})")
        print(f"line ({scale.line.x}, {scale.line.y}, {scale.line.width}, {scale.line.height})")
        scale.draw()
