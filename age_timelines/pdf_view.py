import io
from django.http import FileResponse

from reportlab.graphics.shapes import Drawing, Line, String
from reportlab.lib.colors import black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

from .layout import AgeTimelineLayout, BORDER_SIZE
from .models import AgeTimeline


def pdf_view(request, age_timeline_id):
    age_timeline: AgeTimeline = AgeTimeline.objects.get(id=age_timeline_id)
    layout = AgeTimelineLayout(age_timeline)

    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(
        buffer,
        pagesize=(layout.page_area.width * mm, layout.page_area.height * mm),
    )

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.setStrokeColorRGB(0, 0, 0)

    p.rect(
        layout.drawable_area.x * mm,
        layout.drawable_area.y * mm,
        layout.drawable_area.width * mm,
        layout.drawable_area.height * mm,
    )

    # TODO - try paragraph for title and description
    title_style = ParagraphStyle(
        "Title ParagraphStyle",
        fontName="Times-Roman",
        fontSize=16,
        borderColor=black,
        borderWidth=1,
        leading=22,
    )
    title_paragraph = Paragraph(age_timeline.title, title_style)
    title_paragraph.wrapOn(
        p,
        layout.drawable_area.width * mm,
        0
    )
    layout.define_title_area(title_paragraph.height / mm)
    title_paragraph.drawOn(
        p,
        layout.title_area.x * mm,
        layout.title_area.y * mm
    )

    basic_text_style = ParagraphStyle(
        "Basic Text ParagraphStyle",
        fontName="Times-Roman",
        fontSize=10,
        borderColor=black,
        borderWidth=1,
        leading=14,
    )
    description_paragraph = Paragraph(
        age_timeline.description, basic_text_style
    )
    description_paragraph.wrapOn(
        p,
        layout.drawable_area.width * mm,
        0
    )
    layout.define_description_area(description_paragraph.height / mm)
    description_paragraph.drawOn(
        p,
        layout.description_area.x * mm,
        layout.description_area.y * mm
    )

    layout.define_timeline_area()

    # TODO - create own graphical scale object and get height
    # units
    SCALE_SIZE = 6
    UNIT_LINE_LENGTH = 3
    scale_drawing = Drawing(layout.page_area.width * mm, SCALE_SIZE * mm)
    scale_drawing.add(
        Line(
            BORDER_SIZE * mm,
            SCALE_SIZE * mm,
            (BORDER_SIZE + layout.scale_length) * mm,
            SCALE_SIZE * mm
        )
    )

    y_from = SCALE_SIZE * mm
    y_to = (SCALE_SIZE - UNIT_LINE_LENGTH) * mm
    for i in range(layout.scale_units + 1):
        x = ((i * age_timeline.scale_length * 10) + BORDER_SIZE) * mm
        scale_drawing.add(Line(x, y_from, x, y_to))
        label_text = layout.get_scale_label(i)
        label_width = stringWidth(label_text, "Times-Roman", 10)
        center_x = x - (label_width / 2)
        scale_drawing.add(String(center_x, 0, label_text, fontName="Times-Roman", fontSize=10, fillColor=black))

    scale_drawing.drawOn(p, 0, layout.timeline_area.y * mm)

    # TODO - add scale and event areas to timeline area
    # calculate available space for events
    total_event_area_height = layout.timeline_area.height - SCALE_SIZE * mm

    # get event areas in order of position
    event_areas = age_timeline.set_eventarea.all().order_by("page_position").values()

    # get total weight of all event areas
    total_weight = 0
    for event_area in event_areas:
        total_weight += event_area.weight

    # calculate height per unit weight
    height_per_weight = total_event_area_height / total_weight

    scale_position_calculated = False
    next_y = 0
    for event_area in event_areas:
        if scale_position_calculated is False & age_timeline.page_scale_position < event_area.position:
            pass



    # TODO - timeline could have a default event area built in (position and weight stored with Timeline model)
    # if event does no have a specified event area use that
    # TODO - display an event with a start time
    # TODO - display an event with a start and end time
    # TODO - position events in event area

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="timeline.pdf")
