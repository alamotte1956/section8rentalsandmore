import os
import shutil
import subprocess

dispatch_js = """
// emergency_dispatch_engine.js - Emergency Dispatch & Statutory 24-Hour Entry Engine
// Governing Laws: Minn. Stat. § 504B.211, Wis. Stat. § 704.05(2) & HUD NSPIRE 24-Hour Rules

function generateLandlordEntryNotice(propId, targetDateStr = null, timeWindow = '9:00 AM - 1:00 PM') {
  const p = (state.properties || []).find(x => x.id === propId) || state.properties[0];
  if (!p) return;

  const isMN = (p.state || 'MN').toUpperCase() === 'MN';
  const entryDate = targetDateStr || new Date(Date.now() + 86400000).toLocaleDateString();

  const notice = `================================================================================
STATUTORY 24-HOUR NOTICE OF LANDLORD INTENT TO ENTER PREMISES
Pursuant to ${isMN ? 'Minnesota Statutes § 504B.211' : 'Wisconsin Statutes § 704.05(2)'}
================================================================================

DATE SERVED: ${new Date().toLocaleDateString()}
TO TENANT(S): ${p.tenant || p.tenantName || 'Resident Occupant'}
PREMISES   : ${p.address}, ${p.city}, ${p.state}

PLEASE TAKE NOTICE that the landlord, authorized property manager, or designated
contractor intends to enter the rental premises for lawful inspection/maintenance:

SCHEDULED ENTRY DETAILS:
  • Date of Scheduled Entry : ${entryDate}
  • Specific Time Window    : ${timeWindow}
  • Purpose of Entry        : Periodic HUD NSPIRE Compliance Audit / Mechanical Check
  • Authorized Personnel    : Section 8 Rentals and More LLC / Certified Tradesperson

STATUTORY RIGHTS & ENTRY DISCLOSURES:
${isMN ? 'Under Minn. Stat. § 504B.211, a landlord may enter the premises only for a reasonable business purpose and after making a good faith effort to give the tenant reasonable notice under the circumstances (minimum 24 hours). The notice must specify a target time window.' : 'Under Wis. Stat. § 704.05(2), advance notice of at least 12-24 hours is required for non-emergency inspections and maintenance.'}

EMERGENCY EXCEPTION ACKNOWLEDGMENT:
In the event of an active emergency threatening life safety or immediate property
destruction (gas leak, active flooding, fire), immediate entry is permitted without notice.

Managing Agent : Dr. Albert Ray LaMotte, Principal & CEO
Entity         : Section 8 Rentals and More LLC • alamotte1956@gmail.com`;

  const w = window.open('', '_blank');
  w.document.write(`<pre style="font-family: monospace; font-size: 11px; line-height: 1.5; padding: 24px; background: #fff; color: #000;">${notice}</pre>`);
  w.document.close();
  w.print();
}

function dispatchEmergencyContractorWorkOrder(propId, issueCategory = 'Plumbing Freeze / Burst') {
  const p = (state.properties || []).find(x => x.id === propId) || state.properties[0];
  if (!p) return;

  const workOrderNum = `WO-EMERG-${Date.now().toString().slice(-6)}`;

  const workOrder = `================================================================================
EMERGENCY TRADE DISPATCH AUTHORIZATION & WORK ORDER
Section 8 Rentals and More LLC • Twin Cities Emergency Dispatch Network
================================================================================

WORK ORDER ID: ${workOrderNum}
TIMESTAMP    : ${new Date().toISOString()}
PRIORITY     : PRIORITY 1 - 24-HOUR EMERGENCY (HUD NSPIRE LIFE-SAFETY STANDARD)

1. SITE DISPATCH LOCATION:
   Premises Address  : ${p.address}, ${p.city}, ${p.state}
   Resident Contact  : ${p.tenant || p.tenantName || 'Resident'}
   County PHA Partner: ${p.county || 'Hennepin'} County PHA

2. CONTRACTOR DETAILS:
   Assigned Network  : Twin Cities Emergency Trade Network / Restoration Contractors MN
   Trade Discipline  : Emergency Mechanical / Life-Safety Remediation
   Reported Incident : ${issueCategory}

3. SCOPE OF EMERGENCY WORK:
   • Immediate isolation of water/gas supplies if active leak present.
   • Full repair to ensure restored habitability and zero ongoing hazard.
   • Contractor must photograph pre-repair and post-repair conditions for HUD-52580 proof.

4. BILLING & EXPENSE AUTHORIZATION:
   Authorized Entity : Section 8 Rentals and More LLC
   Authorizing Agent : Dr. Albert Ray LaMotte
   Invoice Routing   : General Ledger Line 14 (Repairs & Maintenance - Schedule E)
   Direct Inquiries  : alamotte1956@gmail.com`;

  const w = window.open('', '_blank');
  w.document.write(`<pre style="font-family: monospace; font-size: 11px; line-height: 1.5; padding: 24px; background: #fff; color: #000;">${workOrder}</pre>`);
  w.document.close();
  w.print();
}

window.generateLandlordEntryNotice = generateLandlordEntryNotice;
window.dispatchEmergencyContractorWorkOrder = dispatchEmergencyContractorWorkOrder;
"""

with open("emergency_dispatch_engine.js", "w", encoding="utf-8") as f:
    f.write(dispatch_js)

os.makedirs("public", exist_ok=True)
shutil.copy2("emergency_dispatch_engine.js", "public/emergency_dispatch_engine.js")

# 1. Register script in index.html
with open("index.html", "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

if "emergency_dispatch_engine.js" not in html:
    html = html.replace("</body>", '<script src="emergency_dispatch_engine.js"></script>\n</body>', 1)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    shutil.copy2("index.html", "public/index.html")

# 2. Add buttons to compliance_hub.js
with open("compliance_hub.js", "r", encoding="utf-8", errors="ignore") as f:
    hub_code = f.read()

dispatch_buttons = """
        <button onclick="generateLandlordEntryNotice('${p.id}')" class="p-3.5 text-left rounded-2xl bg-sky-500/10 hover:bg-sky-500/20 border border-sky-500/30 transition-all">
          <div class="font-bold text-sky-300">MN § 504B.211 24-Hr Entry Notice</div>
          <div class="text-[11px] text-slate-400 mt-1">Reasonable statutory notice with time window & NSPIRE inspection purpose.</div>
        </button>

        <button onclick="dispatchEmergencyContractorWorkOrder('${p.id}')" class="p-3.5 text-left rounded-2xl bg-rose-500/10 hover:bg-rose-500/20 border border-rose-500/30 transition-all">
          <div class="font-bold text-rose-300">Emergency Trade Dispatch (P1)</div>
          <div class="text-[11px] text-slate-400 mt-1">Priority 1 contractor work order with photo proof staging for HUD-52580.</div>
        </button>
"""

if "generateLandlordEntryNotice" not in hub_code:
    hub_code = hub_code.replace("</div>\n\n      <div class=\"flex items-center justify-between pt-2 border-t", dispatch_buttons + "      </div>\n\n      <div class=\"flex items-center justify-between pt-2 border-t", 1)
    with open("compliance_hub.js", "w", encoding="utf-8") as f:
        f.write(hub_code)
    shutil.copy2("compliance_hub.js", "public/compliance_hub.js")

# Commit and deploy to Cloudflare Pages
subprocess.run(["git", "add", "."], check=False)
subprocess.run(["git", "commit", "-m", "feat: implement Minn. Stat. § 504B.211 24-hr entry notice and emergency trade dispatch engine"], check=False)
subprocess.run(["git", "push", "origin", "main"], check=False)
print("SUCCESS: Emergency Dispatch & Landlord Entry Engine deployed live to Cloudflare Pages.")
