import os
import sys

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
except ImportError:
    print("[*] Installing reportlab...")
    os.system(f"{sys.executable} -m pip install reportlab")
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

out_dir = r"C:\section8landlordsmn\statutory_notices\pdf"
os.makedirs(out_dir, exist_ok=True)

def generate_mn_14_day_pdf():
    pdf_path = os.path.join(out_dir, "MN_14_Day_Notice_Official.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []
    styles = getSampleStyleSheet()

    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        alignment=1,
        textColor=colors.HexColor('#1E293B')
    )
    sub_style = ParagraphStyle(
        'SubStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        alignment=1,
        textColor=colors.HexColor('#B91C1C')
    )
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#334155')
    )
    bold_body = ParagraphStyle(
        'BoldBody',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#0F172A')
    )

    story.append(Paragraph("SECTION 8 RENTALS AND MORE LLC", header_style))
    story.append(Paragraph("10805 173rd St W, Unit 127, Lakeville, MN 55044 | Phone: PASTE_NEW_NUMBER_HERE | info@section8rentalsandmore.com", ParagraphStyle('SubCompany', parent=styles['Normal'], fontSize=8, alignment=1, textColor=colors.HexColor('#64748B'))))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0F172A'), spaceAfter=10))

    story.append(Paragraph("FOURTEEN (14) DAY NOTICE TO QUIT FOR NON-PAYMENT OF RENT", header_style))
    story.append(Paragraph("PURSUANT TO MINNESOTA STATUTES SECTION 504B.321", sub_style))
    story.append(Spacer(1, 12))

    meta_data = [
        [Paragraph("<b>DATE OF SERVICE:</b> November 7, 2026", body_style), Paragraph("<b>COUNTY:</b> Hennepin / Dakota / Ramsey", body_style)],
        [Paragraph("<b>TENANT NAME(S):</b> [TENANT FULL NAME]", body_style), Paragraph("<b>HOUSING SPECIALIST:</b> [PHA SPECIALIST]", body_style)],
        [Paragraph("<b>RENTAL PREMISES:</b> [STREET ADDRESS, UNIT #, CITY, MN ZIP]", body_style), Paragraph("<b>PHA CASE #:</b> [CASE NUMBER]", body_style)]
    ]
    t_meta = Table(meta_data, colWidths=[270, 260])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>DEMAND FOR PAYMENT OF RENT:</b>", bold_body))
    story.append(Paragraph("PLEASE TAKE NOTICE that under Minn. Stat. § 504B.321, you are indebted to Section 8 Rentals and More LLC for past-due tenant-portion rent and allowable charges currently due and owing as itemized below:", body_style))
    story.append(Spacer(1, 8))

    ledger_data = [
        [Paragraph("<b>Description of Itemized Charge</b>", bold_body), Paragraph("<b>Due Date</b>", bold_body), Paragraph("<b>Amount Due</b>", bold_body)],
        [Paragraph("Past Due Tenant-Portion Rent (Current Month)", body_style), Paragraph("01/01/2026", body_style), Paragraph("$ 425.00", body_style)],
        [Paragraph("Past Due Tenant-Portion Rent (Prior Month)", body_style), Paragraph("12/01/2025", body_style), Paragraph("$ 425.00", body_style)],
        [Paragraph("Allowable Late Fee (Minn. Stat. § 504B.177, capped at 8%)", body_style), Paragraph("01/15/2026", body_style), Paragraph("$ 34.00", body_style)],
        [Paragraph("Authorized Utility Re-bill / Other Documented Charges", body_style), Paragraph("01/05/2026", body_style), Paragraph("$ 65.00", body_style)],
        [Paragraph("<b>TOTAL AMOUNT CURRENTLY OWED AND DEMANDED:</b>", bold_body), Paragraph("<b>TOTAL</b>", bold_body), Paragraph("<b>$ 949.00</b>", bold_body)]
    ]
    t_ledger = Table(ledger_data, colWidths=[310, 110, 110])
    t_ledger.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#94A3B8')),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#FEF2F2')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_ledger)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>FOURTEEN (14) DAY RIGHT TO CURE OR SURRENDER:</b>", bold_body))
    story.append(Paragraph("You have <b>FOURTEEN (14) DAYS</b> from the date of service/receipt of this notice to either: (1) pay the full balance of <b>$ 949.00</b>, OR (2) completely surrender and vacate possession of the rental property. If you fail to pay or vacate within 14 days, an Eviction Action will be filed immediately in District Court pursuant to Minn. Stat. § 504B.285.", body_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>MANDATORY NOTICE OF FINANCIAL ASSISTANCE RESOURCES:</b>", bold_body))
    story.append(Paragraph("Under Minnesota law, emergency rental assistance may be available from local community and county agencies. Contact your county immediately: Hennepin County: (612) 596-1300 | Ramsey County: (651) 266-4444 | Dakota County CDA: (651) 554-5611 | Anoka County: (763) 422-7200 | Washington County: (651) 430-6455.", body_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>HOUSING AUTHORITY COPY (24 C.F.R. § 982.310(e)(2)(ii)):</b>", bold_body))
    story.append(Paragraph("A true and exact copy of this notice is concurrently delivered to your Housing Authority Specialist administering your Section 8 Housing Choice Voucher.", body_style))
    story.append(Spacer(1, 20))

    sig_data = [
        [Paragraph("____________________________________________<br/><b>Albert Ray LaMotte</b>, Managing Member<br/>Section 8 Rentals and More LLC", body_style),
         Paragraph("____________________________________________<br/><b>Proof of Delivery / Service</b><br/>[ ] Personal Delivery  [ ] Certified Mail  [ ] Posting", body_style)]
    ]
    t_sig = Table(sig_data, colWidths=[270, 260])
    story.append(t_sig)

    doc.build(story)
    print(f"[+] Minnesota 14-Day Notice PDF compiled: {pdf_path}")

if __name__ == "__main__":
    generate_mn_14_day_pdf()
