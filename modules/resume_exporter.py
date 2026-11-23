
from io import BytesIO

from docx import Document
from docx.shared import Inches, Pt, RGBColor

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable
)
from xml.sax.saxutils import escape


def clean_resume_text(text):
    """
    Remove the separate Changes Made section
    from the downloadable resume.
    """

    markers = [
        "\nChanges Made",
        "\n## Changes Made",
        "\n**Changes Made**"
    ]

    for marker in markers:
        if marker.lower() in text.lower():
            position = text.lower().find(marker.lower())
            text = text[:position]
            break

    return text.strip()


def create_word_resume(resume_text):

    resume_text = clean_resume_text(resume_text)

    document = Document()

    section = document.sections[0]

    section.top_margin = Inches(0.65)
    section.bottom_margin = Inches(0.65)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)

    styles = document.styles

    normal = styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(10)

    normal.paragraph_format.space_after = Pt(5)

    for line in resume_text.splitlines():

        line = line.strip()

        if not line:
            continue

        clean_line = line.replace("**", "").replace("__", "")

        if clean_line.startswith("# "):

            paragraph = document.add_paragraph()

            paragraph.alignment = 1

            run = paragraph.add_run(
                clean_line[2:]
            )

            run.bold = True
            run.font.size = Pt(19)
            run.font.color.rgb = RGBColor(31, 78, 121)

        elif clean_line.startswith("## "):

            paragraph = document.add_paragraph()

            run = paragraph.add_run(
                clean_line[3:]
            )

            run.bold = True
            run.font.size = Pt(13)
            run.font.color.rgb = RGBColor(31, 78, 121)

        elif clean_line.startswith("### "):

            paragraph = document.add_paragraph()

            run = paragraph.add_run(
                clean_line[4:]
            )

            run.bold = True
            run.font.size = Pt(11)

        elif clean_line.startswith(("- ", "* ", "• ")):

            paragraph = document.add_paragraph(
                style="List Bullet"
            )

            paragraph.add_run(
                clean_line[2:]
            )

        else:

            document.add_paragraph(clean_line)

    output = BytesIO()

    document.save(output)

    output.seek(0)

    return output.getvalue()


def create_pdf_resume(resume_text):

    resume_text = clean_resume_text(resume_text)

    output = BytesIO()

    document = SimpleDocTemplate(
        output,
        pagesize=A4,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.6 * inch,
        bottomMargin=0.6 * inch
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ResumeTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#1F4E79"),
        alignment=TA_CENTER,
        spaceAfter=12
    )

    heading_style = ParagraphStyle(
        "ResumeHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#1F4E79"),
        spaceBefore=10,
        spaceAfter=5
    )

    normal_style = ParagraphStyle(
        "ResumeNormal",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13,
        alignment=TA_LEFT,
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        "ResumeBullet",
        parent=normal_style,
        leftIndent=14,
        firstLineIndent=-8,
        spaceAfter=4
    )

    story = []

    first_heading = True

    for line in resume_text.splitlines():

        line = line.strip()

        if not line:
            story.append(Spacer(1, 3))
            continue

        clean_line = (
            line.replace("**", "")
            .replace("__", "")
        )

        if clean_line.startswith("# "):

            story.append(
                Paragraph(
                    escape(clean_line[2:]),
                    title_style
                )
            )

            first_heading = False

        elif clean_line.startswith("## "):

            story.append(
                Paragraph(
                    escape(clean_line[3:]),
                    heading_style
                )
            )

            story.append(
                HRFlowable(
                    width="100%",
                    thickness=0.5,
                    color=colors.HexColor("#B7C9D6"),
                    spaceAfter=5
                )
            )

        elif clean_line.startswith("### "):

            story.append(
                Paragraph(
                    f"<b>{escape(clean_line[4:])}</b>",
                    normal_style
                )
            )

        elif clean_line.startswith(("- ", "* ", "• ")):

            story.append(
                Paragraph(
                    "&#8226; " + escape(clean_line[2:]),
                    bullet_style
                )
            )

        else:

            story.append(
                Paragraph(
                    escape(clean_line),
                    normal_style
                )
            )

    document.build(story)

    output.seek(0)

    return output.getvalue()
