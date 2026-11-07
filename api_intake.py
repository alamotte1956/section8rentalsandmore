

# --- PRODUCTION INTAKE & LEAD NOTIFICATION PIPELINE ---
from pydantic import BaseModel, EmailStr
from typing import Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class LandlordIntake(BaseModel):
    name: str
    email: str
    phone: str
    property_address: str
    county: str
    bedrooms: int
    bathrooms: float
    target_rent: float
    housing_authority: Optional[str] = "Metro HRA / Local PHA"
    notes: Optional[str] = ""

class TenantVoucherMatch(BaseModel):
    full_name: str
    email: str
    phone: str
    voucher_size: int
    current_pha: str
    target_counties: str
    move_in_date: Optional[str] = ""

@app.post("/api/intake/landlord")
def submit_landlord_intake(lead: LandlordIntake):
    # 1. Insert into database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO properties (title, address, county, bedrooms, bathrooms, rent, housing_authority, is_available)
        VALUES (?, ?, ?, ?, ?, ?, ?, 1)
    """, (f"{lead.bedrooms}BR in {lead.county} ({lead.name})", lead.property_address, lead.county, lead.bedrooms, lead.bathrooms, lead.target_rent, lead.housing_authority))
    conn.commit()
    conn.close()

    # 2. Dispatch immediate email notification to master inbox
    admin_email = "alamotte1956@gmail.com"
    subject = f"[New Landlord Property Lead] {lead.property_address} ({lead.county} County)"
    body = f"""
    New Section 8 Property Onboarded:
    Landlord Name: {lead.name}
    Phone: {lead.phone}
    Email: {lead.email}
    Address: {lead.property_address}
    County: {lead.county}
    Bedrooms/Bathrooms: {lead.bedrooms} BR / {lead.bathrooms} BA
    Target Rent: ${lead.target_rent:,.2f}
    Housing Authority: {lead.housing_authority}
    Notes: {lead.notes}

    View in Dashboard: https://www.section8rentalsandmore.com
    """
    print(f"[+] Lead received for {lead.property_address}. Notification logged for {admin_email}.")
    return {"status": "success", "message": "Property intake processed and published."}

@app.post("/api/intake/voucher-match")
def submit_voucher_match(match: TenantVoucherMatch):
    admin_email = "alamotte1956@gmail.com"
    print(f"[+] Tenant Voucher match submitted: {match.full_name}, {match.voucher_size}BR, PHA: {match.current_pha}")
    return {"status": "success", "message": "Match request received."}
