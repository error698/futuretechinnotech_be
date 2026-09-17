import io
from datetime import datetime
from typing import Dict, Any
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

class PdfService:
    """Enterprise PDF generation service for RFQ specification and quotations."""

    def generate_rfq_quotation(self, rfq_data: Dict[str, Any]) -> bytes:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        elements = []
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'FTITTitle',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#F42C37'),
            spaceAfter=4
        )
        subtitle_style = ParagraphStyle(
            'FTITSubtitle',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#4B5563'),
            spaceAfter=14
        )
        section_style = ParagraphStyle(
            'FTITSection',
            parent=styles['Heading2'],
            fontSize=13,
            textColor=colors.HexColor('#111827'),
            spaceBefore=10,
            spaceAfter=6
        )
        body_style = ParagraphStyle(
            'FTITBody',
            parent=styles['Normal'],
            fontSize=9,
            leading=13,
            textColor=colors.HexColor('#1F2937')
        )

        # Header
        elements.append(Paragraph("FUTURETECH INNOTECH (FTIT)", title_style))
        elements.append(Paragraph(
            "Tier-1 Automotive Design, Manufacturing & Precision Engineering Solutions<br/>"
            "B-231, 2nd Floor, Shivaji Vihar, Rajouri Garden, New Delhi-110027 | +91 70424 50591 | Pdhead@futuretechinnotech.in",
            subtitle_style
        ))
        elements.append(Spacer(1, 10))

        # Metadata Table
        rfq_id = rfq_data.get('rfqNumber', f"RFQ-{int(datetime.now().timestamp())}")
        client_name = rfq_data.get('name', 'Valued Customer')
        client_email = rfq_data.get('email', '-')
        client_phone = rfq_data.get('phone', '-')
        vehicle = rfq_data.get('vehicle', 'All Models')
        company = rfq_data.get('company', 'Direct Inquiry')

        meta_info = [
            [Paragraph(f"<b>Quotation Reference:</b> {rfq_id}", body_style), Paragraph(f"<b>Date:</b> {datetime.now().strftime('%d-%b-%Y')}", body_style)],
            [Paragraph(f"<b>Client Name:</b> {client_name}", body_style), Paragraph(f"<b>Organization:</b> {company}", body_style)],
            [Paragraph(f"<b>Email / Phone:</b> {client_email} / {client_phone}", body_style), Paragraph(f"<b>Target Vehicle:</b> {vehicle}", body_style)],
        ]
        meta_table = Table(meta_info, colWidths=[270, 270])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F9FAFB')),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E7EB')),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#F3F4F6')),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(meta_table)
        elements.append(Spacer(1, 15))

        # Items Table
        elements.append(Paragraph("Requested Line Items & Specifications", section_style))
        items = rfq_data.get('items', [])
        table_data = [[
            Paragraph("<b>#</b>", body_style),
            Paragraph("<b>Item Name / Spec</b>", body_style),
            Paragraph("<b>Category</b>", body_style),
            Paragraph("<b>Quantity</b>", body_style),
            Paragraph("<b>OEM Grade</b>", body_style)
        ]]

        for idx, it in enumerate(items, 1):
            name = it.get('name', 'Automotive Accessory') if isinstance(it, dict) else getattr(it, 'name', 'Automotive Accessory')
            category = it.get('category', 'Accessories') if isinstance(it, dict) else getattr(it, 'category', 'Accessories')
            qty = it.get('quantity', 1) if isinstance(it, dict) else getattr(it, 'quantity', 1)

            table_data.append([
                Paragraph(str(idx), body_style),
                Paragraph(str(name), body_style),
                Paragraph(str(category), body_style),
                Paragraph(str(qty), body_style),
                Paragraph("Tier-1 Certified", body_style)
            ])

        if len(items) == 0:
            table_data.append([
                Paragraph("1", body_style),
                Paragraph("Standard Automotive Line Item Inquiry", body_style),
                Paragraph("General Catalog", body_style),
                Paragraph("1 Lot", body_style),
                Paragraph("Tier-1", body_style)
            ])

        items_table = Table(table_data, colWidths=[30, 240, 120, 60, 90])
        items_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E293B')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D1D5DB')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9FAFB')]),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(items_table)
        elements.append(Spacer(1, 18))

        # Terms & Engineering Notes
        elements.append(Paragraph("Terms & Engineering Standards", section_style))
        elements.append(Paragraph(
            "• All components are manufactured according to ISO 9001 and IATF 16949 automotive standards.<br/>"
            "• Standard 2-Year Direct Warranty applies against manufacturing defects.<br/>"
            "• Production lead times for custom finishes (Rose Gold, Satin Chrome, Piano Black) are 7-14 business days.",
            body_style
        ))

        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()
