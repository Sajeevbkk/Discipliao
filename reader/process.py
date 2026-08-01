from reader import helper
from db import db
from random import choices
from datetime import datetime, timedelta, time as time_obj

# for pdf creation
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def process_input():
    if not (day_id := helper.choose_day()): return

    create_table(day_id)

def create_table(day_id):
    if not (times := db.get_times(day_id)): return
    if not (topics := db.get_active_topics_with_priorities()): return

    selected_topics = choices(
        topics,
        [topic[5] + (topic[6] if topic[6] is not None else 0) for topic in topics],
        k=len(times)
    )

    selected_topics = db.get_selected_topics([topic[0] for topic in selected_topics])

    print("Time Table")
    time_table = []
    for time, (topic, chapter, subject) in zip(times, selected_topics):
        # Build start datetime
        start_dt = datetime.combine(datetime.today(), time_obj(time[1], time[2]))
        # Add 25 minutes
        end_dt = start_dt + timedelta(minutes=25)

        # Format both times
        start_str = start_dt.strftime("%I:%M%p")
        end_str = end_dt.strftime("%I:%M%p")

        time_table.append((f"{start_str} - {end_str}", topic, chapter, subject))

    create_pdf(db.get_day(day_id)[1], time_table)

def create_pdf(day, raw_data):
    # Create PDF document
    pdf_file = "time_table.pdf"
    doc = SimpleDocTemplate(pdf_file, pagesize=A4)

    # Styles
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    cell_style = styles["Normal"]  # default for Topic
    center_style = ParagraphStyle(
        name="Center",
        parent=styles["Normal"],
        alignment=1  # 0=left, 1=center, 2=right, 4=justify
    )

    # Title at the top center
    title = Paragraph(f"Time Table (Day: {day})", title_style)

    # Convert to Paragraphs for wrapping
    data = [["TIME", "TOPIC", "CHAPTER", "SUBJECT"]]
    for row in raw_data:
        time, topic, chapter, subject = row
        data.append([
            Paragraph(str(time), cell_style),  # Time
            Paragraph(str(topic), cell_style),  # Topic (Normal style, wraps left/center as you prefer)
            Paragraph(str(chapter), center_style),  # Chapter centered
            Paragraph(str(subject), center_style)  # Subject centered
        ])

    # Create table
    table = Table(data, colWidths=[130, 220, 100, 100])

    # Add table style
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4CAF50")),  # Header background
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),  # Header text color
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 12),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),

        # Center everything
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

        # Explicitly center Chapter and Subject columns
        ("ALIGN", (2, 1), (2, -1), "CENTER"),  # Chapter column
        ("ALIGN", (3, 1), (3, -1), "CENTER"),  # Subject column

        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#E8F5E9")),  # Table body background
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#F1F8E9"), colors.HexColor("#DCEDC8")])
    ]))

    # Build PDF
    elements = [title, Spacer(1, 20), table]
    doc.build(elements)

    print(f"PDF '{pdf_file}' created successfully!")
