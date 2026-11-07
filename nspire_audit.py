import json

NSPIRE_STANDARDS = {
    "electrical": [
        {"item": "GFCI Protection", "requirement": "GFCI outlets within 6ft of all water sources functional", "critical": True},
        {"item": "Cover Plates", "requirement": "No missing, cracked, or loose outlet/switch covers", "critical": True},
        {"item": "Electrical Panel", "requirement": "No open knockouts or exposed wiring; breakers labeled", "critical": True}
    ],
    "hvac_plumbing": [
        {"item": "Water Heater TPR Valve", "requirement": "Discharge pipe extends downward to within 6 inches of floor", "critical": True},
        {"item": "Heating System", "requirement": "Capable of maintaining 68°F minimum during MN heating season", "critical": True},
        {"item": "Plumbing Leaks", "requirement": "Zero active leaks under sinks, toilets, or supply lines", "critical": False}
    ],
    "life_safety": [
        {"item": "Smoke Alarms", "requirement": "Installed inside every bedroom and on every level; functional test", "critical": True},
        {"item": "Carbon Monoxide Alarms", "requirement": "Installed within 10 feet of each sleeping room (MN Statute 299F.51)", "critical": True},
        {"item": "Egress Windows", "requirement": "Bedrooms have operational emergency egress with working locks", "critical": True}
    ],
    "building_envelope": [
        {"item": "Entry Doors & Locks", "requirement": "Deadbolts functional without key required on interior", "critical": True},
        {"item": "Window Weatherization", "requirement": "Intact seals, no broken panes, latches secure unit", "critical": False},
        {"item": "Trip Hazards", "requirement": "No flooring elevation changes > 0.75 inch without threshold ramp", "critical": False}
    ]
}

def run_nspire_audit(property_id, audit_responses):
    passed_count = 0
    failed_items = []
    total_checks = 0

    print("==================================================")
    print("       NSPIRE PRE-INSPECTION AUDIT REPORT         ")
    print("==================================================")
    print(f"Property Address:   {property_id}")
    print("Standard Reference: HUD NSPIRE (National Standards for the Physical Inspection of Real Estate)")
    print("--------------------------------------------------")

    for category, checks in NSPIRE_STANDARDS.items():
        for check in checks:
            total_checks += 1
            item_name = check["item"]
            passed = audit_responses.get(item_name, True)
            if passed:
                passed_count += 1
            else:
                failed_items.append({
                    "category": category.upper(),
                    "item": item_name,
                    "requirement": check["requirement"],
                    "critical": check["critical"]
                })

    score = (passed_count / total_checks) * 100
    print(f"Audit Score:        {score:.1f}% ({passed_count}/{total_checks} items passed)")

    if len(failed_items) == 0:
        print("PHA Inspection:     READY (100% Pass Probability)")
    else:
        print(f"PHA Inspection:     ACTION REQUIRED ({len(failed_items)} items to cure before PHA visit)")
        print("\n--- CONTRACTOR PUNCHLIST GENERATED ---")
        for idx, failure in enumerate(failed_items, 1):
            severity = "CRITICAL (Immediate Failure)" if failure["critical"] else "Standard Non-Compliance"
            print(f"{idx}. [{failure['category']}] {failure['item']} - {severity}")
            print(f"   Requirement: {failure['requirement']}")

    report_payload = {
        "property": property_id,
        "score_percentage": score,
        "passed": len(failed_items) == 0,
        "action_items": failed_items
    }

    with open("nspire_audit_report.json", "w", encoding="utf-8") as f:
        json.dump(report_payload, f, indent=2)
    print("--------------------------------------------------")
    print("Generated File:     nspire_audit_report.json")
    print("==================================================")

if __name__ == "__main__":
    sample_audit_field_results = {
        "GFCI Protection": True,
        "Cover Plates": True,
        "Electrical Panel": True,
        "Water Heater TPR Valve": False,  # Missing discharge pipe extension
        "Heating System": True,
        "Plumbing Leaks": True,
        "Smoke Alarms": True,
        "Carbon Monoxide Alarms": True,
        "Egress Windows": True,
        "Entry Doors & Locks": True,
        "Window Weatherization": False,  # Cracked window latch
        "Trip Hazards": True
    }

    run_nspire_audit("10805 173rd St W, Unit 127, Lakeville, MN 55044", sample_audit_field_results)
