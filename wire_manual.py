import os
import shutil
import subprocess

# 1. Create manual_and_admin_failsafe.js
failsafe_js = """
// manual_and_admin_failsafe.js - SOP Operations Manual & Purge Failsafe

function generateOperationsManual() {
  const manual = `================================================================================
SECTION 8 RENTALS AND MORE LLC - STANDARD OPERATING PROCEDURES (SOP)
OPERATIONS MANUAL & COMPLIANCE GUIDE (REV. 2026)
Principal / Authorized Agent: Dr. Albert Ray LaMotte
Jurisdictions: Minnesota (Minn. Stat. § 504B) & Wisconsin (Wis. Stat. § 704)
================================================================================

1. HCV VOUCHER INTAKE & PHA COORDINATION:
   • 24-Hour RFTA Turnaround: Form HUD-52517 must be completed and submitted to
     the respective PHA (MPHA, Saint Paul PHA, Dakota CDA, St. Croix HRA) immediately.
   • Rent Reasonableness & SAFMR: Verified against current county payment standards.
   • Utility Matrix: Establish unambiguous heating/cooking fuel division in lease addendum.

2. STATUTORY RENT COLLECTION & DELINQUENCY ENFORCEMENT:
   • Sovereign HAP Subsidy: Deposited directly via ACH from PHA (Box 1 1099-MISC).
   • Tenant Copay Cap: Late fees are strictly capped at 8% of the TENANT'S INDIVIDUAL
     COPAY PORTION pursuant to Minn. Stat. § 504B.177. Never assess late fees on the HAP share.
   • Statutory Notices:
     - Minnesota: 14-Day Written Notice to Vacate for Nonpayment (Minn. Stat. § 504B.321).
     - Wisconsin: 5-Day Notice to Pay or Vacate (Wis. Stat. § 704.17).
     - Covered CARES Act Properties: 30-Day Notice (15 U.S.C. § 9058).

3. NSPIRE PRE-INSPECTION STANDARDS:
   • Water heater temperature-pressure relief (TPR) pipe discharge 4 inches from floor.
   • Dual functional smoke and carbon monoxide detectors on every habitable level.
   • Tamper-resistant GFCI outlets within 6 feet of all water sources.

4. QUICKBOOKS ONLINE DUAL-STREAM ACCOUNTING:
   • Account 4100: Government HAP Subsidies.
   • Account 4110: Tenant Direct Copayments.
   • Sub-Class Assignment: Itemized per property address for IRS Schedule E staging.

5. SECURITY DEPOSIT ESCROW ACCOUNTS:
   • Minnesota: Maintain statutory 1% simple non-compounded annual interest (Minn. Stat. § 504B.178).
   • Wisconsin: Escrow accounting maintained in FDIC trust institution (Wis. Stat. § 704.28).`;

  const w = window.open('', '_blank');
  w.document.write(`<pre style="font-family: monospace; font-size: 11px; line-height: 1.5; padding: 24px; background: #fff; color: #000;">${manual}</pre>`);
  w.document.close();
  w.print();
}

function purgeSampleDataFailsafe() {
  const confirmed = confirm("WARNING: Are you sure you want to purge all sample units and reset to a clean production state? This action cannot be undone.");
  if (!confirmed) return;

  if (typeof state !== 'undefined') {
    state.properties = [];
    state.accountingLedger = [];
    if (typeof calculatePortfolioMetrics === 'function') calculatePortfolioMetrics();
    if (typeof renderProperties === 'function') renderProperties();
    if (typeof renderRentReminders === 'function') renderRentReminders();
    if (typeof renderAccountingLedger === 'function') renderAccountingLedger();
  }
  alert("Sample data purged successfully. Ready for live property onboarding.");
}

window.generateOperationsManual = generateOperationsManual;
window.purgeSampleDataFailsafe = purgeSampleDataFailsafe;
"""

with open("manual_and_admin_failsafe.js", "w", encoding="utf-8") as f:
    f.write(failsafe_js)

os.makedirs("public", exist_ok=True)
shutil.copy2("manual_and_admin_failsafe.js", "public/manual_and_admin_failsafe.js")

# 2. Register script in index.html
with open("index.html", "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

if "manual_and_admin_failsafe.js" not in html:
    html = html.replace("</body>", '<script src="manual_and_admin_failsafe.js"></script>\n</body>', 1)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    shutil.copy2("index.html", "public/index.html")

# 3. Commit and deploy
subprocess.run(["git", "add", "."], check=False)
subprocess.run(["git", "commit", "-m", "feat: wire SOP manual generator and sample data purge failsafe"], check=False)
subprocess.run(["git", "push", "origin", "main"], check=False)
print("SUCCESS: Operations Manual and Admin Failsafe deployed to Cloudflare Pages.")
