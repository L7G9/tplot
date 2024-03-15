import io

from django.test import TestCase
from reportlab.lib.colors import black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas

from timelines.pdf.pdf_event import PDFEvent

DEFAULT_EVENT_BORDER = 0.5 * mm
LARGE_STRING = (
    "large amount of text - large amount of text -"
    "large amount of text - large amount of text -"
    "large amount of text - large amount of text -"
    "large amount of text - large amount of text"
)
VERY_LARGE_STRING = (
    "large amount of text - large amount of text -"
    "large amount of text - large amount of text -"
    "large amount of text - large amount of text -"
    "large amount of text - large amount of text -"
    "large amount of text - large amount of text -"
    "large amount of text - large amount of text -"
    "large amount of text - large amount of text -"
    "large amount of text - large amount of text"
)


class PDFEventTest(TestCase):
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

    def test_landscape_fit_to_time(self):
        canvas = self.__create_canvas()
        paragraph_style = self.__create_paragraph_style()
        max_height = 100 * mm

        test_event = PDFEvent(
            "12 Years 5 Months",
            "small",
            "",
            "L",
            canvas,
            paragraph_style,
            paragraph_style,
            paragraph_style,
            DEFAULT_EVENT_BORDER,
            max_height=max_height,
        )

        self.assertTrue(test_event.sized_to_min_width)
        self.assertGreaterEqual(test_event.width, test_event.min_width)
        self.assertLessEqual(test_event.height, max_height)

    def test_landscape_fit_to_ratio(self):
        canvas = self.__create_canvas()
        paragraph_style = self.__create_paragraph_style()
        max_height = 100 * mm

        test_event = PDFEvent(
            "12 Years 5 Months",
            LARGE_STRING,
            LARGE_STRING,
            "L",
            canvas,
            paragraph_style,
            paragraph_style,
            paragraph_style,
            DEFAULT_EVENT_BORDER,
            max_height=max_height,
        )

        self.assertTrue(test_event.sized_to_ratio)
        self.assertGreaterEqual(test_event.width, test_event.min_width)
        self.assertLessEqual(test_event.height, max_height)

    def test_landscape_fit_to_max_height(self):
        canvas = self.__create_canvas()
        paragraph_style = self.__create_paragraph_style()
        max_height = 30 * mm

        test_event = PDFEvent(
            "12 Years 5 Months",
            LARGE_STRING,
            LARGE_STRING,
            "L",
            canvas,
            paragraph_style,
            paragraph_style,
            paragraph_style,
            DEFAULT_EVENT_BORDER,
            max_height=max_height,
        )

        self.assertTrue(test_event.sized_to_max_height)
        self.assertGreaterEqual(test_event.width, test_event.min_width)
        self.assertLessEqual(test_event.height, max_height)

    def test_portrait_fit_to_time(self):
        canvas = self.__create_canvas()
        paragraph_style = self.__create_paragraph_style()
        max_width = 300 * mm

        test_event = PDFEvent(
            "12 Years 5 Months",
            "small",
            "",
            "P",
            canvas,
            paragraph_style,
            paragraph_style,
            paragraph_style,
            DEFAULT_EVENT_BORDER,
            max_width=max_width,
        )

        self.assertTrue(test_event.sized_to_min_width)
        self.assertGreaterEqual(test_event.width, test_event.min_width)
        self.assertLessEqual(test_event.width, max_width)

    def test_portrait_fit_to_ratio(self):
        canvas = self.__create_canvas()
        paragraph_style = self.__create_paragraph_style()
        max_width = 100 * mm

        test_event = PDFEvent(
            "12 Years 5 Months",
            LARGE_STRING,
            LARGE_STRING,
            "P",
            canvas,
            paragraph_style,
            paragraph_style,
            paragraph_style,
            DEFAULT_EVENT_BORDER,
            max_width=max_width,
        )

        self.assertTrue(test_event.sized_to_ratio)
        self.assertGreaterEqual(test_event.width, test_event.min_width)
        self.assertLessEqual(test_event.width, max_width)

    def test_portrait_fit_to_max_width(self):
        canvas = self.__create_canvas()
        paragraph_style = self.__create_paragraph_style()
        max_width = 30 * mm

        test_event = PDFEvent(
            "12 Years 5 Months",
            LARGE_STRING,
            VERY_LARGE_STRING,
            "P",
            canvas,
            paragraph_style,
            paragraph_style,
            paragraph_style,
            DEFAULT_EVENT_BORDER,
            max_width=max_width,
        )

        self.assertTrue(test_event.sized_to_max_width)
        self.assertGreaterEqual(test_event.width, test_event.min_width)
        self.assertLessEqual(test_event.width, max_width)
