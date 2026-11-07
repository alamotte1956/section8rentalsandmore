import json
from datetime import datetime

def generate_operations_manual():
    manual = {
        "title": "STANDARD OPERATING PROCEDURE & PROPERTY MANAGEMENT OPERATIONS MANUAL",
        "entity": "Section 8 Rentals and More LLC",
        "principal": "Dr. Albert Ray LaMotte, President & CEO",
        "headquarters": "10805 173rd St W, Unit 127, Lakeville, MN 55044",
        "contact": {
            "phone": "(612) 701-7064",
            "email": "info@Section8RentalsandMore.com",
            "web": "https://section8rentalsandmore.com"
        },
        "effective_date": "FY 2026 - FY 2027",
        "generated_timestamp": datetime.now().isoformat(),
        "modules": [
            {
                "section": "1.0",
                "title": "Executive Summary & Dual-State Jurisdictional Scope",
                "content": (
                    "Section 8 Rentals and More LLC administers specialized property management, "
                    "lease-up execution, and compliance under Section 8 Housing Choice Voucher (HCV) "
                    "programs across the Minneapolis-St. Paul-Bloomington MSA (Dakota, Hennepin, Ramsey, "
                    "Anoka, Washington) and Western Wisconsin (St. Croix County). Operations ensure maximum "
                    "guaranteed contract rents under HUD FY 2027 Fair Market Rents (FMR) while maintaining strict statutory compliance."
                )
            },
            {
                "section": "2.0",
                "title": "Underwriting, Payment Standards & Rent Reasonableness (24 CFR Part 982)",
                "protocols": [
                    "Payment Standards Verification: Query hud_fmr_2027.sqlite prior to tenancy proposal.",
                    "Utility Deductions: Apply local PHA utility allowance schedules to determine maximum net contract rent (Box 12).",
                    "40% Initial Rent Burden Cap (24 CFR 982.508): Ensure tenant family share does not exceed 40% of adjusted monthly income at lease inception.",
                    "Rent Reasonableness Comps (24 CFR 982.507): Retain 3 unassisted market comparables in property file prior to RFTA packet submission."
                ]
            },
            {
                "section": "3.0",
                "title": "Physical Inspections & HUD NSPIRE Compliance",
                "protocols": [
                    "Life Safety: Smoke alarms on every level and inside all bedrooms; carbon monoxide alarms within 10 ft of all bedrooms (Minn. Stat. 299F.51).",
                    "Electrical Safety: GFCI protection operational on all outlets within 6 ft of water sources and exterior receptacles.",
                    "Lead-Safe Housing Rule (24 CFR Part 35): For all properties constructed before 1978, complete visual lead assessment ensuring zero peeling/chipping paint on friction surfaces.",
                    "Egress & Plumbing: Bedroom egress windows functional without prop sticks; Water heater TPR valve piped to within 6 inches of floor."
                ]
            },
            {
                "section": "4.0",
                "title": "Dual-State Statutory Notices & Default Enforcement",
                "protocols": [
                    "Federal CARES Act Mandate: All covered Section 8 tenancies require a mandatory 30-day written notice before eviction filings.",
                    "Minnesota Practice (Minn. Stat. 504B.321): Serve 14-day itemized pre-eviction notice detailing delinquent principal and emergency assistance resources.",
                    "Wisconsin Practice (Wis. Stat. 704.17): Serve 5-day pay-or-quit or 14-day notice terminating tenancy.",
                    "Mandatory PHA Service Copy: Transmit concurrent written copy of all legal notices to the Housing Authority case manager per 24 CFR 982.310(e)(2)(ii)."
                ]
            },
            {
                "section": "5.0",
                "title": "Accounting & QuickBooks Online (QBO) Ledger Reconciliation",
                "protocols": [
                    "Direct HAP Deposit Split: Reconcile electronic ACH subsidy payments from PHA accounts separately from tenant rent portions.",
                    "Property-Specific Ledger Allocation: Segregate repair escrows, utility allocations, and net owner distributions per unique property ID."
                ]
            }
        ]
    }

    with open("PROPERTY_OPERATIONS_MANUAL.json", "w", encoding="utf-8") as f:
        json.dump(manual, f, indent=2)

    md = f"# {manual['title']}\n"
    md += f"**Company:** {manual['entity']}  \n"
    md += f"**Principal:** {manual['principal']}  \n"
    md += f"**Corporate Office:** {manual['headquarters']} | {manual['contact']['phone']}  \n"
    md += f"**Effective Period:** {manual['effective_date']}\n\n---\n\n"

    for mod in manual["modules"]:
        md += f"## {mod['section']} {mod['title']}\n\n"
        if "content" in mod:
            md += f"{mod['content']}\n\n"
        if "protocols" in mod:
            for p in mod["protocols"]:
                md += f"- {p}\n"
            md += "\n"

    with open("PROPERTY_OPERATIONS_MANUAL.md", "w", encoding="utf-8") as f:
        f.write(md)

    print("✔ Operations Manual Generated (JSON & MD)")

if __name__ == "__main__":
    generate_operations_manual()