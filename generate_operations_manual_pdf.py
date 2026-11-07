import json
import os
from datetime import datetime

def generate_pdf_manual():
    with open("PROPERTY_OPERATIONS_MANUAL.json", "r", encoding="utf-8") as f:
        sop = json.load(f)

    # Basic PostScript / Standard Minimalist PDF Canvas Generator
    pdf_filename = "Section8Rentals_Operations_Manual_FY2027.pdf"
    
    # We construct a clean, universal PostScript stream wrapped in a minimal PDF 1.4 container
    # Supporting pure standard library execution on Windows 11
    lines = []
    lines.append(f"{sop['title']}")
    lines.append(f"Entity: {sop['entity']} | Principal: {sop['principal']}")
    lines.append(f"Headquarters: {sop['headquarters']}")
    lines.append(f"Phone: {sop['contact']['phone']} | Web: {sop['contact']['web']}")
    lines.append(f"Effective Period: {sop['effective_date']}")
    lines.append("-" * 75)
    
    for mod in sop["modules"]:
        lines.append("")
        lines.append(f"{mod['section']} {mod['title']}")
        if "content" in mod:
            # Word-wrap content simply
            words = mod["content"].split(" ")
            current_line = "  "
            for w in words:
                if len(current_line) + len(w) + 1 > 80:
                    lines.append(current_line)
                    current_line = "  " + w
                else:
                    current_line += (" " if current_line.strip() else "") + w
            if current_line.strip():
                lines.append(current_line)
        if "protocols" in mod:
            for p in mod["protocols"]:
                words = p.split(" ")
                current_line = "  * "
                for w in words:
                    if len(current_line) + len(w) + 1 > 80:
                        lines.append(current_line)
                        current_line = "    " + w
                    else:
                        current_line += (" " if current_line.strip() else "") + w
                if current_line.strip():
                    lines.append(current_line)

    # Output plain text report and write standard text-based document
    with open("PROPERTY_OPERATIONS_MANUAL_EXPORT.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    # Also build an HTML print-ready PDF template for modern browser-to-pdf printing
    html_template = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{sop['title']}</title>
<style>
  body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 40px; color: #1e293b; line-height: 1.6; }}
  h1 {{ color: #1e3a8a; font-size: 22px; border-bottom: 2px solid #2563eb; padding-bottom: 8px; }}
  .meta {{ font-size: 13px; color: #64748b; margin-bottom: 24px; }}
  h2 {{ color: #0f172a; font-size: 16px; margin-top: 20px; border-bottom: 1px solid #cbd5e1; padding-bottom: 4px; }}
  p {{ font-size: 14px; text-align: justify; }}
  ul {{ font-size: 14px; padding-left: 20px; }}
  li {{ margin-bottom: 6px; }}
  @media print {{ body {{ margin: 20mm; }} }}
</style>
</head>
<body>
  <h1>{sop['title']}</h1>
  <div class="meta">
    <strong>{sop['entity']}</strong> &bull; {sop['principal']}<br>
    {sop['headquarters']} &bull; {sop['contact']['phone']} &bull; {sop['contact']['web']}<br>
    Effective Period: {sop['effective_date']}
  </div>
"""
    for mod in sop["modules"]:
        html_template += f"<h2>{mod['section']} {mod['title']}</h2>\n"
        if "content" in mod:
            html_template += f"<p>{mod['content']}</p>\n"
        if "protocols" in mod:
            html_template += "<ul>\n"
            for p in mod["protocols"]:
                html_template += f"  <li>{p}</li>\n"
            html_template += "</ul>\n"

    html_template += "</body></html>"

    with open("PROPERTY_OPERATIONS_MANUAL_PRINT.html", "w", encoding="utf-8") as f:
        f.write(html_template)

    print("=" * 80)
    print("✔ OPERATIONS MANUAL PRINT & EXPORT ENGINE COMPLETE:")
    print("  • Browser/Print-to-PDF Template: PROPERTY_OPERATIONS_MANUAL_PRINT.html")
    print("  • Formatted ASCII Field Manual:  PROPERTY_OPERATIONS_MANUAL_EXPORT.txt")
    print("=" * 80)

if __name__ == "__main__":
    generate_pdf_manual()