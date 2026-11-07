import os
from datetime import datetime, timedelta

def create_inspection_ics():
    today = datetime.now()
    inspection_date = today + timedelta(days=7)
    
    start_str = inspection_date.strftime("%Y%m%dT140000Z")
    end_str = inspection_date.strftime("%Y%m%dT160000Z")
    stamp_str = today.strftime("%Y%m%dT%H%M%SZ")
    
    ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Section 8 Rentals and More LLC//NSPIRE Pre-Inspection//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH
BEGIN:VEVENT
UID:insp-{today.strftime('%Y%m%d%H%M%S')}@section8rentalsandmore.com
DTSTAMP:{stamp_str}
DTSTART:{start_str}
DTEND:{end_str}
SUMMARY:HUD NSPIRE Pre-Inspection Audit - Section 8 Placement
DESCRIPTION:Pre-inspection compliance walk-through: verify egress windows, check dual-sensor CO/smoke detectors, test GFCI outlets, inspect water heater TPR valve, and audit window paint friction surfaces.
LOCATION:Metro Area Housing Authority Jurisdiction
STATUS:CONFIRMED
PRIORITY:1
BEGIN:VALARM
TRIGGER:-PT24H
ACTION:DISPLAY
DESCRIPTION:Reminder: Section 8 NSPIRE Inspection in 24 hours
END:VALARM
END:VEVENT
END:VCALENDAR
"""
    filename = "inspection_schedule.ics"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(ics_content)
    print(f"[+] Inspection schedule generated: {filename}")
    return filename

if __name__ == "__main__":
    create_inspection_ics()
