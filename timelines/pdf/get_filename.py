from django.utils.text import slugify


def get_filename(timeline_title, extension="pdf"):
    slugify_title = slugify(timeline_title)
    if slugify_title != "":
        return f"{slugify_title}.pdf"
    else:
        return "timeline.pdf"
