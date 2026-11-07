import json
from datetime import datetime

def generate_nspire_checklist(property_address: str, county: str, bedrooms: int, year_built: int, property_type: str = "Single Family Detached") -> dict:
    """Generates official HUD NSPIRE pre-inspection punchlist for Section 8 onboarding."""
    
    lead_paint_audit = {
        "applies": year_built < 1978,
        "standard": "24 CFR Part 35 / HUD Lead Safe Housing Rule",
        "action_required": "Visual paint inspection required; zero chipping, cracking, or peeling on interior and exterior friction surfaces." if year_built < 1978 else "Exempt (Constructed in 1978 or later)."
    }

    nspire_standards = [
        {
            "category": "Life Safety & Alarms",
            "item": "Smoke Detectors",
            "nspire_rule": "Operable sealed 10-year battery or hardwired smoke alarms on every level, inside each bedroom, and outside sleeping areas.",
            "criticality": "Life-Threatening (Fail Item)"
        },
        {
            "category": "Life Safety & Alarms",
            "item": "Carbon Monoxide Alarms",
            "nspire_rule": "Installed within 10 feet of every bedroom in homes with fuel-burning appliances or attached garages (MN Statute 299F.51).",
            "criticality": "Life-Threatening (Fail Item)"
        },
        {
            "category": "Electrical & Shock Prevention",
            "item": "GFCI Receptacles",
            "nspire_rule": "GFCI protection operational on all outlets within 6 feet of sinks, water sources, exterior receptacles, and bathrooms.",
            "criticality": "High (Fail Item)"
        },
        {
            "category": "Electrical & Shock Prevention",
            "item": "Electrical Panels & Covers",
            "nspire_rule": "No open knockouts or exposed wiring; dead-front panel cover tightly fastened.",
            "criticality": "Life-Threatening (Fail Item)"
        },
        {
            "category": "Windows & Egress",
            "item": "Bedroom Egress Windows",
            "nspire_rule": "Windows in designated bedrooms must open smoothly, hold open without props, and latch securely.",
            "criticality": "Severe (Fail Item)"
        },
        {
            "category": "Plumbing & Water Heating",
            "item": "Water Heater TPR Valve & Discharge",
            "nspire_rule": "Temperature/Pressure Relief (TPR) valve installed with rigid discharge pipe terminating within 6 inches of floor.",
            "criticality": "High (Fail Item)"
        },
        {
            "category": "Doors & Security",
            "item": "Exterior Entry Doors",
            "nspire_rule": "Weatherstripped, weather-tight, and equipped with functioning single-cylinder deadbolt (no double-keyed locks).",
            "criticality": "Medium"
        },
        {
            "category": "HVAC & Thermal Environment",
            "item": "Heating System Operational",
            "nspire_rule": "Capable of maintaining continuous minimum 68°F indoor temperature during heating season without unvented space heaters.",
            "criticality": "High (Fail Item)"
        }
    ]

    report = {
        "inspection_standard": "HUD National Standards for the Physical Inspection of Real Estate (NSPIRE)",
        "generated_timestamp": datetime.now().isoformat(),
        "property_details": {
            "address": property_address,
            "county": county,
            "bedrooms": bedrooms,
            "year_built": year_built,
            "property_type": property_type
        },
        "lead_paint_compliance": lead_paint_audit,
        "nspire_checklist": nspire_standards,
        "management_attestation": "Section 8 Rentals and More LLC — Quality Assurance Inspection Division"
    }
    return report

if __name__ == "__main__":
    print("=" * 85)
    print("SECTION 8 RENTALS AND MORE LLC — NSPIRE PRE-INSPECTION AUDIT GENERATOR")
    print("=" * 85)

    audit = generate_nspire_checklist(
        property_address="4120 4th Ave S, Minneapolis, MN 55409",
        county="Hennepin",
        bedrooms=2,
        year_built=1956
    )

    out_file = "sample_nspire_audit_hennepin.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(audit, f, indent=2)

    print(f"✔ Pre-Inspection Audit Generated: {out_file}")
    print(f"  • Property:    {audit['property_details']['address']}")
    print(f"  • Year Built:  {audit['property_details']['year_built']}")
    print(f"  • Lead Status: {audit['lead_paint_compliance']['action_required']}")
    print(f"  • Standards:   {len(audit['nspire_checklist'])} Core NSPIRE Failure Prevention Items")
    print("=" * 85)