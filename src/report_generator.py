
from io import BytesIO
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


def generate_pdf_report(soil_data, predicted_crop):
    """Create a downloadable PDF soil analysis report in memory."""

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
    )

    styles = getSampleStyleSheet()
    content = []

    content.append(
        Paragraph("SoilSense AI", styles["Title"])
    )
    content.append(
        Paragraph(
            "Soil Test Analysis and Crop Recommendation Report",
            styles["Heading2"],
        )
    )
    content.append(
        Paragraph(
            f"Generated on: {datetime.now().strftime('%d %B %Y, %I:%M %p')}",
            styles["Normal"],
        )
    )
    content.append(Spacer(1, 18))

    content.append(
        Paragraph("1. Soil Measurements", styles["Heading2"])
    )

    table_data = [
        ["Parameter", "Value"],
        ["Nitrogen (N)", str(soil_data["N"])],
        ["Phosphorus (P)", str(soil_data["P"])],
        ["Potassium (K)", str(soil_data["K"])],
        ["Soil pH", str(soil_data["ph"])],
        ["Temperature (°C)", str(soil_data["temperature"])],
        ["Humidity (%)", str(soil_data["humidity"])],
        ["Rainfall (mm)", str(soil_data["rainfall"])],
    ]

    table = Table(table_data, colWidths=[8 * cm, 7 * cm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.darkgreen),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("PADDING", (0, 0), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )

    content.append(table)
    content.append(Spacer(1, 20))

    content.append(
        Paragraph("2. Crop Recommendation", styles["Heading2"])
    )
    content.append(
        Paragraph(
            f"Predicted crop: <b>{predicted_crop.title()}</b>",
            styles["Normal"],
        )
    )
    content.append(Spacer(1, 12))

    content.append(
        Paragraph("3. Important Disclaimer", styles["Heading2"])
    )
    content.append(
        Paragraph(
            "This prediction is based on a machine learning model and its "
            "training dataset. It is not a guarantee of crop suitability, "
            "yield, or profitability. Confirm the soil measurements, "
            "regional climate, season, and crop suitability with local "
            "agricultural experts before making farming decisions.",
            styles["Normal"],
        )
    )

    document.build(content)

    pdf_bytes = buffer.getvalue()
    buffer.close()

    return pdf_bytes
