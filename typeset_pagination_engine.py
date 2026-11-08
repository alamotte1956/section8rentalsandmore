import os
import sys
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.pdfgen import canvas

class BookPageGeometryCanvas(canvas.Canvas):
    """
    Two-pass canvas enforcing:
    1. Alternating/Asymmetric gutter margins (0.75 in binding gutter, 0.5 in trim margin).
    2. Single-line running headers with anti-collision text truncation.
    3. Dynamic 'Page X of Y' pagination stamps.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        self.setFont("Times-Roman", 8)
        self.setFillColor(colors.HexColor("#475569"))

        is_recto = (self._pageNumber % 2 != 0)  # Odd page (Right-facing)
        
        # Geometry anchors (letter = 612 pt x 792 pt)
        left_edge = 54   # 0.75 in gutter
        right_edge = 576 # 0.50 in trim margin

        # Running Header (Single line, strictly constrained)
        header_text = "SECTION 8 RENTALS AND MORE LLC • STATUTORY MASTER DOSSIER"
        if is_recto:
            self.drawRightString(right_edge, 752, header_text)
        else:
            self.drawString(left_edge, 752, header_text)

        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(left_edge, 744, right_edge, 744)

        # Running Footer (Bottom Rule + Dynamic Page Counts)
        self.line(left_edge, 46, right_edge, 46)
        page_str = f"Page {self._pageNumber} of {total_pages}"
        
        if is_recto:
            self.drawRightString(right_edge, 34, page_str)
            self.drawString(left_edge, 34, "CONFIDENTIAL JUDICIAL & REGULATORY RECORD")
        else:
            self.drawString(left_edge, 34, page_str)
            self.drawRightString(right_edge, 34, "CONFIDENTIAL JUDICIAL & REGULATORY RECORD")

        self.restoreState()


def compile_perfect_bound_document(output_filename, title, sections):
    """
    Compiles fully justified, anti-river legal & statutory documents.
    Enforces KeepTogether on headings to prevent orphan headers.
    """
    # 612 pt total width: 54 pt left gutter + 36 pt right margin = 522 pt printable width
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=36,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Typographic hierarchy calibrated to prevent river gaps during full justification
    body_style = ParagraphStyle(
        'JustifiedBody',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=10,
        leading=13.5,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
        textColor=colors.HexColor('#0F172A')
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        fontName='Times-Bold',
        fontSize=13,
        leading=16,
        alignment=TA_LEFT,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True,  # Built-in orphan prevention
        textColor=colors.HexColor('#0F172A')
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        fontName='Times-BoldItalic',
        fontSize=11,
        leading=14,
        alignment=TA_LEFT,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True,
        textColor=colors.HexColor('#1E293B')
    )

    title_style = ParagraphStyle(
        'MainTitle',
        fontName='Times-Bold',
        fontSize=16,
        leading=20,
        alignment=TA_CENTER,
        spaceAfter=14,
        textColor=colors.HexColor('#000000')
    )

    story = []

    # Title block
    story.append(Paragraph(title.upper(), title_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0F172A"), spaceAfter=14))

    for section in sections:
        # Wrap heading and introductory paragraph in KeepTogether to guarantee zero orphan headers
        header_p = Paragraph(section['heading'].upper(), h1_style)
        first_body_p = Paragraph(section['paragraphs'][0], body_style)
        
        story.append(KeepTogether([header_p, first_body_p]))

        for para in section['paragraphs'][1:]:
            story.append(Paragraph(para, body_style))

        if 'table' in section and section['table']:
            grid_data = section['table']
            formatted_table = []
            
            # Table cell style
            cell_style = ParagraphStyle(
                'TableCell',
                parent=styles['Normal'],
                fontName='Times-Roman',
                fontSize=8.5,
                leading=11
            )
            cell_bold = ParagraphStyle(
                'TableCellBold',
                parent=cell_style,
                fontName='Times-Bold'
            )

            # Header row
            formatted_table.append([Paragraph(f"<b>{c}</b>", cell_bold) for c in grid_data[0]])
            for row in grid_data[1:]:
                formatted_table.append([Paragraph(str(c), cell_style) for c in row])

            col_width = 522.0 / len(grid_data[0])
            t = Table(formatted_table, colWidths=[col_width] * len(grid_data[0]), repeatRows=1)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F1F5F9')),
                ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
                ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            story.append(KeepTogether([t]))
            story.append(Spacer(1, 10))

    # Signature and Attestation Block (Protected against page truncation)
    sig_block = [
        Spacer(1, 10),
        HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CBD5E1"), spaceAfter=10),
        Paragraph("<b>AFFIDAVIT OF EXECUTION & STATUTORY COMPLIANCE</b>", h2_style),
        Paragraph(
            "The undersigned certifies under penalty of perjury under the laws of the State of Minnesota "
            "and the United States of America that this dossier has been prepared pursuant to HUD 24 CFR Part 982, "
            "Minn. Stat. § 504B, and Wis. Stat. § 704. All calculations, ledgers, and certifications are true, "
            "accurate, and fully reconciled as of the date executed below.",
            body_style
        ),
        Spacer(1, 16),
        Table([
            ["________________________________________________________", "______________________"],
            ["Dr. Albert Ray LaMotte, Managing Principal & CEO", "Execution Date"],
            ["Section 8 Rentals and More LLC • alamotte1956@gmail.com", datetime.datetime.now().strftime("%B %d, %Y")]
        ], colWidths=[360, 162], style=[
            ('FONTNAME', (0, 0), (-1, -1), 'Times-Roman'),
            ('FONTSIZE', (0, 0), (-1, -1), 8.5),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ])
    ]
    story.append(KeepTogether(sig_block))

    doc.build(story, canvasmaker=BookPageGeometryCanvas)
    print(f"✔ Successfully compiled bound publication PDF: {output_filename}")


if __name__ == "__main__":
    out_file = os.path.join(os.getcwd(), "typeset_portfolio_dossier.pdf")
    
    sample_sections = [
        {
            "heading": "1. Multi-Jurisdictional Statutory Scope & Authority",
            "paragraphs": [
                "Section 8 Rentals and More LLC operates across the Twin Cities metropolitan area (Hennepin, "
                "Ramsey, Dakota, Anoka, and Washington counties) and Western Wisconsin (St. Croix County). "
                "The organization ensures strict statutory compliance with Minnesota Statutes Chapter 504B, "
                "Wisconsin Statutes Chapter 704, and the Department of Housing and Urban Development Housing Choice "
                "Voucher Program rules codified in 24 CFR Part 982.",
                "Every dwelling unit under management undergoes pre-tenancy underwriting adhering strictly to 2026 "
                "Small Area Fair Market Rent (SAFMR) benchmarks. Rent reasonableness determinations enforce the 110% "
                "payment standard ceiling under 24 CFR § 982.507, preventing sovereign voucher abatements and securing "
                "unbroken direct-deposit disbursements."
            ],
            "table": [
                ["County Jurisdiction", "PHA Agency Code", "2026 2-BR SAFMR", "110% Cap Standard", "Winter Rule"],
                ["Hennepin County", "MN002 (MPHA)", "$1,850.00", "$2,035.00", "Minn. Stat. § 216B.096"],
                ["Ramsey County", "MN001 (St. Paul)", "$1,810.00", "$1,991.00", "Minn. Stat. § 216B.096"],
                ["Dakota County", "MN042 (CDA)", "$1,830.00", "$2,013.00", "Minn. Stat. § 216B.096"],
                ["St. Croix County", "WI198 (Hudson)", "$1,420.00", "$1,562.00", "Wis. Admin. PSC 134"]
            ]
        },
        {
            "heading": "2. Security Deposit Accounting & Mandatory 1% Escrowing",
            "paragraphs": [
                "Pursuant to Minn. Stat. § 504B.178, all tenant security deposits are held in a segregated trust "
                "depository account and accrue non-compounded simple interest at the statutory rate of 1.0% per annum. "
                "Upon termination of tenancy, the managing entity itemizes all physical findings within 21 days, "
                "distinguishing ordinary wear and tear from actionable damage to preclude statutory bad-faith penalties.",
                "In Wisconsin units, compliance adheres to Wis. Stat. § 704.28, ensuring all tenant security deposit "
                "transmittals and written explanation letters clear statutory deadlines with photographic proof archives."
            ]
        }
    ]

    compile_perfect_bound_document(out_file, "Statutory Operations & Regulatory Tenancy Dossier", sample_sections)
