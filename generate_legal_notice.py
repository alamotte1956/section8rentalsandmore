import json
from datetime import datetime, timedelta

def generate_statutory_notice(
    state: str,
    notice_type: str,
    tenant_name: str,
    property_address: str,
    county: str,
    housing_authority_code: str,
    housing_authority_name: str,
    delinquent_rent_balance: float,
    accounting_breakdown: list,
    notice_date: datetime = None
) -> dict:
    """
    Generates statutory pre-eviction legal notices for MN (Minn. Stat. § 504B.321)
    and WI (Wis. Stat. § 704.17) with Federal CARES Act & Section 8 PHA service compliance.
    """
    if notice_date is None:
        notice_date = datetime.now()

    # Section 8 covered properties enforce 30-day federal CARES Act notice
    cares_act_applies = True
    minimum_days = 30 if cares_act_applies else (14 if state.upper() == "MN" else 5)
    cure_expiration_date = notice_date + timedelta(days=minimum_days)

    statutory_citations = {
        "MN": "Minnesota Statutes § 504B.321 Subd. 1a (14-Day Pre-Eviction Notice Mandate)",
        "WI": "Wisconsin Statutes § 704.17 (Notice Terminating Tenancy for Failure to Pay Rent)"
    }

    management_entity = {
        "company": "Section 8 Rentals and More LLC",
        "principal": "Dr. Albert Ray LaMotte",
        "address": "10805 173rd St W, Unit 127, Lakeville, MN 55044",
        "phone": "(612) 701-7064",
        "email": "info@Section8RentalsandMore.com"
    }

    pha_service_copy = {
        "rule": "24 CFR § 982.310(e)(2)(ii) — Mandatory Landlord Copy to Housing Authority",
        "pha_code": housing_authority_code,
        "pha_name": housing_authority_name,
        "service_requirement": "Concurrent written copy must be transmitted to the PHA case manager."
    }

    notice = {
        "notice_header": f"STATUTORY NOTICE TO REMEDY DEFAULT OR QUIT — {state.upper()}",
        "governing_state_statute": statutory_citations.get(state.upper(), statutory_citations["MN"]),
        "federal_compliance": "Public Law 116-136, Section 4024 (Federal CARES Act 30-Day Notice Mandate Enforced)",
        "service_details": {
            "date_of_service": notice_date.strftime("%B %d, %Y"),
            "expiration_deadline": cure_expiration_date.strftime("%B %d, %Y"),
            "statutory_cure_window_days": minimum_days
        },
        "recipient": {
            "tenant_name": tenant_name,
            "leased_premises": property_address,
            "county": county
        },
        "landlord_entity": management_entity,
        "section_8_housing_authority_notice": pha_service_copy,
        "financial_accounting": {
            "total_delinquent_balance_owed": delinquent_rent_balance,
            "ledger_itemization": accounting_breakdown
        },
        "state_specific_advisories": {
            "financial_assistance_disclosure": (
                "You have the right to seek rent assistance. In Minnesota, you may apply through "
                "your local county health and human services department, community action agency, or by calling 211."
                if state.upper() == "MN" else
                "You may apply for emergency assistance through Wisconsin Emergency Rental Assistance (WERA) or local CAP agencies."
            ),
            "remedy_instruction": (
                f"You must pay the total outstanding amount of ${delinquent_rent_balance:,.2f} on or before "
                f"{cure_expiration_date.strftime('%B %d, %Y')} or vacate the leased premises. "
                "Failure to cure will result in formal unlawful detainer/eviction proceedings."
            )
        }
    }
    return notice

if __name__ == "__main__":
    print("=" * 90)
    print("SECTION 8 RENTALS AND MORE LLC — DUAL-STATE STATUTORY LEGAL NOTICE ENGINE")
    print("=" * 90)

    # Minnesota Scenario: Lakeville / Dakota County CDA (MN042)
    mn_notice = generate_statutory_notice(
        state="MN",
        notice_type="14-Day Pay or Quit",
        tenant_name="Sample Resident",
        property_address="17420 Kenwood Trail, Lakeville, MN 55044",
        county="Dakota",
        housing_authority_code="MN042",
        housing_authority_name="Dakota County Community Development Agency (CDA)",
        delinquent_rent_balance=1240.00,
        accounting_breakdown=[
            {"month": "October 2026", "item": "Tenant Share of Rent", "amount": 620.00},
            {"month": "November 2026", "item": "Tenant Share of Rent", "amount": 620.00}
        ]
    )
    with open("sample_legal_notice_mn.json", "w", encoding="utf-8") as f:
        json.dump(mn_notice, f, indent=2)

    # Wisconsin Scenario: Hudson / St. Croix County Housing Authority (WI036)
    wi_notice = generate_statutory_notice(
        state="WI",
        notice_type="5-Day Remedy or Quit",
        tenant_name="Sample Resident WI",
        property_address="1500 Crest View Dr, Hudson, WI 54016",
        county="St. Croix",
        housing_authority_code="WI036",
        housing_authority_name="St. Croix County Housing Authority",
        delinquent_rent_balance=780.00,
        accounting_breakdown=[
            {"month": "November 2026", "item": "Tenant Share of Rent", "amount": 780.00}
        ]
    )
    with open("sample_legal_notice_wi.json", "w", encoding="utf-8") as f:
        json.dump(wi_notice, f, indent=2)

    print("✔ Minnesota Notice Generated: sample_legal_notice_mn.json")
    print(f"  • Statute:   {mn_notice['governing_state_statute']}")
    print(f"  • Federal:   {mn_notice['federal_compliance']}")
    print(f"  • Deadline:  {mn_notice['service_details']['expiration_deadline']} ({mn_notice['service_details']['statutory_cure_window_days']} Days)")
    print(f"  • PHA Copy:  {mn_notice['section_8_housing_authority_notice']['pha_name']}")
    print("-" * 90)
    print("✔ Wisconsin Notice Generated: sample_legal_notice_wi.json")
    print(f"  • Statute:   {wi_notice['governing_state_statute']}")
    print(f"  • Federal:   {wi_notice['federal_compliance']}")
    print(f"  • Deadline:  {wi_notice['service_details']['expiration_deadline']} ({wi_notice['service_details']['statutory_cure_window_days']} Days)")
    print(f"  • PHA Copy:  {wi_notice['section_8_housing_authority_notice']['pha_name']}")
    print("=" * 90)