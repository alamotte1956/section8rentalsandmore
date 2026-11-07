import json
from datetime import datetime

class LandlordAdSyndicator:
    """
    Automated syndication engine creating targeted ad campaigns for 
    Twin Cities & Western Wisconsin landlord acquisition.
    """
    def __init__(self, portal_url="https://www.section8rentalsandmore.com"):
        self.portal_url = portal_url
        self.contact_email = "info@section8rentalsandmore.com"
        self.date_str = datetime.now().strftime("%B %Y")

    def generate_fb_marketplace_ad(self):
        return {
            "platform": "Facebook Marketplace / Local Rental Groups",
            "category": "Housing / Property Management Services",
            "title": f"Twin Cities Landlords: Get 100% Guaranteed Rent via HUD Section 8 ({self.date_str})",
            "body": f"""Tired of tenant non-payment, vacancy loss, and chasing late checks?

Section 8 Rentals and More LLC connects property owners across the Twin Cities (Hennepin, Ramsey, Dakota, Anoka, Washington) and Western Wisconsin directly with pre-screened voucher holders.

Why Partner With Us?
✔ Guaranteed Direct Deposit: Payments backed by HUD & local housing authorities (MPHA, St. Paul PHA, Dakota CDA).
✔ Maximum Allowable Rent: We audit 2026 Fair Market Rents to ensure you receive top-tier market rates.
✔ Fast-Track Approvals: Automated HUD-52517 RFTA packet prep & NSPIRE pre-inspection compliance.
✔ Complete Legal Compliance: Pre-audited statutory notices compliant with MN § 504B and WI § 704.

Calculate your property's Fair Market Rent in seconds:
👉 {self.portal_url}

Direct Intake: {self.contact_email}"""
        }

    def generate_craigslist_ad(self):
        return {
            "platform": "Craigslist (Minneapolis / St. Paul / Real Estate Services)",
            "title": "Landlords & PMs: Guaranteed Section 8 Direct Deposit | Full Compliance Handling",
            "body": f"""STOP LEAVING RENT ON THE TABLE IN THE TWIN CITIES METRO

Section 8 Rentals and More LLC provides complete voucher facilitation for independent landlords and property managers.

COVERED HOUSING AUTHORITIES:
- Minneapolis Public Housing Authority (MN002)
- Saint Paul Public Housing Agency (MN001)
- Dakota County CDA (MN042)
- Washington County CDA (MN033)
- Anoka County HRA (MN027)
- Western Wisconsin Regional Housing Offices

SERVICES PROVIDED:
1. Automated Rent Reasonableness & Utility Splits Analysis
2. Request for Tenancy Approval (RFTA Form HUD-52517) Fast-Track Packets
3. NSPIRE Pre-Inspection Walk-Through Scoring (zero first-time inspection fails)
4. Dual-State Statutory Notice Generation (MN 14-day pre-filing / WI 5-day / CARES Act)

Visit our live portal to test the 2026 Fair Market Rent Calculator:
{self.portal_url}

Contact our Executive Placement Desk:
{self.contact_email}"""
        }

    def export_campaigns(self):
        campaigns = [
            self.generate_fb_marketplace_ad(),
            self.generate_craigslist_ad()
        ]
        filename = "syndicated_campaigns.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(campaigns, f, indent=2)
        print(f"[+] Multi-channel syndication campaigns saved: {filename}")
        return filename

if __name__ == "__main__":
    syndicator = LandlordAdSyndicator()
    syndicator.export_campaigns()
