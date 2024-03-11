import io

from django.test import TestCase
from reportlab.lib.colors import black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas

from timelines.pdf.pdf_scale_unit_label import PDFScaleUnitLabel

MAX_WIDTH = 20 * mm


class PDFScaleUnitLabelTest(TestCase):
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

    def test_width_under_max(self):
        scale_unit = PDFScaleUnitLabel(
            "20",
            self.__create_paragraph_style(),
            self.__create_canvas(),
            MAX_WIDTH
        )
        self.assertLessEqual(scale_unit.width, MAX_WIDTH)

    def test_width_over_max(self):
        scale_unit = PDFScaleUnitLabel(
            "10 Jan 2024",
            self.__create_paragraph_style(),
            self.__create_canvas(),
            MAX_WIDTH
        )
        self.assertLessEqual(scale_unit.width, MAX_WIDTH)

    def test_set_landscape_position(self):
        scale_unit = PDFScaleUnitLabel(
            "20",
            self.__create_paragraph_style(),
            self.__create_canvas(),
            MAX_WIDTH
        )
        x = 20 * mm
        y = 40 * mm
        scale_unit.set_landscape_position(x, y)

        expected_x = x - (scale_unit.width / 2)
        expected_y = y
        self.assertEqual(scale_unit.x, expected_x)
        self.assertEqual(scale_unit.y, expected_y)

    def test_set_portrait_position(self):
        scale_unit = PDFScaleUnitLabel(
            "20",
            self.__create_paragraph_style(),
            self.__create_canvas(),
            MAX_WIDTH
        )
        x: float = 80 * mm
        y = 15 * mm
        scale_unit.set_portrait_position(x, y)

        expected_x = x - scale_unit.width
        expected_y = y - (scale_unit.height / 2)
        self.assertEqual(scale_unit.x, expected_x)
        self.assertEqual(scale_unit.y, expected_y)
