import io

from django.test import TestCase
from reportlab.lib.colors import black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas

from timelines.pdf.pdf_start_end_event import PDFStartEndEvent

DEFAULT_EVENT_BORDER = 0.5 * mm


class PDFStartEndEventTest(TestCase):
    def __create_canvas(self) -> Canvas:
        buffer = io.BytesIO()
        canvas = Canvas(
            buffer,
            pagesize=(210 * mm, 297 * mm),
        )
        canvas.setStrokeColorRGB(0, 0, 0)
        return canvas

    def __create_paragraph_style(self):
        return ParagraphStyle(
            "Basic Text ParagraphStyle",
            fontName="Times-Roman",
            fontSize=10,
            borderColor=black,
            borderWidth=0,
            leading=14,
        )

    def test_landscape_fits(self):
        canvas = self.__create_canvas()
        paragraph_style = self.__create_paragraph_style()
        fixed_width = 100 * mm

        test_event = PDFStartEndEvent(
            "12 Years 5 Months",
            "event title",
            "event description",
            "L",
            canvas,
            paragraph_style,
            paragraph_style,
            paragraph_style,
            DEFAULT_EVENT_BORDER,
            fixed_width
        )
        self.assertEqual(test_event.width, fixed_width)

    def test_landscape_too_big(self):
        canvas = self.__create_canvas()
        paragraph_style = self.__create_paragraph_style()
        fixed_width = 50 * mm
        max_height = 20 * mm

        test_event = PDFStartEndEvent(
            "12 Years 5 Months",
            "event title",
            "long event description long event description long event description long event description long event description long event description long event description long event description long event description long event description",
            "L",
            canvas,
            paragraph_style,
            paragraph_style,
            paragraph_style,
            DEFAULT_EVENT_BORDER,
            fixed_width
        )
        self.assertEqual(test_event.width, fixed_width)
        self.assertGreater(test_event.height, max_height)

    def test_portrait_fits(self):
        canvas = self.__create_canvas()
        paragraph_style = self.__create_paragraph_style()
        fixed_height = 100 * mm
        max_width = 50 * mm

        test_event = PDFStartEndEvent(
            "12 Years 5 Months",
            "event title",
            "event description",
            "P",
            canvas,
            paragraph_style,
            paragraph_style,
            paragraph_style,
            DEFAULT_EVENT_BORDER,
            fixed_height,
            max_width=max_width
        )
        self.assertLessEqual(test_event.width, max_width)
        self.assertEqual(test_event.height, fixed_height)

    def test_portrait_to_big(self):
        canvas = self.__create_canvas()
        paragraph_style = self.__create_paragraph_style()
        fixed_height = 50 * mm
        max_width = 20 * mm

        test_event = PDFStartEndEvent(
            "12 Years 5 Months",
            "event title",
            "long event description long event description long event description long event description long event description long event description long event description long event description long event description long event description",
            "P",
            canvas,
            paragraph_style,
            paragraph_style,
            paragraph_style,
            DEFAULT_EVENT_BORDER,
            fixed_height,
            max_width=max_width
        )
        self.assertGreater(test_event.width, max_width)
        self.assertEqual(test_event.height, fixed_height)
