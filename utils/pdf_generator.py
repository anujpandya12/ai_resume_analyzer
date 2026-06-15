from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer

from reportlab.lib.styles import getSampleStyleSheet

from reportlab.platypus import ListFlowable
from reportlab.platypus import ListItem

from reportlab.lib.pagesizes import letter


def generate_pdf_report(
    ats_score,
    match_score,
    skills,
    missing_skills,
    feedback,
    ai_feedback
):

    filename = "static/reports/ats_report.pdf"

    doc = SimpleDocTemplate(
        filename,
        pagesize=letter
    )

    styles = getSampleStyleSheet()

    elements = []

    # Title
    title = Paragraph(
        "AI Resume Analysis Report",
        styles['Title']
    )

    elements.append(title)

    elements.append(Spacer(1, 20))

    # ATS Score
    ats = Paragraph(
        f"<b>ATS Score:</b> {ats_score}/100",
        styles['BodyText']
    )

    elements.append(ats)

    elements.append(Spacer(1, 10))

    # Job Match Score
    match = Paragraph(
        f"<b>Job Match Score:</b> {match_score}%",
        styles['BodyText']
    )

    elements.append(match)

    elements.append(Spacer(1, 20))

    # Skills
    elements.append(
        Paragraph(
            "<b>Detected Skills</b>",
            styles['Heading2']
        )
    )

    skill_items = []

    for skill in skills:

        skill_items.append(
            ListItem(
                Paragraph(skill, styles['BodyText'])
            )
        )

    elements.append(
        ListFlowable(skill_items)
    )

    elements.append(Spacer(1, 20))

    # Missing Skills
    elements.append(
        Paragraph(
            "<b>Missing Skills</b>",
            styles['Heading2']
        )
    )

    missing_items = []

    for skill in missing_skills:

        missing_items.append(
            ListItem(
                Paragraph(skill, styles['BodyText'])
            )
        )

    elements.append(
        ListFlowable(missing_items)
    )

    elements.append(Spacer(1, 20))

    # Feedback
    elements.append(
        Paragraph(
            "<b>Resume Feedback</b>",
            styles['Heading2']
        )
    )

    feedback_items = []

    for item in feedback:

        feedback_items.append(
            ListItem(
                Paragraph(item, styles['BodyText'])
            )
        )

    elements.append(
        ListFlowable(feedback_items)
    )

    elements.append(Spacer(1, 20))

    # AI Suggestions
    elements.append(
        Paragraph(
            "<b>AI Suggestions</b>",
            styles['Heading2']
        )
    )

    ai_items = []

    for item in ai_feedback:

        ai_items.append(
            ListItem(
                Paragraph(item, styles['BodyText'])
            )
        )

    elements.append(
        ListFlowable(ai_items)
    )

    # Build PDF
    doc.build(elements)

    return filename