import json
import os

print("=" * 80)
print("SECTION 8 RENTALS & MORE LLC - PHASE 9: LEAD-BASED PAINT (LBP) ENGINE AUDIT")
print("Target: C:\\section8landlordsmn")
print("Standard: 24 CFR Part 35 / 40 CFR Part 745 & HUD Inspection Protocol")
print("=" * 80)

properties = [
    {
        "property_id": "PROP-MN-001",
        "address": "10805 173rd St W, Unit 127, Lakeville, MN 55044",
        "year_built": 2004,
        "property_type": "Townhouse",
        "bedroom_count": 3,
        "occupants_child_under_6": False
    },
    {
        "property_id": "PROP-MN-002",
        "address": "2412 Nicollet Ave, Minneapolis, MN 55404",
        "year_built": 1968,
        "property_type": "Multi-Family Apartment",
        "bedroom_count": 2,
        "occupants_child_under_6": True
    },
    {
        "property_id": "PROP-WI-001",
        "address": "567 2nd St, Hudson, WI 54016",
        "year_built": 1974,
        "property_type": "Senior Housing",
        "bedroom_count": 1,
        "occupants_child_under_6": False,
        "elderly_designated": True
    }
]

lbp_results = []

print("\n[STEP 1] EVALUATING LBP HAZARD RISK & EXEMPTION STATUS...")
for prop in properties:
    year = prop["year_built"]
    address = prop["address"]
    child_under_6 = prop.get("occupants_child_under_6", False)
    elderly_designated = prop.get("elderly_designated", False)
    
    if year >= 1978:
        status = "EXEMPT"
        reason = f"Constructed in {year} (Post-1978 Federal Exemption)"
        action_required = "None. Retain build documentation in tenant file."
    elif elderly_designated and not child_under_6:
        status = "EXEMPT"
        reason = f"Constructed in {year} - Designated Elderly/Disabled Housing with NO child under age 6 residing"
        action_required = "Maintain age-restriction covenant and certification on record."
    else:
        status = "ACTION_REQUIRED"
        reason = f"Target Housing (Built {year}, Pre-1978) - Subject to Full LBP Disclosure & Inspection"
        action_required = "Mandatory EPA Pamphlet ('Protect Your Family From Lead in Your Home'), signed HUD-52517 LBP Disclosure, and visual paint assessment."

    entry = {
        "property_id": prop["property_id"],
        "address": address,
        "year_built": year,
        "exemption_status": status,
        "legal_basis": reason,
        "compliance_action": action_required
    }
    lbp_results.append(entry)

    print(f"\n  • Property:  {address}")
    print(f"    - Year Built:       {year}")
    print(f"    - Classification:   {status}")
    print(f"    - Legal Basis:      {reason}")
    print(f"    - Required Action:  {action_required}")

with open("lbp_compliance_audit.json", "w", encoding="utf-8") as f:
    json.dump(lbp_results, f, indent=2)

print("\n[STEP 2] VERIFYING DISCLOSURE ATTACHMENT GATING...")
mpls_asset = next(x for x in lbp_results if x["property_id"] == "PROP-MN-002")
if mpls_asset["exemption_status"] == "ACTION_REQUIRED":
    print("  ✔ Gating Logic PASS: Minneapolis pre-1978 unit correctly requires signed EPA disclosure")
else:
    print("  ✖ Gating Logic FAIL: Minneapolis unit misclassified")

lakeville_asset = next(x for x in lbp_results if x["property_id"] == "PROP-MN-001")
if lakeville_asset["exemption_status"] == "EXEMPT":
    print("  ✔ Exemption Logic PASS: Lakeville 2004 asset correctly exempted from Pre-1978 LBP protocol")
else:
    print("  ✖ Exemption Logic FAIL: Lakeville asset misclassified")

print("\n" + "=" * 80)
print("PHASE 9 AUDIT COMPLETE: MANIFEST SAVED TO lbp_compliance_audit.json")
print("=" * 80)
