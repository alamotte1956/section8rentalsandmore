import os
import subprocess
import sys
import json
import re
from urllib.parse import urlparse

BASE_DIR = r"C:\section8landlordsmn"

def run_comprehensive_audit():
    print("=" * 75)
    print("  SECTION 8 RENTALS AND MORE LLC - MASTER SYSTEM VERIFICATION")
    print("=" * 75)

    # 1. HTML File & Link Integrity Audit
    print("\n[PHASE 1] HTML INTEGRITY & INTERNAL ROUTING AUDIT")
    html_files = [f for f in os.listdir(BASE_DIR) if f.endswith(".html")]
    all_files = set(os.listdir(BASE_DIR))
    link_pattern = re.compile(r'(?:href|src)=["\']([^"\']+)["\']', re.IGNORECASE)

    total_links = 0
    broken_links = 0

    for doc in sorted(html_files):
        path = os.path.join(BASE_DIR, doc)
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        doc_links = 0
        for match in link_pattern.finditer(content):
            target = match.group(1).strip()
            total_links += 1
            doc_links += 1

            if not target or target.startswith(("#", "http://", "https://", "mailto:", "tel:", "javascript:")):
                continue

            parsed_path = urlparse(target).path.lstrip("./").lstrip("/")
            if parsed_path:
                if parsed_path.startswith("api/"):
                    continue
                if parsed_path not in all_files and not os.path.exists(os.path.join(BASE_DIR, parsed_path)):
                    print(f"  [x] Broken route in '{doc}': target '{target}'")
                    broken_links += 1

        print(f"  [✓] {doc:<28} | Checked {doc_links} links")

    print(f"\nPhase 1 Result: {len(html_files)} documents audited | {total_links} links checked | {broken_links} broken")

    # 2. Automation Engines Runtime Suite
    print("\n" + "-" * 75)
    print("[PHASE 2] PYTHON AUTOMATION ENGINES & COMPLIANCE ENGINES")
    
    engines = [
        ("HUD-52517 RFTA Generator", "generate_rfta.py"),
        ("NSPIRE Pre-Audit Scoring Tool", "nspire_audit.py"),
        ("Dual-State Notice Engine (MN/WI)", "generate_notices.py"),
        ("Federal CARES Act 30-Day Notice", "cares_act_notice.py"),
        ("Operations Manual Compiler", "generate_manual.py"),
        ("ICS Inspection Calendar Engine", "export_calendar.py"),
        ("QuickBooks Online REST Sync", "qbo_sync.py"),
        ("Multi-Channel Ad Syndicator", "syndicate_ads.py")
    ]

    engines_passed = 0
    engines_failed = 0

    for name, script in engines:
        if not os.path.exists(os.path.join(BASE_DIR, script)):
            print(f"  [MISSING] {name:<35} -> {script}")
            engines_failed += 1
            continue

        res = subprocess.run([sys.executable, os.path.join(BASE_DIR, script)], capture_output=True, text=True)
        if res.returncode == 0:
            print(f"  [✓] PASS: {name:<33} ({script})")
            engines_passed += 1
        else:
            print(f"  [x] FAIL: {name:<33} (Exit Code: {res.returncode})")
            engines_failed += 1

    print(f"\nPhase 2 Result: {engines_passed}/{len(engines)} Engines operational | {engines_failed} Failures")

    # 3. Critical Artifacts & Data Payloads
    print("\n" + "-" * 75)
    print("[PHASE 3] PRODUCTION PAYLOAD INTEGRITY CHECK")

    artifacts = [
        ("Operations Manual (Markdown)", "OPERATIONS_MANUAL_2026.md"),
        ("Inspection Schedule (iCalendar)", "inspection_schedule.ics"),
        ("QBO Financial Ledger Export (JSON)", "qbo_ledger_export.json"),
        ("Ad Syndication Campaigns (JSON)", "syndicated_campaigns.json"),
        ("AWS / HIPAA Security Spec (Markdown)", "aws_compliance_architecture.md")
    ]

    artifacts_verified = 0
    for label, filename in artifacts:
        fpath = os.path.join(BASE_DIR, filename)
        if os.path.exists(fpath) and os.path.getsize(fpath) > 0:
            size_kb = os.path.getsize(fpath) / 1024
            print(f"  [✓] {label:<38} -> {filename} ({size_kb:.2f} KB)")
            artifacts_verified += 1
        else:
            print(f"  [x] Missing or 0 bytes: {filename}")

    print(f"\nPhase 3 Result: {artifacts_verified}/{len(artifacts)} Artifacts verified")

    # 4. Final Verdict
    print("=" * 75)
    if broken_links == 0 and engines_failed == 0 and artifacts_verified == len(artifacts):
        print("  STATUS: 100% PRODUCTION OPERATIONAL - ZERO ERRORS DETECTED")
    else:
        print(f"  STATUS: ISSUES DETECTED - {broken_links} Broken Links, {engines_failed} Engine Fails")
    print("=" * 75)

if __name__ == "__main__":
    run_comprehensive_audit()
