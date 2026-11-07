import os
import json
import datetime

today = datetime.date.today()
portfolio_file = "property_inspection_schedules.json"

if os.path.exists(portfolio_file):
    with open(portfolio_file, "r", encoding="utf-8") as f:
        portfolio = json.load(f)
else:
    portfolio = {
        "portfolio": "Section 8 Rentals and More LLC",
        "last_audit_run": str(today),
        "properties": [
            {
                "property_id": "MN-LAKEVILLE-17420",
                "address": "17420 Kenwood Trail, Lakeville, MN 55044",
                "pha_name": "Dakota County CDA",
                "insp_days": 12,
                "recert_days": 22
            },
            {
                "property_id": "MN-MPLS-2415",
                "address": "2415 18th Ave S, Minneapolis, MN 55404",
                "pha_name": "Minneapolis Public Housing Authority (MPHA)",
                "insp_days": 48,
                "recert_days": 55
            },
            {
                "property_id": "WI-HUDSON-502",
                "address": "502 2nd St, Hudson, WI 54016",
                "pha_name": "West Central Wisconsin CAA",
                "insp_days": 82,
                "recert_days": 114
            }
        ]
    }

report_lines = [
    "=" * 75,
    "SECTION 8 RENTALS AND MORE LLC - INSPECTION & RECERTIFICATION AUDIT",
    f"Audit Run: {today}",
    "=" * 75
]

for p in portfolio["properties"]:
    insp_date = today + datetime.timedelta(days=p["insp_days"])
    recert_date = today + datetime.timedelta(days=p["recert_days"])
    if p["insp_days"] <= 14:
        status = "CRITICAL (<= 14 Days) - Conduct Pre-Inspection Walk"
    elif p["recert_days"] <= 30:
        status = "IMMINENT (15-30 Days) - Issue 14-Day Notice & Check GFCI/Alarms"
    else:
        status = "ROUTINE COMPLIANCE"

    report_lines.append(f"[{p['property_id']}] {p['address']}")
    report_lines.append(f"  Housing Agency: {p['pha_name']}")
    report_lines.append(f"  NSPIRE Inspection:  {insp_date} ({p['insp_days']} days remaining)")
    report_lines.append(f"  Annual Recert Date: {recert_date} ({p['recert_days']} days remaining)")
    report_lines.append(f"  Action Status:      {status}\n")

report_text = "\n".join(report_lines)
with open("INSPECTION_ACTION_REPORT.txt", "w", encoding="utf-8") as f:
    f.write(report_text)

print(report_text)
