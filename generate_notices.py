import os
import sys
from datetime import datetime, timedelta

def generate_mn_14_day(tenant_name, property_address, amount_due, landlord_name, landlord_phone):
    today = datetime.now()
    due_date = today + timedelta(days=14)
    content = f"""================================================================================
MINNESOTA 14-DAY STATUTORY PRE-FILING NOTICE
Pursuant to Minn. Stat. § 504B.321, Subd. 1a
================================================================================

DATE OF SERVICE: {today.strftime('%B %d, %Y')}

TO TENANT(S):
  {tenant_name}
  {property_address}

FROM LANDLORD / AUTHORIZED AGENT:
  Section 8 Rentals and More LLC / {landlord_name}
  Phone: {landlord_phone}

YOU ARE HEREBY NOTIFIED that you owe past due rent in the amount of: ${amount_due:,.2f}

ITEMIZATION OF PAST DUE RENT:
  Total Subsidized / Tenant Share Past Due: ${amount_due:,.2f}

REQUIRED STATUTORY WARNING:
Under Minnesota law, you have 14 DAYS from the date this notice was served to pay the 
total amount due in full. 

DEADLINE FOR FULL PAYMENT: {due_date.strftime('%B %d, %Y')} by 5:00 PM CST.

If you do not pay the total amount due or vacate the premises on or before this date,
an eviction action may be filed against you in District Court.

HOUSING ASSISTANCE RECIPIENTS:
A copy of this notice is being transmitted simultaneously to your administering
Public Housing Authority (PHA) case officer in compliance with federal HAP guidelines.

AUTHORIZED SIGNATURE:
___________________________________________________
Section 8 Rentals and More LLC
Compliance & Property Management Operations
================================================================================
"""
    filename = f"NOTICE_MN_14DAY_{tenant_name.replace(' ', '_')}_{today.strftime('%Y%m%d')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[+] Minnesota 14-Day Notice generated: {filename}")
    return filename

def generate_wi_5_day(tenant_name, property_address, amount_due, landlord_name, landlord_phone):
    today = datetime.now()
    due_date = today + timedelta(days=5)
    content = f"""================================================================================
WISCONSIN 5-DAY NOTICE TO REMEDY DEFAULT OR VACATE
Pursuant to Wis. Stat. § 704.17
================================================================================

DATE OF SERVICE: {today.strftime('%B %d, %Y')}

TO TENANT(S):
  {tenant_name}
  {property_address}

FROM LANDLORD / AUTHORIZED AGENT:
  Section 8 Rentals and More LLC / {landlord_name}
  Phone: {landlord_phone}

TAKE NOTICE that you are in default of your residential rental agreement due to 
unpaid rent in the amount of: ${amount_due:,.2f}

STATUTORY NOTICE PERIOD:
You have FIVE (5) DAYS from the date of service to either:
1. Pay the full past-due rent balance to the landlord, OR
2. Surrender possession and vacate the premises.

DEADLINE: {due_date.strftime('%B %d, %Y')} by 5:00 PM CST.

Failure to remedy this default within five days will result in formal termination
of your tenancy and the immediate filing of an eviction action in Circuit Court.

HOUSING AUTHORITY NOTICE:
For units under a Section 8 Housing Assistance Payments (HAP) contract, a concurrent
copy of this notice is provided to your housing voucher coordinator.

AUTHORIZED SIGNATURE:
___________________________________________________
Section 8 Rentals and More LLC
================================================================================
"""
    filename = f"NOTICE_WI_5DAY_{tenant_name.replace(' ', '_')}_{today.strftime('%Y%m%d')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[+] Wisconsin 5-Day Notice generated: {filename}")
    return filename

if __name__ == "__main__":
    print("--- Section 8 Rentals and More LLC: Statutory Notice Engine ---")
    generate_mn_14_day("Sample Tenant", "1234 Nicollet Ave, Minneapolis, MN 55403", 1450.00, "Dr. Albert Ray LaMotte", "952-555-0199")
    generate_wi_5_day("Sample Tenant WI", "567 2nd St, Hudson, WI 54016", 1120.00, "Dr. Albert Ray LaMotte", "952-555-0199")
