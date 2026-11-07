import os
from datetime import datetime, timedelta

def generate_cares_act_30_day(tenant_name, property_address, amount_due, landlord_name, landlord_phone):
    today = datetime.now()
    due_date = today + timedelta(days=30)
    content = f"""================================================================================
FEDERAL CARES ACT 30-DAY NOTICE TO VACATE FOR NONPAYMENT
Section 4024 of the Coronavirus Aid, Relief, and Economic Security Act (15 U.S.C. 9058)
================================================================================

DATE OF SERVICE: {today.strftime('%B %d, %Y')}

TO TENANT(S):
  {tenant_name}
  {property_address}

FROM LANDLORD / AUTHORIZED AGENT:
  Section 8 Rentals and More LLC / {landlord_name}
  Phone: {landlord_phone}

SUBJECT PROPERTY: COVERED UNDER FEDERAL HOUSING PROGRAM (SECTION 8 / HAP CONTRACT)

YOU ARE HEREBY NOTIFIED that you owe past due rent in the amount of: ${amount_due:,.2f}

FEDERAL 30-DAY STATUTORY REQUIREMENT:
Under Section 4024(c) of the CARES Act, the lessor of a covered dwelling may not require
a tenant to vacate earlier than 30 days after the lessor provides the tenant with a notice
to vacate.

DEADLINE TO VACATE OR CURE: {due_date.strftime('%B %d, %Y')} by 5:00 PM CST.

If the past-due balance is not satisfied or possession surrendered within thirty (30) days
from service, legal proceedings for eviction will be initiated in the appropriate court.

COPIES TRANSMITTED:
- Administering Public Housing Authority (PHA) Section 8 Case Office
- Landlord Compliance Records

AUTHORIZED AGENT:
___________________________________________________
Section 8 Rentals and More LLC
================================================================================
"""
    filename = f"NOTICE_CARES_30DAY_{tenant_name.replace(' ', '_')}_{today.strftime('%Y%m%d')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[+] CARES Act 30-Day Notice generated: {filename}")
    return filename

if __name__ == "__main__":
    generate_cares_act_30_day("Sample Tenant CARES", "1234 Nicollet Ave, Minneapolis, MN 55403", 1850.00, "Dr. Albert Ray LaMotte", "952-555-0199")
