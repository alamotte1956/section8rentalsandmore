import os
import subprocess
import sys
import json

TESTS = [
    ("HUD-52517 RFTA Generator", "generate_rfta.py"),
    ("NSPIRE Pre-Audit Scoring Tool", "nspire_audit.py"),
    ("Dual-State Notice Engine", "generate_notices.py"),
    ("Federal CARES Act Generator", "cares_act_notice.py"),
    ("Operations Manual Compiler", "generate_manual.py"),
    ("ICS Inspection Exporter", "export_calendar.py"),
    ("QuickBooks Online REST Sync", "qbo_sync.py"),
    ("Multi-Channel Ad Syndicator", "syndicate_ads.py")
]

def run_e2e_suite():
    print("=" * 70)
    print("SECTION 8 RENTALS AND MORE LLC - ENGINE VERIFICATION TEST SUITE")
    print("=" * 70)
    
    passed = 0
    failed = 0
    
    for name, script in TESTS:
        if not os.path.exists(script):
            print(f"[-] [MISSING] {name} ({script}) not found in workspace.")
            failed += 1
            continue
            
        res = subprocess.run([sys.executable, script], capture_output=True, text=True)
        if res.returncode == 0:
            print(f"[✓] [PASS] {name} executed cleanly.")
            passed += 1
        else:
            print(f"[x] [FAIL] {name} failed with exit code {res.returncode}:")
            print(res.stderr.strip())
            failed += 1

    # Verify generated files integrity
    print("-" * 70)
    print("[*] Verifying critical operational data files:")
    critical_files = [
        "OPERATIONS_MANUAL_2026.md",
        "inspection_schedule.ics",
        "qbo_ledger_export.json",
        "syndicated_campaigns.json",
        "aws_compliance_architecture.md"
    ]
    for cf in critical_files:
        if os.path.exists(cf) and os.path.getsize(cf) > 0:
            print(f"  [✓] Verified: {cf} ({os.path.getsize(cf)} bytes)")
        else:
            print(f"  [x] Missing or empty: {cf}")

    print("=" * 70)
    print(f"Test Suite Summary: {passed}/{len(TESTS)} Engines Passed | {failed} Failures")
    print("=" * 70)

if __name__ == "__main__":
    run_e2e_suite()
